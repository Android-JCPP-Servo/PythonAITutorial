from datetime import date
from enum import Enum
from uuid import uuid4
from sounds import play_greeting, play_response, play_response_2, play_command, play_rejection, play_goodbye


class Status(Enum):
    NOT_STARTED = 0
    IN_PROGRESS = 1
    COMPLETED = 2

class Priority(Enum):
    LOW = 0
    MEDIUM = 1
    HIGH = 2

class Item():
    __creation_date = date.today()
    __title = "empty"
    __status = Status.NOT_STARTED
    __priority = Priority.LOW
    __flag = False
    __url = ""
    __due_date = date
    __state = False
    __notes = ""
    __icon = ""

    def __init__(self, title:str=None):
        if title is not None:
            self.__title = title
        self.__id = str(uuid4())
    
    """
    PROPERTIES
    """
    @property
    def creation_date(self):
        return self.__creation_date
    
    @property
    def title(self):
        return self.__title
    
    @property
    def status(self):
        return self.__status
    
    @property
    def priority(self):
        return self.__priority
    
    @property
    def age(self):
        return self.__creation_date - date.today()
    
    @property
    def id(self):
        return self.__id
    
    @property
    def flag(self):
        return self.__flag
    
    @property
    def url(self):
        return self.__url
    
    @property
    def due_date(self):
        return self.__due_date
    
    @property
    def state(self):
        return self.__state
    
    @property
    def notes(self):
        return self.__notes
    
    @property
    def icon(self):
        return self.__icon

    """
    SETTERS
    """
    @creation_date.setter
    def creation_date(self, value):
        self.__creation_date = value

    @title.setter
    def title(self, value):
        self.__title = value
    
    @status.setter
    def status(self, value):
        self.__status = value
    
    @priority.setter
    def priority(self, value):
        self.__priority = value
    
    @flag.setter
    def flag(self, value):
        self.__flag = value
    
    @url.setter
    def url(self, value):
        self.__url = value
    
    @due_date.setter
    def due_date(self, value):
        self.__due_date = value
    
    @state.setter
    def state(self, value):
        self.__state = value
    
    @notes.setter
    def notes(self, value):
        self.__notes = value
    
    @icon.setter
    def icon(self, value):
        self.__icon = value

class Todo():
    __todos = []

    def __init__(self):
        print("New todo list created")
        self._current = -1
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self._current < len(self.__todos) - 1:
            self._current += 1
            print(self.__todos[self._current])
            return self.__todos[self._current]
        else:
            self._current = -1
        raise StopIteration
    
    def __len__(self):
        return len(self.__todos)
    
    def new_item(self, item:Item):
        print("Adding item...")
        self.__todos.append(item)
        play_response()
    
    @property
    def items(self):
        return self.__todos
    
    def show(self):
        print("*"*80)
        for item in self.__todos:
            print(item.title, item.status, item.priority, item.age)
    
    def remove_item(self, uuid:str=None, title:str=None):
        if title is None and uuid is None:
            print("You need to provide some details for me to remove this item: either ID or title")
            play_rejection()
        if uuid is None and title:
            for item in self.__todos:
                if item.title == title:
                    self.__todos.remove(item)
                    play_response()
                    return True
            print("Item with title", title, "was not found")
            return False
        if uuid:
            self.__todos.remove(uuid)
            play_response()
            return True