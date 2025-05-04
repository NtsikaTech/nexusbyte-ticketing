# TO DO:
# 1. Add a ticket
# 2. View all tickets
# 3. Mark a ticket as resolved
# 4. Delete a ticket
# 5. Save/load tickets from file

#Nexusbyte Client Ticketing System

import json
import shutil
import os
import random
import json
import time

otp_storage = {}


#request user identity (email address)
def request_identification():
    user_id = input("Enter your email address: ").strip()
    return user_id 



#this function will load the tickets from a json file and if the file does not exist it will create a new one
#this will allow us to store the tickets in a json file so that we can access them later
def backup_data():
    try:
        if not os.path.exists("tickets.json"):
            print("No ticket data found to back up.")
            return
        
        backup_filename = "tickets_backup.json"
        shutil.copy("tickets.json", backup_filename)
        print(f"Backup created successfully as {backup_filename}.")
    except Exception as e:
        print(f"An error occurred while creating the backup: {e}")

#this function will load the tickets from a json file and if the file does not exist it will create a new one
#this will allow us to store the tickets in a json file so that we can access them later       
def restore_data():
    try:
        if not os.path.exists("tickets_backup.json"):
            print("No backup file found to restore from.")
            return
        
        shutil.copy("tickets_backup.json", "tickets.json")
        print("Ticket data restored from backup.")
    except Exception as e:
        print(f"An error occurred while restoring the backup: {e}")
        



#this function will load the tickets from a json file and if the file does not exist it will create a new one
#this will allow us to store the tickets in a json file so that we can access them later

def load_tickets():
    try:
        with open("tickets.json", "r") as file:
            # Load tickets and handle empty files
            tickets = json.load(file)
            if not tickets:
                print("No tickets found, starting fresh.")
                tickets = []
    except FileNotFoundError:
        print("Tickets file not found. Creating a new one.")
        tickets = []
    except json.JSONDecodeError:
        print("Error reading the tickets file. Starting fresh.")
        tickets = []
    
    return tickets


#this function will save the tickets to a json file so that we can access them later
#this will allow us to store the tickets in a json file so that we can access them later

def save_tickets(tickets):
    try:
        with open("tickets.json", "w") as file:
            json.dump(tickets, file, indent=4)
            print("Tickets saved successfully.")
    except Exception as e:
        print(f"Error saving tickets: {e}")

#this function will allow us to view the open tickets in the list
#it will first show us the tickets that are in the list and then we will be able to view the open tickets by entering the ticket number
       
def view_open_tickets():
    open_tickets = [ticket for ticket in tickets if ticket['status'] == "open"]
    
    if not open_tickets:
        print("No open tickets available.")
        return
    
    print("\nOpen Tickets:")
    for ticket in open_tickets:
        print(f"Name: {ticket['name']}, Issue: {ticket['issue']}, Status: {ticket['status']}")

#this function will allow us to view the tickets by urgency
#it will first show us the tickets that are in the list and then we will be able to view the tickets by urgency by entering the urgency level

def view_tickets_by_urgency(urgency_level):
    urgency_tickets = [ticket for ticket in tickets if ticket['urgency'] == urgency_level]
    
    if not urgency_tickets:
        print(f"No tickets with {urgency_level} urgency.")
        return
    
    print(f"\nTickets with {urgency_level} urgency:")
    for ticket in urgency_tickets:
        print(f"Name: {ticket['name']}, Issue: {ticket['issue']}, Urgency: {ticket['urgency']}, Status: {ticket['status']}")

#This function will allow us to generate reports based on the tickets
#it will first show us the tickets that are in the list and then we will be able to generate reports by entering the report type

def report_open_tickets():
    open_tickets = [ticket for ticket in tickets if ticket['status'] == "open"]
    print(f"\nTotal Open Tickets: {len(open_tickets)}")
    for ticket in open_tickets:
        print(f"Name: {ticket['name']}, Issue: {ticket['issue']}, Urgency: {ticket['urgency']}")

#this function will allow us to generate a report of all the tickets in the list
#it will first show us the tickets that are in the list and then we will be able to generate a report of all the tickets by entering the report type

def report_all_tickets():
    print("\nFull Ticket Report:")
    for ticket in tickets:
        print(f"Name: {ticket['name']}, Issue: {ticket['issue']}, Urgency: {ticket['urgency']}, Status: {ticket['status']}")



tickets = load_tickets()  #this will store all our ticket entries

