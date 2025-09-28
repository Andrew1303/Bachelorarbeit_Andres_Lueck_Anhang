import re

def remove_10_powers(text):
    return re.sub(r'10\^(\d+)', '', text)

# Example
input_text = "According to the table, the Base Failure Rate (BFR) for a Diode Low Frequency is:\n\n* 0.0038 failures per 10^6 hours (General Purpose Analog)\n* 0.0010 "
output_text = remove_10_powers(input_text)
print(output_text)
