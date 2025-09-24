from tkinter import *

#main fraim
window = Tk()
window.title("todo list")
window.geometry("800x600")


# Configure grid weights 
window.grid_columnconfigure(0, weight=1)  
window.grid_columnconfigure(1, weight=2)  
window.grid_rowconfigure(0, weight=1)    
window.grid_rowconfigure(1, weight=0, minsize=50)

todolistbox = Listbox(window)
todolistbox.config(width=20,height=20,bg="gray",border=2,relief="groove")
todolistbox.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)


tasks_frame = Frame(window)
tasks_frame.config(height=30,width=600,)
tasks_frame.grid(row=0, column=1, rowspan=2, sticky="nsew", padx=5, pady=5)


button_frame = Frame(window)
button_frame.config(height=50,width=20,bg="black")
button_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)



window.mainloop()