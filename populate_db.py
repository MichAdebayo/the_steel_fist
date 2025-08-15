"""Utility script to populate the Steel Fist database with realistic dummy data.

Usage:
  python populate_db.py              # Populate only if tables empty
  python populate_db.py --force      # Force populate (adds on top)

Data generation order respects foreign key dependencies.
The script is idempotent by default (skips a table if it already has rows).
"""


from __future__ import annotations

import argparse
import random
from datetime import datetime, timedelta, timezone

from faker import Faker
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from init_db import engine
from model import Members, Coaches, Accesscards, Registrations, Courses

SPECIALTIES = [
    "yoga",
    "pilates",
    "crossfit",
    "calisthenic",
    "body training",
    "athletes trainings",
    "zumba",
]

fake = Faker()


def table_has_rows(session: Session, model) -> bool:
    """Checks if a database table contains any rows.
    
    This function determines whether the specified table has at least one row.

    Args:
        session: The SQLModel session used for querying.
        model: The SQLModel table class to check.

    Returns:
        bool: True if the table contains at least one row, False otherwise.
    """
    return session.exec(select(model).limit(1)).first() is not None


def create_members(session: Session, count: int = 40, force: bool = False):
    """Populates the Members table with randomly generated member data.

    This function adds a specified number of new members to the database unless the table already contains rows and force is not set.

    Args:
        session: The SQLModel session used for database operations.
        count: The number of members to create. Defaults to 40.
        force: If True, members are added regardless of existing rows. Defaults to False.

    Returns:
        None
    """
    if not force and table_has_rows(session, Members):
        return
    for _ in range(count):
        m = Members(member_name=fake.name(), email=fake.unique.email())
        session.add(m)
    session.commit()


def create_access_cards(session: Session, force: bool = False):
    """Assigns access cards to members in the database.

    This function creates and links access cards to members who do not already have one, unless force is set.

    Args:
        session: The SQLModel session used for database operations.
        force: If True, assigns new access cards regardless of existing links. Defaults to False.

    Returns:
        None
    """
    members = session.exec(select(Members)).all()
    if not members:
        return
    # Build set of member_ids already linked
    existing_card_member_ids = {m.member_id for m in members if m.access_card_id}
    for m in members:
        if m.member_id in existing_card_member_ids and not force:
            continue
        card = Accesscards(unique_number=fake.unique.random_number(digits=8))
        session.add(card)
        session.flush()  # assign card_id
        m.access_card_id = card.card_id
    session.commit()


def create_coaches(session: Session, count: int = 12, force: bool = False):
    """Populates the Coaches table with randomly generated coach data.

    This function adds a specified number of new coaches to the database unless the table already contains rows and force is not set.

    Args:
        session: The SQLModel session used for database operations.
        count: The number of coaches to create. Defaults to 12.
        force: If True, coaches are added regardless of existing rows. Defaults to False.

    Returns:
        None
    """
    if not force and table_has_rows(session, Coaches):
        return
    for _ in range(count):
        c = Coaches(coach_name=fake.name(), specialty=random.choice(SPECIALTIES))
        session.add(c)
    session.commit()


def _random_future_datetime(days_ahead: int = 120) -> datetime:
    """Generates a random future datetime within a specified time range.

    This function creates a datetime object representing a random future time from now, with configurable maximum days ahead.

    Args:
        days_ahead: Maximum number of days in the future to generate a datetime. Defaults to 120.

    Returns:
        datetime: A randomly generated future datetime in UTC timezone.
    """
    base = datetime.now(timezone.utc)
    delta = timedelta(days=random.randint(1, days_ahead), hours=random.randint(6, 20))
    return base + delta

def create_courses(session: Session, count: int = 40, force: bool = False):
    """Populates the Courses table with randomly generated course data.

    This function creates a specified number of courses assigned to random coaches, ensuring unique time slots and variety.

    Args:
        session: The SQLModel session used for database operations.
        count: The number of courses to create. Defaults to 40.
        force: If True, courses are added regardless of existing rows. Defaults to False.

    Returns:
        None
    """
    if not force and table_has_rows(session, Courses):
        return
    coaches = session.exec(select(Coaches)).all()
    if not coaches:
        return
    # coach_id is Optional[int]; reflect that in the key type
    used_slots: set[tuple[int, int, int | None]] = set()  # (year, day_of_year, coach_id) to minimize duplicates
    for _ in range(count):
        coach = random.choice(coaches)
        # Ensure some variety & avoid too many identical timestamps for same coach
        for _attempt in range(12):
            dt = _random_future_datetime()
            slot_key = (dt.year, dt.timetuple().tm_yday, coach.coach_id)
            if slot_key not in used_slots:
                used_slots.add(slot_key)
                break
        course = Courses(
            course_name=random.choice(SPECIALTIES),
            time_plan=dt,
            max_capacity=random.randint(10, 30),
            coach_id=coach.coach_id,
        )
        session.add(course)
    session.commit()


def create_registrations(session: Session, count: int = 120, force: bool = False):
    """Populates the Registrations table with randomly generated registration data.

    This function creates a specified number of course registrations by linking random members to random courses, handling potential duplicate registrations.

    Args:
        session: The SQLModel session used for database operations.
        count: The number of registrations to create. Defaults to 120.
        force: If True, registrations are added regardless of existing rows. Defaults to False.

    Returns:
        None
    """
    if not force and table_has_rows(session, Registrations):
        return
    members = session.exec(select(Members)).all()
    courses = session.exec(select(Courses)).all()
    if not members or not courses:
        return
    for _ in range(count):
        member = random.choice(members)
        course = random.choice(courses)
        # registration_date expects datetime
        reg_dt = fake.date_time_between(start_date="-180d", end_date="now")
        r = Registrations(
            registration_date=reg_dt,
            member_id=str(member.member_id),
            course_id=str(course.course_id),
        )
        session.add(r)
        try:
            session.flush()
        except IntegrityError:
            session.rollback()
            continue
    session.commit()


def populate(force: bool = False):
    """Populates the Steel Fist database with dummy data in a specific order.

    This function sequentially creates database entries for members, access cards, coaches, courses, and registrations, respecting foreign key dependencies.

    Args:
        force: If True, data is added to tables even if they already contain rows. Defaults to False.

    Returns:
        None
    """
    with Session(engine) as session:
        create_members(session, force=force)
        create_access_cards(session, force=force)
        create_coaches(session, force=force)
        create_courses(session, force=force)
        create_registrations(session, force=force)


def parse_args():
    """Parses command-line arguments for database population script.

    This function sets up an argument parser to handle optional force flag for database population.

    Returns:
        Parsed command-line arguments with optional force flag.
    """
    parser = argparse.ArgumentParser(description="Populate Steel Fist database with dummy data")
    parser.add_argument("--force", action="store_true", help="Insert data even if tables already contain rows")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    populate(force=args.force)