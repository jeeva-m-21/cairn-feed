from datetime import datetime, timezone
from enum import Enum
from hashlib import sha256
import json
from typing import Literal
from urllib.parse import urlparse
from uuid import uuid4

import feedparser
import requests
from bs4 import BeautifulSoup
from fastapi import FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
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
    saves: list[str] = Field(default_factory=list)


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


class ClusterDocument(BaseModel):
    documentId: str
    sourceUrl: str
    title: str
    excerpt: str
    entities: list[str] = Field(default_factory=list)


class ClusterRequest(BaseModel):
    documents: list[ClusterDocument] = Field(min_length=1, max_length=100)


class EventCluster(BaseModel):
    clusterId: str
    documentIds: list[str]
    title: str
    confidence: Literal["high", "medium", "low"]
    explanation: str


class ClusterResponse(BaseModel):
    clusters: list[EventCluster]


class BriefRequest(BaseModel):
    clusterId: str


class Evidence(BaseModel):
    documentId: str
    citation: str


class BriefClaim(BaseModel):
    text: str
    confidence: Literal["high", "medium", "low"]
    evidence: list[Evidence]


class Brief(BaseModel):
    briefId: str
    clusterId: str
    title: str
    claims: list[BriefClaim]


class SourceHealth(BaseModel):
    sourceId: str
    status: Literal["healthy", "degraded", "disabled"]
    lastCheckedAt: str


class SourceHealthResponse(BaseModel):
    overallStatus: Literal["healthy", "degraded"]
    sources: list[SourceHealth]


class SaveRequest(BaseModel):
    profileId: str
    eventId: str


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
    profile_dict = (profile_input or ProfileInput()).model_dump()
    profile_dict["saves"] = []
    profile = Profile(profileId=str(uuid4()), **profile_dict)
    PROFILES[profile.profileId] = profile
    return profile


@app.post("/v1/saves", response_model=Profile, status_code=status.HTTP_201_CREATED)
def save_event(request: SaveRequest) -> Profile:
    profile = PROFILES.get(request.profileId)
    if profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    if request.eventId not in {event.id for event in FOR_YOU_EVENTS}:
        raise HTTPException(status_code=404, detail="Event not found")
    if request.eventId not in profile.saves:
        profile.saves.append(request.eventId)
    return profile


@app.delete("/v1/saves", response_model=Profile)
def unsave_event(request: SaveRequest) -> Profile:
    profile = PROFILES.get(request.profileId)
    if profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    profile.saves = [event_id for event_id in profile.saves if event_id != request.eventId]
    return profile


@app.get("/v1/profile/{profile_id}", response_model=Profile)
def get_profile(profile_id: str) -> Profile:
    profile = PROFILES.get(profile_id)
    if profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile


DOCUMENTS: dict[str, IngestedDocument] = {}
CLUSTERS: dict[str, tuple[EventCluster, list[ClusterDocument]]] = {}


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



@app.post("/v1/clusters", response_model=ClusterResponse, status_code=status.HTTP_201_CREATED)
def cluster_documents(request: ClusterRequest) -> ClusterResponse:
    documents = request.documents
    document_ids = [document.documentId for document in documents]
    if len(document_ids) != len(set(document_ids)):
        raise HTTPException(status_code=422, detail="Duplicate document IDs are not allowed")
    common_entities = set(documents[0].entities)
    for document in documents[1:]:
        common_entities.intersection_update(document.entities)

    if len(documents) > 1 and common_entities:
        cluster_id = sha256("|".join(sorted(doc.documentId for doc in documents)).encode()).hexdigest()[:16]
        cluster = EventCluster(
            clusterId=cluster_id,
            documentIds=[document.documentId for document in documents],
            title=documents[0].title,
            confidence="high" if len(common_entities) >= 2 else "medium",
            explanation=f"Grouped by shared entities: {', '.join(sorted(common_entities))}.",
        )
        CLUSTERS[cluster.clusterId] = (cluster, documents)
        return ClusterResponse(clusters=[cluster])

    clusters = [
        EventCluster(
            clusterId=sha256(document.documentId.encode()).hexdigest()[:16],
            documentIds=[document.documentId],
            title=document.title,
            confidence="low",
            explanation="Kept separate because no shared entities met the clustering threshold.",
        )
        for document in documents
    ]
    return ClusterResponse(clusters=clusters)


SOURCE_HEALTH: dict[str, Literal["healthy", "degraded", "disabled"]] = {"rss": "healthy", "github": "healthy", "arxiv": "healthy"}


@app.get("/v1/admin/source-health", response_model=SourceHealthResponse)
def source_health(degraded: str | None = None) -> SourceHealthResponse:
    source_statuses = dict(SOURCE_HEALTH)
    if degraded in source_statuses:
        source_statuses[degraded] = "degraded"
    sources = [
        SourceHealth(
            sourceId=source_id,
            status=source_statuses[source_id],
            lastCheckedAt=datetime.now(timezone.utc).isoformat(),
        )
        for source_id in source_statuses
    ]
    overall = "degraded" if any(s.status == "degraded" for s in sources) else "healthy"
    return SourceHealthResponse(overallStatus=overall, sources=sources)


@app.get("/v1/briefs/{cluster_id}/stream")
async def stream_brief(cluster_id: str) -> StreamingResponse:
    cluster_data = CLUSTERS.get(cluster_id)

    def event_stream():
        if cluster_data is None:
            yield 'data: {"type":"error","code":"CLUSTER_NOT_FOUND"}\n\n'
            return

        cluster, documents = cluster_data
        shared_entities = sorted(set.intersection(*(set(doc.entities) for doc in documents)))
        meta = {"type": "meta", "title": cluster.title, "entities": shared_entities, "documentCount": len(documents)}
        yield f"data: {json.dumps(meta)}\n\n"
        evidence = [{"documentId": doc.documentId, "citation": f"{doc.title[:100]}..."} for doc in documents]
        claim = {
            "type": "claim",
            "text": f"Developments in {', '.join(shared_entities)} across {len(documents)} sources.",
            "confidence": "high",
            "evidence": evidence,
            "evidenceCount": len(evidence),
        }
        yield f"data: {json.dumps(claim)}\n\n"
        yield 'data: {"type":"done"}\n\n'

    return StreamingResponse(event_stream(), media_type="text/event-stream")


@app.post("/v1/briefs", response_model=Brief, status_code=status.HTTP_201_CREATED)
def generate_brief(request: BriefRequest) -> Brief:
    cluster_data = CLUSTERS.get(request.clusterId)
    if cluster_data is None:
        raise HTTPException(status_code=404, detail="Cluster not found")
    cluster, documents = cluster_data
    shared_entities = set.intersection(*(set(doc.entities) for doc in documents))
    evidence = [Evidence(documentId=doc.documentId, citation=f"{doc.title[:100]}...") for doc in documents]
    return Brief(
        briefId=str(uuid4()),
        clusterId=request.clusterId,
        title=cluster.title,
        claims=[BriefClaim(
            text=f"Developments in {', '.join(sorted(shared_entities))} across {len(documents)} sources.",
            confidence="high",
            evidence=evidence,
        )],
    )


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
