import uuid
from enum import Enum
from typing import Any


class ModelObject(str, Enum):
    yandex = "Yandex"
    whoosh = "Whoosh"
    urent = "Urent"
    deck = "Deck"
    foot = "Foot"
    head = "Head"
    zebra = "Zebra"

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name


class ViolationNames(str, Enum):
    more_than_one_people = "Нарушение: Два или более человека на самокате"
    zebra_crossing = "Нарушение: Езда по пешеходному переходу не спешиваясь с СИМ"

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name


class Violation:
    def __init__(self, violation_name: ViolationNames, global_coordinates: Any = None, time: Any = None):
        self.violation_name = violation_name
        self.global_coordinates = global_coordinates
        self.time = time
        # TODO Артему необходимо заменить здесь координаты нарушения + добавить время нарушения

    def __hash__(self):
        return hash(self.violation_name.name)

    def __eq__(self, other):
        return self.violation_name.name == other.violation_name.name

    def __repr__(self):
        return f"[{self.time}]: {self.violation_name} in {self.global_coordinates}"


MODEL_OBJECTS_FROM_STRING = {"Yandex": ModelObject.yandex,
                             "Whoosh": ModelObject.whoosh,
                             "Urent": ModelObject.urent,
                             "Deck": ModelObject.deck,
                             "Foot": ModelObject.foot,
                             "Head": ModelObject.head,
                             "Zebra": ModelObject.zebra}
OBJECT_ID = {ModelObject.yandex: 0,
             ModelObject.whoosh: 1,
             ModelObject.urent: 2,
             ModelObject.deck: 3,
             ModelObject.foot: 4,
             ModelObject.head: 5,
             ModelObject.zebra: 6}

SCOOTERS = [ModelObject.yandex, ModelObject.urent, ModelObject.whoosh]


class Dot:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y


class DetectedObject:
    def __init__(self, _id: int, name: ModelObject, cords: tuple[float, float, float, float]):
        self.id = int(_id)
        self.name = name
        self.cords = cords
        self.top_left = Dot(cords[0], cords[1])
        self.bottom_right = Dot(cords[2], cords[3])
        self.w = abs(cords[0] - cords[2])
        self.h = abs(cords[1] - cords[3])
        self.center = Dot(self.top_left.x + self.w / 2, self.top_left.y + self.h / 2)

    def __repr__(self):
        return f"{self.name}[{self.id}]: {self.cords}"

    def dot_inside(self):
        pass
