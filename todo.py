import json

TASKS_FILE = "tasks.json"


class Task:
    def __init__(self, text, done=False):
        self.text = text
        self.done = done

    def to_dict(self):
        return {"text": self.text, "done": self.done}

    @classmethod
    def from_dict(cls, data):
        return cls(data["text"], data["done"])


def load_tasks():
    try:
        with open(TASKS_FILE, "r") as file:
            data = json.load(file)
            return [Task.from_dict(item) for item in data]
    except FileNotFoundError:
        return []


def save_tasks(tasks):
    with open(TASKS_FILE, "w") as file:
        json.dump([task.to_dict() for task in tasks], file, indent=2)


def prompt_nonblank(prompt):
    text = input(prompt).strip()
    if not text:
        return None
    return text


def add_task(tasks):
    task_text = prompt_nonblank("Enter the new task: ")
    if task_text is None:
        print("Task can't be blank.")
        return

    tasks.append(Task(task_text))
    print(f"Added: {task_text}")


def view_tasks(tasks):
    if not tasks:
        print("No tasks yet!")
        return

    for index, task in enumerate(tasks, start=1):
        status = "x" if task.done else " "
        print(f"{index}. [{status}] {task.text}")


def get_valid_task_index(tasks, prompt):
    view_tasks(tasks)
    if not tasks:
        return None

    choice = input(prompt)

    if not choice.isdigit():
        print("Please enter a number.")
        return None

    index = int(choice) - 1

    if 0 <= index < len(tasks):
        return index

    print("That's not a valid task number.")
    return None


def toggle_task(tasks):
    index = get_valid_task_index(tasks, "Which task number do you want to toggle? ")
    if index is None:
        return

    tasks[index].done = not tasks[index].done
    status = "done" if tasks[index].done else "not done"
    print(f"Marked '{tasks[index].text}' as {status}.")


def delete_task(tasks):
    index = get_valid_task_index(tasks, "Which task number do you want to delete? ")
    if index is None:
        return

    removed = tasks.pop(index)
    print(f"Deleted: {removed.text}")


def edit_task(tasks):
    index = get_valid_task_index(tasks, "Which task number do you want to edit? ")
    if index is None:
        return

    new_text = prompt_nonblank(f"New text for '{tasks[index].text}': ")
    if new_text is None:
        print("Task can't be blank.")
        return

    tasks[index].text = new_text
    print("Updated.")


def move_task(tasks):
    from_index = get_valid_task_index(tasks, "Which task number do you want to move? ")
    if from_index is None:
        return

    to_choice = input(f"Move it to which position (1-{len(tasks)})? ")

    if not to_choice.isdigit():
        print("Please enter a number.")
        return

    to_index = int(to_choice) - 1

    if not (0 <= to_index < len(tasks)):
        print("That's not a valid position.")
        return

    task = tasks.pop(from_index)
    tasks.insert(to_index, task)
    print(f"Moved '{task.text}' to position {to_index + 1}.")


def main():
    tasks = load_tasks()

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
            add_task(tasks)
            save_tasks(tasks)
        elif choice == "2":
            view_tasks(tasks)
        elif choice == "3":
            toggle_task(tasks)
            save_tasks(tasks)
        elif choice == "4":
            delete_task(tasks)
            save_tasks(tasks)
        elif choice == "5":
            edit_task(tasks)
            save_tasks(tasks)
        elif choice == "6":
            move_task(tasks)
            save_tasks(tasks)
        elif choice == "7":
            print("Goodbye!")
            break
        else:
            print("That's not a valid option, try again.")


if __name__ == "__main__":
    main()
