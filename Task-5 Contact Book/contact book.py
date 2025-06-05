import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import json
import os
import csv

CONTACT_FILE = "contacts.json"

class ContactBook:
    def __init__(self, root):
        self.root = root
        self.root.title("📒 Advanced Contact Book")
        self.root.geometry("800x550")
        self.root.config(bg="lightyellow")

        self.contacts = []
        self.load_contacts()

        self.create_widgets()

    def create_widgets(self):
        title = tk.Label(self.root, text="Advanced Contact Book", font=("Times New Roman", 22, "bold"), bg="lightyellow", fg="black")
        title.pack(pady=10)

        input_frame = tk.Frame(self.root, bg="lightyellow")
        input_frame.pack(pady=5)

        # Input fields
        labels = ["Name", "Phone", "Email", "Address"]
        self.entries = {}

        for i, label in enumerate(labels):
            tk.Label(input_frame, text=f"{label}:", font=("Times New Roman", 12, "bold"), bg="lightyellow").grid(row=i, column=0, sticky='w')
            entry = tk.Entry(input_frame, width=40)
            entry.grid(row=i, column=1, padx=10, pady=2)
            self.entries[label.lower()] = entry

        # Buttons
        btn_frame = tk.Frame(self.root, bg="lightyellow")
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Add Contact", bg="#2ecc71", fg="white", font=("Times New Roman", 12, "bold"), command=self.add_contact).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Update", bg="#f39c12", fg="white", font=("Times New Roman", 12, "bold"), command=self.update_contact).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Delete", bg="#e74c3c", fg="white", font=("Times New Roman", 12, "bold"), command=self.delete_contact).grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="Clear", bg="#34495e", fg="white", font=("Times New Roman", 12, "bold"), command=self.clear_fields).grid(row=0, column=3, padx=5)
        tk.Button(btn_frame, text="Export CSV", bg="#9b59b6", fg="white", font=("Times New Roman", 12, "bold"), command=self.export_to_csv).grid(row=0, column=4, padx=5)

        # Search bar
        search_frame = tk.Frame(self.root, bg="lightyellow")
        search_frame.pack(pady=5)

        tk.Label(search_frame, text="Search:", font=("Times New Roman", 12, "bold"), bg="lightyellow").grid(row=0, column=0)
        self.search_entry = tk.Entry(search_frame, width=40)
        self.search_entry.grid(row=0, column=1, padx=10)
        tk.Button(search_frame, text="Search", bg="black", fg="white", font=("Times New Roman", 11, "bold"), command=self.search_contact).grid(row=0, column=2)

        # Sort Buttons
        tk.Button(search_frame, text="Sort by Name", bg="#1abc9c", fg="white", font=("Times New Roman", 11, "bold"), command=self.sort_by_name).grid(row=0, column=3, padx=5)
        tk.Button(search_frame, text="Sort by Phone", bg="#3498db", fg="white", font=("Times New Roman", 11, "bold"), command=self.sort_by_phone).grid(row=0, column=4)

        # Treeview
        self.tree = ttk.Treeview(self.root, columns=("Name", "Phone", "Email", "Address"), show="headings", height=10)
        for col in ("Name", "Phone", "Email", "Address"):
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor='center', width=150)
        self.tree.pack(pady=10, fill=tk.BOTH, expand=True)
        self.tree.bind("<ButtonRelease-1>", self.select_contact)

        # Status
        self.status = tk.Label(self.root, text="Ready", font=("Times New Roman", 11), anchor='w', bg="lightyellow", fg="green")
        self.status.pack(fill=tk.X)

        self.refresh_contacts()

    def load_contacts(self):
        if os.path.exists(CONTACT_FILE):
            with open(CONTACT_FILE, 'r') as f:
                self.contacts = json.load(f)

    def save_contacts(self):
        with open(CONTACT_FILE, 'w') as f:
            json.dump(self.contacts, f, indent=4)

    def refresh_contacts(self):
        self.tree.delete(*self.tree.get_children())
        for contact in self.contacts:
            self.tree.insert("", "end", values=(contact['name'], contact['phone'], contact['email'], contact['address']))
        self.status.config(text=f"Loaded {len(self.contacts)} contacts")
        self.search_entry.delete(0, tk.END)

    def add_contact(self):
        contact = {k: v.get().strip() for k, v in self.entries.items()}
        if not contact['name'] or not contact['phone']:
            messagebox.showwarning("Missing Info", "Name and Phone are required!")
            return
        if any(c['phone'] == contact['phone'] for c in self.contacts):
            messagebox.showwarning("Duplicate", "Contact with this phone number already exists.")
            return

        self.contacts.append(contact)
        self.save_contacts()
        self.refresh_contacts()
        self.clear_fields()
        self.status.config(text="Contact added")

    def update_contact(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Select Contact", "Select a contact to update.")
            return
        index = self.tree.index(selected[0])
        updated = {k: v.get().strip() for k, v in self.entries.items()}
        self.contacts[index] = updated
        self.save_contacts()
        self.refresh_contacts()
        self.clear_fields()
        self.status.config(text="Contact updated")

    def delete_contact(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Select Contact", "Select a contact to delete.")
            return
        index = self.tree.index(selected[0])
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this contact?")
        if confirm:
            del self.contacts[index]
            self.save_contacts()
            self.refresh_contacts()
            self.clear_fields()
            self.status.config(text="Contact deleted")

    def clear_fields(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)
        self.search_entry.delete(0, tk.END)
        self.status.config(text="Cleared input fields")

    def search_contact(self):
        query = self.search_entry.get().strip().lower()
        if not query:
            self.refresh_contacts()
            return
        results = [c for c in self.contacts if query in c['name'].lower() or query in c['phone']]
        self.tree.delete(*self.tree.get_children())
        for contact in results:
            self.tree.insert("", "end", values=(contact['name'], contact['phone'], contact['email'], contact['address']))
        self.status.config(text=f"Found {len(results)} match(es)")

    def select_contact(self, event):
        selected = self.tree.selection()
        if selected:
            values = self.tree.item(selected[0], 'values')
            keys = ['name', 'phone', 'email', 'address']
            for i, k in enumerate(keys):
                self.entries[k].delete(0, tk.END)
                self.entries[k].insert(0, values[i])

    def export_to_csv(self):
        file = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file:
            with open(file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["Name", "Phone", "Email", "Address"])
                for c in self.contacts:
                    writer.writerow([c['name'], c['phone'], c['email'], c['address']])
            self.status.config(text="Contacts exported to CSV")

    def sort_by_name(self):
        self.contacts.sort(key=lambda x: x['name'].lower())
        self.refresh_contacts()
        self.status.config(text="Sorted by Name")

    def sort_by_phone(self):
        self.contacts.sort(key=lambda x: x['phone'])
        self.refresh_contacts()
        self.status.config(text="Sorted by Phone")


# Launch App
root = tk.Tk()
app = ContactBook(root)
root.mainloop()
