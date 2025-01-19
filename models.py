from typing import List, Optional, Dict
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, create_engine
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.types import JSON
from datetime import datetime

Base = declarative_base()


class ChatHistory(Base):
    __tablename__ = "chat_histories"

    id = Column(Integer, primary_key=True, index=True)
    message_id = Column(Integer, ForeignKey("chat_messages.id"))
    message = relationship("ChatMessage", lazy="joined")

class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    from_user = Column(String, nullable=False)  # e.g., "ClaudeAI" or "ChatGPT"
    to_user = Column(String, nullable=False)    # e.g., "ChatGPT" or "ClaudeAI"
    content = Column(Text, nullable=False)      # The actual message content
    timestamp = Column(DateTime, default=datetime.utcnow)  # When the message was sent

    # # Optional: Foreign key to link to a character or campaign if needed
    # character_id = Column(Integer, ForeignKey("characters.id"), nullable=True)
    # character = relationship("Character", back_populates="messages", lazy="joined")

class Character(Base):
    __tablename__ = "characters"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    class_primary = Column(String)
    class_secondary = Column(String, nullable=True)
    level = Column(Integer)
    race = Column(String)
    background = Column(String, nullable=True)
    experience_points = Column(Integer, default=0)
    player = Column(String)
    # messages = relationship("ChatMessage", back_populates="character")

    # JSON fields for complex structures
    attributes = Column(JSON)
    combat = Column(JSON)
    proficiencies = Column(JSON)
    features = Column(JSON)
    spellcasting = Column(JSON)
    equipment = Column(JSON)
    appearance = Column(JSON)


# Base schema for shared fields
class ChatMessageBase(BaseModel):
    from_user: str
    to_user: str
    content: str
    character_id: Optional[int] = None

# Schema for creating a chat message (used in POST requests)
class ChatMessageCreate(ChatMessageBase):
    pass

# Schema for reading a chat message (used in GET responses)
class ChatMessageRead(ChatMessageBase):
    id: int
    timestamp: datetime

    class Config:
        orm_mode = True

class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    model: str = "gpt-3.5-turbo"
    messages: List[Message]


# Define sub-models for nested structures
class CharacterClass(BaseModel):
    primary: str
    secondary: Optional[str]
    level: int


class Basics(BaseModel):
    name: str
    class_: CharacterClass
    race: str
    background: Optional[str]
    experiencePoints: int
    player: str


class AttributeScore(BaseModel):
    score: int
    modifier: int


class Attributes(BaseModel):
    strength: AttributeScore
    dexterity: AttributeScore
    constitution: AttributeScore
    intelligence: AttributeScore
    wisdom: AttributeScore
    charisma: AttributeScore


class HitPoints(BaseModel):
    maximum: int
    current: Optional[int]
    temporary: Optional[int]


class DeathSaves(BaseModel):
    successes: int
    failures: int


class Combat(BaseModel):
    armorClass: int
    initiative: int
    hitPoints: HitPoints
    hitDice: str
    deathSaves: DeathSaves


class Skill(BaseModel):
    name: str
    ability: str
    modifier: int


class Proficiencies(BaseModel):
    armor: List[str]
    weapons: List[str]
    languages: List[str]
    skills: List[Skill]


class Features(BaseModel):
    racial: Dict[str, str]
    class_: Dict[str, List[str]]


class Spell(BaseModel):
    name: str
    source: str
    attackBonus: Optional[int] = None
    damage: Optional[str] = None
    range: Optional[str] = None


class Spells(BaseModel):
    cantrips: List[Spell]
    level1: List[Spell]


class Spellcasting(BaseModel):
    ability: str
    saveDC: int
    attackBonus: int
    spells: Spells


class Weapon(BaseModel):
    name: str
    attackBonus: Optional[int] = None
    damage: Optional[str] = None
    properties: Optional[str] = None


class CarriedItem(BaseModel):
    name: str
    quantity: int
    weight: float


class OtherEquipment(BaseModel):
    weightCarried: float
    weightEncumbered: float
    pushDragLift: float


class Equipment(BaseModel):
    weapons: List[Weapon]
    carried: List[CarriedItem]
    other: OtherEquipment


class Appearance(BaseModel):
    gender: str
    age: int
    size: str
    height: str
    weight: int
    faith: str
    skin: str
    eyes: str
    hair: str


# Top-level schema
class CharacterCreate(BaseModel):
    basics: Basics
    attributes: Attributes
    combat: Combat
    proficiencies: Proficiencies
    features: Features
    spellcasting: Spellcasting
    equipment: Equipment
    appearance: Appearance