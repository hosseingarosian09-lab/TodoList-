from tkinter import *
from tkinter import messagebox, font
from todolist import todolist, task

# Main window
window = Tk()
window.title("To-Do List")
window.geometry("800x600")
window.config(bg="#f0f0f0")  # Light gray background for main window

default_font = font.nametofont("TkDefaultFont")
default_font.configure(family="Arial", size=10)
title_font = ("Arial", 12, "bold")
overstrike_font = ("Arial", 10, "overstrike")

priority_colors = {
    5: "red",
    4: "orange",
    3: "gold",
    2: "green",
    1: "blue"
}

# Configure grid weights 
window.grid_columnconfigure(0, weight=1)  
window.grid_columnconfigure(1, weight=2)  
window.grid_rowconfigure(0, weight=1)    
window.grid_rowconfigure(1, weight=0, minsize=50)

# 3 main frames 
todolistbox = Listbox(window, bg="white", fg="black", selectbackground="#4CAF50", selectforeground="white", font=default_font)
todolistbox.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

# Tasks frame with scrollable canvas
tasks_frame = Frame(window, bg="#f0f0f0")
tasks_frame.grid(row=0, column=1, rowspan=2, sticky="nsew", padx=10, pady=10)
tasks_canvas = Canvas(tasks_frame, bg="white", highlightthickness=1, highlightbackground="#ddd")
tasks_canvas.pack(side=LEFT, fill=BOTH, expand=True)
scrollbar = Scrollbar(tasks_frame, orient=VERTICAL, command=tasks_canvas.yview)
scrollbar.pack(side=RIGHT, fill=Y)
tasks_canvas.configure(yscrollcommand=scrollbar.set)
tasks_inner_frame = Frame(tasks_canvas, bg="white")
tasks_canvas.create_window((0, 0), window=tasks_inner_frame, anchor="nw")
tasks_inner_frame.bind("<Configure>", lambda e: tasks_canvas.configure(scrollregion=tasks_canvas.bbox("all")))

button_frame = Frame(window, bg="#ddd")  # Lighter gray for button frame
button_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

# List of to-do lists 
todolist_list = []
task_checkboxes = []

# Function to update task display in tasks_frame
def update_task_display():
    # Clear existing widgets
    for widget in tasks_inner_frame.winfo_children():
        widget.destroy()
    task_checkboxes.clear()

    # Check if a to-do list is selected
    if not todolistbox.curselection():
        return
    
    # Select a to-do list
    selected_index = todolistbox.curselection()[0]
    selected_list = todolist_list[selected_index]

    # Sort tasks by priority (descending order)
    sorted_tasks = sorted(selected_list.my_list, key=lambda t: t.priority, reverse=True)

    # Display tasks
    for i, task in enumerate(sorted_tasks):
        
        task_frame = Frame(tasks_inner_frame, bg="white", bd=1, relief="groove", padx=10, pady=5)
        task_frame.grid(row=i, column=0, sticky="ew", padx=5, pady=5)
        tasks_inner_frame.grid_columnconfigure(0, weight=1)

        # Checkbox for completion status
        var = IntVar(value=1 if task.completed else 0)
        task_checkboxes.append(var)
        Checkbutton(task_frame, variable=var, command=lambda t=task, v=var: toggle_task_completion(t, v), bg="white").pack(side=LEFT, padx=5)

        # Task title with overstrike if completed
        title_label_font = overstrike_font if task.completed else title_font
        title_fg = "gray" if task.completed else "black"
        Label(task_frame, text=task.title, bg="white", fg=title_fg, font=title_label_font, anchor="w").pack(side=LEFT, fill=X, expand=True)

        # Priority indicator
        priority_fg = priority_colors.get(task.priority, "black")
        Label(task_frame, text=f"[Priority: {task.priority}]", bg="white", fg=priority_fg, font=default_font).pack(side=RIGHT, padx=5)

        # Description on new line
        desc_frame = Frame(task_frame, bg="white")
        desc_frame.pack(fill=X, pady=2)
        desc_fg = "gray" if task.completed else "black"
        Label(desc_frame, text=task.description, bg="white", fg=desc_fg, font=default_font, justify=LEFT, wraplength=400, anchor="w").pack(side=LEFT, fill=X, expand=True)

# Function to toggle task completion
def toggle_task_completion(task, var):
    task.toggle_complete()
    update_task_display()

# Function to handle listbox selection
def on_list_select(event):
    update_task_display()

# Bind selection event to todolistbox
todolistbox.bind("<<ListboxSelect>>", on_list_select)

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
    popup.config(bg="#f0f0f0")
    popup.transient(window)
    popup.grab_set()

    popup.grid_columnconfigure(0, weight=1)
    popup.grid_columnconfigure(1, weight=3)
    for i in range(5):
        popup.grid_rowconfigure(i, weight=1)

    Label(popup, text="Title:", bg="#f0f0f0", font=default_font).grid(row=0, column=0, padx=10, pady=10, sticky="e")
    title_entry = Entry(popup, font=default_font)
    title_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

    Label(popup, text="Description:", bg="#f0f0f0", font=default_font).grid(row=1, column=0, padx=10, pady=10, sticky="e")
    desc_entry = Text(popup, height=4, width=30, font=default_font)
    desc_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

    Label(popup, text="Priority (1-5):", bg="#f0f0f0", font=default_font).grid(row=2, column=0, padx=10, pady=10, sticky="e")
    priority_entry = Entry(popup, font=default_font)
    priority_entry.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

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
        update_task_display()
        popup.destroy()

    Button(popup, text="Add Task", command=submit_task, bg="#4CAF50", fg="white", font=default_font).grid(row=3, column=0, columnspan=2, pady=10, padx=10, sticky="ew")
    Button(popup, text="Cancel", command=popup.destroy, bg="#ddd", fg="black", font=default_font).grid(row=4, column=0, columnspan=2, pady=10, padx=10, sticky="ew")

