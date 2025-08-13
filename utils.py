from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import Session, select, update
from model import Members, Coaches, Accesscards, Registrations, Courses
from init_db import engine
import datetime
import pandas as pd
import random


def all_coach_info():  
    """Retrieve all coaches information from the database."""
    try:
        with Session(engine) as session:
            stmt = select(Coaches)
            results = session.exec(stmt).all()
            data = [{"coach_id": row.coach_id, "coach_name": row.coach_name, "specialty": row.specialty} for row in results]
            df = pd.DataFrame(data)
            df.index = df.index + 1  # Start index from 1
            return df
    except SQLAlchemyError as e:
        print(f"Database error in all_coach_info(): {e}")
        return pd.DataFrame()  # Return an empty DataFrame if there is an error


def add_coach(name, specialty):
    """Add a new coach to the database with the specified name and specialty."""
    try:
        with Session(engine) as session:
            new_coach = Coaches(coach_name=name, specialty=specialty)
            session.add(new_coach)
            session.commit()
            print(f"Successfully added coach {name}")
            return True, f"Addition of the new coach {name} successful"
    except SQLAlchemyError as e:
        print(f"Error adding coach {name}: {e}")
        return False, f"Error adding coach {name}: {e}"


def delete_coach(coach_id):
    """Delete a coach from the database by their unique ID."""
    try:
        with Session(engine) as session:
            statement = select(Coaches).where(Coaches.coach_id == coach_id)
            to_delete = session.exec(statement).one_or_none()
            if not to_delete:
                print(f"No coach found with ID: {coach_id}")
                return False, f"No coach found with ID: {coach_id}"
            session.delete(to_delete)
            session.commit()
            print(f"Successfully deleted coach with ID: {coach_id}")
            return True, f"Coach with ID: {coach_id} deleted successfully"
    except SQLAlchemyError as e:
        print(f"Error deleting coach with ID {coach_id}: {e}")
        return False, f"Error deleting coach: {e}"


def modify_coach(coach_id, new_name=None, new_specialty=None):
    """Modify a coach's name and/or specialty by their unique ID."""
    try:
        with Session(engine) as session:
            # Retrieve the coach to modify
            statement = select(Coaches).where(Coaches.coach_id == coach_id)
            coach_to_modify = session.exec(statement).one_or_none()

            if not coach_to_modify:
                return False, f"No coach found with ID: {coach_id}"

            # Update the coach's name and specialty if new values are provided
            if new_name:
                coach_to_modify.coach_name = new_name
            if new_specialty:
                coach_to_modify.specialty = new_specialty

            # Commit the changes
            session.commit()
            print(f"Successfully modified coach with ID: {coach_id}")
            return True, f"Coach with ID: {coach_id} updated successfully"
    except SQLAlchemyError as e:
        print(f"Error modifying coach with ID {coach_id}: {e}")
        return False, f"Error modifying coach: {e}"


def select_course(course_name):
    """Select courses by course name."""
    with Session(engine) as session:
        statement = select(Courses).where(Courses.course_name == course_name)
        results = session.exec(statement)
        access = results.all()
    return access


def add_member(name, mail, access):
    """Add a new member with an access card to the database."""
    try:
        with Session(engine) as session:
            # Generate a random 6-digit number for the access card
            unique_number = random.randint(100000, 999999)
            new_member = Members(member_name=name, email=mail, access_card_id=access)
            new_card = Accesscards(card_id=access, unique_number=unique_number)
            session.add(new_member)
            session.add(new_card)
            session.commit()
            validation = f"Addition of the new member {name} successful"
            return validation
    except SQLAlchemyError as e:
        return f"Error adding member {name}: {e}"


def add_course(name, date, max_participants, coach_id):
    """Add a new course to the database."""
    try:
        with Session(engine) as session:
            date_obj = datetime.datetime.fromisoformat(date)
            new_course = Courses(
                course_name=name,
                time_plan=date_obj,
                max_capacity=max_participants,
                coach_id=coach_id
            )
            session.add(new_course)
            session.commit()
            return f"Addition of the course {name} at {date} with the coach {coach_id}"
    except SQLAlchemyError as e:
        return f"Error adding course {name}: {e}"


def delete_member(name):
    """Delete a member from the database by name."""
    try:
        with Session(engine) as session:
            statement = select(Members).where(Members.member_name == name)
            results = session.exec(statement)
            to_delete = results.one_or_none()
            if not to_delete:
                return f"No member found with name: {name}"
            session.delete(to_delete)
            session.commit()
            validation = f"The member {name} has been removed from the database"
            return validation
    except SQLAlchemyError as e:
        return f"Error deleting member {name}: {e}"


