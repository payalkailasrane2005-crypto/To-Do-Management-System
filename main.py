import tkinter as tk
from tkinter import messagebox
import mysql.connector


# ---------------- DATABASE CONNECTION ----------------

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="todo_user",
        password="todo123",
        database="todo_management"
    )


# ---------------- ADD TASK ----------------

def add_task():
    window = tk.Toplevel(root)
    window.title("Add Task")
    window.geometry("450x500")
    window.configure(bg="#F5F7FA")

    tk.Label(
        window,
        text="ADD TASK",
        font=("Arial", 22, "bold"),
        bg="#F5F7FA",
        fg="#2C3E50"
    ).pack(pady=20)

    tk.Label(window, text="Task Name", bg="#F5F7FA").pack()
    task_name = tk.Entry(window, width=35)
    task_name.pack(pady=5)

    tk.Label(window, text="Description", bg="#F5F7FA").pack()
    description = tk.Entry(window, width=35)
    description.pack(pady=5)

    tk.Label(window, text="Due Date", bg="#F5F7FA").pack()
    due_date = tk.Entry(window, width=35)
    due_date.pack(pady=5)

    tk.Label(window, text="Status", bg="#F5F7FA").pack()
    status = tk.Entry(window, width=35)
    status.insert(0, "Pending")
    status.pack(pady=5)

    def save_task():

        name = task_name.get()
        desc = description.get()
        date = due_date.get()
        stat = status.get()

        if name == "":
            messagebox.showerror("Error", "Please enter task name")
            return

        try:
            db = connect_db()
            cursor = db.cursor()

            query = """
            INSERT INTO tasks
            (task_name, description, due_date, status)
            VALUES (%s, %s, %s, %s)
            """

            values = (name, desc, date, stat)

            cursor.execute(query, values)
            db.commit()

            cursor.close()
            db.close()

            messagebox.showinfo(
                "Success",
                "Task Added Successfully"
            )

            task_name.delete(0, tk.END)
            description.delete(0, tk.END)
            due_date.delete(0, tk.END)
            status.delete(0, tk.END)
            status.insert(0, "Pending")

        except Exception as e:
            messagebox.showerror(
                "Database Error",
                str(e)
            )

    tk.Button(
        window,
        text="ADD TASK",
        width=20,
        bg="#27AE60",
        fg="white",
        font=("Arial", 11, "bold"),
        command=save_task
    ).pack(pady=20)

    tk.Button(
        window,
        text="CLEAR",
        width=20,
        bg="#95A5A6",
        fg="white",
        command=lambda: [
            task_name.delete(0, tk.END),
            description.delete(0, tk.END),
            due_date.delete(0, tk.END)
        ]
    ).pack(pady=5)


# ---------------- VIEW TASKS ----------------

def view_tasks():

    window = tk.Toplevel(root)
    window.title("View Tasks")
    window.geometry("750x500")
    window.configure(bg="#F5F7FA")

    tk.Label(
        window,
        text="ALL TASKS",
        font=("Arial", 22, "bold"),
        bg="#F5F7FA",
        fg="#2C3E50"
    ).pack(pady=20)

    try:
        db = connect_db()
        cursor = db.cursor()

        cursor.execute(
            "SELECT id, task_name, description, due_date, status FROM tasks"
        )

        tasks = cursor.fetchall()

        if len(tasks) == 0:

            tk.Label(
                window,
                text="No tasks available",
                font=("Arial", 13),
                bg="#F5F7FA"
            ).pack(pady=30)

        else:

            for task in tasks:

                text = (
                    f"ID: {task[0]}    "
                    f"Task: {task[1]}    "
                    f"Description: {task[2]}    "
                    f"Due Date: {task[3]}    "
                    f"Status: {task[4]}"
                )

                tk.Label(
                    window,
                    text=text,
                    anchor="w",
                    bg="white",
                    relief="solid",
                    padx=10,
                    pady=8
                ).pack(fill="x", padx=15, pady=5)

        cursor.close()
        db.close()

    except Exception as e:

        messagebox.showerror(
            "Database Error",
            str(e)
        )


# ---------------- SEARCH TASK ----------------

