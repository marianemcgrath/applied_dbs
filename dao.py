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

    # Step 2: Get and validate degree of separation (2-4)
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