# ticketing_gui.py

from datetime import datetime
import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
import csv
import os

TICKETS_CSV_FILE = "tickets.csv"

# Users
users = [
    {"username": "admin", "password": "admin123", "role": "admin"},
    {"username": "support1", "password": "support123", "role": "support"},
    {"username": "guest", "password": "guest123", "role": "user"},
    {"username": "Ntsika", "password": "Testing123", "role": "admin"}
]

tickets = []

# Ticket ID generator
def generate_ticket_id():
    if not tickets:
        return 1
    return max(ticket["id"] for ticket in tickets) + 1

# Save to CSV
def save_tickets():
    with open(TICKETS_CSV_FILE, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Name", "Urgency", "Title", "Description", "Status", "Created"])
        for ticket in tickets:
            writer.writerow([ticket["id"], ticket["name"], ticket["urgency"], ticket["title"],
                             ticket["description"], ticket["status"], ticket["created"]])

# Load from CSV
def load_tickets():
    if not os.path.exists(TICKETS_CSV_FILE):
        return
    with open(TICKETS_CSV_FILE, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            tickets.append({
                "id": int(row["ID"]),
                "name": row["Name"],
                "urgency": row["Urgency"],
                "title": row["Title"],
                "description": row["Description"],
                "status": row["Status"],
                "created": row["Created"]
            })

def export_tickets_to_csv():
    save_tickets()
    messagebox.showinfo("Export", f"✅ Tickets exported to {TICKETS_CSV_FILE}")

# Add new ticket
def add_ticket():
    name = name_entry.get().strip()
    urgency = urgency_var.get().strip()
    title = title_entry.get().strip()
    description = desc_entry.get("1.0", tk.END).strip()

    if not name or not urgency or not title or not description:
        messagebox.showwarning("Missing Info", "⚠️ Please fill in all fields.")
        return

    ticket_id = generate_ticket_id()
    ticket = {
        "id": ticket_id,
        "name": name,
        "urgency": urgency,
        "title": title,
        "description": description,
        "status": "Open",
        "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    tickets.append(ticket)
    save_tickets()
    update_ticket_list()

    name_entry.delete(0, tk.END)
    urgency_var.set("")
    title_entry.delete(0, tk.END)
    desc_entry.delete("1.0", tk.END)

    messagebox.showinfo("Success", f"🎫 Ticket #{ticket_id} created successfully!")

def update_ticket_list():
    ticket_list.delete(*ticket_list.get_children())
    for ticket in tickets:
        ticket_list.insert("", tk.END, values=(
            ticket["id"], ticket["name"], ticket["urgency"],
            ticket["title"], ticket["status"], ticket["created"]
        ))

def mark_ticket_closed():
    selected = ticket_list.selection()
    if not selected:
        messagebox.showwarning("Select Ticket", "⚠️ Please select a ticket.")
        return
    item = ticket_list.item(selected[0])
    ticket_id = int(item["values"][0])
    for ticket in tickets:
        if ticket["id"] == ticket_id:
            ticket["status"] = "Closed"
            break
    save_tickets()
    update_ticket_list()

def delete_ticket():
    selected = ticket_list.selection()
    if not selected:
        messagebox.showwarning("Select Ticket", "⚠️ Please select a ticket.")
        return
    item = ticket_list.item(selected[0])
    ticket_id = int(item["values"][0])
    for ticket in tickets:
        if ticket["id"] == ticket_id:
            tickets.remove(ticket)
            break
    save_tickets()
    update_ticket_list()

def open_admin_panel():
    admin_window = tk.Toplevel(root)
    admin_window.title("Admin Panel")
    admin_window.configure(bg="#1e1e1e")

    def update_user_list():
        user_list.delete(*user_list.get_children())
        for user in users:
            user_list.insert("", tk.END, values=(user["username"], user["role"]))

    def edit_user_role():
        selected = user_list.selection()
        if not selected:
            messagebox.showwarning("Select User", "⚠️ Please select a user.")
            return
        item = user_list.item(selected[0])
        username = item["values"][0]
        new_role = simpledialog.askstring("Edit Role", f"Enter new role for {username} (admin/support/user):")
        if new_role:
            for user in users:
                if user["username"] == username:
                    user["role"] = new_role
                    break
            update_user_list()

    user_list = ttk.Treeview(admin_window, columns=("Username", "Role"), show="headings")
    user_list.heading("Username", text="Username")
    user_list.heading("Role", text="Role")
    user_list.pack(padx=10, pady=10, fill="both", expand=True)

    edit_btn = tk.Button(admin_window, text="Edit Role", command=edit_user_role, bg="#00c896", fg="white")
    edit_btn.pack(pady=10)

    update_user_list()

def logout():
    root.withdraw()
    login_screen()

def login_screen():
    login_win = tk.Toplevel()
    login_win.title("Login")
    login_win.geometry("300x200")
    login_win.configure(bg="#1e1e1e")
    login_win.eval('tk::PlaceWindow . center')

    def attempt_login():
        username = username_entry.get().strip()
        password = password_entry.get().strip()
        for user in users:
            if user["username"] == username and user["password"] == password:
                login_win.destroy()
                root.deiconify()
                return
        messagebox.showerror("Login Failed", "❌ Invalid credentials.")

    tk.Label(login_win, text="Username", bg="#1e1e1e", fg="white").pack(pady=5)
    username_entry = tk.Entry(login_win, bg="#333", fg="white")
    username_entry.pack()

    tk.Label(login_win, text="Password", bg="#1e1e1e", fg="white").pack(pady=5)
    password_entry = tk.Entry(login_win, show="*", bg="#333", fg="white")
    password_entry.pack()

    tk.Button(login_win, text="Login", command=attempt_login, bg="green", fg="white").pack(pady=10)

# ---------------- Main UI ----------------
root = tk.Tk()
root.title("NexusByte Ticketing System")
root.geometry("950x600")
root.configure(bg="#1e1e1e")
root.withdraw()  # Hide until login
style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview", background="#2e2e2e", foreground="white", rowheight=25, fieldbackground="#2e2e2e")
style.map("Treeview", background=[("selected", "#555")])

tk.Label(root, text="Name & Surname", bg="#1e1e1e", fg="white").pack()
name_entry = tk.Entry(root, width=60, bg="#2e2e2e", fg="white")
name_entry.pack(pady=2)

tk.Label(root, text="Ticket Urgency", bg="#1e1e1e", fg="white").pack()
urgency_var = tk.StringVar()
urgency_dropdown = ttk.Combobox(root, textvariable=urgency_var, values=["Low", "Medium", "High"], width=57)
urgency_dropdown.pack(pady=2)

tk.Label(root, text="Ticket Title", bg="#1e1e1e", fg="white").pack()
title_entry = tk.Entry(root, width=60, bg="#2e2e2e", fg="white")
title_entry.pack(pady=2)

tk.Label(root, text="Description", bg="#1e1e1e", fg="white").pack()
desc_entry = tk.Text(root, height=4, width=60, bg="#2e2e2e", fg="white")
desc_entry.pack(pady=2)

btn_frame = tk.Frame(root, bg="#1e1e1e")
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Add Ticket", command=add_ticket, bg="green", fg="white", width=15).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="Mark Closed", command=mark_ticket_closed, bg="#444", fg="white", width=15).grid(row=0, column=1, padx=5)
tk.Button(btn_frame, text="Delete Ticket", command=delete_ticket, bg="#c0392b", fg="white", width=15).grid(row=0, column=2, padx=5)
tk.Button(btn_frame, text="Export CSV", command=export_tickets_to_csv, bg="#007acc", fg="white", width=15).grid(row=0, column=3, padx=5)
tk.Button(btn_frame, text="Admin Panel", command=open_admin_panel, bg="#5c5", fg="black", width=15).grid(row=0, column=4, padx=5)
tk.Button(btn_frame, text="Logout", command=logout, bg="#555", fg="white", width=15).grid(row=0, column=5, padx=5)

ticket_list = ttk.Treeview(root, columns=("ID", "Name", "Urgency", "Title", "Status", "Created"), show="headings")
for col in ticket_list["columns"]:
    ticket_list.heading(col, text=col)
ticket_list.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