def search_task():

    window = tk.Toplevel(root)
    window.title("Search Task")
    window.geometry("550x450")
    window.configure(bg="#F5F7FA")

    tk.Label(
        window,
        text="SEARCH TASK",
        font=("Arial", 22, "bold"),
        bg="#F5F7FA",
        fg="#2C3E50"
    ).pack(pady=20)

    tk.Label(
        window,
        text="Enter Task Name",
        bg="#F5F7FA"
    ).pack()

    search_entry = tk.Entry(window, width=35)
    search_entry.pack(pady=10)

    result = tk.Label(
        window,
        text="",
        font=("Arial", 12),
        bg="#F5F7FA",
        justify="left"
    )
    result.pack(pady=20)

    def search():

        name = search_entry.get()

        if name == "":
            messagebox.showerror(
                "Error",
                "Please enter task name"
            )
            return

        try:
            db = connect_db()
            cursor = db.cursor()

            cursor.execute(
                """
                SELECT id, task_name, description, due_date, status
                FROM tasks
                WHERE task_name = %s
                """,
                (name,)
            )

            task = cursor.fetchone()

            if task:

                result.config(
                    text=
                    f"ID: {task[0]}\n\n"
                    f"Task Name: {task[1]}\n\n"
                    f"Description: {task[2]}\n\n"
                    f"Due Date: {task[3]}\n\n"
                    f"Status: {task[4]}"
                )

            else:

                result.config(
                    text="Task Not Found",
                    fg="red"
                )

            cursor.close()
            db.close()

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                str(e)
            )

    tk.Button(
        window,
        text="SEARCH",
        width=18,
        bg="#3498DB",
        fg="white",
        font=("Arial", 11, "bold"),
        command=search
    ).pack(pady=10)


# ---------------- UPDATE TASK ----------------

def update_task():

    window = tk.Toplevel(root)
    window.title("Update Task")
    window.geometry("500x550")
    window.configure(bg="#F5F7FA")

    tk.Label(
        window,
        text="UPDATE TASK",
        font=("Arial", 22, "bold"),
        bg="#F5F7FA",
        fg="#2C3E50"
    ).pack(pady=20)

    tk.Label(
        window,
        text="Task ID",
        bg="#F5F7FA"
    ).pack()

    id_entry = tk.Entry(window, width=30)
    id_entry.pack(pady=5)

    tk.Label(
        window,
        text="New Task Name",
        bg="#F5F7FA"
    ).pack()

    name_entry = tk.Entry(window, width=30)
    name_entry.pack(pady=5)

    tk.Label(
        window,
        text="New Description",
        bg="#F5F7FA"
    ).pack()

    desc_entry = tk.Entry(window, width=30)
    desc_entry.pack(pady=5)

    tk.Label(
        window,
        text="New Due Date",
        bg="#F5F7FA"
    ).pack()

    date_entry = tk.Entry(window, width=30)
    date_entry.pack(pady=5)

    tk.Label(
        window,
        text="New Status",
        bg="#F5F7FA"
    ).pack()

    status_entry = tk.Entry(window, width=30)
    status_entry.pack(pady=5)

    def update():

        task_id = id_entry.get()
        name = name_entry.get()
        desc = desc_entry.get()
        date = date_entry.get()
        status = status_entry.get()

        if task_id == "":
            messagebox.showerror(
                "Error",
                "Please enter Task ID"
            )
            return

        try:

            db = connect_db()
            cursor = db.cursor()

            query = """
            UPDATE tasks
            SET task_name=%s,
                description=%s,
                due_date=%s,
                status=%s
            WHERE id=%s
            """

            values = (
                name,
                desc,
                date,
                status,
                task_id
            )

            cursor.execute(query, values)
            db.commit()

            if cursor.rowcount == 0:

                messagebox.showwarning(
                    "Warning",
                    "Task ID not found"
                )

            else:

                messagebox.showinfo(
                    "Success",
                    "Task Updated Successfully"
                )

            cursor.close()
            db.close()

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                str(e)
            )

    tk.Button(
        window,
        text="UPDATE TASK",
        width=20,
        bg="#F39C12",
        fg="white",
        font=("Arial", 11, "bold"),
        command=update
    ).pack(pady=20)


# ---------------- DELETE TASK ----------------

