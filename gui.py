import tkinter as tk
from tkinter import messagebox
from ticketing_gui import save_tickets, load_tickets

tickets = load_tickets()

def refresh_ticket_list():
    ticket_listbox.delete(0, tk.END)
    for i, t in enumerate(tickets):
        status = "✅ Resolved" if t["status"] == "resolved" else "🟡 Open"
        ticket_listbox.insert(
            tk.END,
            f"{i + 1}. {t['name']} - {t['issue']} ({t['urgency']}) [{status}]"
        )

def submit_ticket():
    name = name_entry.get()
    issue = issue_entry.get()
    ref = ref_entry.get()
    date = date_entry.get()
    urgency = urgency_var.get()

    if not all([name, issue, ref, date, urgency]):
        messagebox.showwarning("Input Error", "Please fill out all fields.")
        return

    ticket = {
        "name": name,
        "issue": issue,
        "Reference": ref,
        "Clients name": name,
        "issue type": issue,
        "date": date,
        "urgency": urgency,
        "status": "open"
    }

    tickets.append(ticket)
    save_tickets(tickets)
    messagebox.showinfo("Ticket Added", "Ticket added successfully!")
    refresh_ticket_list()

    name_entry.delete(0, tk.END)
    issue_entry.delete(0, tk.END)
    ref_entry.delete(0, tk.END)
    date_entry.delete(0, tk.END)
    urgency_var.set("low")

def mark_selected_resolved():
    selected = ticket_listbox.curselection()
    if not selected:
        messagebox.showwarning("No selection", "Please select a ticket to mark as resolved.")
        return

    index = selected[0]
    if tickets[index]["status"] == "resolved":
        messagebox.showinfo("Already Resolved", "This ticket is already resolved.")
        return

    tickets[index]["status"] = "resolved"
    save_tickets(tickets)
    messagebox.showinfo("Success", "Ticket marked as resolved.")
    refresh_ticket_list()

def delete_selected_ticket():
    selected = ticket_listbox.curselection()
    if not selected:
        messagebox.showwarning("No selection", "Please select a ticket to delete.")
        return

    index = selected[0]
    confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete ticket: {tickets[index]['issue']}?")
    
    if confirm:
        deleted_ticket = tickets.pop(index)
        save_tickets(tickets)
        refresh_ticket_list()
        messagebox.showinfo("Deleted", f"Deleted ticket: {deleted_ticket['issue']}")

# ---- GUI Setup ----
app = tk.Tk()
app.title("Nexusbyte Ticketing System")
app.geometry("750x650")

# ---- Ticket Form ----
tk.Label(app, text="Client Name").pack()
name_entry = tk.Entry(app, width=40)
name_entry.pack()

tk.Label(app, text="Issue").pack()
issue_entry = tk.Entry(app, width=40)
issue_entry.pack()

tk.Label(app, text="Reference").pack()
ref_entry = tk.Entry(app, width=40)
ref_entry.pack()

tk.Label(app, text="Date (YYYY-MM-DD)").pack()
date_entry = tk.Entry(app, width=40)
date_entry.pack()

tk.Label(app, text="Urgency").pack()
urgency_var = tk.StringVar(value="low")
tk.OptionMenu(app, urgency_var, "low", "medium", "high").pack()

tk.Button(app, text="➕ Submit Ticket", command=submit_ticket).pack(pady=10)

# ---- Ticket Listbox ----
tk.Label(app, text="📋 Ticket List").pack(pady=5)
ticket_listbox = tk.Listbox(app, width=90, height=15)
ticket_listbox.pack(pady=5)

tk.Button(app, text="✅ Mark as Resolved", command=mark_selected_resolved).pack(pady=5)

# ---- Initial Load ----
refresh_ticket_list()

app.mainloop()
