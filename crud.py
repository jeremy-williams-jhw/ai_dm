from sqlalchemy.orm import Session
from models import CharacterCreate, Character, ChatHistory
from database import SessionLocal


# Create a new character
def create_character(db: Session, character_data: CharacterCreate):
    """
    Add a new character to the database.
    :param db: SQLAlchemy session object.
    :param character_data: CharacterCreate schema containing character details.
    :return: Newly created character.
    """
    db_character = Character(
        name=character_data.basics.name,
        class_primary=character_data.basics.class_.primary,
        class_secondary=character_data.basics.class_.secondary,
        level=character_data.basics.class_.level,
        race=character_data.basics.race,
        background=character_data.basics.background,
        experience_points=character_data.basics.experiencePoints,
        player=character_data.basics.player,
        attributes=character_data.attributes.dict(),
        combat=character_data.combat.dict(),
        proficiencies=character_data.proficiencies.dict(),
        features=character_data.features.dict(),
        spellcasting=character_data.spellcasting.dict(),
        equipment=character_data.equipment.dict(),
        appearance=character_data.appearance.dict(),
    )
    db.add(db_character)
    db.commit()
    db.refresh(db_character)
    return db_character


# Get a character by ID
def get_character(db: Session, character_id: int):
    """
    Retrieve a character by ID.
    :param db: SQLAlchemy session object.
    :param character_id: ID of the character to retrieve.
    :return: Character object or None if not found.
    """
    return db.query(Character).filter(Character.id == character_id).first()


# Get all characters
def get_characters(db: Session, skip: int = 0, limit: int = 10):
    """
    Retrieve all characters with pagination.
    :param db: SQLAlchemy session object.
    :param skip: Number of records to skip.
    :param limit: Maximum number of records to retrieve.
    :return: List of characters.
    """
    return db.query(Character).offset(skip).limit(limit).all()


# Update a character
def update_character(db: Session, character_id: int, character_data: CharacterCreate):
    """
    Update an existing character by ID.
    :param db: SQLAlchemy session object.
    :param character_id: ID of the character to update.
    :param character_data: Updated character data (CharacterCreate schema).
    :return: Updated character object or None if not found.
    """
    db_character = db.query(Character).filter(Character.id == character_id).first()
    if db_character is None:
        return None

    db_character.name = character_data.basics.name
    db_character.class_primary = character_data.basics.class_.primary
    db_character.class_secondary = character_data.basics.class_.secondary
    db_character.level = character_data.basics.class_.level
    db_character.race = character_data.basics.race
    db_character.background = character_data.basics.background
    db_character.experience_points = character_data.basics.experiencePoints
    db_character.player = character_data.basics.player
    db_character.attributes = character_data.attributes.dict()
    db_character.combat = character_data.combat.dict()
    db_character.proficiencies = character_data.proficiencies.dict()
    db_character.features = character_data.features.dict()
    db_character.spellcasting = character_data.spellcasting.dict()
    db_character.equipment = character_data.equipment.dict()
    db_character.appearance = character_data.appearance.dict()

    db.commit()
    db.refresh(db_character)
    return db_character


# Delete a character
def delete_character(db: Session, character_id: int):
    """
    Delete a character by ID.
    :param db: SQLAlchemy session object.
    :param character_id: ID of the character to delete.
    :return: True if deletion was successful, False otherwise.
    """
    db_character = db.query(Character).filter(Character.id == character_id).first()
    if db_character is None:
        return False

    db.delete(db_character)
    db.commit()
    return True

def add_chat_message(db: Session, message_from: str, message_to: str, content: str):
    new_message = ChatHistory(message_from=message_from, message_to=message_to, content=content)
    db.add(new_message)
    db.commit()
    return new_message

def get_chat_history(db: Session):
    return db.query(ChatHistory).all()