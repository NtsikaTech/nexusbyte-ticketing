import tkinter as tk
from tkinter import messagebox, simpledialog
import json
from tkinter import filedialog

# Global list to store tickets
tickets = []

# Functions for each button
def add_ticket_gui():
    def submit_ticket():
        title = title_entry.get()
        description = description_entry.get("1.0", tk.END).strip()
        urgency = urgency_var.get()

        if not title or not description or urgency == "Select":
            messagebox.showwarning("Input Error", "Please fill all fields!")
            return

        # Generate ticket ID
        ticket_id = f"Nexus-{len(tickets) + 1}"

        # Save ticket
        new_ticket = {
            "ticket_id": ticket_id,
            "title": title,
            "description": description,
            "urgency": urgency,
            "status": "Open"
        }
        tickets.append(new_ticket)

        messagebox.showinfo("Ticket Added", f"Ticket '{ticket_id}' added successfully!")
        add_ticket_window.destroy()

    # Create a new top-level window for adding a ticket
    add_ticket_window = tk.Toplevel(root)
    add_ticket_window.title("Add New Ticket")
    add_ticket_window.geometry("400x400")
    add_ticket_window.configure(bg="white")

    # Title
    title_label = tk.Label(add_ticket_window, text="Ticket Title", font=("Arial", 12), bg="white")
    title_label.pack(pady=(10, 5))

    title_entry = tk.Entry(add_ticket_window, font=("Arial", 12), width=30)
    title_entry.pack(pady=5)

    # Description
    description_label = tk.Label(add_ticket_window, text="Ticket Description", font=("Arial", 12), bg="white")
    description_label.pack(pady=(10, 5))

    description_entry = tk.Text(add_ticket_window, font=("Arial", 12), width=30, height=5)
    description_entry.pack(pady=5)

    # Urgency
    urgency_label = tk.Label(add_ticket_window, text="Urgency", font=("Arial", 12), bg="white")
    urgency_label.pack(pady=(10, 5))

    urgency_var = tk.StringVar(value="Select")
    urgency_options = ["Select", "Low", "Medium", "High"]
    urgency_menu = tk.OptionMenu(add_ticket_window, urgency_var, *urgency_options)
    urgency_menu.config(font=("Arial", 12), width=30)
    urgency_menu.pack(pady=5)

    # Submit Button
    submit_button = tk.Button(add_ticket_window, text="Add Ticket", command=submit_ticket, font=("Arial", 12), bg="#4CAF50", fg="white", width=30, height=2)
    submit_button.pack(pady=(20, 10))

def view_tickets_gui():
    # Create a new top-level window to show all tickets
    view_tickets_window = tk.Toplevel(root)
    view_tickets_window.title("View All Tickets")
    view_tickets_window.geometry("500x400")
    view_tickets_window.configure(bg="white")

    # Create a listbox to display tickets
    listbox = tk.Listbox(view_tickets_window, font=("Arial", 12), width=50, height=15)
    listbox.pack(pady=20)

    # Display each ticket in the listbox
    for idx, ticket in enumerate(tickets, start=1):
        listbox.insert(tk.END, f"{ticket['ticket_id']} - {ticket['title']} - {ticket['urgency']} - {ticket['status']}")


def view_open_tickets_gui():
    # Create a new top-level window to show only open tickets
    view_open_window = tk.Toplevel(root)
    view_open_window.title("View Open Tickets")
    view_open_window.geometry("500x400")
    view_open_window.configure(bg="white")

    # Create a listbox to display open tickets
    listbox = tk.Listbox(view_open_window, font=("Arial", 12), width=50, height=15)
    listbox.pack(pady=20)

    # Filter and display only open tickets
    open_tickets = [ticket for ticket in tickets if ticket['status'] == "Open"]
    if not open_tickets:
        listbox.insert(tk.END, "No open tickets at the moment.")
    else:
        for idx, ticket in enumerate(open_tickets, start=1):
            listbox.insert(tk.END, f"{idx}. {ticket['title']} - {ticket['urgency']} - {ticket['status']}")

def mark_resolved_gui():
    # Get the ticket number to mark as resolved
    ticket_numbers = [str(i+1) for i, ticket in enumerate(tickets) if ticket['status'] == 'Open']
    if not ticket_numbers:
        messagebox.showinfo("No Open Tickets", "There are no open tickets to resolve.")
        return
    
    # Ask the user to select a ticket number
    ticket_number = simpledialog.askstring("Select Ticket", f"Enter the ticket number to resolve:\n{', '.join(ticket_numbers)}")
    
    if ticket_number not in ticket_numbers:
        messagebox.showerror("Invalid Input", "Please enter a valid ticket number.")
        return

    # Find the selected ticket and mark it as resolved
    selected_ticket = tickets[int(ticket_number) - 1]
    selected_ticket['status'] = 'Resolved'
    
    messagebox.showinfo("Ticket Resolved", f"Ticket '{selected_ticket['title']}' has been marked as resolved.")

