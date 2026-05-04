# Data Access Object - Database query functions
# Author: Mariane McGrath
#
# INNOVATION FEATURE - Networking Intelligence Tool
#
# suggest_connections():
#   Implements a recommendation system using Neo4j.
#   Identifies second-to-fourth degree connections by traversing the graph,
#   excluding already connected attendees.
#   Suggestions are ranked by number of mutual connections.
#   MySQL is used to retrieve attendee names and session data for display.
#
# key_connectors():
#   Ranks all attendees by number of connections in the Neo4j graph.
#   Identifies the most networked attendees at the conference.
#   Useful for seating plans, panel selection, and facilitated introductions.

from db_connection import get_connection
from neo4j_connection import get_neo4j_driver


def suggest_connections():
    while True:
        attendee_input = input("Enter Attendee ID : ").strip()
        
        if not attendee_input:
            print("*** ERROR *** Attendee ID cannot be empty")
            continue
        
        if not attendee_input.isdigit():
            print("*** ERROR *** Invalid attendee ID")
            continue
        
        attendee_id = int(attendee_input)
        
        # Check attendee exists (MySQL) before querying Neo4j
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT attendeeName FROM attendee WHERE attendeeID = %s",
            (attendee_id,)
        )
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            print("*** ERROR *** Attendee does not exist")
            continue
        
        attendee_name = row[0]
        
        print(f"\nSuggested connections for {attendee_name}")
        print("(Based on shared connections in the network)")
        print("--------------------------------------------------")
        
        driver = get_neo4j_driver()
        
        with driver.session(database="appdbprojNeo4j") as session:
            result = session.run(
                """
                MATCH (a:Attendee {AttendeeID: $id})
                
                MATCH path = (a)-[:CONNECTED_TO*2..4]-(suggested)
                WHERE NOT (a)-[:CONNECTED_TO]-(suggested)
                AND a <> suggested
                
                WITH suggested, MIN(length(path)) AS degrees
                
                OPTIONAL MATCH (a)-[:CONNECTED_TO]-(mutual)-[:CONNECTED_TO]-(suggested)
                
                RETURN 
                    suggested.AttendeeID AS id,
                    COUNT(DISTINCT mutual) AS score,
                    degrees
                
                ORDER BY score DESC, degrees ASC
                LIMIT 5
                """,
                id=attendee_id
            )
            
            suggestions = list(result)
        
        if not suggestions:
            print("No suggestions available (no suitable connections found within 2–4 degrees)")
            driver.close()
            break
        
        # Only print header if we have results
        print("Rank | Name                 | Mutual | Degree")
        print("--------------------------------------------------")
        
        # MySQL query to get names, companies and sessions for suggested attendees
        conn = get_connection()
        cursor = conn.cursor()
        
        ids = [s["id"] for s in suggestions]
        placeholders = ','.join(['%s'] * len(ids))
        
        cursor.execute(f"""
            SELECT 
                a.attendeeID,
                a.attendeeName,
                c.companyName,
                GROUP_CONCAT(DISTINCT s.sessionTitle SEPARATOR ', ') AS sessions
            FROM attendee a
            JOIN company c ON a.attendeeCompanyID = c.companyID
            LEFT JOIN registration r ON a.attendeeID = r.attendeeID
            LEFT JOIN session s ON r.sessionID = s.sessionID
            WHERE a.attendeeID IN ({placeholders})
            GROUP BY a.attendeeID, a.attendeeName, c.companyName
        """, tuple(ids))
        
        rows = cursor.fetchall()
        conn.close()
        
        data_map = {}
        for attendeeID, name, company, sessions in rows:
            data_map[attendeeID] = {
                "name": name,
                "company": company,
                "sessions": sessions if sessions else "None recorded"
            }
        
        rank = 1
        for s in suggestions:
            sid = s["id"]
            mutual_count = s["score"]
            degrees = s["degrees"]
            
            person = data_map.get(sid, {})
            name = person.get("name", "Unknown")
            company = person.get("company", "Unknown")
            sessions = person.get("sessions", "None recorded")
            
            print(f"{rank:<4} | {name:<20} | {mutual_count:<6} | {degrees}")
            print(f"    Company: {company}")
            print(f"    Sessions: {sessions}")
            print()
            rank += 1
        
        print("Tip: These attendees share mutual connections — consider facilitating an introduction.")
        driver.close()
        break


def key_connectors():
    print("\nKey Connectors at this Conference")
    print("(Attendees ranked by number of connections)")
    print("--------------------------------------------------")
    
    driver = get_neo4j_driver()
    
    with driver.session(database="appdbprojNeo4j") as session:
        result = session.run(
            """
            MATCH (a:Attendee)
            OPTIONAL MATCH (a)-[:CONNECTED_TO]-(b:Attendee)
            RETURN a.AttendeeID AS id, COUNT(DISTINCT b) AS connections
            ORDER BY connections DESC
            LIMIT 10
            """
        )
        connectors = list(result)
    
    driver.close()
    
    if not connectors:
        print("No connection data available")
        return
    
    conn = get_connection()
    cursor = conn.cursor()
    
    ids = [c["id"] for c in connectors]
    placeholders = ','.join(['%s'] * len(ids))
    
    cursor.execute(f"""
        SELECT a.attendeeID, a.attendeeName, c.companyName
        FROM attendee a
        JOIN company c ON a.attendeeCompanyID = c.companyID
        WHERE a.attendeeID IN ({placeholders})
    """, tuple(ids))
    
    rows = cursor.fetchall()
    conn.close()
    
    data_map = {row[0]: {"name": row[1], "company": row[2]} for row in rows}
    
    print(f"\n{'Rank':<5} | {'Name':<20} | {'Company':<20} | Connections")
    print("------------------------------------------------------------------")
    
    rank = 1
    for c in connectors:
        cid = c["id"]
        count = c["connections"]
        person = data_map.get(cid, {})
        name = person.get("name", "Unknown")
        company = person.get("company", "Unknown")
        
        print(f"{rank:<5} | {name:<20} | {company:<20} | {count}")
        rank += 1
    
    print("\nTip: These are your most networked attendees — ideal for panels, table leads, or introductions.")