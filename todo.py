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


def prompt_nonblank(prompt):
    text = input(prompt).strip()
    if not text:
        return None
    return text


class TodoList:
    def __init__(self):
        self.tasks = []
        self.load()

    def load(self):
        try:
            with open(TASKS_FILE, "r") as file:
                data = json.load(file)
                self.tasks = [Task.from_dict(item) for item in data]
        except FileNotFoundError:
            self.tasks = []
        except json.JSONDecodeError:
            print("Warning: tasks.json is corrupted or unreadable. Starting with an empty list.")
            self.tasks = []

    def save(self):
        with open(TASKS_FILE, "w") as file:
            json.dump([task.to_dict() for task in self.tasks], file, indent=2)

    def add_task(self):
        task_text = prompt_nonblank("Enter the new task: ")
        if task_text is None:
            print("Task can't be blank.")
            return

        self.tasks.append(Task(task_text))
        print(f"Added: {task_text}")

    def view_tasks(self):
        if not self.tasks:
            print("No tasks yet!")
            return

        for index, task in enumerate(self.tasks, start=1):
            status = "x" if task.done else " "
            print(f"{index}. [{status}] {task.text}")

    def get_valid_task_index(self, prompt):
        self.view_tasks()
        if not self.tasks:
            return None

        choice = input(prompt)

        if not choice.isdigit():
            print("Please enter a number.")
            return None

        index = int(choice) - 1

        if 0 <= index < len(self.tasks):
            return index

        print("That's not a valid task number.")
        return None

    def toggle_task(self):
        index = self.get_valid_task_index("Which task number do you want to toggle? ")
        if index is None:
            return

        self.tasks[index].done = not self.tasks[index].done
        status = "done" if self.tasks[index].done else "not done"
        print(f"Marked '{self.tasks[index].text}' as {status}.")

    def delete_task(self):
        index = self.get_valid_task_index("Which task number do you want to delete? ")
        if index is None:
            return

        removed = self.tasks.pop(index)
        print(f"Deleted: {removed.text}")

    def edit_task(self):
        index = self.get_valid_task_index("Which task number do you want to edit? ")
        if index is None:
            return

        new_text = prompt_nonblank(f"New text for '{self.tasks[index].text}': ")
        if new_text is None:
            print("Task can't be blank.")
            return

        self.tasks[index].text = new_text
        print("Updated.")

    def move_task(self):
        from_index = self.get_valid_task_index("Which task number do you want to move? ")
        if from_index is None:
            return

        to_choice = input(f"Move it to which position (1-{len(self.tasks)})? ")

        if not to_choice.isdigit():
            print("Please enter a number.")
            return

        to_index = int(to_choice) - 1

        if not (0 <= to_index < len(self.tasks)):
            print("That's not a valid position.")
            return

        task = self.tasks.pop(from_index)
        self.tasks.insert(to_index, task)
        print(f"Moved '{task.text}' to position {to_index + 1}.")


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
