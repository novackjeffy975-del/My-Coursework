import json # Importing the json module for reading and writing JSON data to a file.
from pathlib import Path # Importing the Path class from the pathlib module for file path handling.

DATA_FILE = Path(__file__).with_name("study_log.txt") # Defines the path to the data file for storing study sessions.
def classify_session(duration): # this function classifies a study session based on its duration.
    """Return the category for a study session based on its duration."""
    if duration < 30:
        return "Short"
    if duration <= 90:
        return "Medium"
    return "Long"


def load_sessions(): # used to load the study sessions from the JSON file. If the file does not exist or is corrupted, it returns an empty list.
    """Load saved sessions from the JSON file or return an empty list."""
    if not DATA_FILE.exists():
        return []

    try:
        with DATA_FILE.open("r", encoding="utf-8") as file: 
            data = json.load(file)
            if isinstance(data, list):
                return data
            return []
    except (json.JSONDecodeError, OSError):
        print("Warning: study_log.txt is missing or corrupted. Starting with a new list.")
        return []


def save_sessions(sessions):
    """Save sessions to the JSON file."""
    try:
        with DATA_FILE.open("w", encoding="utf-8") as file:
            json.dump(sessions, file, indent=2)
    except OSError as error:
        print(f"Error saving sessions: {error}")


def add_session(sessions):
    """Collect and store a study session."""
    subject = input("Enter subject name: ").strip()
    topic = input("Enter topic covered: ").strip()
    date = input("Enter date or day label: ").strip()

    while True:
        try:
            duration = int(input("Enter duration in minutes: "))
            if duration > 0:
                break
            print("Duration must be a positive number.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    session = {
        "subject": subject,
        "topic": topic,
        "date": date,
        "duration": duration,
    }
    sessions.append(session)
    print("Session added successfully!")


def view_sessions(sessions):
    """Display all study sessions in a readable table."""
    if not sessions:
        print("No sessions recorded yet.")
        return

    print(f"{'Subject':<15} {'Topic':<20} {'Date':<15} {'Duration':<10} {'Classification'}")
    print("-" * 75)
    for session in sessions:
        classification = classify_session(session["duration"])
        print(
            f"{session['subject']:<15} {session['topic']:<20} "
            f"{session['date']:<15} {session['duration']:<10} {classification}"
        )


def search_by_subject(sessions, subject):
    """Find sessions matching the provided subject name."""
    found = False
    total_time = 0

    print(f"\nSessions for subject: '{subject}'")
    print(f"{'Topic':<20} {'Date':<15} {'Duration':<10} {'Classification'}")
    print("-" * 60)

    for session in sessions:
        if subject.lower() in session["subject"].lower():
            found = True
            total_time += session["duration"]
            classification = classify_session(session["duration"])
            print(
                f"{session['topic']:<20} {session['date']:<15} "
                f"{session['duration']:<10} {classification}"
            )

    if not found:
        print("No sessions found for that subject.")
        return

    print(f"\nTotal time spent on this subject: {total_time} minutes ({total_time / 60:.2f} hours)")


def study_statistics(sessions):
    """Display aggregate statistics for all stored sessions."""
    if not sessions:
        print("No data available for statistics.")
        return

    total_minutes = sum(session["duration"] for session in sessions)
    total_hours = total_minutes / 60

    subject_totals = {}
    longest_session = None

    for session in sessions:
        subject = session["subject"]
        subject_totals[subject] = subject_totals.get(subject, 0) + session["duration"]

        if longest_session is None or session["duration"] > longest_session["duration"]:
            longest_session = session

    weakest_subject = min(subject_totals, key=subject_totals.get)
    weakest_time = subject_totals[weakest_subject]

    print("=== Study Statistics ===")
    print(f"Total hours studied overall: {total_hours:.2f} hours")
    print("Total hours per subject:")
    for subject, minutes in subject_totals.items():
        print(f"  - {subject}: {minutes / 60:.2f} hours")

    print(
        f"Weakest subject (least total time): {weakest_subject} "
        f"({weakest_time / 60:.2f} hours)"
    )
    print(
        f"Longest single session recorded: {longest_session['duration']} minutes on "
        f"{longest_session['subject']} ({classify_session(longest_session['duration'])})"
    )


def main():
    """Run the smart study planner menu loop."""
    sessions = load_sessions()

    while True:
        print("================================")
        print("=== + Machar's study Planner + |")
        print("================================")
        print("1. Add a study session")
        print("2. View all sessions")
        print("3. Search by subject")
        print("4. View statistics")
        print("5. Save & Exit")

        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            add_session(sessions)
        elif choice == "2":
            view_sessions(sessions)
        elif choice == "3":
            subject = input("Enter subject name to search: ").strip()
            search_by_subject(sessions, subject)
        elif choice == "4":
            study_statistics(sessions)
        elif choice == "5":
            save_sessions(sessions)
            print("Data saved. Goodbye!")
            break
        else:
            print("Invalid menu choice. Please select from 1 to 5.")


if __name__ == "__main__":
    main()
