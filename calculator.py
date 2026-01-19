
import os
import datetime
import json

HISTORY_FILE = 'history.json'

def ensure_history_file():
    """Creates history.json if it doesn't exist."""
    if not os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'w') as f:
            json.dump([], f)
        print(f"Created new history file: {os.path.abspath(HISTORY_FILE)}")

def append_to_history(expression, result):
    """Appends the calculation to the history file as a JSON entry."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_entry = {
        "timestamp": timestamp,
        "expression": expression,
        "result": result
    }
    
    try:
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, 'r') as f:
                history = json.load(f)
        else:
            history = []
            
        history.append(new_entry)
        
        with open(HISTORY_FILE, 'w') as f:
            json.dump(history, f, indent=4)
    except (json.JSONDecodeError, IOError):
        # Fallback if file is corrupted or can't be read
        with open(HISTORY_FILE, 'w') as f:
            json.dump([new_entry], f, indent=4)

def view_history():
    """Reads and prints the history file."""
    if os.path.exists(HISTORY_FILE):
        print("\n--- History ---")
        try:
            with open(HISTORY_FILE, 'r') as f:
                history = json.load(f)
                if not history:
                    print("History is empty.")
                for entry in history:
                    print(f"[{entry['timestamp']}] {entry['expression']} = {entry['result']}")
        except (json.JSONDecodeError, IOError):
            print("Error: Could not read history file.")
        print("---------------")
    else:
        print("No history file found.")

def calculate():
    print("Persistent Python Calculator")
    print("----------------------------")
    ensure_history_file()
    print(f"History file located at: {os.path.abspath(HISTORY_FILE)}")
    
    while True:
        print("\nOptions:")
        print("Enter 'add', 'sub', 'mul', 'div' to calculate")
        print("Enter 'history' to view history")
        print("Enter 'quit' to exit")
        
        choice = input("Enter choice: ").lower().strip()
        
        if choice == 'quit':
            print("Exiting calculator. Goodbye!")
            break
        
        if choice == 'history':
            view_history()
            continue
        
        if choice not in ('add', 'sub', 'mul', 'div'):
            print("Invalid choice, please try again.")
            continue
            
        try:
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))
        except ValueError:
            print("Invalid input. Please enter numeric values.")
            continue
        
        result = None
        operator_symbol = ""
        
        #add
        if choice == 'add':
            result = num1 + num2
            operator_symbol = '+'
           
        #sub
        elif choice == 'sub':
                result = num1 - num2 
                operator_symbol ="-"
        #mul
        
      

if __name__ == "__main__":
    calculate()
