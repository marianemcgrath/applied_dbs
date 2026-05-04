# Applied Databases Project 2026 — Conference Management System
**Author:** Mariane McGrath  
**Module:** Applied Databases — HDip in Science in Data Analytics, ATU

---

## Overview

A conference management system built with a hybrid database approach — MySQL for structured 
data, Neo4j for relationship data. The system lets event organisers manage attendees, 
companies, sessions, and rooms, while also surfacing intelligent networking insights 
from the connections between attendees.

- **MySQL** → attendees, companies, sessions, rooms, registrations
- **Neo4j** → professional connections between attendees
- **Python** → application logic, DAO pattern, menu-driven interface

---

## Features

- View speakers and their sessions
- View attendees by company
- Add new attendees
- View an attendee's existing connections
- Add new connections between attendees
- View room details (cached per session)
- **Networking Intelligence Tool** *(Innovation Feature — see below)*

---

## 🤝 Innovation Feature — Networking Intelligence Tool

A conference is only as valuable as the connections and the experience it creates. The Networking Intelligence 
Tool gives event organisers two powerful views of their attendee network — one focused on individuals and
one on the conference as a whole.

This enables organisers to identify high-value networking opportunities and support targeted introductions
between attendees.

### What it does:

**1. Suggested Connections (Attendee-level)**

- Enter any attendee ID
- The system traverses the Neo4j graph to find second-to-fourth degree connections
- Suggestions are ranked by number of mutual connections (most relevant first)
- Results are enriched with attendee name, company, and sessions attended
- Existing direct connections are excluded — no noise, just new leads

This enables organisers to facilitate meaningful introductions. Instead of leaving networking to chance,
they can proactively suggest who should meet who, supporting more effective engagement during the event.

**2. Key Connectors (Conference-level)**

- No input needed — this is a bird's-eye view of the whole network
- Ranks all attendees by their number of connections
- Identifies highly connected attendees who may act as central nodes within the network, supporting decisions around
group facilitation, panel selection, or networking activities.

This is useful for things like seating plans, panel selection, breakout group design, 
or simply knowing who the natural connectors in the room are.

### Why Neo4j?

Relationship traversal at multiple degrees of separation is exactly what graph databases are built for. Running this kind
of query in MySQL would require complex recursive joins — in Neo4j it's a natural, efficient path query.

Together, these two views turn the system from a static database into a network analysis and decision-support tool (built into the organiser's
existing workflow).

This demonstrates the suitability of graph databases for complex relationship-heavy queries that are inefficient in relational models.

---

## Tech Stack

- Python
- MySQL (`mysql-connector-python`)
- Neo4j (`neo4j` driver)
- `python-dotenv` for environment variables

---

## Installation

```bash
pip install neo4j mysql-connector-python python-dotenv
```

---

## Setup

1. Import `appdbproj.sql` into MySQL
2. Import `appdbprojNeo4j.json` into a Neo4j database called `appdbprojNeo4j`
3. Ensure MySQL and Neo4j are both running before launching the app

---

## Run

```bash
python main.py
```

---

## Project Structure

main.py             # Menu-driven application entry point
dao.py              # All database logic (DAO pattern)
db_connection.py    # MySQL connection helper
neo4j_connection.py # Neo4j connection helper
GitLink.pdf         # Link to GitHub repository

---

## Design Decisions

- **DAO pattern** keeps database logic cleanly separated from application logic
- **Hybrid database approach** — relational for structure, graph for relationships
- **Room data is cached** on first load and reused for the session (as per spec)
- **Neo4j MERGE** is used when adding connections, so nodes are created automatically 
  if they do not already exist

---

## Notes

- Designed and tested for the ATU VM environment
- MySQL and Neo4j must both be running before launching the app
- The networking feature requires a minimum level of connectivity in the Neo4j
  graph to return meaningful results.