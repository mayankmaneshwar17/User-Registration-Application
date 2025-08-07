# Registration Form Using Python
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import os

# Database file name 
DB_FILE = "user_data.db"

def clear_screen():
    """Clears the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def connect_db():
    """Connects to the SQLite database."""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
        table_exists = cursor.fetchone()
        if not table_exists:
            cursor.execute("""
                CREATE TABLE users (
                    user_id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL,
                    phone TEXT NOT NULL,
                    dob TEXT NOT NULL
                )
            """)
            conn.commit()
            print("Created new table 'users'")
        return conn
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Error connecting to database: {e}")
        return None
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")
        return None

# Closes the database connection.
def close_db(conn):
    
    if conn:
        conn.close()

class UserRegistrationApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.form_frame = None
        self.title("User Registration Application")
        self.geometry("600x400")  
        self.resizable(False, False) 

        self.conn = connect_db()
        if self.conn is None:
            # If database connection fails.
            messagebox.showerror("Error", "Failed to connect to the database. Exiting.")
            self.destroy()
            return

        self.create_widgets()
        # the database connection is closed when the window is destroyed.
        self.protocol("WM_DELETE_WINDOW", self.on_close)

   # Creates the GUI widgets
    def create_widgets(self):
        
        # Use a PanedWindow for better layout management
        self.paned_window = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        self.paned_window.pack(fill=tk.BOTH, expand=True)

        # Left frame for buttons
        self.left_frame = ttk.Frame(self.paned_window)
        self.paned_window.add(self.left_frame)

        # Right frame for forms/details
        self.right_frame = ttk.Frame(self.paned_window)
        self.paned_window.add(self.right_frame, weight=1)  

        # Buttons in the left frame
        self.register_button = ttk.Button(self.left_frame, text="Register User", command=self.show_register_form)
        self.register_button.pack(pady=10, padx=10, fill=tk.X)

        self.view_button = ttk.Button(self.left_frame, text="View User Details", command=self.show_view_form)
        self.view_button.pack(pady=10, padx=10, fill=tk.X)

        self.update_button = ttk.Button(self.left_frame, text="Update User Details", command=self.show_update_form)
        self.update_button.pack(pady=10, padx=10, fill=tk.X)

        self.delete_button = ttk.Button(self.left_frame, text="Delete User", command=self.show_delete_form)
        self.delete_button.pack(pady=10, padx=10, fill=tk.X)

        self.list_button = ttk.Button(self.left_frame, text="List All Users", command=self.show_list_users)
        self.list_button.pack(pady=10, padx=10, fill=tk.X)

        self.exit_button = ttk.Button(self.left_frame, text="Exit", command=self.on_close)
        self.exit_button.pack(pady=10, padx=10, fill=tk.X)

        # Placeholder frame for forms in the right frame
        self.form_frame = ttk.Frame(self.right_frame)
        self.form_frame.pack(fill=tk.BOTH, expand=True)

       # Show register form by default
        self.show_register_form()

      # clear the form frame
    def clear_form(self):
        
        for widget in self.form_frame.winfo_children():
            widget.destroy()

    # Displays the user registration form
    def show_register_form(self):
        
        self.clear_form()
        self.form_frame.configure(padding=(20, 20))  # Add padding for visual appeal

        title_label = ttk.Label(self.form_frame, text="Register New User", font=("Arial", 16))
        title_label.pack(pady=10)

        user_id_label = ttk.Label(self.form_frame, text="User ID:")
        user_id_label.pack(anchor=tk.W)
        self.user_id_entry = ttk.Entry(self.form_frame)
        self.user_id_entry.pack(fill=tk.X, pady=5)

        name_label = ttk.Label(self.form_frame, text="Name:")
        name_label.pack(anchor=tk.W)
        self.name_entry = ttk.Entry(self.form_frame)
        self.name_entry.pack(fill=tk.X, pady=5)

        email_label = ttk.Label(self.form_frame, text="Email:")
        email_label.pack(anchor=tk.W)
        self.email_entry = ttk.Entry(self.form_frame)
        self.email_entry.pack(fill=tk.X, pady=5)

        phone_label = ttk.Label(self.form_frame, text="Phone Number:")
        phone_label.pack(anchor=tk.W)
        self.phone_entry = ttk.Entry(self.form_frame)
        self.phone_entry.pack(fill=tk.X, pady=5)

        dob_label = ttk.Label(self.form_frame, text="Date of Birth (YYYY-MM-DD):")
        dob_label.pack(anchor=tk.W)
        self.dob_entry = ttk.Entry(self.form_frame)
        self.dob_entry.pack(fill=tk.X, pady=5)

        register_button = ttk.Button(self.form_frame, text="Register", command=self.register_user)
        register_button.pack(pady=20)
     
     #Displays the form to view user details.
    def show_view_form(self):
        
        self.clear_form()
        self.form_frame.configure(padding=(20, 20))

        title_label = ttk.Label(self.form_frame, text="View User Details", font=("Arial", 16))
        title_label.pack(pady=10)

        user_id_label = ttk.Label(self.form_frame, text="Enter User ID:")
        user_id_label.pack(anchor=tk.W)
        self.user_id_entry = ttk.Entry(self.form_frame)
        self.user_id_entry.pack(fill=tk.X, pady=5)

        self.view_details_label = ttk.Label(self.form_frame, text="", font=("Arial", 12))  
        self.view_details_label.pack(pady=10)

        view_button = ttk.Button(self.form_frame, text="View Details", command=self.view_user_details)
        view_button.pack(pady=20)

     # Displays the form to update user details
    def show_update_form(self):
        
        self.clear_form()
        self.form_frame.configure(padding=(20, 20))

        title_label = ttk.Label(self.form_frame, text="Update User Details", font=("Arial", 16))
        title_label.pack(pady=10)

        user_id_label = ttk.Label(self.form_frame, text="Enter User ID:")
        user_id_label.pack(anchor=tk.W)
        self.user_id_entry = ttk.Entry(self.form_frame)
        self.user_id_entry.pack(fill=tk.X, pady=5)

        self.name_label = ttk.Label(self.form_frame, text="Name:")
        self.name_label.pack(anchor=tk.W)
        self.name_entry = ttk.Entry(self.form_frame)
        self.name_entry.pack(fill=tk.X, pady=5)

        self.email_label = ttk.Label(self.form_frame, text="Email:")
        self.email_label.pack(anchor=tk.W)
        self.email_entry = ttk.Entry(self.form_frame)
        self.email_entry.pack(fill=tk.X, pady=5)

        self.phone_label = ttk.Label(self.form_frame, text="Phone Number:")
        self.phone_label.pack(anchor=tk.W)
        self.phone_entry = ttk.Entry(self.form_frame)
        self.phone_entry.pack(fill=tk.X, pady=5)

        self.dob_label = ttk.Label(self.form_frame, text="Date of Birth (YYYY-MM-DD):")
        self.dob_label.pack(anchor=tk.W)
        self.dob_entry = ttk.Entry(self.form_frame)
        self.dob_entry.pack(fill=tk.X, pady=5)

        update_button = ttk.Button(self.form_frame, text="Update Details", command=self.update_user_details)
        update_button.pack(pady=20)

     # Displays the form to delete a user
    def show_delete_form(self):
        
        self.clear_form()
        self.form_frame.configure(padding=(20, 20))

        title_label = ttk.Label(self.form_frame, text="Delete User", font=("Arial", 16))
        title_label.pack(pady=10)

        user_id_label = ttk.Label(self.form_frame, text="Enter User ID:")
        user_id_label.pack(anchor=tk.W)
        self.user_id_entry = ttk.Entry(self.form_frame)
        self.user_id_entry.pack(fill=tk.X, pady=5)

        delete_button = ttk.Button(self.form_frame, text="Delete User", command=self.delete_user)
        delete_button.pack(pady=20)
        self.delete_message_label = ttk.Label(self.form_frame, text="",  foreground="red")
        self.delete_message_label.pack(pady=10)

      # Displays the list of all users
    def show_list_users(self):
        
        self.clear_form()
        self.form_frame.configure(padding=(20, 20))

        title_label = ttk.Label(self.form_frame, text="List of All Users", font=("Arial", 16))
        title_label.pack(pady=10)

        self.listbox = tk.Listbox(self.form_frame, width=50, height=15)
        self.listbox.pack(pady=10, fill=tk.BOTH, expand=True)

        conn = self.conn
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        users_data = cursor.fetchall()

        if not users_data:
            self.listbox.insert(tk.END, "No users registered yet.")
        else:
            for user in users_data:
                self.listbox.insert(tk.END, f"User ID: {user[0]}, Name: {user[1]}, Email: {user[2]}")
    
    # Registers a new user   
    def register_user(self):
        
        user_id = self.user_id_entry.get()
        name = self.name_entry.get()
        email = self.email_entry.get()
        phone = self.phone_entry.get()
        dob = self.dob_entry.get()

        if not user_id or not name or not email or not phone or not dob:
            messagebox.showerror("Error", "All fields are required.")
            return

        try:
            user_id = int(user_id)
        except ValueError:
            messagebox.showerror("Error", "Invalid User ID.  Must be an integer.")
            return

        conn = self.conn
        cursor = conn.cursor()

        # Check if user_id already exists
        cursor.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,))
        if cursor.fetchone():
            messagebox.showerror("Error", "User ID already exists. Please choose a unique ID.")
            return

        try:
            cursor.execute("""
                INSERT INTO users (user_id, name, email, phone, dob)
                VALUES (?, ?, ?, ?, ?)
            """, (user_id, name, email, phone, dob))
            conn.commit()
            messagebox.showinfo("Success", "User registered successfully!")
            self.show_list_users()  #refresh user list
            self.show_register_form() #stay on register form
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error registering user: {e}")
            conn.rollback()

    # View details of a specific user
    def view_user_details(self):
        
        user_id = self.user_id_entry.get()
        if not user_id:
            messagebox.showerror("Error", "Please enter a User ID.")
            return

        try:
            user_id = int(user_id)
        except ValueError:
            messagebox.showerror("Error", "Invalid User ID.  Must be an integer.")
            return
        conn = self.conn
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        user_data = cursor.fetchone()

        if user_data:
            details_text = f"User ID: {user_data[0]}\nName: {user_data[1]}\nEmail: {user_data[2]}\nPhone Number: {user_data[3]}\nDate of Birth: {user_data[4]}"
            self.view_details_label.config(text=details_text)
        else:
            self.view_details_label.config(text="User not found.")

    #Updates details of an existing user
    def update_user_details(self):
        
        user_id = self.user_id_entry.get()
        if not user_id:
            messagebox.showerror("Error", "Please enter a User ID.")
            return
        try:
            user_id = int(user_id)
        except ValueError:
            messagebox.showerror("Error", "Invalid User ID. Must be an integer.")
            return

        conn = self.conn
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        user_data = cursor.fetchone()

        if user_data:
            name = self.name_entry.get()
            email = self.email_entry.get()
            phone = self.phone_entry.get()
            dob = self.dob_entry.get()

            updates = []
            values = []
            if name:
                updates.append("name = ?")
                values.append(name)
            if email:
                updates.append("email = ?")
                values.append(email)
            if phone:
                updates.append("phone = ?")
                values.append(phone)
            if dob:
                updates.append("dob = ?")
                values.append(dob)

            if updates:
                query = "UPDATE users SET " + ", ".join(updates) + " WHERE user_id = ?"
                values.append(user_id)
                try:
                    cursor.execute(query, values)
                    conn.commit()
                    messagebox.showinfo("Success", "User details updated successfully!")
                    self.show_list_users()
                    self.show_update_form()
                except sqlite3.Error as e:
                    messagebox.showerror("Error", f"Error updating user details: {e}")
                    conn.rollback()
            else:
                messagebox.showinfo("Info", "No updates were made.")
        else:
            messagebox.showerror("Error", "User not found.")
  
    # Deletes a user 
    def delete_user(self):
        
        user_id = self.user_id_entry.get()
        if not user_id:
            messagebox.showerror("Error", "Please enter a User ID.")
            return

        try:
            user_id = int(user_id)
        except ValueError:
             messagebox.showerror("Error", "Invalid User ID. Must be an integer.")
             return

        conn = self.conn
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,))
        if cursor.fetchone():
            try:
                cursor.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
                conn.commit()
                messagebox.showinfo("Success", "User deleted successfully!")
                self.show_list_users()
                self.show_delete_form()
            except sqlite3.Error as e:
                messagebox.showerror("Error", f"Error deleting user: {e}")
                conn.rollback()
            finally:
                pass
        else:
            messagebox.showerror("Error", "User not found.")

     #Closes the database connection
    def on_close(self):
        
        if self.conn:
            close_db(self.conn)
            # main window is destroy
        self.destroy() 
if __name__ == "__main__":
    app = UserRegistrationApp()
    app.mainloop()

