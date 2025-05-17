import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import csv
import os
import datetime

TICKETS_CSV_FILE = "tickets.csv"

users = [
    {"username": "admin", "password": "admin123", "role": "admin"},
    {"username": "support1", "password": "support123", "role": "support"},
    {"username": "guest", "password": "guest123", "role": "user"},
    {"username": "Ntsika", "password": "Testing123", "role": "admin"},
]

tickets = []
current_user = None

def save_tickets():
    with open(TICKETS_CSV_FILE, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Title", "Description", "Status", "Created"])
        for ticket in tickets:
            writer.writerow([ticket["id"], ticket["title"], ticket["description"], ticket["status"], ticket["created"]])

def load_tickets():
    if not os.path.exists(TICKETS_CSV_FILE):
        return
    with open(TICKETS_CSV_FILE, mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            tickets.append({
                "id": int(row["ID"]),
                "title": row["Title"],
                "description": row["Description"],
                "status": row["Status"],
                "created": row["Created"]
            })

def export_tickets_to_csv():
    save_tickets()
    modern_popup("Tickets exported successfully!")

def add_ticket():
    title = title_entry.get()
    description = desc_entry.get("1.0", tk.END).strip()
    if not title or not description:
        messagebox.showwarning("Missing Info", "Please fill in all fields.")
        return
    ticket_id = len(tickets) + 1
    ticket = {
        "id": ticket_id,
        "title": title,
        "description": description,
        "status": "Open",
        "created": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    tickets.append(ticket)
    save_tickets()
    update_ticket_list()
    title_entry.delete(0, tk.END)
    desc_entry.delete("1.0", tk.END)
    modern_popup("Ticket added successfully!")

def update_ticket_list():
    ticket_list.delete(*ticket_list.get_children())
    for ticket in tickets:
        ticket_list.insert("", tk.END, values=(ticket["id"], ticket["title"], ticket["status"], ticket["created"]))

def mark_ticket_closed():
    selected = ticket_list.selection()
    if not selected:
        messagebox.showwarning("Select Ticket", "Please select a ticket.")
        return
    item = ticket_list.item(selected[0])
    ticket_id = int(item["values"][0])
    for ticket in tickets:
        if ticket["id"] == ticket_id:
            ticket["status"] = "Closed"
            break
    save_tickets()
    update_ticket_list()
    modern_popup("Ticket marked as closed.")

def delete_ticket():
    selected = ticket_list.selection()
    if not selected:
        messagebox.showwarning("Select Ticket", "Please select a ticket.")
        return
    item = ticket_list.item(selected[0])
    ticket_id = int(item["values"][0])
    for ticket in tickets:
        if ticket["id"] == ticket_id:
            tickets.remove(ticket)
            break
    save_tickets()
    update_ticket_list()
    modern_popup("Ticket deleted.")

def open_admin_panel():
    if current_user["role"] != "admin":
        messagebox.showerror("Access Denied", "You do not have permission to access the admin panel.")
        return

    admin_window = tk.Toplevel(root)
    admin_window.title("Admin Panel")
    admin_window.configure(bg="#1e1e1e")
    admin_window.geometry("400x300")

    def update_user_list():
        user_list.delete(*user_list.get_children())
        for user in users:
            user_list.insert("", tk.END, values=(user["username"], user["role"]))

    def edit_user_role():
        selected = user_list.selection()
        if not selected:
            messagebox.showwarning("Select User", "Please select a user.")
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
    user_list.configure(style="Treeview")

    edit_btn = tk.Button(admin_window, text="Edit Role", command=edit_user_role, bg="#3CB371", fg="white")
    edit_btn.pack(pady=10)

    update_user_list()

def modern_popup(message):
    popup = tk.Toplevel(root)
    popup.geometry("300x100+{}+{}".format(
        root.winfo_x() + int(root.winfo_width()/2) - 150,
        root.winfo_y() + int(root.winfo_height()/2) - 50))
    popup.configure(bg="#2b2b2b")
    popup.overrideredirect(True)

    label = tk.Label(popup, text=message, bg="#2b2b2b", fg="white", font=("Arial", 12, "bold"))
    label.pack(pady=20)
    popup.after(2000, popup.destroy)

def logout():
    global current_user
    current_user = None
    root.withdraw()
    login_screen()

def login_screen():
    login_win = tk.Toplevel()
    login_win.title("Login")
    login_win.geometry("300x200")
    login_win.configure(bg="#1e1e1e")
    login_win.grab_set()
    login_win.eval('tk::PlaceWindow . center')

    tk.Label(login_win, text="Username", bg="#1e1e1e", fg="white").pack(pady=(20, 5))
    username_entry = tk.Entry(login_win, bg="#2e2e2e", fg="white")
    username_entry.pack()

    tk.Label(login_win, text="Password", bg="#1e1e1e", fg="white").pack(pady=5)
    password_entry = tk.Entry(login_win, show="*", bg="#2e2e2e", fg="white")
    password_entry.pack()

def login_screen():
    login_win = tk.Toplevel()
    login_win.title("Login")
    login_win.geometry("300x200")
    login_win.configure(bg="#1e1e1e")
    login_win.grab_set()

    # Manual center
    login_win.update_idletasks()
    width = login_win.winfo_width()
    height = login_win.winfo_height()
    x = (login_win.winfo_screenwidth() // 2) - (width // 2)
    y = (login_win.winfo_screenheight() // 2) - (height // 2)
    login_win.geometry(f'+{x}+{y}')

    tk.Label(login_win, text="Username", bg="#1e1e1e", fg="white").pack(pady=(20, 5))
    username_entry = tk.Entry(login_win, bg="#2e2e2e", fg="white")
    username_entry.pack()

    tk.Label(login_win, text="Password", bg="#1e1e1e", fg="white").pack(pady=5)
    password_entry = tk.Entry(login_win, show="*", bg="#2e2e2e", fg="white")
    password_entry.pack()

    def attempt_login():
        global current_user
        username = username_entry.get()
        password = password_entry.get()
        for user in users:
            if user["username"] == username and user["password"] == password:
                current_user = user
                login_win.destroy()
                root.deiconify()
                return
        messagebox.showerror("Login Failed", "Invalid username or password.")

    tk.Button(login_win, text="Login", command=attempt_login, bg="#3CB371", fg="white").pack(pady=15)

# Initialize root window
root = tk.Tk()
root.title("NexusByte Ticketing System")
root.geometry("900x600")
root.configure(bg="#1e1e1e")
root.withdraw()

# Style
style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview", background="#2e2e2e", foreground="white", rowheight=25, fieldbackground="#2e2e2e")
style.map("Treeview", background=[("selected", "#444")])

# Layout
top_frame = tk.Frame(root, bg="#1e1e1e")
top_frame.pack(pady=10)
tk.Button(top_frame, text="Logout", command=logout, bg="#444", fg="white").pack(side="right", padx=10)

tk.Label(root, text="Ticket Title", bg="#1e1e1e", fg="white", font=("Arial", 12)).pack()
title_entry = tk.Entry(root, width=60, bg="#2e2e2e", fg="white")
title_entry.pack(pady=5)

tk.Label(root, text="Description", bg="#1e1e1e", fg="white", font=("Arial", 12)).pack()
desc_entry = tk.Text(root, height=4, width=60, bg="#2e2e2e", fg="white")
desc_entry.pack(pady=5)

btn_frame = tk.Frame(root, bg="#1e1e1e")
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Add Ticket", command=add_ticket, bg="#3CB371", fg="white", width=15).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="Mark Closed", command=mark_ticket_closed, bg="#444", fg="white", width=15).grid(row=0, column=1, padx=5)
tk.Button(btn_frame, text="Delete Ticket", command=delete_ticket, bg="#bb2124", fg="white", width=15).grid(row=0, column=2, padx=5)
tk.Button(btn_frame, text="Export CSV", command=export_tickets_to_csv, bg="#3CB371", fg="white", width=15).grid(row=0, column=3, padx=5)
tk.Button(btn_frame, text="Admin Panel", command=open_admin_panel, bg="#007acc", fg="white", width=15).grid(row=0, column=4, padx=5)

ticket_list = ttk.Treeview(root, columns=("ID", "Title", "Status", "Created"), show="headings")
ticket_list.heading("ID", text="ID")
ticket_list.heading("Title", text="Title")
ticket_list.heading("Status", text="Status")
ticket_list.heading("Created", text="Created")
ticket_list.pack(padx=10, pady=10, fill="both", expand=True)

# Load and show
load_tickets()
update_ticket_list()
login_screen()
root.mainloop()