def delete_task():

    window = tk.Toplevel(root)
    window.title("Delete Task")
    window.geometry("450x300")
    window.configure(bg="#F5F7FA")

    tk.Label(
        window,
        text="DELETE TASK",
        font=("Arial", 22, "bold"),
        bg="#F5F7FA",
        fg="#2C3E50"
    ).pack(pady=25)

    tk.Label(
        window,
        text="Enter Task ID",
        bg="#F5F7FA"
    ).pack()

    id_entry = tk.Entry(window, width=30)
    id_entry.pack(pady=10)

    def delete():

        task_id = id_entry.get()

        if task_id == "":
            messagebox.showerror(
                "Error",
                "Please enter Task ID"
            )
            return

        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this task?"
        )

        if not confirm:
            return

        try:

            db = connect_db()
            cursor = db.cursor()

            cursor.execute(
                "DELETE FROM tasks WHERE id=%s",
                (task_id,)
            )

            db.commit()

            if cursor.rowcount == 0:

                messagebox.showwarning(
                    "Warning",
                    "Task ID not found"
                )

            else:

                messagebox.showinfo(
                    "Success",
                    "Task Deleted Successfully"
                )

                id_entry.delete(0, tk.END)

            cursor.close()
            db.close()

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                str(e)
            )

    tk.Button(
        window,
        text="DELETE TASK",
        width=20,
        bg="#E74C3C",
        fg="white",
        font=("Arial", 11, "bold"),
        command=delete
    ).pack(pady=20)


# ---------------- LOGOUT ----------------

def logout():

    dashboard_window.destroy()
    root.deiconify()


# ---------------- DASHBOARD ----------------

def dashboard():

    global dashboard_window

    dashboard_window = tk.Toplevel(root)
    dashboard_window.title("Dashboard")
    dashboard_window.geometry("550x650")
    dashboard_window.configure(bg="#ECF0F1")

    tk.Label(
        dashboard_window,
        text="TO-DO MANAGEMENT SYSTEM",
        font=("Arial", 24, "bold"),
        bg="#ECF0F1",
        fg="#2C3E50"
    ).pack(pady=30)

    tk.Label(
        dashboard_window,
        text="Dashboard",
        font=("Arial", 16),
        bg="#ECF0F1",
        fg="#34495E"
    ).pack(pady=5)

    tk.Button(
        dashboard_window,
        text="ADD TASK",
        width=25,
        height=2,
        bg="#27AE60",
        fg="white",
        font=("Arial", 11, "bold"),
        command=add_task
    ).pack(pady=8)

    tk.Button(
        dashboard_window,
        text="VIEW TASKS",
        width=25,
        height=2,
        bg="#2980B9",
        fg="white",
        font=("Arial", 11, "bold"),
        command=view_tasks
    ).pack(pady=8)

    tk.Button(
        dashboard_window,
        text="SEARCH TASK",
        width=25,
        height=2,
        bg="#8E44AD",
        fg="white",
        font=("Arial", 11, "bold"),
        command=search_task
    ).pack(pady=8)

    tk.Button(
        dashboard_window,
        text="UPDATE TASK",
        width=25,
        height=2,
        bg="#F39C12",
        fg="white",
        font=("Arial", 11, "bold"),
        command=update_task
    ).pack(pady=8)

    tk.Button(
        dashboard_window,
        text="DELETE TASK",
        width=25,
        height=2,
        bg="#E74C3C",
        fg="white",
        font=("Arial", 11, "bold"),
        command=delete_task
    ).pack(pady=8)

    tk.Button(
        dashboard_window,
        text="LOGOUT",
        width=25,
        height=2,
        bg="#34495E",
        fg="white",
        font=("Arial", 11, "bold"),
        command=logout
    ).pack(pady=20)


# ---------------- LOGIN ----------------

def login():

    if username.get() == "admin" and password.get() == "admin123":

        root.withdraw()
        dashboard()

    else:

        messagebox.showerror(
            "Login Error",
            "Invalid Username or Password"
        )


# ---------------- MAIN LOGIN WINDOW ----------------

root = tk.Tk()

root.title("To-Do Management System - Login")
root.geometry("450x450")
root.configure(bg="#ECF0F1")

tk.Label(
    root,
    text="TO-DO MANAGEMENT SYSTEM",
    font=("Arial", 20, "bold"),
    bg="#ECF0F1",
    fg="#2C3E50"
).pack(pady=40)

tk.Label(
    root,
    text="Username",
    font=("Arial", 12),
    bg="#ECF0F1"
).pack()

username = tk.Entry(
    root,
    width=30
)
username.pack(pady=8)

tk.Label(
    root,
    text="Password",
    font=("Arial", 12),
    bg="#ECF0F1"
).pack()

password = tk.Entry(
    root,
    width=30,
    show="*"
)
password.pack(pady=8)

tk.Button(
    root,
    text="LOGIN",
    width=20,
    height=2,
    bg="#3498DB",
    fg="white",
    font=("Arial", 11, "bold"),
    command=login
).pack(pady=25)

tk.Label(
    root,
    text="Username: admin    Password: admin123",
    font=("Arial", 9),
    bg="#ECF0F1",
    fg="#7F8C8D"
).pack()

root.mainloop()