from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
import random

app = FastAPI()

# connect database
conn = sqlite3.connect("tickets.db", check_same_thread=False)
cur = conn.cursor()

# create table
cur.execute("""
CREATE TABLE IF NOT EXISTS tickets(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT,
    category TEXT,
    severity TEXT,
    status TEXT,
    department TEXT,
    assignee TEXT,
    sentiment TEXT,
    summary TEXT
)
""")

# simple employee list (manual)
employees = [
    {"name": "Ravi", "dept": "IT", "load": 2},
    {"name": "Priya", "dept": "Finance", "load": 1},
    {"name": "Arjun", "dept": "Engineering", "load": 3},
    {"name": "Sneha", "dept": "HR", "load": 0}
]

class Ticket(BaseModel):
    text: str


# basic analysis function
def analyze_ticket(text):
    t = text.lower()

    if "password" in t:
        category = "Access"
        dept = "IT"
        status = "Auto-Resolved"
    elif "salary" in t:
        category = "Billing"
        dept = "Finance"
        status = "Assigned"
    elif "bug" in t:
        category = "Bug"
        dept = "Engineering"
        status = "Assigned"
    elif "leave" in t:
        category = "HR"
        dept = "HR"
        status = "Assigned"
    else:
        category = "Other"
        dept = "General"
        status = "Assigned"

    severity = random.choice(["Low", "Medium", "High"])

    if "urgent" in t:
        sentiment = "Frustrated"
    else:
        sentiment = "Neutral"

    summary = "Issue related to " + category

    return category, dept, status, severity, sentiment, summary


# choose employee with least load
def assign_emp(dept):
    available = [e for e in employees if e["dept"] == dept]

    if len(available) == 0:
        return "Not Assigned"

    # sort by load
    available.sort(key=lambda x: x["load"])
    return available[0]["name"]


# create ticket
@app.post("/ticket")
def create_ticket(ticket: Ticket):

    category, dept, status, severity, sentiment, summary = analyze_ticket(ticket.text)

    emp = assign_emp(dept)

    cur.execute(
        "INSERT INTO tickets (text, category, severity, status, department, assignee, sentiment, summary) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (ticket.text, category, severity, status, dept, emp, sentiment, summary)
    )

    conn.commit()

    return {
        "msg": "Ticket created",
        "category": category,
        "department": dept,
        "status": status,
        "assigned_to": emp
    }


# get tickets
@app.get("/tickets")
def get_all():
    cur.execute("SELECT * FROM tickets")
    data = cur.fetchall()

    res = []
    for row in data:
        res.append({
            "id": row[0],
            "text": row[1],
            "category": row[2],
            "severity": row[3],
            "status": row[4],
            "department": row[5],
            "assignee": row[6],
            "sentiment": row[7],
            "summary": row[8]
        })

    return res


# simple analytics
@app.get("/stats")
def stats():
    cur.execute("SELECT COUNT(*) FROM tickets")
    total = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM tickets WHERE status='Auto-Resolved'")
    auto = cur.fetchone()[0]

    return {
        "total_tickets": total,
        "auto_resolved": auto
    }


@app.get("/")
def home():
    return {"message": "AI Ticket System running"}