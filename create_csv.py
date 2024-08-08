import csv
import os

# Define the file path for the CSV in the Downloads directory
downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
file_path = os.path.join(downloads_path, "test_csv_file.csv")

# Ensure the Downloads directory exists
if not os.path.exists(downloads_path):
    os.makedirs(downloads_path)

# Sample data to write to the CSV file
data = [
    ['Name', 'Age', 'City'],
    ['Alice', 30, 'New York'],
    ['Bob', 25, 'Los Angeles'],
    ['Charlie', 35, 'Chicago']
]

# Open a CSV file to write the sample data
try:
    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(data)
    print(f"CSV file created successfully at {file_path}")
except Exception as e:
    print(f"An error occurred: {e}")
