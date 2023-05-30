import pyjokes
from ai import AI
from todo import Todo, Item
from weather import Weather
from randfacts import randfacts
from datetime import datetime
from calendar_skill import Calendar_skill
import dateparser

# Sound effects to replace voice
from sounds import play_greeting, play_response, play_response_2, play_command, play_rejection, play_goodbye, play_acknowledge

jack = AI()
todo = Todo()
calendar = Calendar_skill()
calendar.load()

"""
FACTS
"""
def facts():
    fact = randfacts.get_fact()
    print(fact)
    play_command()

"""
JOKES
"""
def joke():
    funny = pyjokes.get_joke()
    print(funny)

"""
TODOS
"""
def add_todo():
    item = Item()
    # jack.say("Tell me what to add to the list")
    print("Tell me what to add to the list")
    play_command()
    try:
        item.title = jack.listen()
        todo.new_item(item)
        message = "Added " + item.title
        # jack.say(message)
        print(message)
        play_command()
        return True
    except:
        print("Oops, there was an error")
        play_rejection()
        return False

def list_todos():
    if len(todo) > 0:
        jack.say("Here are your to do's...")
        for item in todo:
            # jack.say(item.title)
            print(item.title)
        play_response_2()
    else:
        jack.say("The list is empty!")
        play_rejection()

def remove_todo():
    jack.say("Tell me which to remove...")
    try:
        item_title = jack.listen()
        todo.remove_item(title=item_title)
        message = "Removed " + item_title
        # jack.say(message)
        print(message)
        play_response()
        return True
    except:
        print("Oops, there was an error")
        play_rejection()
        return False

"""
WEATHER
"""
def weather():
    myweather = Weather()
    print(myweather.forecast)
    play_response_2()

"""
CALENDAR
"""
def add_event():
    print("What is the name of the event?")
    play_response_2()
    try:
        event_name = jack.listen()
        # Get the time the event starts
        print("When is the event?")
        play_acknowledge()
        event_begin = jack.listen()
        event_isodate = dateparser.parse(event_begin).strftime("%Y-%m-%d %H:%M:%D")
        # Get the event description
        print("What is the event description?")
        play_acknowledge()
        event_description = jack.listen()
        # Print the success/failure message
        message = "Ok, adding event" + event_name
        print(message)
        play_response()
        calendar.add_event(begin=event_isodate, name=event_name, description=event_description)
        calendar.save()
        return True
    except:
        print("ERROR: Could not add event")
        play_rejection()

def remove_event():
    print("What is the name of the event you want to remove?")
    try:
        event_name = jack.listen()
        try:
            calendar.remove_event(event_name = event_name)
            print("Removed event successfully")
            play_command()
            return True
        except:
            print("Failed to remove event:", event_name)
            play_rejection()
            return False
    except:
        print("ERROR: Unrecognized action. Please try again.")
        play_rejection()
        return False

def list_events(period):
    this_period = calendar.list_events(period = period)
    if this_period is not None:
        message = "There "
        if len(this_period) > 1:
            message += "are "
        else:
            message += "is "
        message += str(len(this_period))
        if len(this_period) > 1:
            message += " events "
        else:
            message += " event "
        message += "in this diary."
        print(message)
        play_acknowledge()
        for event in this_period:
            event_date = event.begin.datetime
            weekday = datetime.strftime(event_date, "%A")
            day = str(event.begin.datetime.day)
            month = datetime.strftime(event_date, "%B")
            year = datetime.strftime(event_date, "%Y")
            time = datetime.strftime(event_date, "%I:%M %p")
            name = event.name
            description = event.description
            message = f"On {weekday} {day} of {month}, {year} at {time}, there is an event called {name} with an event description of {description}."
            print(message)
            play_response_2()

# Initialize Jack
command = ""
print("Hello!")
play_greeting()    

while True and command not in ["good bye", 'bye', 'quit', 'exit', 'goodbye', 'exit', 'stop']:
    # handleCommands(command)
    try:
        command = jack.listen()
        command = command.lower()
    except:
        print("Oops, there was an error")
        play_rejection()
        command = ""
    print("Command was", command)
    if command in ["tell me a joke", "got any funny jokes"]:
        joke()
        command = ""
    if command in ["add to-do", "add to do", "add item to list"]:
        add_todo()
        command = ""
    if command in ["list todos", "show to do list", "what's on my todo list", "what's on my to do list", "show to-do list"]:
        list_todos()
        command = ""
    if command in ["remove todo", "remove item from list", "remove to do from list"]:
        remove_todo()
        command = ""
    if command in ["what's the weather today", "what's today's weather", "what's it like outside"]:
        weather()
        command = ""
    if command in ["tell me a fact", "tell me something new", "tell me something interesting"]:
        facts()
        command = ""
    # Additional greetings
    if command in ["good morning", "good afternoon", "good evening", "good night"]:
        now = datetime.now()
        hr = now.hour
        if hr <= 0 <= 12:
            message = "Morning"
        if hr >= 12 <= 17:
            message = "Afternoon"
        if hr >= 17 <= 21:
            message = "Evening"
        if hr > 21: message = "Night"
        message = f"Good {message}, Andersen"
        print(message)
        play_command()
        # Give me the deets!
        list_todos()
        weather()
        joke()
        facts()
    # Calendar commands
    if command in ["add event", "add to calendar", "new event", "add a new event"]:
        add_event()
        command = ""
    if command in ["delete event", "delete from calendar", "remove event", "cancel event"]:
        remove_event()
        command = ""
    if command in ["anything this month", "list all events this month", "what's going on this month"]:
        list_events(period="month")
        command = ""
    if command in ["what's going on this week", "list this week's events", "anything happening this week"]:
        list_events(period="week")
        command = ""
    if command in ["list all events"]:
        list_events(period="all")
        command = ""

print("Goodbye!")
jack.stop_ai()