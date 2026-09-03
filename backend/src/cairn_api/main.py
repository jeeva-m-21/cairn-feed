from typing import Literal

from fastapi import FastAPI, Query
from pydantic import BaseModel

app = FastAPI(title="Cairn API")


class EventCard(BaseModel):
    id: str
    title: str
    category: str
    sourceCount: int
    relevanceReason: str


class FeedResponse(BaseModel):
    section: str
    items: list[EventCard]


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


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "cairn-api"}


@app.get("/v1/feed", response_model=FeedResponse)
def feed(section: Literal["for_you"] = Query(default="for_you")) -> FeedResponse:
    return FeedResponse(section=section, items=FOR_YOU_EVENTS)
