import csv
import os
from google.adk.agents import Agent
from pydantic import BaseModel

# Path to the students CSV file
CSV_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "students.csv")


def load_students_data() -> str:
    """Load all students from CSV and format as text."""
    students = []
    with open(CSV_PATH, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            students.append(row)
    
    data = "WORKSHOP ATTENDEES:\n\n"
    for s in students:
        data += f"- {s['name']} ({s['email']})\n"
        data += f"  Interests: {s['interests']}\n"
        data += f"  Looking to connect with: {s['looking_to_connect_with']}\n\n"
    return data


# Pydantic models for structured output
class StudentGroup(BaseModel):
    group: list[str]
    description: str


class GroupsResponse(BaseModel):
    groups: list[StudentGroup]


# Load student data
STUDENT_DATA = load_students_data()

# Create the ADK agent
root_agent = Agent(
    model='gemini-2.0-flash',
    name='workshop_matchmaker',
    description='Groups workshop attendees based on shared interests.',
    instruction=f'''You are a workshop matchmaker. Group students into teams 
based on their shared interests.

RULES:
- Create MULTIPLE groups
- Each group should have MAXIMUM 3 people
- Group people with similar interests together
- Every attendee should be in at least one group

Here is the data of all workshop attendees:

{STUDENT_DATA}

Create meaningful groups and explain why each group should connect.''',
    output_schema=GroupsResponse,
)