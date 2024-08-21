import sqlite3
from datetime import datetime, timedelta
import unittest

# connect to database 
conn = sqlite3.connect('habit_tracker.db')
c = conn.cursor()

# create tables 
c.execute('''
    CREATE TABLE IF NOT EXISTS habits (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        periodicity TEXT NOT NULL,  -- daily or weekly
        streak INTEGER DEFAULT 0,
        longest_streak INTEGER DEFAULT 0,
        last_checked DATE
    )
''')

c.execute('''
    CREATE TABLE IF NOT EXISTS habit_checks (
        id INTEGER PRIMARY KEY,
        habit_id INTEGER,
        date_checked DATE NOT NULL,
        FOREIGN KEY(habit_id) REFERENCES habits(id)
    )
''')

conn.commit()

# function that displays the list of habits
def display_list(conn):
    c = conn.cursor()
    c.execute("SELECT * FROM habits")
    habits = c.fetchall()
    for habit in habits:
        print(habit)

# function to add a habit
def add_habit(conn, name, periodicity):
    c = conn.cursor()
    c.execute("INSERT INTO habits (name, periodicity) VALUES (?, ?)", (name, periodicity))
    conn.commit()

# function to edit or delete a habit
def edit_habit(conn, habit_id, action):
    c = conn.cursor()
    if action == 'delete':
        c.execute("DELETE FROM habits WHERE id = ?", (habit_id,))
        conn.commit()
    elif action == 'check':
        check_habit(conn, habit_id)

# function to check a habit
def check_habit(conn, habit_id):
    c = conn.cursor()
    c.execute("SELECT * FROM habits WHERE id = ?", (habit_id,))
    habit = c.fetchone()
    
    today = datetime.today().date()
    if habit:
        last_checked = habit[5]
        streak = habit[3]
        longest_streak = habit[4]
        
        if last_checked is None or last_checked != str(today):
            if habit_broken(last_checked, habit[2]):
                streak = 0  # Reset streak if the habit was broken
            streak += 1
            longest_streak = max(streak, longest_streak)
            
            c.execute("UPDATE habits SET streak = ?, longest_streak = ?, last_checked = ? WHERE id = ?",
                      (streak, longest_streak, today, habit_id))
            c.execute("INSERT INTO habit_checks (habit_id, date_checked) VALUES (?, ?)", (habit_id, today))
            conn.commit()

# function to determine if a habit was broken
def habit_broken(last_checked, periodicity):
    if last_checked is None:
        return False
    last_checked_date = datetime.strptime(last_checked, '%Y-%m-%d').date()
    if periodicity == 'daily' and last_checked_date < datetime.today().date() - timedelta(days=1):
        return True
    elif periodicity == 'weekly' and last_checked_date < datetime.today().date() - timedelta(weeks=1):
        return True
    return False

# function to display habits by periodicity 
def display_habits_by_periodicity(conn, periodicity):
    c = conn.cursor()
    c.execute("SELECT * FROM habits WHERE periodicity = ?", (periodicity,))
    habits = c.fetchall()
    for habit in habits:
        print(habit)

# main flow based on the flowchart
def main():
    conn = sqlite3.connect('habit_tracker.db')
    while True:
        print("\n1. Display list\n2. Add habit\n3. Edit habit\n4. Display daily habits\n5. Display weekly habits\n6. Exit")
        choice = int(input("Enter your choice: "))
        
        if choice == 1:
            display_list(conn)
        elif choice == 2:
            name = input("Enter habit name: ")
            periodicity = input("Enter periodicity (daily/weekly): ")
            add_habit(conn, name, periodicity)
        elif choice == 3:
            habit_id = int(input("Enter habit ID to edit: "))
            action = input("Enter action (delete/check): ")
            edit_habit(conn, habit_id, action)
        elif choice == 4:
            display_habits_by_periodicity(conn, 'daily')
        elif choice == 5:
            display_habits_by_periodicity(conn, 'weekly')
        elif choice == 6:
            break
        else:
            print("Invalid choice! Please try again.")
    conn.close()

if __name__ == "__main__":
    main()

