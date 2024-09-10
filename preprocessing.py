import csv
from datetime import datetime

def parse_date(date_str):
    return datetime.strptime(date_str, '%m/%d/%Y').date()

def get_shift(selected_date):
    shifts = ['A', 'B', 'C']
    shift_day_types = []
    start_date = datetime(2024, 4, 30).date()
    days_since_start = (selected_date - start_date).days

    for shift in shifts:
        shift_index = shifts.index(shift)
        day_type_index = (days_since_start + shift_index * 2) % 6
        day_type = ['DAY', 'NIGHT', 'OFF'][day_type_index // 2]
        shift_day_types.append(f"{shift}: {day_type}")

    return shift_day_types

input_file = 'data/aglBreakagesYear8_raw.csv'
output_file = 'data/aglBreakagesYear8.csv'

with open(input_file, mode='r', newline='') as infile, \
        open(output_file, mode='w', newline='') as outfile:
    reader = csv.DictReader(infile)
    fieldnames = reader.fieldnames
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()

    for row in reader:
        selected_date = parse_date(row['Date'])
        shift = get_shift(selected_date)
        shift_category = next(category.split(': ')[1] for category in shift if category.startswith(row['Shift']))
        row['Category'] = shift_category
        writer.writerow(row)

print(f"Updated CSV written to {output_file}.")