def delete_course(number):
    """Delete a course from the database by course ID."""
    try:
        with Session(engine) as session:
            statement = select(Courses).where(Courses.course_id == number)
            results = session.exec(statement)
            to_delete = results.one_or_none()
            if not to_delete:
                return f"No course found with ID: {number}"
            session.delete(to_delete)
            session.commit()
            validation = f"The course {number} has been removed from the database"
            return validation
    except SQLAlchemyError as e:
        return f"Error deleting course {number}: {e}"


def update_members(member_id, new_name=None, new_mail=None):
    """Update member information by member ID."""
    try:
        with Session(engine) as session:
            # Prepare the fields to update dynamically
            updates = {}
            if new_name is not None and new_name.strip():
                updates["member_name"] = new_name
            if new_mail is not None and new_mail.strip():
                updates["email"] = new_mail

            if not updates:
                return "No fields to update."
            
            # First check if member exists
            existing_member = session.exec(select(Members).where(Members.member_id == member_id)).first()
            if not existing_member:
                return f"No member with ID {member_id} was found."
            
            stmt = (
                update(Members)
                .where(Members.member_id == member_id)
                .values(**updates)
            )
            # Execute the query
            session.execute(stmt)
            session.commit()

            return f"Member ID {member_id} updated successfully!"
    except SQLAlchemyError as e:
        return f"Error updating member {member_id}: {e}"


def registrations(id_member, id_course):
    """Register a member for a course."""
    try:
        with Session(engine) as session:
            # Convert inputs to appropriate types
            member_id_str = str(id_member)
            course_id_int = int(id_course)
            course_id_str = str(id_course)
            
            # Check if member exists
            member = session.exec(select(Members).where(Members.member_id == int(id_member))).first()
            if not member:
                return f"Member with ID {id_member} not found"
            
            # Check if course exists
            course = session.exec(select(Courses).where(Courses.course_id == course_id_int)).first()
            if not course:
                return f"Course with ID {id_course} not found"
            
            # Check current registrations for this course
            current_registrations = session.exec(
                select(Registrations).where(Registrations.course_id == course_id_str)
            ).all()
            
            if len(current_registrations) >= 10:  # Assuming max capacity is 10
                return 'Course is full'
            
            # Check if member is already registered for this course
            existing_registration = session.exec(
                select(Registrations).where(
                    (Registrations.member_id == member_id_str) & 
                    (Registrations.course_id == course_id_str)
                )
            ).first()
            
            if existing_registration:
                return f"Member {id_member} is already registered for this course"

            # Create a new registration
            new_registration = Registrations(
                registration_date=course.time_plan,
                member_id=member_id_str,
                course_id=course_id_str
            )

            session.add(new_registration)
            session.commit()
            return f"Member {id_member} successfully registered"
            
    except ValueError as e:
        return f"Invalid input: {e}"
    except SQLAlchemyError as e:
        return f"Error registering member: {e}"


def historic_number_registrations(name):
    """Get the number of registrations for a member by name."""
    try:
        with Session(engine) as session:
            statement = select(Members.member_id).where(Members.member_name == name)
            member_result = session.exec(statement).first()
            if member_result is None:
                return 0  # No member found, so 0 registrations
            
            name_id = str(member_result)  # Convert to string to match model
            # Get all registrations for this member
            registrations_list = session.exec(
                select(Registrations).where(Registrations.member_id == name_id)
            ).all()
            return len(registrations_list)
    except SQLAlchemyError as e:
        print(f"Error getting registration count for {name}: {e}")
        return 0


def historic_registrations(name):
    """Get all registrations for a member by name."""
    try:
        with Session(engine) as session:
            statement = select(Members.member_id).where(Members.member_name == name)
            member_result = session.exec(statement).first()
            if member_result is None:
                return []  # No member found, so no registrations
            
            name_id = str(member_result)  # Convert to string to match model
            statementh = select(Registrations).where(Registrations.member_id == name_id)
            result = session.exec(statementh).all()
            return result
    except SQLAlchemyError as e:
        print(f"Error getting registrations for {name}: {e}")
        return []


def add_coaches(name, specialty):
    """Alias for add_coach function to maintain compatibility."""
    return add_coach(name, specialty)
