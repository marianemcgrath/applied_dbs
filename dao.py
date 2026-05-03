# Data Access Object - Database query functions
# Author: Mariane McGrath
#
# NOTE: This file contains the INNOVATION FEATURE - Networking (Suggested Connections)
# The networking() function implements a friend-of-a-friend recommendation engine
# using Neo4j graph traversal up to 4 degrees of separation.

from db_connection import get_connection
from neo4j_connection import get_neo4j_driver

# INNOVATION FEATURE - Networking (Suggested Connections)

# Uses Neo4j shortestPath to find attendees within N degrees of separation
# who are not already directly connected to the given attendee.
# The user can filter results by choosing how many degrees away to search (2-4).
# Names are looked up from MySQL to enrich the Neo4j results.


def networking():
    # --- Step 1: Get and validate attendee ID ---
    while True:
        attendee_input = input("Enter Attendee ID : ")

        if not attendee_input.isdigit():
            print("*** ERROR *** Invalid attendee ID")
            continue

        attendee_id = int(attendee_input)

        # Check attendee exists in MySQL
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT attendeeName FROM attendee WHERE attendeeID = %s", (attendee_id,))
        mysql_row = cursor.fetchone()
        conn.close()

        if not mysql_row:
            print("*** ERROR *** Attendee does not exist")
            continue

        attendee_name = mysql_row[0]
        print(f"Attendee Name:  {attendee_name}")
        print("--------------------")
        break

    # Step 2: Get and validate degree of separation (2-4) ---
    while True:
        degree_input = input("Show suggested connections up to how many degrees away? (2-4) : ")

        if not degree_input.isdigit():
            print("*** ERROR *** Please enter a number between 2 and 4")
            continue

        max_degree = int(degree_input)

        if max_degree < 2 or max_degree > 4:
            print("*** ERROR *** Degree must be between 2 and 4")
            continue

        break

    # Step 3: Query Neo4j for suggested connections ---
    driver = get_neo4j_driver()
    suggestions = []

    with driver.session(database="appdbprojNeo4j") as session:
        result = session.run(
            """
            MATCH path = shortestPath(
                (a:Attendee {AttendeeID: $id})-[:CONNECTED_TO*2..$max_deg]-(suggested:Attendee)
            )
            WHERE NOT (a)-[:CONNECTED_TO]-(suggested)
            AND suggested.AttendeeID <> $id
            RETURN suggested.AttendeeID AS suggestedID, length(path) AS degrees
            ORDER BY degrees, suggested.AttendeeID
            """,
            id=attendee_id,
            max_deg=max_degree
        )
        suggestions = [(record["suggestedID"], record["degrees"]) for record in result]

    driver.close()

    # Step 4: Display results ---
    print(f"\nSuggested Connections (up to {max_degree} degrees away)")
    print("--------------------------------------------------")

    if not suggestions:
        print(f"No networking suggestions found within {max_degree} degrees.")
        return

    # Look up names from MySQL for each suggested attendee
    conn = get_connection()
    cursor = conn.cursor()

    for (suggested_id, degrees) in suggestions:
        cursor.execute("""
        SELECT a.attendeeName, c.companyName, s.sessionTitle
        FROM attendee a
        JOIN company c ON a.attendeeCompanyID = c.companyID
        LEFT JOIN registration r ON a.attendeeID = r.attendeeID
        LEFT JOIN session s ON r.sessionID = s.sessionID
        WHERE a.attendeeID = %s
    """, (suggested_id,))
    rows = cursor.fetchall()

    name = rows[0][0] if rows else "Unknown"
    company = rows[0][1] if rows else "Unknown"
    degree_label = f"{degrees} degree{'s' if degrees > 1 else ''} away"
    print(f"{degree_label:<20} | {suggested_id:<6} | {name:<20} | {company}")

    if rows and rows[0][2]:
        for row in rows:
            print(f"{'':20}   {'':6}   Sessions: {row[2]}")
    else:
        print(f"{'':20}   {'':6}   No sessions recorded")
 
    conn.close()
    