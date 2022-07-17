import datetime
import dateparser
import csv
import timedelta

class AgendaHandler :
    def __init__(self, csv_file_path):
        self.csv_file_path = csv_file_path
        with open(csv_file_path) as csvfile:
            heading = next(csvfile)
            input = csv.reader(csvfile)
            self.formatted_data=[]
            for row in input:
                self.formatted_data.append([])
                self.formatted_data[-1].append(dateparser.parse(row[0]+ " "+row[1]))
                self.formatted_data[-1].append(dateparser.parse(row[0]+ " "+row[2]))
                self.formatted_data[-1].append(row[3])
                self.formatted_data[-1].append(row[4])
                self.formatted_data[-1].append(row[5])

    def find_event(self, date_time):
        # time must already be formatted (no date)
        matched_events = []
        for event in self.formatted_data:
            if self.time_in_range(event[0],event[1],date_time):
                matched_events.append(event)
        return matched_events
    
    def find_event_time_range(self, start_time, end_time, date=''):
        # time must already be formatted (no date)
        if date=='':
            date=datetime.datetime.now().strftime('%-m/%d/%Y')
        start_date_time = dateparser.parse(date + ' ' + start_time)
        end_date_time = dateparser.parse(date + ' ' + end_time)
        matched_events = []
        for event in self.formatted_data:
            if self.time_in_range(event[1],event[2],start_date_time):
                matched_events.append(event)
            if self.time_in_range(event[1],event[2],end_date_time):
                matched_events.append(event)
        return matched_events
    
    def time_in_range(self, start, end, x):
        """Return true if x is in the range [start, end]"""
        if start <= end:
            return start <= x <= end
        else:
            return start <= x or x <= end

# print(datetime.datetime.now().strftime('%x') == datetime.datetime(2022,7,17).strftime('%x'))