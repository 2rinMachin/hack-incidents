from enum import Enum

from pydantic import BaseModel


class IncidentKind(str, Enum):
    behavior = "behavior"
    aggression = "aggression"


class IncidentUrgency(str, Enum):
    low = "low"
    mid = "mid"
    high = "high"


class Incident(BaseModel):
    id: str
    kind: IncidentKind
    description: str
    location: str
    urgency: IncidentUrgency
