import csv
import ast

data = "microsoft_full.csv"
parsed_data = open("microsoft_diff.csv", "w", newline='')


with open(data) as csvfile:
    with parsed_data as csvwrite:
        writer = csv.writer(csvwrite)
        reader = csv.reader(csvfile)
        for row in reader:
            date = row[0]
            date = date[:7]
            date = date.replace('-', '/')
            for d in senti_data:
                if date == d[0]:
                    writer.writerow([date, row[4], d[1]])