def delete_ticket_gui():
    # Get the ticket number to delete
    ticket_numbers = [str(i+1) for i, ticket in enumerate(tickets)]
    if not ticket_numbers:
        messagebox.showinfo("No Tickets", "There are no tickets to delete.")
        return
    
    # Ask the user to select a ticket number
    ticket_number = simpledialog.askstring("Select Ticket", f"Enter the ticket number to delete:\n{', '.join(ticket_numbers)}")
    
    if ticket_number not in ticket_numbers:
        messagebox.showerror("Invalid Input", "Please enter a valid ticket number.")
        return

    # Delete the selected ticket
    selected_ticket = tickets.pop(int(ticket_number) - 1)
    
    messagebox.showinfo("Ticket Deleted", f"Ticket '{selected_ticket['title']}' has been deleted.")

def search_tickets_gui():
    # Ask for search keyword
    keyword = simpledialog.askstring("Search Tickets", "Enter a keyword to search for tickets:")
    
    if not keyword:
        messagebox.showwarning("No Keyword", "Please enter a keyword to search.")
        return
    
    # Filter tickets based on the keyword in title or description
    matching_tickets = [ticket for ticket in tickets if keyword.lower() in ticket['title'].lower() or keyword.lower() in ticket['description'].lower()]
    
    # Show results
    if not matching_tickets:
        messagebox.showinfo("No Matches", f"No tickets found matching '{keyword}'.")
    else:
        result_window = tk.Toplevel(root)
        result_window.title(f"Search Results for '{keyword}'")
        result_window.geometry("500x400")
        result_window.configure(bg="white")
        
        listbox = tk.Listbox(result_window, font=("Arial", 12), width=50, height=15)
        listbox.pack(pady=20)
        
        for idx, ticket in enumerate(matching_tickets, start=1):
            listbox.insert(tk.END, f"{idx}. {ticket['title']} - {ticket['urgency']} - {ticket['status']}")

def report_open_tickets_gui():
    # Create a new window to show the report of open tickets
    open_tickets = [ticket for ticket in tickets if ticket['status'] == "Open"]
    if not open_tickets:
        messagebox.showinfo("No Open Tickets", "No open tickets to generate a report.")
        return

    report_window = tk.Toplevel(root)
    report_window.title("Report of Open Tickets")
    report_window.geometry("500x400")
    report_window.configure(bg="white")

    listbox = tk.Listbox(report_window, font=("Arial", 12), width=50, height=15)
    listbox.pack(pady=20)

    for idx, ticket in enumerate(open_tickets, start=1):
        listbox.insert(tk.END, f"{idx}. {ticket['title']} - {ticket['urgency']} - {ticket['status']}")

def report_all_tickets_gui():
    # Create a new window to show the report of all tickets
    report_window = tk.Toplevel(root)
    report_window.title("Full Ticket Report")
    report_window.geometry("500x400")
    report_window.configure(bg="white")

    listbox = tk.Listbox(report_window, font=("Arial", 12), width=50, height=15)
    listbox.pack(pady=20)

    if not tickets:
        listbox.insert(tk.END, "No tickets available.")
    else:
        for idx, ticket in enumerate(tickets, start=1):
            listbox.insert(tk.END, f"{idx}. {ticket['title']} - {ticket['urgency']} - {ticket['status']}")

def backup_data_gui():
    if not tickets:
        messagebox.showinfo("No Tickets", "There are no tickets to back up.")
        return

    # Ask where to save the backup
    file_path = filedialog.asksaveasfilename(
        defaultextension=".json",
        filetypes=[("JSON files", "*.json")],
        title="Save Backup As"
    )

    if not file_path:
        return  # User cancelled

    try:
        with open(file_path, "w") as f:
            json.dump(tickets, f, indent=4)
        messagebox.showinfo("Backup Successful", f"Tickets successfully backed up to:\n{file_path}")
    except Exception as e:
        messagebox.showerror("Backup Failed", f"An error occurred: {e}")

