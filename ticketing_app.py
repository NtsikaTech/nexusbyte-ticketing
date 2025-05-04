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

# Initialize the list of tickets
tickets = []

# Backup function to create a backup of ticket data
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

# Restore ticket data from backup
def restore_data():
    try:
        if not os.path.exists("tickets_backup.json"):
            print("No backup file found to restore from.")
            return
        
        shutil.copy("tickets_backup.json", "tickets.json")
        print("Ticket data restored from backup.")
    except Exception as e:
        print(f"An error occurred while restoring the backup: {e}")

# Load tickets from a JSON file
def load_tickets():
    try:
        with open("tickets.json", "r") as file:
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

# Save tickets to a JSON file
def save_tickets(tickets):
    try:
        with open("tickets.json", "w") as file:
            json.dump(tickets, file, indent=4)
            print("Tickets saved successfully.")
    except Exception as e:
        print(f"Error saving tickets: {e}")

# Function to display open tickets
def view_open_tickets():
    open_tickets = [ticket for ticket in tickets if ticket['status'] == "open"]
    if not open_tickets:
        print("No open tickets available.")
        return
    
    print("\nOpen Tickets:")
    for ticket in open_tickets:
        print(f"Name: {ticket['name']}, Issue: {ticket['issue']}, Status: {ticket['status']}")

# Function to add a ticket
def add_ticket():
    name = input("Enter client's name: ")
    issue = input("Enter issue: ")
    Reference = input("Enter reference number: ")
    date = input("Enter date (YYYY-MM-DD): ")
    urgency = input("Enter urgency (low, medium, high): ")

    ticket = {
        "name": name,
        "issue": issue,
        "Reference": Reference,
        "Clients name": name,
        "issue type": issue,
        "date": date,
        "urgency": urgency,
        "status": "open"
    }

    tickets.append(ticket)
    save_tickets(tickets)  # <-- Save after adding
    print("Ticket added successfully!")

# Function to mark a ticket as resolved
def mark_resolved():
    view_open_tickets()
    
    if not tickets:
        return
    
    ticket_number = int(input("Enter the ticket number to mark as resolved: ")) - 1
    
    if 0 <= ticket_number < len(tickets):
        tickets[ticket_number]["status"] = "resolved"
        save_tickets(tickets)
        print("Ticket marked as resolved.")
    else:
        print("Invalid ticket number.")

# Function to delete a ticket
def delete_ticket():
    view_open_tickets()
    
    if not tickets:
        return
    
    ticket_number = int(input("Enter the ticket number to delete: ")) - 1
    
    if 0 <= ticket_number < len(tickets):
        deleted_ticket = tickets.pop(ticket_number)
        save_tickets(tickets)
        print(f"Ticket '{deleted_ticket['issue']}' deleted successfully.")
    else:
        print("Invalid ticket number.")

# Function to search tickets by query
def search_tickets(query):
    found_tickets = []
    for ticket in tickets:
        if any(query.lower() in str(ticket[key]).lower() for key in ticket):
            found_tickets.append(ticket)

    if found_tickets:
        print("\nFound Tickets:")
        for i, ticket in enumerate(found_tickets, start=1):
            print(f"{i}. Name: {ticket['name']}, Issue: {ticket['issue']}, Reference: {ticket['Reference']}, Date: {ticket['date']}, Urgency: {ticket['urgency']}, Status: {ticket['status']}")
    else:
        print("No tickets found matching that query.")

# Function to show the menu options
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

# Main function
def main():
    global tickets
    tickets = load_tickets()
    while True:
        show_menu()
        choice = input("Enter your choice (1-12): ")

        if choice == "1":
            add_ticket()
        elif choice == "2":
            view_open_tickets()
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
            report_open_tickets()
        elif choice == "9":
            report_all_tickets()
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
