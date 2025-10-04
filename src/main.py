from ultralytics import YOLO
import cv2
import numpy as np
import os
import random
import random
def uniqueid():
    seed = random.getrandbits(32)
    while True:
       yield seed
       seed += 1
unique_sequence = uniqueid()
model = YOLO("C:\\Users\\Fortniter\\PycharmProjects\\Kickshering neyron\\runs\\detect\\red10\\weights\\best.pt")
# Список цветов для различных классов
colors = [
    (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (0, 255, 255),
    (255, 0, 255), (192, 192, 192), (128, 128, 128), (128, 0, 0), (128, 128, 0),
    (0, 128, 0), (128, 0, 128), (0, 128, 128), (0, 0, 128), (72, 61, 139),
    (47, 79, 79), (47, 79, 47), (0, 206, 209), (148, 0, 211), (255, 20, 147)
]


# Функция для обработки изображения
def process_image(image_path):
    # Загрузка изображения
    image = cv2.imread(image_path)
    results = model(image)[0]

    # Получение оригинального изображения и результатов
    image = results.orig_img
    classes_names = results.names
    classes = results.boxes.cls.cpu().numpy()
    boxes = results.boxes.xyxy.cpu().numpy().astype(np.int32)

    # Подготовка словаря для группировки результатов по классам
    grouped_objects = {}
    ls = []
    # Рисование рамок и группировка результатов
    for class_id, box in zip(classes, boxes):
        class_name = classes_names[int(class_id)]
        color = colors[int(class_id) % len(colors)]  # Выбор цвета для класса
        id = str(next(unique_sequence))
        if class_name not in grouped_objects:
            grouped_objects[id + " "+class_name] = []
        grouped_objects[id+" "+class_name].append(box)

        # Рисование рамок на изображении
        x1, y1, x2, y2 = box
        cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)
        cv2.putText(image, id + " " + class_name, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        ls.append(id)
    # Сохранение измененного изображения
    new_image_path = os.path.splitext(image_path)[0] + '_yolo' + os.path.splitext(image_path)[1]
    cv2.imwrite(new_image_path, image)

    # Сохранение данных в текстовый файл
    text_file_path = os.path.splitext(image_path)[0] + '_data.txt'
    with open(text_file_path, 'w') as f:
        for class_name, details in grouped_objects.items():
            f.write(f"{class_name}:\n")
            for detail in details:
                f.write(f"Coordinates: ({detail[0]}, {detail[1]}, {detail[2]}, {detail[3]})\n")

    print(f"Processed {image_path}:")
    print(f"Saved bounding-box image to {new_image_path}")
    print(f"Saved data to {text_file_path}")
    for class_name, details in grouped_objects.items():
        if "Whoosh" in class_name or "Urent" in class_name or "Yandex" in class_name:
            x1 = 0
            y1 = 0
            w1 = 0
            h1 = 0
            for detail in details:
                x = detail[0]
                w = detail[1]
                y = detail[2]
                h = detail[3]
            for class_name1, details1 in grouped_objects.items():
                if "Deck" in class_name1:
                    for details in details1:
                        if (x - w // 2) < details[0] and (x + w // 2) > details[0]  and y > details[2] and h > details[3]:
                            x1 = details[0]
                            w1 = details[1]
                            y1 = details[2]
                            h1 = details[3]
            head = 0
            foot = 0
            zebra = 0
            pred = 0
            for class_name1, details1 in grouped_objects.items():
                if "Head" in class_name1:
                    for detail in details1:
                        if (x - w // 2) < (detail[0] - detail[1] // 2) and (detail[0] + detail[1] // 2) < (x + w // 2):
                            if abs(detail[0] - pred) > 75:
                                head += 1
                                pred = detail[0]
                if "Foot" in class_name1:
                    for detail in details1:
                        if (abs(x - detail[0]) < 250 and abs(y - detail[2]) < 250) or (abs(x1 - detail[0]) < 250 and x1 != 0):
                            foot += 1
                if "Zebra" in class_name1:
                    for detail in details1:
                        if x > detail[0] and y < detail[2] and (detail[1] > w or detail[3] > h):
                            zebra += 1
            if zebra > 0 and (foot > 1 or head > 1):
                print("Пересечение перехода на сим вдвоём" + " ", class_name)
            elif zebra > 0:
                print("Пересечение перехода на сим" + " ", class_name)
            elif (foot > 1 or head > 1):
                print("Катание на сим вдвоём" + " ", class_name)
            else:
                print("Без нарушений" + " ", class_name)
    print(len(grouped_objects))







process_image("C:\\Users\\Fortniter\\PycharmProjects\\Kickshering Neyron2.0\\dataset2\\output_images\\1758821633198_frame1_03093.jpg")