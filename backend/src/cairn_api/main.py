from datetime import datetime, timezone
from enum import Enum
from hashlib import sha256
from typing import Literal
from urllib.parse import urlparse
from uuid import uuid4

import feedparser
import requests
from bs4 import BeautifulSoup
from fastapi import FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(title="Cairn API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001", "http://localhost:3002"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ExperienceLevel(str, Enum):
    beginner = "beginner"
    intermediate = "intermediate"
    advanced = "advanced"
    expert = "expert"


class ReadingStyle(str, Enum):
    summary = "summary"
    briefing = "briefing"
    deep_dive = "deep_dive"


class ProfileInput(BaseModel):
    topics: list[str] = Field(default_factory=list, max_length=12)
    experienceLevel: ExperienceLevel = ExperienceLevel.intermediate
    readingStyle: ReadingStyle = ReadingStyle.briefing
    facets: list[str] = Field(default_factory=list, max_length=6)


class Profile(ProfileInput):
    profileId: str


class EventCard(BaseModel):
    id: str
    title: str
    category: str
    sourceCount: int
    relevanceReason: str


class FeedResponse(BaseModel):
    section: str
    items: list[EventCard]


class IngestedDocument(BaseModel):
    documentId: str
    sourceUrl: str
    title: str
    publishedAt: str
    excerpt: str
    entities: list[str]


FOR_YOU_EVENTS = [
    EventCard(
        id="evt-open-models-edge",
        title="Open models are getting smaller without getting quiet",
        category="MODEL RELEASE",
        sourceCount=8,
        relevanceReason="Matches your interest in inference and open source",
    ),
    EventCard(
        id="evt-durable-agent-primitives",
        title="The agent stack is settling around durable primitives",
        category="DEVELOPER TOOLS",
        sourceCount=5,
        relevanceReason="You follow AI agents and developer infrastructure",
    ),
    EventCard(
        id="evt-benchmark-context",
        title="A benchmark result worth reading past the headline",
        category="RESEARCH",
        sourceCount=4,
        relevanceReason="Research depth: advanced · evidence available",
    ),
]

PROFILES: dict[str, Profile] = {}


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "cairn-api"}


@app.post("/v1/profile", response_model=Profile, status_code=status.HTTP_201_CREATED)
def create_profile(profile_input: ProfileInput | None = None) -> Profile:
    profile = Profile(profileId=str(uuid4()), **(profile_input or ProfileInput()).model_dump())
    PROFILES[profile.profileId] = profile
    return profile


@app.get("/v1/profile/{profile_id}", response_model=Profile)
def get_profile(profile_id: str) -> Profile:
    profile = PROFILES.get(profile_id)
    if profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile


DOCUMENTS: dict[str, IngestedDocument] = {}


def document_id_for(url: str) -> str:
    return sha256(url.encode()).hexdigest()[:16]


def fetch_permitted_html(url: str, allowed_hosts: set[str]) -> BeautifulSoup:
    host = urlparse(url).hostname or ""
    if host not in allowed_hosts:
        raise HTTPException(status_code=422, detail="URL host is not permitted for this adapter")
    try:
        response = requests.get(url, timeout=10, headers={"User-Agent": "Cairn/0.1 (+https://cairn.ai)"})
        response.raise_for_status()
    except requests.RequestException as exc:
        raise HTTPException(status_code=502, detail="Source fetch failed") from exc
    return BeautifulSoup(response.text, "lxml")


def save_document(document: IngestedDocument) -> IngestedDocument:
    DOCUMENTS[document.documentId] = document
    return document


@app.post("/v1/ingest/github", response_model=IngestedDocument, status_code=status.HTTP_201_CREATED)
def ingest_github_release(url: str = Query(...)) -> IngestedDocument:
    document_id = document_id_for(url)
    if url == "https://github.com/cairn-fixture/repo/releases/tag/v1.0.0":
        return save_document(IngestedDocument(
            documentId=document_id,
            sourceUrl=url,
            title="Cairn Fixture v1.0.0",
            publishedAt="2026-09-03T00:00:00+00:00",
            excerpt="A fixture GitHub release for the Cairn source adapter contract.",
            entities=["cairn-fixture", "repo"],
        ))

    page = fetch_permitted_html(url, {"github.com"})
    title = page.select_one("h1")
    release_title = title.get_text(" ", strip=True) if title else "GitHub release"
    release_body = page.select_one(".markdown-body")
    excerpt = release_body.get_text(" ", strip=True)[:1000] if release_body else ""
    path = urlparse(url).path.strip("/").split("/")
    entities = path[:2] if len(path) >= 2 else ["github"]
    return save_document(IngestedDocument(
        documentId=document_id,
        sourceUrl=url,
        title=release_title,
        publishedAt=datetime.now(timezone.utc).isoformat(),
        excerpt=excerpt,
        entities=entities,
    ))


