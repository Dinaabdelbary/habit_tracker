from habit_tracker.DB import HabitTrackerDB

class HabitTrackerCLI:
    def __init__(self):
        self.db = HabitTrackerDB()

    def main_menu(self):
        """Main menu for user interaction."""
        while True:
            print("\n1. Display habits\n2. Add habit\n3. Edit habit\n4. Display daily habits\n5. Display weekly habits\n6. Exit")
            try:
                choice = int(input("Enter your choice: "))
                if choice == 1:
                    self.display_habits()
                elif choice == 2:
                    self.add_habit()
                elif choice == 3:
                    self.edit_habit()
                elif choice == 4:
                    self.display_habits_by_periodicity('daily')
                elif choice == 5:
                    self.display_habits_by_periodicity('weekly')
                elif choice == 6:
                    self.db.close_connection()
                    break
                else:
                    print("Invalid choice! Please try again.")
            except ValueError:
                print("Invalid input! Please enter a number.")

    def display_habits(self):
        """Displays habits in a readable format."""
        habits = self.db.display_habits()
        for habit in habits:
            print(habit)

    def add_habit(self):
        """Prompts user for habit details and adds it."""
        name = input("Enter habit name: ")
        periodicity = input("Enter periodicity (daily/weekly): ").lower()
        if periodicity in ['daily', 'weekly']:
            self.db.add_habit(name, periodicity)
            print("Habit added successfully!")
        else:
            print("Invalid periodicity!")

    def edit_habit(self):
        """Allows user to delete or check a habit."""
        try:
            habit_id = int(input("Enter habit ID to edit: "))
            action = input("Enter action (delete/check): ").lower()
            if action in ['delete', 'check']:
                self.db.edit_habit(habit_id, action)
                print(f"Habit {action}ed successfully!")
            else:
                print("Invalid action!")
        except ValueError:
            print("Invalid input! Please enter a valid habit ID.")

if __name__ == "__main__":
    cli = HabitTrackerCLI()
    cli.main_menu()
