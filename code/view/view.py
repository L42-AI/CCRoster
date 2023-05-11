from typing import Protocol

class View(Protocol):
    def home():
        ...

class Viewer(View):
    def home():
        pass