from enum import Enum
from typing import Any

from pydantic import BaseModel


class UserRole(str, Enum):
    student = "student"
    staff = "staff"
    authority = "authority"


class User(BaseModel):
    id: str
    email: str
    username: str
    password: str
    role: UserRole


class IncidentKind(str, Enum):
    behavior = "behavior"
    aggression = "aggression"


class IncidentUrgency(str, Enum):
    low = "low"
    mid = "mid"
    high = "high"


class IncidentStatus(str, Enum):
    pending = "pending"
    attending = "attending"
    done = "done"


class IncidentAuthor(BaseModel):
    id: str
    email: str
    username: str
    role: UserRole


class IncidentHistoryEntry(BaseModel):
    status: IncidentStatus
    actor: IncidentAuthor
    date: str


class Incident(BaseModel):
    id: str
    kind: IncidentKind
    description: str
    location: str
    urgency: IncidentUrgency
    status: IncidentStatus
    author: IncidentAuthor
    history: list[IncidentHistoryEntry] = []
    created_at: str


class IncidentSubscription(BaseModel):
    connection_id: str


class BroadcastMessageKind(str, Enum):
    incident_create = "incident_create"
    incident_status_update = "incident_status_update"


class BroadcastMessage(BaseModel):
    kind: BroadcastMessageKind
    data: Any
