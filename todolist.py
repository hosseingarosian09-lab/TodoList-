import csv

if __name__ != "__main__" : 
    class task:
        def __init__(self, title, description, priority, completed=False):
            self.title = title
            self.description = description
            self.priority = int(priority)
            self.completed = bool(completed)

        def send_priority(self):
            return self.priority
        def send_title(self):
            return self.title
        def send_description(self):
            return self.description
        def send_completed(self):
            return self.completed
        def toggle_complete(self):
            self.completed = not self.completed

    class todolist:
        def __init__(self, name):
            self.list_name = name 
            self.my_list = []
    
        def add_task(self, title, description, priority, completed=False):
            self.my_list.append(task(title, description, priority, completed))
    
        def remove_task(self, title):
            for t in self.my_list[:]:
                if t.title == title:
                    self.my_list.remove(t)
                    print(f"Task '{title}' removed successfully.")
                    return
            print(f"Error: Task with title '{title}' not found")
   
        def show_titel(self):
            if not self.my_list:
                return f"The to-do list '{self.list_name}' is empty."
            return "\n".join(f"{i}. {t.title} [{'✔' if t.completed else ' '}]" for i, t in enumerate(self.my_list, 1))
        
        def get_priority(self, title):
            for t in self.my_list:
                if t.title == title:
                    return t.send_priority()
    
        def saveCSV(self, filename):
            try:
                if not filename.endswith('.csv'):
                    filename += '.csv'
                with open(filename, 'w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow(['Title', 'Description', 'Priority', 'Completed'])
                    for t in self.my_list:
                        writer.writerow([t.title, t.description, t.priority, t.completed])
                print(f"Tasks saved to {filename} successfully.")
                return True
            except Exception as e:
                print(f"Error saving to CSV: {e}")
                return False
    
        def loadCSV(self, filename):
            try:
                if not filename.endswith('.csv'):
                    filename += '.csv'
                self.my_list = []  
                with open(filename, 'r', newline='', encoding='utf-8') as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        completed = row.get('Completed', 'False').lower() == 'true'
                        new_task = task(row['Title'], row['Description'], int(row['Priority']), completed)
                        self.my_list.append(new_task)
                print(f"Tasks loaded from {filename} successfully.")
                return True
            except Exception as e:
                print(f"Error loading CSV: {e}")
                return False
else :
    print("open the main file")