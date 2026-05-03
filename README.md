# Applied Databases Project 2026 — Conference Management System

This project was completed for the Applied Databases module as part of the HDip Data Analytics course at ATU. 

Author: Mariane McGrath

✨ Overview

This is a conference management system that integrates relational and graph databases to manage attendees, companies, and professional connections.

 - MySQL → structured data (attendees, companies)
 - Neo4j → relationships between attendees

A key feature of the system is a networking tool that recommends new professional connections.

🤝 Innovation Feature - Suggested Connections (Social Network)

The Suggested Connections feature allows users to discover new attendees to connect with using friend-of-a-friend relationships.

Features:

 * Supports 2–4 degrees of separation
 * Excludes existing direct connections
 * Recommends relevant new contacts
 * Displays degree of separation
 * Enriches results with attendee and company data

This transforms the system into a simple recommendation engine for networking.

🛠 Tech Stack
 - Python
 - Neo4j
 - MySQL
 - neo4j driver
 - mysql-connector-python
 - python-dotenv

⚙️ Installation
pip install neo4j mysql-connector-python python-dotenv

▶️ Run the Application
python main.py

🚀 Using the Networking Feature
 1. Run the application
 2. Select Option 7 — Networking
 3. Enter an attendee ID
 4. Choose degree of separation (2–4)
 5. View suggested connections

🔍 Verify in Neo4j Browser

MATCH (a:Attendee {AttendeeID: 101})-[:CONNECTED_TO*1..3]-(b:Attendee)
RETURN a, b

📁 Project Structure

main.py        # Application entry point  
dao.py         # Database logic (DAO pattern)  
.env           # Environment variables

🧠 Design Choices

 * Graph database for relationship traversal
 * Relational database for structured data
 * DAO pattern for separation of concerns
 * Hybrid database approach for efficiency

⚠️ Notes

 * Designed to run in a VM environment
 * Ensure MySQL and Neo4j are running before execution
 * No additional dependencies required beyond installation step