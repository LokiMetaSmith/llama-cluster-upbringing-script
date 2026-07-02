from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class Device(BaseModel):
    id: str
    type: str
    state: Dict[str, Any] = Field(default_factory=dict)
    location_id: Optional[str] = None

class Occupant(BaseModel):
    name: str
    type: str

class Location(BaseModel):
    id: str
    name: str
    infrastructure: List[Device] = Field(default_factory=list)
    occupants: List[Occupant] = Field(default_factory=list)

class Agent(BaseModel):
    id: str
    name: str
    node_id: Optional[str] = None
    state: Dict[str, Any] = Field(default_factory=dict)

class Node(BaseModel):
    id: str
    name: str
    address: Optional[str] = None
    status: str = "unknown"
    resources: Dict[str, Any] = Field(default_factory=dict)

class Cluster(BaseModel):
    id: str
    name: str
    nodes: List[Node] = Field(default_factory=list)

class WorldOntology(BaseModel):
    locations: List[Location] = Field(default_factory=list)
    cluster: Optional[Cluster] = None
    agents: List[Agent] = Field(default_factory=list)
    devices: List[Device] = Field(default_factory=list)
