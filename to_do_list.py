print("To do list program ")

def manage_to_do():
    to_do_list = []
    while True:
        print("MENU")
        print ('If you want to add task(s) please enter "1"')
        print('If you want to see task(s) please enter "2"')
        print('If you wan to quit function please enter "3"')

        choice = input("Enter your choice; 1,2 or 3: ")
        if choice == "1":
            task_add_input = input("Enter your task: ")
            to_do_list.append(task_add_input)
            print(f"{task_add_input} is added to the list! ")

        elif choice == "2":
            if len(to_do_list) > 0:
                print(f"Here is your list: {to_do_list}")
            elif len(to_do_list) == 0:
                print("Your list is empty, enjoy your free time! ")

            else:
                print(f"Here is your list: {to_do_list} ")
        elif choice == "3":
            print("System is shutting down right now, see you!")
            break

        else:
            print("Please enter a valid choice. 1 2 or 3")


manage_to_do()