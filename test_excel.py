import csv
import dateparser



with open("agenda.csv") as csvfile:
    heading = next(csvfile)
    input = csv.reader(csvfile)
    csv_input_data = []
    for row in input:
        csv_input_data.append(row)

# print(csv_input_data)

# speakers = []

# date = dateparser.parse("2022-07-17T15:00:00-04:00")
# print(date.strftime("%B"))

event_data = []
event_id = 1
for event in csv_input_data:
    event_data.append([])
    event_data[-1].append(event_id)
    event_id += 1
    for data in event:
        event_data[-1].append(data)

print(event_data)

with open("agenda_indexed.csv", "wb") as f:
    writer = csv.writer(f)
    writer.writerow(['Event Number','Date', 'Start Time', 'End Time', 'Location', 'Event Name', 'People'])
    writer.writerows(event_data)