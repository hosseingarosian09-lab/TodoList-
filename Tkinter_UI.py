from tkinter import *

#main fraim
window = Tk()
window.title("todo list")

todolistbox = Listbox(window)
todolistbox.config(width=20,height=30,bg="gray",border=2,relief="groove")
todolistbox.pack(side="left",fill="both")


tasks_frame = Frame(window)
tasks_frame.config(height=30,width=600,)
tasks_frame.pack(side="right",fill="both")


window.mainloop()