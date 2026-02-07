# Subject Data

n = int(input("How many subjects do you have? "))
print("\nPlease enter details for each subject:")
for i in range(n):
        print(f"\n--- Subject {i+1} ---")
        name = input(f"Subject Name (default 'Subject {i+1}'): ").strip()
        if not name:
            name = f"Subject {i+1}"

        while True:
            try:
                g_str = input(f"Grade (1.0-5.0) for '{name}': ").strip()
                grade = float(g_str)
                if 1.0 <= grade <= 5.0:
                    grade.append(grade)
                    break
                else:
                    print(f"Error: Grade for '{name}' must be between 1.0 and 5.0.")
            except ValueError:
                print("Error: Make sure grades are numbers.")

        while True:
            try:
                u_str = input(f"Units (1-4) for '{name}': ").strip()
                unit = int(u_str)
                if 1 <= unit <= 4:
                    unit.append(unit)
                    break
                else:
                    print(f"Error: Units for '{name}' must be between 1 and 4.")
            except ValueError:
                print("Error: Make sure units are integers.")