# testing
class TestHabitTracker(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up a temporary in-memory SQLite database for testing."""
        cls.conn = sqlite3.connect(':memory:')
        cls.c = cls.conn.cursor()

        # create the tables in the database
        cls.c.execute('''
            CREATE TABLE IF NOT EXISTS habits (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                periodicity TEXT NOT NULL,
                streak INTEGER DEFAULT 0,
                longest_streak INTEGER DEFAULT 0,
                last_checked DATE
            )
        ''')
        
        cls.c.execute('''
            CREATE TABLE IF NOT EXISTS habit_checks (
                id INTEGER PRIMARY KEY,
                habit_id INTEGER,
                date_checked DATE NOT NULL,
                FOREIGN KEY(habit_id) REFERENCES habits(id)
            )
        ''')
        cls.conn.commit()

    @classmethod
    def tearDownClass(cls):
        """Tear down the database connection after tests."""
        cls.conn.close()

    def setUp(self):
        """Clear data before each test."""
        self.c.execute("DELETE FROM habits")
        self.c.execute("DELETE FROM habit_checks")
        self.conn.commit()

    def test_add_habit(self):
        """Test adding a habit."""
        add_habit(self.conn, 'Test Habit', 'daily')
        self.c.execute("SELECT * FROM habits WHERE name = 'Test Habit'")
        habit = self.c.fetchone()
        self.assertIsNotNone(habit)
        self.assertEqual(habit[1], 'Test Habit')
        self.assertEqual(habit[2], 'daily')

    def test_check_habit(self):
        """Test checking a habit."""
        add_habit(self.conn, 'Test Habit', 'daily')
        self.c.execute("SELECT id FROM habits WHERE name = 'Test Habit'")
        habit_id = self.c.fetchone()[0]
        check_habit(self.conn, habit_id)

        # check that the streak is updated
        self.c.execute("SELECT streak FROM habits WHERE id = ?", (habit_id,))
        streak = self.c.fetchone()[0]
        self.assertEqual(streak, 1)

    def test_streak_reset_on_break(self):
        """Test if the streak resets when a habit is broken."""
        add_habit(self.conn, 'Test Habit', 'daily')
        self.c.execute("SELECT id FROM habits WHERE name = 'Test Habit'")
        habit_id = self.c.fetchone()[0]

        # Simulate two consecutive days of checks
        check_habit(self.conn, habit_id)
        self.c.execute("UPDATE habits SET last_checked = ? WHERE id = ?", 
                       (datetime.today().date() - timedelta(days=2), habit_id))
        check_habit(self.conn, habit_id)

        # check that the streak reset
        self.c.execute("SELECT streak FROM habits WHERE id = ?", (habit_id,))
        streak = self.c.fetchone()[0]
        self.assertEqual(streak, 1)  # reset and counted as 1 for today

    def test_longest_streak(self):
        """Test if the longest streak is updated correctly."""
        add_habit(self.conn, 'Test Habit', 'daily')
        self.c.execute("SELECT id FROM habits WHERE name = 'Test Habit'")
        habit_id = self.c.fetchone()[0]

        # simulate three consecutive days of checks
        check_habit(self.conn, habit_id)
        self.c.execute("UPDATE habits SET last_checked = ? WHERE id = ?", 
                       (datetime.today().date() - timedelta(days=2), habit_id))
        check_habit(self.conn, habit_id)
        self.c.execute("UPDATE habits SET last_checked = ? WHERE id = ?", 
                       (datetime.today().date() - timedelta(days=1), habit_id))
        check_habit(self.conn, habit_id)

        # check that the longest streak is 2
        self.c.execute("SELECT longest_streak FROM habits WHERE id = ?", (habit_id,))
        longest_streak = self.c.fetchone()[0]
        self.assertEqual(longest_streak, 2)

    def test_display_habits_by_periodicity(self):
        """Test displaying habits by periodicity."""
        add_habit(self.conn, 'Daily Habit', 'daily')
        add_habit(self.conn, 'Weekly Habit', 'weekly')

        # shows the output of the display function using a context manager
        import io
        from contextlib import redirect_stdout
        
        # test for daily habits
        daily_output = io.StringIO()
        with redirect_stdout(daily_output):
            display_habits_by_periodicity(self.conn, 'daily')
        daily_habits = daily_output.getvalue().strip().split('\n')
        self.assertEqual(len(daily_habits), 1)
        self.assertIn('Daily Habit', daily_habits[0])

        # test for weekly habits
        weekly_output = io.StringIO()
        with redirect_stdout(weekly_output):
            display_habits_by_periodicity(self.conn, 'weekly')
        weekly_habits = weekly_output.getvalue().strip().split('\n')
        self.assertEqual(len(weekly_habits), 1)
        self.assertIn('Weekly Habit', weekly_habits[0])

    def test_edit_habit_delete(self):
        """Test deleting a habit."""
        add_habit(self.conn, 'Test Habit', 'daily')
        self.c.execute("SELECT id FROM habits WHERE name = 'Test Habit'")
        habit_id = self.c.fetchone()[0]

        edit_habit(self.conn, habit_id, 'delete')

        self.c.execute("SELECT * FROM habits WHERE id = ?", (habit_id,))
        habit = self.c.fetchone()
        self.assertIsNone(habit)

    def test_edit_habit_check(self):
        """Test checking a habit using edit functionality."""
        add_habit(self.conn, 'Test Habit', 'daily')
        self.c.execute("SELECT id FROM habits WHERE name = 'Test Habit'")
        habit_id = self.c.fetchone()[0]

        edit_habit(self.conn, habit_id, 'check')

        # check that the streak is updated
        self.c.execute("SELECT streak FROM habits WHERE id = ?", (habit_id,))
        streak = self.c.fetchone()[0]
        self.assertEqual(streak, 1)

if __name__ == '__main__':
    unittest.main()
