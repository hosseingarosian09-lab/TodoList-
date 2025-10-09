from tkinter import *
from tkinter import messagebox
from todolist import todolist, task

# Main window
window = Tk()
window.title("To-Do List")
window.geometry("800x600")

# Configure grid weights 
window.grid_columnconfigure(0, weight=1)  
window.grid_columnconfigure(1, weight=2)  
window.grid_rowconfigure(0, weight=1)    
window.grid_rowconfigure(1, weight=0, minsize=50)

# 3 main frames 
todolistbox = Listbox(window)
todolistbox.config(width=20, height=20, bg="gray", border=2, relief="groove")
todolistbox.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

# Tasks frame with scrollable canvas
tasks_frame = Frame(window)
tasks_frame.config(height=30, width=600)
tasks_frame.grid(row=0, column=1, rowspan=2, sticky="nsew", padx=5, pady=5)
tasks_canvas = Canvas(tasks_frame, bg="white")
tasks_canvas.pack(side=LEFT, fill=BOTH, expand=True)
scrollbar = Scrollbar(tasks_frame, orient=VERTICAL, command=tasks_canvas.yview)
scrollbar.pack(side=RIGHT, fill=Y)
tasks_canvas.configure(yscrollcommand=scrollbar.set)
tasks_inner_frame = Frame(tasks_canvas, bg="white")
tasks_canvas.create_window((0, 0), window=tasks_inner_frame, anchor="nw")
tasks_inner_frame.bind("<Configure>", lambda e: tasks_canvas.configure(scrollregion=tasks_canvas.bbox("all")))

button_frame = Frame(window)
button_frame.config(height=50, width=20, bg="black")
button_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

# List of to-do lists 
todolist_list = []
task_checkboxes = []  # Store checkbox variables for tasks

# Function to create pop-up for adding a task
def add_task_popup():
    if not todolistbox.curselection():
        messagebox.showwarning("No List Selected", "Please select a to-do list from the listbox.")
        return
    
    selected_index = todolistbox.curselection()[0]
    selected_list = todolist_list[selected_index]

    popup = Toplevel(window)
    popup.title("Add Task")
    popup.geometry("400x300")
    popup.transient(window)
    popup.grab_set()

    popup.grid_columnconfigure(0, weight=1)
    popup.grid_columnconfigure(1, weight=3)
    for i in range(5):
        popup.grid_rowconfigure(i, weight=1)

    Label(popup, text="Title:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    title_entry = Entry(popup)
    title_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

    Label(popup, text="Description:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    desc_entry = Text(popup, height=4, width=30)
    desc_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

    Label(popup, text="Priority (1-5):").grid(row=2, column=0, padx=5, pady=5, sticky="e")
    priority_entry = Entry(popup)
    priority_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

    def submit_task():
        title = title_entry.get().strip()
        description = desc_entry.get("1.0", END).strip()
        priority = priority_entry.get().strip()

        if not title or not description:
            messagebox.showerror("Input Error", "Title and Description cannot be empty.")
            return
        try:
            priority = int(priority)
            if not 1 <= priority <= 5:
                raise ValueError
        except ValueError:
            messagebox.showerror("Input Error", "Priority must be a number between 1 and 5.")
            return

        selected_list.add_task(title, description, priority)
        messagebox.showinfo("Success", f"Task '{title}' added to '{selected_list.list_name}'.")
        popup.destroy()

    Button(popup, text="Add Task", command=submit_task).grid(row=3, column=0, columnspan=2, pady=10)
    Button(popup, text="Cancel", command=popup.destroy).grid(row=4, column=0, columnspan=2, pady=5)

# Function to create pop-up for adding a to-do list
def add_todolist_popup():
    popup = Toplevel(window)
    popup.title("Add To-Do List")
    popup.geometry("300x150")
    popup.transient(window)
    popup.grab_set()

    popup.grid_columnconfigure(0, weight=1)
    popup.grid_columnconfigure(1, weight=3)
    popup.grid_rowconfigure(0, weight=1)
    popup.grid_rowconfigure(1, weight=1)
    popup.grid_rowconfigure(2, weight=1)

    Label(popup, text="List Name:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    name_entry = Entry(popup)
    name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

    def submit_todolist():
        name = name_entry.get().strip()
        if not name:
            messagebox.showerror("Input Error", "List name cannot be empty.")
            return
        if any(todo.list_name == name for todo in todolist_list):
            messagebox.showerror("Input Error", f"A list named '{name}' already exists.")
            return

        new_list = todolist(name)
        todolist_list.append(new_list)
        todolistbox.insert(END, name)
        messagebox.showinfo("Success", f"To-Do List '{name}' created.")
        popup.destroy()

    Button(popup, text="Add List", command=submit_todolist).grid(row=1, column=0, columnspan=2, pady=5)
    Button(popup, text="Cancel", command=popup.destroy).grid(row=2, column=0, columnspan=2, pady=5)


# Function to create pop-up for deleting a to-do list
def delete_list_popup():
    if not todolistbox.curselection():
        messagebox.showwarning("No List Selected", "Please select a to-do list to delete.")
        return
    
    selected_index = todolistbox.curselection()[0]
    selected_list = todolist_list[selected_index]

    popup = Toplevel(window)
    popup.title("Delete To-Do List")
    popup.geometry("300x150")
    popup.transient(window)
    popup.grab_set()

    popup.grid_columnconfigure(0, weight=1)
    popup.grid_rowconfigure(0, weight=1)
    popup.grid_rowconfigure(1, weight=1)
    popup.grid_rowconfigure(2, weight=1)

    Label(popup, text=f"Are you sure you want to delete '{selected_list.list_name}'?").grid(row=0, column=0, padx=5, pady=5)

    def submit_delete_list():
        todolist_list.pop(selected_index)
        todolistbox.delete(selected_index)
        messagebox.showinfo("Success", f"To-Do List '{selected_list.list_name}' deleted.")
        popup.destroy()

    Button(popup, text="Delete List", command=submit_delete_list).grid(row=1, column=0, pady=5)
    Button(popup, text="Cancel", command=popup.destroy).grid(row=2, column=0, pady=5)

# Buttons 
addtask_button = Button(button_frame, text="Add Task", command=add_task_popup)
addtask_button.pack(fill="x")

addlist_button = Button(button_frame, text="Add Todo-List", command=add_todolist_popup)
addlist_button.pack(fill="x")

removetask_button = Button(button_frame, text="Remove Task", )
removetask_button.pack(fill="x")

delete_list_button = Button(button_frame, text="Delete List", command=delete_list_popup)
delete_list_button.pack(fill="x")

window.mainloop()