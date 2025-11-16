from enum import Enum
from typing import Any

from pydantic import BaseModel


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


class Incident(BaseModel):
    id: str
    kind: IncidentKind
    description: str
    location: str
    urgency: IncidentUrgency
    status: IncidentStatus


class IncidentSubscription(BaseModel):
    connection_id: str


class BroadcastMessageKind(str, Enum):
    incident_create = "incident_create"
    incident_status_update = "incident_status_update"


class BroadcastMessage(BaseModel):
    kind: BroadcastMessageKind
    data: Any