def show_menu():
    print("\nNexusbyte Client Ticketing System")
    print("1. Add a ticket")
    print("2. View all tickets")
    print("3. View open tickets")
    print("4. View tickets by urgency")
    print("5. Mark a ticket as resolved")
    print("6. Delete a ticket")
    print("7. Search tickets")
    print("8. View report of open tickets")
    print("9. View full ticket report")
    print("10. Backup ticket data")
    print("11. Restore ticket data from backup")
    print("12. Exit")

    
#this will ask the user to input information inside the ticekt list

def add_ticket():
    name = input("Enter clients name: ")
    issue = input("Enter issue: ")
    Reference = input("Enter reference number: ")
    date = input("Enter date (YYYY-MM-DD): ")
    urgency = input("Enter urgency (low, medium, high): ")   
    
    ticket = {
        "name": name,
        "issue": issue,
        "Reference": Reference,
        "Clients name": name,
        "issue type": issue
        "date": date,
        "urgency": urgency,
        "status": "open"
    }
    
    tickets.append(ticket)
    save_tickets(tickets)  # <-- Save after adding
    print("Ticket added successfully!")
    
#with this function we will be able to view all the tickets that are in the list

def view_tickets():
    if not tickets:
        print("No tickets available.")
        return
    
    print("\nTickets:")
    for i, ticket in enumerate(tickets, start=1):
        print(f"{i}. Name: {ticket['name']}, Issue: {ticket['issue']}, Reference: {ticket['Reference']}, Date: {ticket['date']}, Urgency: {ticket['urgency']}, Status: {ticket['status']}")

#this function will allow us to mark a ticket as resolved
#it will first show us the tickets that are in the list and then we will be able to mark a ticket as resolved by entering the ticket number
     
def mark_resolved():
    view_tickets()
    
    if not tickets:
        return
    
    ticket_number = int(input("Enter the ticket number to mark as resolved: ")) - 1
    
    if 0 <= ticket_number < len(tickets):
        tickets[ticket_number]["status"] = "resolved"
        save_tickets(tickets)  # <-- Save after resolving
        print("Ticket marked as resolved.")
    else:
        print("Invalid ticket number.")

        
#this function will allow us to delete a ticket from the list
#it will first show us the tickets that are in the list and then we will be able to delete a ticket by entering the ticket number

def delete_ticket():
    view_tickets()
    
    if not tickets:
        return
    
    ticket_number = int(input("Enter the ticket number to delete: ")) - 1
    
    if 0 <= ticket_number < len(tickets):
        deleted_ticket = tickets.pop(ticket_number)
        save_tickets(tickets)  # <-- Save after deleting
        print(f"Ticket '{deleted_ticket['issue']}' deleted successfully.")
    else:
        print("Invalid ticket number.")
       
#this function will allow us to search for a ticket in the list
#it will first show us the tickets that are in the list and then we will be able to search for a ticket by entering the ticket number 
def search_tickets(query):
    found_tickets = []
    for ticket in tickets:
        # Convert all text to lowercase for case-insensitive searching
        if any(query.lower() in str(ticket[key]).lower() for key in ticket):
            found_tickets.append(ticket)

    if found_tickets:
        print("\nFound Tickets:")
        for i, ticket in enumerate(found_tickets, start=1):
            print(f"{i}. Name: {ticket['name']}, Issue: {ticket['issue']}, Reference: {ticket['Reference']}, Date: {ticket['date']}, Urgency: {ticket['urgency']}, Status: {ticket['status']}")
    else:
        print("No tickets found matching that query.")

# Call load_tickets() before starting the main loop to load saved tickets
load_tickets()

#adding a main menu it will allow us to test the function

def main():
    while True:
        show_menu()
        choice = input("Enter your choice (1-12): ")

        if choice == "1":
            add_ticket()
        elif choice == "2":
            view_tickets()
        elif choice == "3":
            view_open_tickets()
        elif choice == "4":
            view_tickets_by_urgency()
        elif choice == "5":
            mark_resolved()
        elif choice == "6":
            delete_ticket()
        elif choice == "7":
            query = input("Enter search keyword: ")
            search_tickets(query)
        elif choice == "8":
            view_open_report()
        elif choice == "9":
            view_full_report()
        elif choice == "10":
            backup_data()
        elif choice == "11":
            restore_data()
        elif choice == "12":
            print("Exiting the system.")
            break
        else:
            print("Invalid choice. Please try again.")

            
if __name__ == "__main__":
    main()