def restore_data_gui():
    global tickets

    file_path = filedialog.askopenfilename(
        filetypes=[("JSON files", "*.json")],
        title="Select Backup File"
    )

    if not file_path:
        return

    try:
        with open(file_path, "r") as f:
            loaded_tickets = json.load(f)

        # Modern confirmation popup
        confirm = modern_popup("Confirm Restore", "Restoring will overwrite current tickets.\nProceed?", popup_type="confirm")

        if confirm:
            tickets = loaded_tickets
            modern_popup("Restore Successful", "Tickets successfully restored from backup.", popup_type="info")
    except Exception as e:
        modern_popup("Restore Failed", f"An error occurred: {e}", popup_type="error")

def modern_popup(title, message, popup_type="info"):
    popup = tk.Toplevel(root)
    popup.title(title)
    popup.geometry("400x200")
    popup.configure(bg="white")
    popup.resizable(False, False)

    label = tk.Label(popup, text=message, font=("Arial", 12), bg="white", wraplength=350)
    label.pack(pady=20)

    if popup_type == "confirm":
        result = {"value": False}

        def on_yes():
            result["value"] = True
            popup.destroy()

        def on_no():
            result["value"] = False
            popup.destroy()

        button_frame = tk.Frame(popup, bg="white")
        button_frame.pack(pady=10)

        yes_btn = tk.Button(button_frame, text="Yes", command=on_yes, width=10, bg="#4CAF50", fg="white", font=("Arial", 11))
        yes_btn.grid(row=0, column=0, padx=10)

        no_btn = tk.Button(button_frame, text="No", command=on_no, width=10, bg="#f44336", fg="white", font=("Arial", 11))
        no_btn.grid(row=0, column=1, padx=10)

        popup.wait_window()
        return result["value"]
    else:
        ok_btn = tk.Button(popup, text="OK", command=popup.destroy, width=15, bg="#4CAF50", fg="white", font=("Arial", 11))
        ok_btn.pack(pady=10)

#function that saves the current state of tickets to a JSON file when the app exits and loads them when the app starts.

def save_tickets():
    try:
        with open("tickets.json", "w") as f:
            json.dump(tickets, f, indent=4)
    except Exception as e:
        messagebox.showerror("Save Error", f"An error occurred while saving tickets: {e}")
     
def load_tickets():
    global tickets
    try:
        with open("tickets.json", "r") as f:
            tickets = json.load(f)
    except FileNotFoundError:
        # If the file doesn't exist, start with an empty list
        tickets = []
    except Exception as e:
        messagebox.showerror("Load Error", f"An error occurred while loading tickets: {e}")

        

# GUI Setup
root = tk.Tk()
root.title("Nexusbyte Client Ticketing System")

# Set window size
root.geometry("500x700")
root.configure(bg="white")  # White background

# Create a Canvas and Scrollbar
canvas = tk.Canvas(root, bg="white", highlightthickness=0)
scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)

# Scrollable frame inside the canvas
scrollable_frame = tk.Frame(canvas, bg="white")

# Bind the frame size to the canvas scroll region
scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="n", width=480)  # Center nicely

# Load and resize logo
logo = tk.PhotoImage(file="logo.gif")
logo = logo.subsample(3, 3)
logo_label = tk.Label(scrollable_frame, image=logo, bg="white")
logo_label.pack(pady=(10, 5))

# Title label inside scrollable frame
title_label = tk.Label(scrollable_frame, text="Nexusbyte Ticketing System", font=("Arial", 18, "bold"), bg="white", pady=10)
title_label.pack()

# Define a common button style
button_style = {
    "font": ("Arial", 11),
    "bg": "#4CAF50",
    "fg": "white",
    "activebackground": "#45a049",
    "width": 30,
    "height": 1,
    "bd": 0,
    "relief": "raised"
}

# List of buttons
buttons = [
    ("Add Ticket", add_ticket_gui),
    ("View All Tickets", view_tickets_gui),
    ("View Open Tickets", view_open_tickets_gui),
    ("Mark Ticket as Resolved", mark_resolved_gui),
    ("Delete Ticket", delete_ticket_gui),
    ("Search Tickets", search_tickets_gui),
    ("View Report of Open Tickets", report_open_tickets_gui),
    ("View Full Ticket Report", report_all_tickets_gui),
    ("Backup Ticket Data", backup_data_gui),
    ("Restore Ticket Data", restore_data_gui),
    ("Exit", root.quit)
]

# Create buttons inside scrollable frame
for text, command in buttons:
    btn = tk.Button(scrollable_frame, text=text, command=command, **button_style)
    btn.pack(pady=6)

# Pack canvas and scrollbar
canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)
scrollbar.pack(side="right", fill="y")

# Run the app
root.mainloop()
