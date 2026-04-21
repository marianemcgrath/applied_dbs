# Applied Databases Project
# Author: Mariane McGrath

from db_connection import get_connection

def main():
    print("Conference Management")
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

if __name__ == "__main__":
    main()