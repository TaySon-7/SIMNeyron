from ultralytics.engine.results import Results

from src.classificator.model_object import MODEL_OBJECTS_FROM_STRING, DetectedObject, SCOOTERS, ModelObject, \
    ViolationNames, Violation
from ultralytics.engine.results import Results

from src.classificator.model_object import MODEL_OBJECTS_FROM_STRING, DetectedObject, SCOOTERS, ModelObject, \
    ViolationNames, Violation


def detect_violation(image: Results) -> dict[DetectedObject, set[Violation]] | None:
    objects_dict: dict[str, list[DetectedObject]] = dict()
    violations: dict[DetectedObject, set[Violation]] = dict()
    for key in MODEL_OBJECTS_FROM_STRING.values():
        objects_dict[key] = []
    if image.boxes is None or image.boxes.is_track is False:
        return None
    names = image.names
    cords = image.boxes.xyxy.tolist()
    classes = image.boxes.cls.tolist()
    # print(image.boxes)
    ids = image.boxes.id.tolist()
    for i in range(len(cords)):
        obj = DetectedObject(ids[i], MODEL_OBJECTS_FROM_STRING[names[classes[i]]], cords[i])
        objects_dict.get(obj.name).append(obj)
    # print(objects_dict)
    for scooter_type in SCOOTERS:
        for scooter in objects_dict[scooter_type]:
            deck = None
            for checked_deck in objects_dict[ModelObject.deck]:
                if scooter.top_left.x < checked_deck.center.x < scooter.bottom_right.x and scooter.center.y < checked_deck.center.y and scooter.h > checked_deck.h:
                    deck = checked_deck
                    break
            if deck is None:
                continue
            head_count, foot_count, zebra_count = 0, 0, 0
            for cur_head in objects_dict[ModelObject.head]:
                if scooter.top_left.x < cur_head.top_left.x < scooter.bottom_right.x:
                    head_count += 1

            for cur_foot in objects_dict[ModelObject.foot]:
                if deck.top_left.x < cur_foot.center.x < deck.bottom_right.x and deck.center.y > cur_foot.center.y:
                    foot_count += 1

            for cur_zebra in objects_dict[ModelObject.zebra]:
                if scooter.center.x > cur_zebra.center.x and scooter.center.y < cur_zebra.center.y and (
                        cur_zebra.w > scooter.w or cur_zebra.h > scooter.h):
                    zebra_count += 1

            violations[scooter] = set()
            if foot_count > 1 or head_count > 1:
                violations[scooter].add(
                    Violation(
                        ViolationNames.more_than_one_people, scooter_type))  # TODO Артему передать в Violation время и координаты
            elif zebra_count > 0 and foot_count > 0:
                violations[scooter].add(
                    Violation(ViolationNames.zebra_crossing, scooter_type))  # TODO Артему передать в Violation время и координаты
    return violations
