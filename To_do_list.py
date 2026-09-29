import os

def to_do_list():
    def load_to_do_list():
        if os.path.exists("to_do_list.txt"):
            with open("to_do_list.txt", "r") as f:
                lines = f.readlines()
                To_do = {}
                for line in lines:
                    task_id, task, status = line.strip().split("|")
                    To_do[int(task_id)] = {"task": task, "status": status}
                return To_do
        else:
            return {}
    To_do = load_to_do_list()
    def print_to_do_list():
        print("\nTo-do list:")
        if not To_do:
            print("  (no tasks)")
        for task_id, details in To_do.items():
            status_marker = "✓" if details["status"] == "completed" else " "
            print(f"  [{status_marker}] {task_id}. {details['task']} ({details['status']})")
    print_to_do_list()
    def add_task():
        task = input("Enter a task to add: ")
        To_do[len(To_do) + 1] = {"task": task, "status": "incomplete"}
        print(f"Added task: {task}")
        print("Updated to-do list:")
        print_to_do_list()
    def remove_task():
        print("Current to-do list:")
        print_to_do_list()
        task = int(input("Enter a task to remove: "))
        if task in To_do:
            del To_do[task]
            print(f"Removed task: {task}")
        else:
            print(f"Task '{task}' not found in the to-do list.")
        print("Updated to-do list:")
        print_to_do_list()
    def mark_task_completed():
        print("Current to-do list:")
        print_to_do_list()
        task = int(input("Enter a task to mark as completed: "))
        if task in To_do:
            To_do[task]["status"] = "completed"
            print(f"Marked task '{task}' as completed.")
        else:
            print(f"Task '{task}' not found in the to-do list.")
        print("Updated to-do list:")
        print_to_do_list()
    while True:
        print_to_do_list()
        print("\nOptions:")
        print("1. Add a note")
        print("2. Remove a note")
        print("3. Mark a note as completed")
        print("4. Exit")
        choice = input("Enter your choice : ").strip().lower()
        if choice == 'add' or choice == '1':
            add_task()
        elif choice == 'remove' or choice == '2':
            remove_task()
        elif choice == 'mark' or choice == 'complete' or choice == '3':
            mark_task_completed()
        elif choice == 'exit' or choice == '4':
            print("Exiting the to-do list application.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    to_do_list()
