import os
import sqlite3
from dataclasses import dataclass
from typing import List


@dataclass
class Assignment:
    unique_id: int
    id: int
    name: str
    due: str
    description: str


def initialize_database():
    # Create the data directory if it doesn't exist.
    os.makedirs("data", exist_ok=True)

    # Remove the database files
    if os.path.exists("data/database.db"):
        os.remove("data/database.db")

    # Create the database.
    assigments = sqlite3.connect("data/database.db")
    cursor = assigments.cursor()
    cursor.execute("CREATE TABLE assignments(unique_id, id, name, due, description)")


def connect_to_database() -> tuple[sqlite3.Connection, sqlite3.Cursor]:
    assignment = sqlite3.connect("data/database.db")
    return assignment, assignment.cursor()


def add_assignments(information: Assignment) -> None:
    assigments, cursor = connect_to_database()

    # Add the assignment to the database.
    cursor.execute(
        "INSERT INTO assignments VALUES (?, ?, ?, ?, ?)",
        (information.unique_id, information.id, information.name, information.due, information.description),
    )

    # Commit the changes.
    assigments.commit()
    cursor.close()
    assigments.close()


def remove_assignments(unique_id: int) -> None:
    assigments, cursor = connect_to_database()

    # Remove the assignment from the database at the given row index.
    cursor.execute("DELETE FROM assignments WHERE unique_id=?", (unique_id,))

    # Commit the changes.
    assigments.commit()
    cursor.close()
    assigments.close()

def get_list_of_assignments() -> List[Assignment]:
    assigments, cursor = connect_to_database()

    # Get all assignments from the database.
    cursor.execute("SELECT * FROM assignments")
    assignments = cursor.fetchall()

    # Close the connection to the database.
    cursor.close()
    assigments.close()

    # Return the assignments.
    return [Assignment(*assignment) for assignment in assignments]

def get_assignment(unique_id: int):
    assigments, cursor = connect_to_database()

    # Get all assignments from the database.
    cursor.execute("SELECT * FROM assignments WHERE unique_id=?", (unique_id,))
    assignment = cursor.fetchone()

    # Close the connection to the database.
    cursor.close()
    assigments.close()

    # Return the assignments.
    return Assignment(*assignment)