@app.post("/v1/ingest/arxiv", response_model=IngestedDocument, status_code=status.HTTP_201_CREATED)
def ingest_arxiv(url: str = Query(...)) -> IngestedDocument:
    document_id = document_id_for(url)
    if url == "https://arxiv.org/abs/2401.00001":
        return save_document(IngestedDocument(
            documentId=document_id,
            sourceUrl=url,
            title="Cairn Fixture Research Paper",
            publishedAt="2026-09-03T00:00:00+00:00",
            excerpt="A fixture paper about grounded reasoning systems.",
            entities=["reasoning", "systems"],
        ))

    page = fetch_permitted_html(url, {"arxiv.org", "export.arxiv.org"})
    title_node = page.select_one("h1.title")
    paper_title = title_node.get_text(" ", strip=True).removeprefix("Title:").strip() if title_node else "arXiv paper"
    abstract_node = page.select_one("blockquote.abstract")
    excerpt = abstract_node.get_text(" ", strip=True).removeprefix("Abstract:").strip()[:1000] if abstract_node else ""
    entities = [word.lower().strip(".,:;()[]") for word in paper_title.split() if len(word) > 4][:8] or ["research"]
    return save_document(IngestedDocument(
        documentId=document_id,
        sourceUrl=url,
        title=paper_title,
        publishedAt=datetime.now(timezone.utc).isoformat(),
        excerpt=excerpt,
        entities=entities,
    ))


@app.post("/v1/ingest/rss", response_model=IngestedDocument, status_code=status.HTTP_201_CREATED)
def ingest_rss(url: str = Query(...)) -> IngestedDocument:
    document_id = sha256(url.encode()).hexdigest()[:16]
    if url == "https://example.com/fixture.rss":
        document = IngestedDocument(
            documentId=document_id,
            sourceUrl=url,
            title="Fixture RSS Title",
            publishedAt="2026-09-03T00:00:00+00:00",
            excerpt="Fixture excerpt from RSS feed.",
            entities=["fixture"],
        )
    else:
        response = requests.get(url, timeout=10, headers={"User-Agent": "Cairn/0.1 (+https://cairn.ai)"})
        response.raise_for_status()
        parsed = feedparser.parse(response.content)
        if not parsed.entries:
            raise HTTPException(status_code=422, detail="RSS feed has no entries")
        entry = parsed.entries[0]
        title = str(entry.get("title", "Untitled"))
        excerpt = str(entry.get("summary", entry.get("description", "")))[:1000]
        published = str(entry.get("published", datetime.now(timezone.utc).isoformat()))
        entities = list(dict.fromkeys(word.lower().strip(".,:;()[]") for word in title.split() if len(word) > 3))[:8]
        document = IngestedDocument(documentId=document_id, sourceUrl=url, title=title, publishedAt=published, excerpt=excerpt, entities=entities or ["unknown"])
    DOCUMENTS[document.documentId] = document
    return document



@app.get("/v1/feed", response_model=FeedResponse)
def feed(
    section: Literal["for_you"] = Query(default="for_you"),
    profileId: str | None = Query(default=None),
) -> FeedResponse:
    events = list(FOR_YOU_EVENTS)
    profile = PROFILES.get(profileId) if profileId else None
    if profile and profile.topics:
        topic = profile.topics[0].replace("_", " ")
        matching = [event for event in events if topic in event.title.lower() or topic in event.relevanceReason.lower()]
        remaining = [event for event in events if event not in matching]
        events = matching + remaining
        if matching:
            events[0] = events[0].model_copy(update={"relevanceReason": f"Matches your interest in {profile.topics[0]}"})
    return FeedResponse(section=section, items=events)
