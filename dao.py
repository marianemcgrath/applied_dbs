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

        driver = get_neo4j_driver()

        with driver.session(database="appdbprojNeo4j") as session:
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

        # Fetch names in one query
        conn = get_connection()
        cursor = conn.cursor()

        ids = [s["id"] for s in suggestions]
        placeholders = ",".join(["%s"] * len(ids))

        cursor.execute(
            f"SELECT attendeeID, attendeeName FROM attendee WHERE attendeeID IN ({placeholders})",
            tuple(ids)
        )

        name_map = dict(cursor.fetchall())
        conn.close()

        # Clean formatted output
        print(f"{'ID':<6} | {'Name':<20} | Mutual Connections")
        print("--------------------------------------------------")

        for s in suggestions:
            name = name_map.get(s["id"], "Unknown")
            print(f"{s['id']:<6} | {name:<20} | {s['score']}")

        print("\nTip: These people share mutual connections with you — ideal for networking.")
        break
