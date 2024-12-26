
import sys

MAX_TASK_LENGTH = 100

class Month:
    def __init__(self, year, month):
        self.year = year
        self.month = month
        self.num_days = self.get_num_days(year, month)
        self.start_day = self.calculate_start_day(year, month)
        self.tasks = [''] * self.num_days

    @staticmethod
    def is_leap_year(year):
        return (year % 4 == 0 and year % 100 != 0) or year % 400 == 0

    @staticmethod
    def get_num_days(year, month):
        if month == 2:
            return 29 if Month.is_leap_year(year) else 28
        elif month in [4, 6, 9, 11]:
            return 30
        else:
            return 31

    @staticmethod
    def calculate_start_day(year, month):
        y = year - (14 - month) // 12
        m1 = month + 12 * ((14 - month) // 12) - 2
        return (1 + y + y // 4 - y // 100 + y // 400 + (31 * m1) // 12) % 7

    def print_month(self):
        print(f"\n\n {self.month}/{self.year}")
        print("Su Mo Tu We Th Fr Sa")
        print(" " * self.start_day, end='')
        for i in range(1, self.num_days + 1):
            print(f"{i:2d} ", end='')
            if (i + self.start_day) % 7 == 0:
                print()

    def add_task(self, day, task):
        if day < 1 or day > self.num_days:
            print("Invalid day! Task not added.")
            return
        self.tasks[day - 1] = task[:MAX_TASK_LENGTH - 1]

    def modify_task(self, day):
        if day < 1 or day > self.num_days:
            print("Invalid day!")
            return
        index = day - 1
        if self.tasks[index]:
            print(f"Current task for Day {day}: {self.tasks[index]}")
            task = input("Enter new task description: ")
            self.tasks[index] = task[:MAX_TASK_LENGTH - 1]
            print("Task modified successfully!")
        else:
            print(f"No tasks found for Day {day}")

    def delete_task(self, day):
        if day < 1 or day > self.num_days:
            print("Invalid day!")
            return
        index = day - 1
        if self.tasks[index]:
            print(f"Deleting task for Day {day}: {self.tasks[index]}")
            self.tasks[index] = ''
            print("Task deleted successfully!")
        else:
            print(f"No tasks found for Day {day}")

    def view_tasks(self):
        day = int(input(f"\nEnter day to view tasks (1-{self.num_days}, 0 to exit): "))
        if day == 0:
            return
        if day < 1 or day > self.num_days:
            print("Invalid day!")
            return
        index = day - 1
        if self.tasks[index]:
            print(f"Tasks for Day {day}: {self.tasks[index]}")
            print("Select an option:")
            print("1. Modify task")
            print("2. Delete task")
            print("3. Change task date")
            print("0. Exit")
            option = int(input("Enter option: "))
            if option == 1:
                self.modify_task(day)
            elif option == 2:
                self.delete_task(day)
            elif option == 3:
                new_day = int(input("Enter new day for the task: "))
                if new_day < 1 or new_day > self.num_days:
                    print("Invalid day!")
                else:
                    task = self.tasks[index]
                    self.tasks[index] = ''
                    self.add_task(new_day, task)
                    print("Task date changed successfully!")
            elif option == 0:
                return
            else:
                print("Invalid option!")
        else:
            print(f"No tasks found for Day {day}")
            print("Select an option:")
            print("1. Add task on this day")
            print("0. Exit")
            option = int(input("Enter option: "))
            if option == 0:
                return
            elif option == 1:
                task = input("Enter task description: ")
                self.add_task(day, task)
                print("Task added successfully!")
            else:
                print("Invalid option!")

    def save_tasks(self, filename):
        with open(filename, 'w') as file:
            file.write(f"{self.year},{self.month}\n")
            for i in range(self.num_days):
                if self.tasks[i]:
                    file.write(f"{i + 1},{self.tasks[i]}\n")
        print("Tasks saved successfully!")

    def load_tasks(self, filename):
        with open(filename, 'r') as file:
            line = file.readline()
            self.year, self.month = map(int, line.split(','))
            self.tasks = [''] * self.num_days
            for line in file:
                day, task = line.strip().split(',', 1)
                day = int(day)
                if 1 <= day <= self.num_days:
                    self.tasks[day - 1] = task
        print("Tasks loaded successfully!")

    def search_tasks(self, task_description):
        print(f"Tasks matching the description '{task_description}':")
        found = False
        for i in range(self.num_days):
            if self.tasks[i] == task_description:
                print(f"Day {i + 1}: {self.tasks[i]}")
                found = True

        if not found:
            print("No tasks found.")
            print("Select an option:")
            print("1. Add task with this description")
            print("0. Exit")
            option = int(input("Enter option: "))
            if option == 0:
                return
            elif option == 1:
                day = int(input("Enter day to add the task: "))
                if day < 1 or day > self.num_days:
                    print("Invalid day!")
                else:
                    self.add_task(day, task_description)
                    print("Task added successfully!")
            else:
                print("Invalid option!")
        else:
            print("Select an option:")
            print("1. Change task date")
            print("0. Exit")
            option = int(input("Enter option: "))
            if option == 0:
                return
            elif option == 1:
                new_day = int(input("Enter new day for the task: "))
                if new_day < 1 or new_day > self.num_days:
                    print("Invalid day!")
                else:
                    for i in range(self.num_days):
                        if self.tasks[i] == task_description:
                            self.tasks[i] = ''
                            self.add_task(new_day, task_description)
                            print("Task date changed successfully!")
                            break
            else:
                print("Invalid option!")

def main():
    while True:
        year = int(input("Enter year: "))
        month = int(input("Enter month (1-12): "))
        m = Month(year, month)
        m.print_month()
        print("\nEnter tasks (press enter to finish):")
        
        while True:
            day = int(input("Enter day to add a task (0 to finish): "))
            if day == 0:
                break
            task = input("Enter task description: ")
            m.add_task(day, task)
        
        m.print_month()
        m.view_tasks()

        choice = input("Do you want to search for tasks? (y/n): ")
        if choice.lower() == 'y':
            while True:
                description = input("Enter task description to search: ")
                m.search_tasks(description)
                choice = input("Do you want to search for more tasks? (y/n): ")
                if choice.lower() != 'y':
                    break
        
        choice = input("Do you want to save tasks? (y/n): ")
        if choice.lower() == 'y':
            filename = input("Enter filename to save tasks: ")
            m.save_tasks(filename)
        
        choice = input("Do you want to load tasks? (y/n): ")
        if choice.lower() == 'y':
            filename = input("Enter filename to load tasks: ")
            m.load_tasks(filename)
            m.print_month()
            m.view_tasks()
        
        choice = input("Do you want to create tasks for another month? (y/n): ")
        if choice.lower() != 'y':
            break

if __name__ == "__main__":
    main()
