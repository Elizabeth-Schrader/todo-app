from todolist import TodoList


def main():
    todo_list = TodoList()

    while True:
        print("\n--- To-Do List ---")
        print("1. Add task")
        print("2. View tasks")
        print("3. Mark/unmark task as done")
        print("4. Delete task")
        print("5. Edit task text")
        print("6. Reorder task")
        print("7. Quit")

        choice = input("Choose an option: ")

        if choice == "1":
            todo_list.add_task()
            todo_list.save()
        elif choice == "2":
            todo_list.view_tasks()
        elif choice == "3":
            todo_list.toggle_task()
            todo_list.save()
        elif choice == "4":
            todo_list.delete_task()
            todo_list.save()
        elif choice == "5":
            todo_list.edit_task()
            todo_list.save()
        elif choice == "6":
            todo_list.move_task()
            todo_list.save()
        elif choice == "7":
            print("Goodbye!")
            break
        else:
            print("That's not a valid option, try again.")


if __name__ == "__main__":
    main()
