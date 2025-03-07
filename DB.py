import sqlite3
from datetime import datetime, timedelta

class HabitTrackerDB:
    def __init__(self, db_name="habit_tracker.db"):
        self.conn = sqlite3.connect(db_name)
        self.c = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        """Creates the necessary tables if they do not exist."""
        self.c.execute('''
            CREATE TABLE IF NOT EXISTS habits (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                periodicity TEXT NOT NULL,  -- daily or weekly
                streak INTEGER DEFAULT 0,
                longest_streak INTEGER DEFAULT 0,
                last_checked DATE
            )
        ''')

        self.c.execute('''
            CREATE TABLE IF NOT EXISTS habit_checks (
                id INTEGER PRIMARY KEY,
                habit_id INTEGER,
                date_checked DATE NOT NULL,
                FOREIGN KEY(habit_id) REFERENCES habits(id)
            )
        ''')

        self.conn.commit()

    def add_habit(self, name, periodicity):
        """Adds a new habit to the database."""
        self.c.execute("INSERT INTO habits (name, periodicity) VALUES (?, ?)", (name, periodicity))
        self.conn.commit()

    def display_habits(self):
        """Displays the list of habits."""
        self.c.execute("SELECT * FROM habits")
        return self.c.fetchall()

    def edit_habit(self, habit_id, action):
        """Edits or deletes a habit."""
        if action == 'delete':
            self.c.execute("DELETE FROM habits WHERE id = ?", (habit_id,))
            self.conn.commit()
        elif action == 'check':
            self.check_habit(habit_id)

    def check_habit(self, habit_id):
        """Checks a habit and updates streaks."""
        self.c.execute("SELECT * FROM habits WHERE id = ?", (habit_id,))
        habit = self.c.fetchone()
        today = datetime.today().date()

        if habit:
            last_checked = habit[5]
            streak = habit[3]
            longest_streak = habit[4]

            if last_checked is None or last_checked != str(today):
                if self.habit_broken(last_checked, habit[2]):
                    streak = 0  
                streak += 1
                longest_streak = max(streak, longest_streak)

                self.c.execute("UPDATE habits SET streak = ?, longest_streak = ?, last_checked = ? WHERE id = ?",
                              (streak, longest_streak, today, habit_id))
                self.c.execute("INSERT INTO habit_checks (habit_id, date_checked) VALUES (?, ?)", (habit_id, today))
                self.conn.commit()

    def habit_broken(self, last_checked, periodicity):
        """Determines if a habit was broken."""
        if last_checked is None:
            return False
        last_checked_date = datetime.strptime(last_checked, '%Y-%m-%d').date()
        if periodicity == 'daily' and last_checked_date < datetime.today().date() - timedelta(days=1):
            return True
        elif periodicity == 'weekly' and last_checked_date < datetime.today().date() - timedelta(weeks=1):
            return True
        return False

    def display_habits_by_periodicity(self, periodicity):
        """Displays habits based on periodicity."""
        self.c.execute("SELECT * FROM habits WHERE periodicity = ?", (periodicity,))
        return self.c.fetchall()

    def close_connection(self):
        """Closes the database connection."""
        self.conn.close()
