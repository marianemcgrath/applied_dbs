# Main application file for conference management system
# Author: Mariane McGrath

import re
from db_connection import get_connection
from neo4j_connection import get_neo4j_driver

# INNOVATION FEATURE - import networking function from dao.py
from dao import suggest_connections, key_connectors

# Cache for rooms (loaded once per session - option 6 requirement)
_rooms_cache = None


def view_speakers_and_sessions():
    search = input("Enter speaker name : ")

    if not search.strip():
        print("*** ERROR *** Please enter a speaker name")
        return

    print(f"Session Details For : {search}")
    print("--------------------------------------------")
    
    conn = get_connection()
    cursor = conn.cursor()
    
    query = """
        SELECT s.speakerName, s.sessionTitle, r.roomName
        FROM session s
        JOIN room r ON s.roomID = r.roomID
        WHERE s.speakerName LIKE %s
    """
    cursor.execute(query, (f"%{search}%",))
    rows = cursor.fetchall()
    
    if rows:
        for row in rows:
            print(f"{row[0]:<20} | {row[1]:<35} | {row[2]}")
    else:
        print("No speakers found of that name")
    
    conn.close()


def view_attendees_by_company():
    while True:
        company_id = input("Enter Company ID : ")
        
        if not company_id.isdigit() or int(company_id) <= 0:
            print("*** ERROR *** Invalid Company ID")
            continue
        
        company_id = int(company_id)
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT companyName FROM company WHERE companyID = %s", (company_id,))
        company = cursor.fetchone()
        
        if not company:
            print(f"Company with ID {company_id} doesn't exist")
            conn.close()
            continue
        
        company_name = company[0]
        print(f"{company_name} Attendees")
        print("----------------------------------------------------------------------------------------------------------------------------------")
        
        query = """
            SELECT a.attendeeName, a.attendeeDOB, s.speakerName, 
                   s.sessionTitle, s.sessionDate, r.roomName
            FROM attendee a
            JOIN registration reg ON a.attendeeID = reg.attendeeID
            JOIN session s ON reg.sessionID = s.sessionID
            JOIN room r ON s.roomID = r.roomID
            WHERE a.attendeeCompanyID = %s
        """
        cursor.execute(query, (company_id,))
        rows = cursor.fetchall()
        
        if not rows:
            print(f"No attendees found for {company_name}")
        else:
            for row in rows:
                print(f"{row[0]:<20} | {row[1]} | {row[2]:<20} | {row[3]:<35} | {row[4]} | {row[5]}")
                # Order: AttendeeName | DOB | SpeakerName | SessionTitle | SessionDate | RoomName
        conn.close()
        break


