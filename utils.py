from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import Session, select, update
from model import Members, Coaches, Accesscards, Registrations, Courses
from init_db import engine
import datetime
import pandas as pd
import random


def all_coach_info():  
    """Displays a browser for available courses with filtering and registration options.

    This function presents available courses in a card format, allowing users to filter, sort, and register for courses. It handles empty and filtered data gracefully and provides interactive registration buttons.

    Args:
        courses_df (pd.DataFrame): DataFrame containing available course data.

    Returns:
        None
    """
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
    """Adds a new coach to the database with the given name and specialty.

    This function creates a new coach record in the database and returns a success status and message. It handles database errors gracefully.

    Args:
        name (str): The full name of the coach.
        specialty (str): The specialty area of the coach.

    Returns:
        tuple: (bool, str) indicating success status and a descriptive message.
    """
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
    """Deletes a coach from the database by their unique ID.

    This function removes a coach record from the database using the provided coach ID and returns a success status and message. It handles cases where the coach does not exist and database errors.

    Args:
        coach_id (int): The unique identifier of the coach to delete.

    Returns:
        tuple: (bool, str) indicating success status and a descriptive message.
    """
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
    """Modifies a coach's name and/or specialty in the database.

    This function updates the name and/or specialty of a coach identified by their unique ID. It returns a success status and message, handling cases where the coach does not exist and database errors.

    Args:
        coach_id (int): The unique identifier of the coach to modify.
        new_name (str, optional): The new name for the coach.
        new_specialty (str, optional): The new specialty for the coach.

    Returns:
        tuple: (bool, str) indicating success status and a descriptive message.
    """
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
    """Retrieves course records from the database by course name.

    This function returns a list of course records that match the provided course name. It is used to access course details for further operations.

    Args:
        course_name (str): The name of the course to search for.

    Returns:
        list: List of course records matching the course name.
    """
    with Session(engine) as session:
        statement = select(Courses).where(Courses.course_name == course_name)
        results = session.exec(statement)
        access = results.all()
    return access


def add_member(name, mail, access):
    """Adds a new member to the database with the given name, email, and access card.

    This function creates a new member record and associated access card in the database. It returns a success message or an error message if the operation fails.

    Args:
        name (str): The full name of the member.
        mail (str): The email address of the member.
        access (str): The access card identifier for the member.

    Returns:
        str: Success or error message describing the result.
    """
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
    """Adds a new course to the database with the given details.

    This function creates a new course record in the database using the provided name, date, maximum participants, and coach ID. It returns a success message or an error message if the operation fails.

    Args:
        name (str): The name of the course.
        date (str): The date and time of the course in ISO format.
        max_participants (int): The maximum number of participants allowed.
        coach_id (int): The unique identifier of the coach assigned to the course.

    Returns:
        str: Success or error message describing the result.
    """
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
    """Deletes a member from the database by their name.

    This function removes a member record from the database using the provided member name and returns a success or error message. It handles cases where the member does not exist and database errors.

    Args:
        name (str): The name of the member to delete.

    Returns:
        str: Success or error message describing the result.
    """
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
    """Deletes a course from the database by its unique ID.

    This function removes a course record from the database using the provided course ID and returns a success or error message. It handles cases where the course does not exist and database errors.

    Args:
        number (int): The unique identifier of the course to delete.

    Returns:
        str: Success or error message describing the result.
    """
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
    """Updates a member's name and/or email in the database.

    This function modifies the name and/or email of a member identified by their unique ID. It returns a success message or an error message, handling cases where the member does not exist or no fields are provided for update.

    Args:
        member_id (int): The unique identifier of the member to update.
        new_name (str, optional): The new name for the member.
        new_mail (str, optional): The new email address for the member.

    Returns:
        str: Success or error message describing the result.
    """
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
    """Registers a member for a course in the database.

    This function creates a new registration for a member in a specified course, checking for member and course existence, course capacity, and duplicate registrations. It returns a success or error message describing the result.

    Args:
        id_member (int or str): The unique identifier of the member to register.
        id_course (int or str): The unique identifier of the course to register for.

    Returns:
        str: Success or error message describing the result.
    """
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
    """Returns the total number of registrations for a member by name.

    This function retrieves the count of all course registrations associated with a member's name. It returns 0 if the member does not exist or if an error occurs.

    Args:
        name (str): The name of the member.

    Returns:
        int: The total number of registrations for the member.
    """
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
    """Returns a list of all registration records for a member by name.

    This function retrieves all course registration records associated with a member's name. It returns an empty list if the member does not exist or if an error occurs.

    Args:
        name (str): The name of the member.

    Returns:
        list: List of registration records for the member.
    """
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
    """Adds a new coach to the database using the provided name and specialty.

    This function is a wrapper for add_coach and returns the result of adding a coach to the database.

    Args:
        name (str): The full name of the coach.
        specialty (str): The specialty area of the coach.

    Returns:
        tuple: (bool, str) indicating success status and a descriptive message.
    """
    return add_coach(name, specialty)
