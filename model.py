from sqlmodel import SQLModel, Field, Relationship 
from datetime import datetime
from typing import Optional


class Members(SQLModel, table=True):
    """
    Represents a member in the fitness club database.

    This class defines the structure for storing member information, including their unique identifier, 
    name, contact details, and relationships with access cards and course registrations.
    """
    member_id: int | None = Field(default=None, primary_key=True, nullable=False)
    member_name: str = Field(index=True, nullable=False)
    email: str = Field(index=True, nullable=False)

    access_card_id: int | None = Field(default=None, foreign_key="accesscards.card_id")
    access_card: Optional["Accesscards"] = Relationship(back_populates="member")
    registration: list["Registrations"] = Relationship(back_populates="member",cascade_delete=True)

class Accesscards(SQLModel, table=True):
    """
    Represents an access card in the fitness club database.

    This class defines the structure for storing access card information with a unique identifier and its associated member.
    """
    card_id: int | None  = Field(default=None, primary_key=True, nullable=False)
    unique_number: int 

    member: Optional["Members"] = Relationship(sa_relationship_kwargs={'uselist': False}, back_populates="access_card")

class Registrations(SQLModel, table=True):
    """
    Represents a course registration in the fitness club database.

    This class defines the structure for storing registration details, linking members to specific courses and tracking registration dates.
    """
    registration_id: int | None = Field(default=None, primary_key=True)
    registration_date: datetime = Field(nullable=False)

    member_id: str = Field(default=None, foreign_key="members.member_id")
    course_id: str = Field(default=None, foreign_key="courses.course_id")
    member: Optional["Members"] = Relationship(back_populates="registration")
    course: Optional["Courses"] = Relationship(back_populates="registration")

class Coaches(SQLModel, table=True):
    """
    Represents a coach in the fitness club database.

    This class defines the structure for storing coach information, including their unique identifier,
    name, specialty, and relationships with courses.
    """
    coach_id: int | None = Field(default=None, primary_key=True)
    coach_name: str = Field(index=True, nullable=False)
    specialty: str

    course: Optional["Courses"] = Relationship(back_populates="coach", cascade_delete=True)

class Courses(SQLModel, table=True):
    """
    Represents a course in the fitness club database.

    This class defines the structure for storing course information, including its unique identifier, name, schedule, capacity, and relationships with coaches and registrations.
    """    
    course_id: int | None = Field(default=None, primary_key=True, nullable=False)
    course_name: str = Field(index=True, nullable=False)
    time_plan: datetime = Field(index=True, nullable=False)
    max_capacity: int

    coach_id: int | None = Field(default=None, foreign_key="coaches.coach_id")
    registration: list["Registrations"] = Relationship(back_populates="course", cascade_delete=True)
    coach: list["Coaches"] = Relationship(back_populates="course")
