# Data Access Object - Database query functions
# Author: Mariane McGrath
#
# INNOVATION FEATURE - Suggested Connections
#
# This feature implements a recommendation system using Neo4j.
# It identifies second-degree connections (friends-of-friends) by traversing the graph and excluding already connected attendees.

# Suggested attendees are ranked based on the number of mutual connections they share with the user. 

# MySQL is used to retrieve attendee names for display.

from db_connection import get_connection
from neo4j_connection import get_neo4j_driver

def suggest_connections():

    while True:
        attendee_input = input("Enter Attendee ID : ")

        if not attendee_input.isdigit():
            print("*** ERROR *** Invalid attendee ID")
            continue

        attendee_id = int(attendee_input)

        # Check attendee exists
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

        #  Neo4j query
        driver = get_neo4j_driver()

        with driver.session() as session:
            result = session.run(
                """
                MATCH (a:Attendee {AttendeeID: $id})-[:CONNECTED_TO]-(mutual)-[:CONNECTED_TO]-(suggested)
                WHERE NOT (a)-[:CONNECTED_TO]-(suggested)
                AND a <> suggested
                RETURN suggested.AttendeeID AS id, count(mutual) AS score
                ORDER BY score DESC
                LIMIT 5
                """,
                id=attendee_id
            )

            suggestions = list(result)
# Data Access Object - Database query functions
# Author: Mariane McGrath
#
# INNOVATION FEATURE - Suggested Connections
#
# This feature implements a recommendation system using Neo4j.
# It identifies second-degree connections (friends-of-friends) by traversing the graph and excluding already connected attendees.

# Suggested attendees are ranked based on the number of mutual connections they share with the user. 

# MySQL is used to retrieve attendee names for display.

from db_connection import get_connection
from neo4j_connection import get_neo4j_driver

print(">>> NEW VERSION RUNNING <<<")

def suggest_connections():

    while True:
        attendee_input = input("Enter Attendee ID : ")

        if not attendee_input.isdigit():
            print("*** ERROR *** Invalid attendee ID")
            continue

        attendee_id = int(attendee_input)

        # Check attendee exists
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

        #  Neo4j query
        driver = get_neo4j_driver()

        with driver.session() as session:
            result = session.run(
                """
                MATCH (a:Attendee {AttendeeID: $id})-[:CONNECTED_TO]-(mutual)-[:CONNECTED_TO]-(suggested)
                WHERE NOT (a)-[:CONNECTED_TO]-(suggested)
                AND a <> suggested
                RETURN suggested.AttendeeID AS id, count(mutual) AS score
                ORDER BY score DESC
                LIMIT 5
                """,
                id=attendee_id
            )

            suggestions = list(result)

        driver.close()

        if not suggestions:
            print("No suggestions available (no second-degree connections found)")
            break

        # MySQL enrichment 
        conn = get_connection()
        cursor = conn.cursor()

        ids = [s["id"] for s in suggestions]
        format_strings = ",".join(["%s"] * len(ids))

        cursor.execute(f"""
            SELECT 
                a.attendeeID,
                a.attendeeName,
                c.companyName,
                s.sessionTitle
            FROM attendee a
            JOIN company c ON a.attendeeCompanyID = c.companyID
            LEFT JOIN attendee_session r ON a.attendeeID = r.attendeeID
            LEFT JOIN session s ON r.sessionID = s.sessionID
            WHERE a.attendeeID IN ({format_strings})
        """, tuple(ids))

        rows = cursor.fetchall()
        conn.close()

        # Organise data 
        data_map = {}

        for attendeeID, name, company, session in rows:
            if attendeeID not in data_map:
                data_map[attendeeID] = {
                    "name": name,
                    "company": company,
                    "sessions": []
                }

            if session:
                data_map[attendeeID]["sessions"].append(session)

        #  Output 
        print("--------------------------------------------------")

        rank = 1
        for s in suggestions:
            sid = s["id"]
            score = s["score"]

            person = data_map.get(sid, {})
            name = person.get("name", "Unknown")
            company = person.get("company", "Unknown")
            sessions = person.get("sessions", [])

            print(f"{rank} | {name:<20} | {score} mutual connection(s)")
            print(f"    Company: {company}")

            if sessions:
                print(f"    Sessions: {', '.join(sessions)}")
            else:
                print("    Sessions: None recorded")

            print()
            rank += 1

        print("Tip: These people share mutual connections with you — ideal for networking.")

        driver.close()

        if not suggestions:
            print("No suggestions available (no second-degree connections found)")
            break

        # MySQL enrichment 
        conn = get_connection()
        cursor = conn.cursor()

        ids = [s["id"] for s in suggestions]
        format_strings = ",".join(["%s"] * len(ids))

        cursor.execute(f"""
            SELECT 
                a.attendeeID,
                a.attendeeName,
                c.companyName,
                s.sessionTitle
            FROM attendee a
            JOIN company c ON a.attendeeCompanyID = c.companyID
            LEFT JOIN registration r ON a.attendeeID = r.attendeeID
            LEFT JOIN session s ON r.sessionID = s.sessionID
            WHERE a.attendeeID IN ({format_strings})
        """, tuple(ids))

        rows = cursor.fetchall()
        conn.close()

        # Organise data 
        data_map = {}

        for attendeeID, name, company, session in rows:
            if attendeeID not in data_map:
                data_map[attendeeID] = {
                    "name": name,
                    "company": company,
                    "sessions": []
                }

            if session:
                data_map[attendeeID]["sessions"].append(session)

        #  Output 
        print("--------------------------------------------------")

        rank = 1
        for s in suggestions:
            sid = s["id"]
            score = s["score"]

            person = data_map.get(sid, {})
            name = person.get("name", "Unknown")
            company = person.get("company", "Unknown")
            sessions = person.get("sessions", [])

            print(f"{rank} | {name:<20} | {score} mutual connection(s)")
            print(f"    Company: {company}")

            if sessions:
                print(f"    Sessions: {', '.join(sessions)}")
            else:
                print("    Sessions: None recorded")

            print()
            rank += 1

        print("Tip: These people share mutual connections with you — ideal for networking.")
        break