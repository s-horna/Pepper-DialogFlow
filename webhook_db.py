import datetime
import dateparser
from flask import Flask, request

from agenda_handler import AgendaHandler
app = Flask(__name__)

my_agenda_handler = AgendaHandler('agenda.csv')

@app.route('/') # this is the home page route
def hello_world(): # this is the home page function that generates the page code
    return "Hello world!"
    
@app.route('/webhook', methods=['POST'])
def webhook():
  req = request.get_json(silent=True, force=True)
  fulfillmentText = ''
  query_result = req.get('queryResult')
  if query_result.get('action') == 'find.event':
    time = str(query_result.get('parameters').get('time'))
    date = str(query_result.get('parameters').get('date'))
    if not date == '':
        date = date[:date.index('T')]
    else:
        date=datetime.datetime.now().strftime("%m/%d/%Y")
    time = time[time.index('T') + 1:-6]
    date_time = dateparser.parse(date + ' ' + time)
    print('time received = {0}'.format(time))
    print('date received = {0}'.format(date))
    search_results = my_agenda_handler.find_event(date_time)
    # print(search_results)
    num_events = len(search_results)
    if num_events == 0:
        fulfillmentText = "There are no events at " + date_time.strftime("%I%p") + "."
    else:
        if num_events == 1:
            fulfillmentText = 'There is one event at ' + date_time.strftime("%I%p") + '. '
        else:
            fulfillmentText = 'There are ' + str(num_events) + ' events at ' + date_time.strftime("%I%p") + '. '
        for event in search_results:
            fulfillmentText += str(event[3]) + ' will happen from ' + event[0].strftime("%I%p") + ' to ' + event[1].strftime("%I%p") + '. '
            if not event[2] == '':
                fulfillmentText += 'It will take place at ' + str(event[2]) + '. '
            if not event[4] == '':
                fulfillmentText += 'It will be led by ' + str(event[4]) + '. '
  return {
        "fulfillmentText": fulfillmentText,
        "source": "webhookdata"
    }

 
if __name__ == '__main__':
  app.run()