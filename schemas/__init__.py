from enum import Enum

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