# Function to create pop-up for adding a to-do list
def add_todolist_popup():
    popup = Toplevel(window)
    popup.title("Add To-Do List")
    popup.geometry("300x150")
    popup.config(bg="#f0f0f0")
    popup.transient(window)
    popup.grab_set()

    popup.grid_columnconfigure(0, weight=1)
    popup.grid_columnconfigure(1, weight=3)
    popup.grid_rowconfigure(0, weight=1)
    popup.grid_rowconfigure(1, weight=1)
    popup.grid_rowconfigure(2, weight=1)

    Label(popup, text="List Name:", bg="#f0f0f0", font=default_font).grid(row=0, column=0, padx=10, pady=10, sticky="e")
    name_entry = Entry(popup, font=default_font)
    name_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

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

    Button(popup, text="Add List", command=submit_todolist, bg="#4CAF50", fg="white", font=default_font).grid(row=1, column=0, columnspan=2, pady=5, padx=10, sticky="ew")
    Button(popup, text="Cancel", command=popup.destroy, bg="#ddd", fg="black", font=default_font).grid(row=2, column=0, columnspan=2, pady=5, padx=10, sticky="ew")

# Function to create pop-up for removing a task
def remove_task_popup():
    if not todolistbox.curselection():
        messagebox.showwarning("No List Selected", "Please select a to-do list from the listbox.")
        return
    
    selected_index = todolistbox.curselection()[0]
    selected_list = todolist_list[selected_index]

    if not selected_list.my_list:
        messagebox.showwarning("No Tasks", f"The to-do list '{selected_list.list_name}' is empty.")
        return

    popup = Toplevel(window)
    popup.title("Remove Task")
    popup.geometry("300x300")
    popup.config(bg="#f0f0f0")
    popup.transient(window)
    popup.grab_set()

    popup.grid_columnconfigure(0, weight=1)
    popup.grid_rowconfigure(0, weight=3)
    popup.grid_rowconfigure(1, weight=1)
    popup.grid_rowconfigure(2, weight=1)

    task_listbox = Listbox(popup, bg="white", fg="black", selectbackground="#4CAF50", selectforeground="white", font=default_font)
    task_listbox.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
    for task in selected_list.my_list:
        task_listbox.insert(END, task.title)

    def submit_remove_task():
        if not task_listbox.curselection():
            messagebox.showwarning("No Task Selected", "Please select a task to remove.")
            return
        selected_task_index = task_listbox.curselection()[0]
        task_title = task_listbox.get(selected_task_index)
        selected_list.remove_task(task_title)
        messagebox.showinfo("Success", f"Task '{task_title}' removed from '{selected_list.list_name}'.")
        update_task_display()
        popup.destroy()

    Button(popup, text="Remove Task", command=submit_remove_task, bg="#f44336", fg="white", font=default_font).grid(row=1, column=0, pady=5, padx=10, sticky="ew")
    Button(popup, text="Cancel", command=popup.destroy, bg="#ddd", fg="black", font=default_font).grid(row=2, column=0, pady=5, padx=10, sticky="ew")

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
    popup.config(bg="#f0f0f0")
    popup.transient(window)
    popup.grab_set()

    popup.grid_columnconfigure(0, weight=1)
    popup.grid_rowconfigure(0, weight=1)
    popup.grid_rowconfigure(1, weight=1)
    popup.grid_rowconfigure(2, weight=1)

    Label(popup, text=f"Are you sure you want to delete '{selected_list.list_name}'?", bg="#f0f0f0", font=default_font).grid(row=0, column=0, padx=10, pady=10)

    def submit_delete_list():
        todolist_list.pop(selected_index)
        todolistbox.delete(selected_index)
        update_task_display()
        messagebox.showinfo("Success", f"To-Do List '{selected_list.list_name}' deleted.")
        popup.destroy()

    Button(popup, text="Delete List", command=submit_delete_list, bg="#f44336", fg="white", font=default_font).grid(row=1, column=0, pady=5, padx=10, sticky="ew")
    Button(popup, text="Cancel", command=popup.destroy, bg="#ddd", fg="black", font=default_font).grid(row=2, column=0, pady=5, padx=10, sticky="ew")

# Buttons 
addtask_button = Button(button_frame, text="Add Task", command=add_task_popup, bg="#4CAF50", fg="white", font=default_font)
addtask_button.pack(fill="x", pady=2)

addlist_button = Button(button_frame, text="Add Todo-List", command=add_todolist_popup, bg="#4CAF50", fg="white", font=default_font)
addlist_button.pack(fill="x", pady=2)

removetask_button = Button(button_frame, text="Remove Task", command=remove_task_popup, bg="#f44336", fg="white", font=default_font)
removetask_button.pack(fill="x", pady=2)

delete_list_button = Button(button_frame, text="Delete List", command=delete_list_popup, bg="#f44336", fg="white", font=default_font)
delete_list_button.pack(fill="x", pady=2)

window.mainloop()