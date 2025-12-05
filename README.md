# Workshop: Building AI Agents with Google ADK

A hands-on workshop to build an AI-powered student matchmaker using Google's Agent Development Kit (ADK).

## What You'll Build

An AI agent that:
- Reads workshop attendee data from a CSV file
- Groups students based on shared interests
- Returns structured JSON responses

---

## Prerequisites

- Python 3.10 or higher
- Google AI API Key (free from [Google AI Studio](https://aistudio.google.com/apikey))

---

## Step 1: Create Project Directory

```bash
mkdir Google-ADK-Workshop
cd Google-ADK-Workshop
```

## Step 2: Set Up Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

## Step 3: Install Google ADK

```bash
pip install google-adk
```

## Step 4: Create Your Agent

Use the ADK CLI to scaffold an agent:

```bash
adk create my_agent
```

When prompted:
1. Choose model: `gemini-2.5-flash` (option 1)
2. Choose backend: `Google AI` (option 1)
3. Enter your Google API Key

This creates:
```
my_agent/
├── __init__.py
├── agent.py
└── .env          # Contains your API key
```

## Step 5: Create Student Data

Create a file `students.csv` in the project root:

```csv
id,name,email,interests,looking_to_connect_with
1,Alice Johnson,alice@example.com,"AI, Machine Learning, Python","Backend developers, Data scientists"
2,Bob Smith,bob@example.com,"Web Development, React, TypeScript","Frontend developers, UI designers"
3,Carol Williams,carol@example.com,"Data Science, Machine Learning, Statistics","AI enthusiasts, Researchers"
4,David Brown,david@example.com,"Backend Development, Python, FastAPI","AI enthusiasts, Full-stack developers"
5,Eve Davis,eve@example.com,"UI/UX Design, Figma, User Research","Frontend developers, Product managers"
6,Frank Miller,frank@example.com,"DevOps, Cloud, Kubernetes","Backend developers, Security experts"
7,Grace Lee,grace@example.com,"AI, NLP, Deep Learning","Data scientists, Researchers"
8,Henry Wilson,henry@example.com,"Full-stack Development, React, Node.js","Backend developers, UI designers"
9,Ivy Chen,ivy@example.com,"Product Management, Agile, Strategy","UI designers, Full-stack developers"
10,Jack Taylor,jack@example.com,"Security, Cryptography, Ethical Hacking","DevOps engineers, Backend developers"
```

## Step 6: Update the Agent

Replace the contents of `my_agent/agent.py` with:

```python
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
```

## Step 7: Test with CLI

Quick test using the ADK CLI:

```bash
adk run my_agent
```

Type a message like:
```
Create groups for all attendees
```

Type `exit` to quit.

---

## Step 8: Run the API Server

Start the ADK API server:

```bash
adk api_server
```

Server runs at `http://localhost:8000`

## Step 9: Use the API


### Option A: Use curl

```bash
# 1. Create a session
curl -X POST "http://localhost:8000/apps/my_agent/users/user1/sessions/session1" \
  -H "Content-Type: application/json" -d '{}'

# 2. Run the agent
curl -X POST http://localhost:8000/run \
  -H "Content-Type: application/json" \
  -d '{
    "appName": "my_agent",
    "userId": "user1",
    "sessionId": "session1",
    "newMessage": {"role": "user", "parts": [{"text": "Create groups"}]}
  }'
```

### Option B: Use Python Script

Create `run_agent.py`:

```python
import requests
import json

# Create session
requests.post("http://localhost:8000/apps/my_agent/users/u1/sessions/s1", json={})

# Run agent
response = requests.post("http://localhost:8000/run", json={
    "appName": "my_agent",
    "userId": "u1",
    "sessionId": "s1",
    "newMessage": {"role": "user", "parts": [{"text": "Create groups for all attendees"}]}
})

# Extract clean JSON
events = response.json()
result = json.loads(events[-1]["content"]["parts"][0]["text"])

print(json.dumps(result, indent=2))
```

Run it:
```bash
python run_agent.py
```

---

## Project Structure

```
Google-ADK-Workshop/
├── my_agent/
│   ├── __init__.py      # Module init
│   ├── agent.py         # ADK agent definition
│   └── .env             # API key (GOOGLE_API_KEY=...)
├── students.csv         # Workshop attendee data
├── run_agent.py         # Optional: Python script to run agent
└── README.md            # This file
```

---

## Key Concepts Covered

| Concept | Description |
|---------|-------------|
| **ADK Agent** | AI agent with instructions and optional tools |
| **Pydantic Schema** | Structured JSON output using `output_schema` |
| **ADK CLI** | `adk create`, `adk run`, `adk api_server` |
| **REST API** | `/run` endpoint for programmatic access |
| **Sessions** | Conversation state management |

## Troubleshooting

**"Session not found" error**
→ Create a session first before calling `/run`

**Agent not loading**
→ Make sure `agent.py` has a `root_agent` variable

**API key issues**
→ Check `.env` file has `GOOGLE_API_KEY=your-key`

---

## Next Steps

- Add tools for dynamic data fetching
- Deploy to Google Cloud Run
- Build a frontend UI
- Explore multi-agent systems

---

## Resources

- [Google ADK Documentation](https://google.github.io/adk-docs/)
- [Google AI Studio](https://aistudio.google.com/) - Get API keys
- [ADK GitHub Repository](https://github.com/google/adk-python)
