import csv
import ast

data = "microsoft_full.csv"
parsed_data = open("microsoft_diff.csv", "w", newline='')


with open(data) as csvfile:
    with parsed_data as csvwrite:
        writer = csv.writer(csvwrite)
        reader = csv.reader(csvfile)
        lastrow = row in reader
        for row in reader:
            diff = float(row[1]) - float(lastrow[1])
            writer.writerow([row[0], row[1], diff])
            lastrow = row
            

