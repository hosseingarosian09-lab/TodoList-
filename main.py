from todolist import *
import os

if __name__ == "__main__" :
    print("welcome to this todo list ")

    def clear_screen():
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')

    open_list = "your"
    all_lists = []
    while True: 
        while True : 
            #menu 
            print('- enter 1 to create a list')
            print('- enter 2 to open a list')
            print(f'- enter 3 to add task to {open_list} todo list') 
            print('- enter 4 to remove a task ')
            print('- enter 5 to remove a list ')
            print('- enter 6 to see your list ')
            print('- enter 7 to save your to do list as a csv')
            print('- enter 8 to load a csv file')
            print('- enter 0 to exit ')

            user_input = input()
            if user_input in ['0','1','2','3','4','5','6','7','8']:
                break
            else :
                print("Invalid input!")

        # creating to do list 
        if user_input == "1":
            clear_screen()
            name = input("enter the name of todo list:")
            all_lists.append((name, todolist(name)))
            clear_screen()
            print(f"{name} successfully made!")

        # opening a to do list 
        elif user_input == "2":
            if not all_lists:
                clear_screen()
                print("you don't have a todo list yet, please make one")
            else :
                clear_screen()
                print("enter the name of the list that you want to open:")
                list_titles = []
                for i in all_lists:
                    print(f"- {i[0]}")
                    list_titles.append(i[0])
                opening_list = input()
                if open_list == opening_list :
                    clear_screen()
                    print(f"{opening_list} is already open")
                elif opening_list in list_titles :
                    clear_screen()
                    open_list = opening_list 
                    print(f"{opening_list} has been opened successfully")
                else : 
                    clear_screen()
                    print("invalid input!")

        # add task to list 
        elif user_input == "3" :
            if open_list == "your":
                clear_screen()
                print("first open a list")
            else :    
                clear_screen()
                while True :
                    title = input("write a title for your task:")
                    dis = input("write a description for your task:")
                    try:
                        Priority = int(input("enter a Priority from 1 to 5:"))
                        if Priority in [1,2,3,4,5]:
                            break
                        else:
                            clear_screen()
                            print("out of range!")
                    except ValueError :
                        clear_screen()
                        print("enter a number!")
                    except Exception as e :
                        clear_screen()
                        print(f"error: {e}")
                for i in all_lists :
                    if i[0] == open_list:
                        add = i[1]
                add.add_task(title, dis , Priority)
                clear_screen()
                print("task added successfully")

        # remove task
        elif user_input == "4" :
            clear_screen()
            if open_list == "your":
                clear_screen()
                print("first open a list")
            else :
                for i in all_lists :
                    if i[0] == open_list:
                        remove = i[1]
                if remove.show_titel() != False :
                    print("enter the title of the task you want to remove:")
                    remove_input = input()
                    clear_screen()
                    remove.remove_task(remove_input)

        # list remove        
        elif user_input == "5":
            clear_screen()
            print("which list do you want to delete:")
            for i in all_lists : 
                print(f"-{i[0]}")
            x = input()
            found = False
            for i in all_lists[:]:
                if i[0] == x :
                    all_lists.remove(i)
                    clear_screen()
                    print(f"{x} removed successfully")
                    found = True
                    break
            if not found:
                print("no such file found")   

        # show list 
        elif user_input == "6" :
            print("which list do you want to see?")
            for i in all_lists : 
                print(f"-{i[0]}")
            show_list = input()
            found = False
            for i in all_lists:
                if i[0] == show_list :
                    pri = i[1]
                    pri.show_list()
                    found = True
                    break
            if not found:
                print("no such list found")

        # save csv
        elif user_input == "7" :
            clear_screen()
            print("which list do you want to save:")
            for i in all_lists : 
                print(f"-{i[0]}")
            csv_save = input()
            found = False
            for i in all_lists:
                if i[0] == csv_save:
                    save_csv = i[1]
                    clear_screen()
                    save_csv.saveCSV(csv_save)
                    found = True
                    break
            if not found:
                print("no such list found")

        # load csv
        elif user_input == "8" :
            clear_screen()
            all_files = os.listdir('.')
            csv_files = [file for file in all_files if file.endswith('.csv')]
            for csv_file in csv_files:
                print(f"- {csv_file}")
            selected_csv = input("which file do you want to open:")
            selected_csv_title = selected_csv[:-4] if selected_csv.endswith('.csv') else selected_csv
            if selected_csv in csv_files :
                new_list = todolist(selected_csv_title)
                new_list.loadCSV(selected_csv)
                all_lists.append((selected_csv_title, new_list))
                print("file opened successfully")
            else :
                print("no such file found!")

else :
    print("you should open this directly")

