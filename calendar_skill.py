# Calendar_skill.py AI Skill
# May 30, 2023

from ics import Calendar, Event
from pathlib import Path
import os
import yaml
from datetime import datetime
from dateutil.relativedelta import *
import pytz
# from yaml import loader

from sounds import play_greeting, play_response, play_response_2, play_command, play_rejection, play_goodbye

calendar_filename = 'docs/myfile.ics'
calendar_datafile = 'myfile.yml'

class Calendar_skill():
    c = Calendar()

    def __init__(self):
        """ Print a nice banner """
        print("")
        print("*"*50)
        print("Calendar Skill Loaded")
        print("*"*50)

    def add_event(self, begin:str, name:str, description:str=None):
        """ Add an event to the calendar """
        e = Event()
        e.name = name
        e.begin = begin
        e.description = description
        try:
            self.c.events.add(e)
            return True
        except:
            print("ERROR: Could not add event")
            play_rejection()
            return False
        
    def remove_event(self, event_name:str):
        """ Removes the event from the calendar """
        # Find the event
        for event in self.c.events:
            if event.name == event_name:
                # Found it!
                self.c.events.remove(event)
                print("Removed event:", event_name)
                play_response()
        # Could not find...
        print("ERROR: Could not find event to remove:", event_name)
        play_rejection()
    
    def parse_to_dict(self):
        dict = []
        for event in self.c.events:
            my_event = {}
            my_event['begin'] = event.begin.datetime
            my_event['name'] = event.name
            my_event['description'] = event.description
            dict.append(my_event)
        return dict
    
    def save(self):
        # Save to ICS file
        with open(calendar_filename, 'w') as my_file:
            my_file.writelines(self.c)
        # Save the YAML data file
        # Check if there are some entries in the dictionary; otherwise, remove the file
        if self.c.events == set():
            print("No Events - Removing YAML file")
            play_rejection()
            try:
                os.remove(calendar_datafile)
                play_response()
            except:
                print("ERROR: Could not remove YAML file")
                play_rejection()
        else:
            with open(calendar_datafile, 'w') as outfile:
                yaml.dump(self.parse_to_dict(), outfile, default_flow_style=False)
    
    def load(self):
        """ Load the Calendar data from the YAML file """
        filename = calendar_datafile
        my_file = Path(filename)
        # Check if the file exists
        if my_file.is_file():
            stream = open(filename, 'r')
            events_list = yaml.load(stream)
            for item in events_list:
                e = Event()
                e.begin = item['begin']
                e.description = item['description']
                e.name = item['name']
                self.c.events.add(e)
        else:
            # File doesn't exist
            print("File does not exist:", filename)
            play_rejection()

    def list_events(self, period:str=None):
        """
            Lists the upcoming events
            If `period` is left empty it will default to today
            Other options are:
            `all` - lists all events in the calendar
            `this week` - lists all the events this week
            `this month` - lists all the events this month
        """
        if period == None:
            period = "this week"
        # Check that there are events:
        if self.c.events == set():
            # No events found
            print("No Events in Calendar")
            play_rejection()
            return False
        else:
            event_list = []
            # Have to fix the localization - that's the +00 timezone bit on the date
            # Otherwise, it complains of non-naive date being compared with naive date
            now = pytz.utc.localize(datetime.now())
            if period == "this week":
                nextperiod = now + relativedelta(weeks = +1)
            if period == "this month":
                nextperiod = now + relativedelta(months = +1)
            if period == "all":
                nextperiod = now + relativedelta(years = +100)
            for event in self.c.events:
                event_date = event.begin.datetime
                if (event_date >= now) and (event_date <= nextperiod):
                    event_list.append(event)
            return event_list