import time

# Initialize the starting text
current_text = "Starting text"

# Print the initial text
print(current_text, end='', flush=True)

# Simulate appending words every second
for i in range(70):
    time.sleep(1)
    
    # Append new words to the existing text
    current_text += f" and more text {i}"
    
    # Use \r to overwrite the line and print the updated text
    print(f"\r{current_text}", end='', flush=True)
    
# Ensure final new line after the loop
print()