def add_new_attendee():
    print("\nAdd New Attendee")
    print("----------------")
    
    attendee_id = input("Attendee ID : ")
    name = input("Name : ")
    dob = input("DOB : ")
    gender = input("Gender : ").upper()
    company_id = input("Company ID : ")
    
    conn = get_connection()
    cursor = conn.cursor()
    
    if not attendee_id.isdigit():
        print("*** ERROR *** Invalid Attendee ID")
        conn.close()
        return
    
    if not re.match(r'^\d{4}-\d{2}-\d{2}$', dob):
        print("*** ERROR *** Invalid DOB")
        conn.close()
        return
    
    if gender not in ("M", "F"):
        print("*** ERROR *** Gender must be M/F")
        conn.close()
        return
    
    cursor.execute("SELECT attendeeID FROM attendee WHERE attendeeID = %s", (attendee_id,))
    if cursor.fetchone():
        print(f"*** ERROR *** Attendee ID: {attendee_id} already exists")
        conn.close()
        return
    
    cursor.execute("SELECT companyID FROM company WHERE companyID = %s", (company_id,))
    if not cursor.fetchone():
        print(f"*** ERROR *** Company ID: {company_id} does not exist")
        conn.close()
        return
    
    try:
        query = """
            INSERT INTO attendee (attendeeID, attendeeName, attendeeDOB, attendeeGender, attendeeCompanyID)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (attendee_id, name, dob, gender, company_id))
        conn.commit()
        print("Attendee successfully added")
    except Exception as e:
        print(f"*** ERROR *** {e}")
    
    conn.close()


def view_connected_attendees():
    while True:
        attendee_input = input("Enter Attendee ID : ")
        
        if not attendee_input.isdigit():
            print("*** ERROR *** Invalid attendee ID")
            continue
        
        attendee_id = int(attendee_input)
        
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT attendeeName FROM attendee WHERE attendeeID = %s", (attendee_id,))
        mysql_row = cursor.fetchone()
        conn.close()
        
        if not mysql_row:
            print("*** ERROR *** Attendee does not exist")
            continue
        
        attendee_name = mysql_row[0]
        print(f"Attendee Name: {attendee_name}")
        print("--------------------")
        
        driver = get_neo4j_driver()
        with driver.session(database="appdbprojNeo4j") as session:
            node_check = session.run(
                "MATCH (a:Attendee {AttendeeID: $id}) RETURN a",
                id=attendee_id
            )
            node_exists = node_check.single() is not None
            
            if not node_exists:
                print("No connections")
            else:
                result = session.run(
                    """
                    MATCH (a:Attendee {AttendeeID: $id})-[:CONNECTED_TO]-(b:Attendee)
                    RETURN b.AttendeeID AS connectedID
                    """,
                    id=attendee_id
                )
                connected_ids = [record["connectedID"] for record in result]
                
                if not connected_ids:
                    print("No connections")
                else:
                    print("These attendees are connected:")
                    conn = get_connection()
                    cursor = conn.cursor()
                    for cid in connected_ids:
                        cursor.execute("SELECT attendeeName FROM attendee WHERE attendeeID = %s", (cid,))
                        row = cursor.fetchone()
                        name = row[0] if row else "Unknown"
                        print(f"{cid}  |  {name}")
                    conn.close()
        driver.close()
        break


def add_attendee_connection():
    while True:
        id1_input = input("Enter Attendee 1 ID : ")
        id2_input = input("Enter Attendee 2 ID : ")
        
        if not id1_input.isdigit() or not id2_input.isdigit():
            print("*** ERROR *** Attendee IDs must be numbers")
            continue
        
        id1 = int(id1_input)
        id2 = int(id2_input)
        
        if id1 == id2:
            print("*** ERROR *** An attendee cannot connect to him/herself")
            continue
        
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT attendeeID FROM attendee WHERE attendeeID IN (%s, %s)", (id1, id2))
        found = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        if id1 not in found or id2 not in found:
            print("*** ERROR *** One or both attendee IDs do not exist")
            continue
        
        driver = get_neo4j_driver()
        with driver.session(database="appdbprojNeo4j") as session:
            result = session.run(
                """
                MATCH (a:Attendee {AttendeeID: $id1})-[:CONNECTED_TO]-(b:Attendee {AttendeeID: $id2})
                RETURN count(*) AS cnt
                """,
                id1=id1, id2=id2
            )
            already_connected = result.single()["cnt"] > 0
            
            if already_connected:
                print("*** ERROR *** These attendees are already connected")
                driver.close()
                continue
            
            # Relationship treated as undirected (as per spec)
            session.run(
                """
                MERGE (a:Attendee {AttendeeID: $id1})
                MERGE (b:Attendee {AttendeeID: $id2})
                MERGE (a)-[:CONNECTED_TO]-(b)
                """,
                id1=id1, id2=id2
            )
        
        driver.close()
        print(f"Attendee {id1} is now CONNECTED_TO attendee {id2}")
        break


def view_rooms():
    global _rooms_cache
    
    if _rooms_cache is None:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT roomID, roomName, capacity FROM room ORDER BY roomID")
        _rooms_cache = cursor.fetchall()
        conn.close()
    
    print(f"{'RoomID':<8} | {'RoomName':<20} | Capacity")
    print("-" * 45)
    for row in _rooms_cache:
        print(f"{row[0]:<8} | {row[1]:<20} | {row[2]}")


def main():
    while True:
        print("\nConference Management")
        print("--------------------")
        print("\nMENU")
        print("====")
        print("1 - View Speakers & Sessions")
        print("2 - View Attendees by Company")
        print("3 - Add New Attendee")
        print("4 - View Connected Attendees")
        print("5 - Add Attendee Connection")
        print("6 - View Rooms")
        print("7 - Networking Insights")
        print("x - Exit application")
        
        choice = input("Choice: ").strip()
        
        if choice == "1":
            view_speakers_and_sessions()
        elif choice == "2":
            view_attendees_by_company()
        elif choice == "3":
            add_new_attendee()
        elif choice == "4":
            view_connected_attendees()
        elif choice == "5":
            add_attendee_connection()
        elif choice == "6":
            view_rooms()
        elif choice == "7":
            suggest_connections()
            key_connectors()
        elif choice == "x":
            print("Goodbye!")
            break


if __name__ == "__main__":
    main()