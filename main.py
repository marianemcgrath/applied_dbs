# Applied Databases Project
# Author: Mariane McGrath

from db_connection import get_connection
from neo4j_connection import get_neo4j_driver

def view_speakers_and_sessions():
    search = input("Enter speaker name : ")
    print(f"Session Details For :  {search}")
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
            print("Enter a valid Company ID")
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
        
        query = """
            SELECT a.attendeeName, a.attendeeDOB, s.sessionTitle, 
                   s.speakerName, s.sessionDate, r.roomName
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
                print(f"{row[0]:<15} | {row[1]} | {row[2]:<35} | {row[3]:<20} | {row[4]} | {row[5]}")
        
        conn.close()
        break

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
        print("x - Exit application")
        
        choice = input("Choice: ")

        if choice == "1":
            view_speakers_and_sessions()
        elif choice == "2":
            view_attendees_by_company()
        elif choice == "x":
            print("Goodbye!")
            break

if __name__ == "__main__":
    main()