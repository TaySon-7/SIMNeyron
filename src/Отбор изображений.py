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

def resize_image(image, size=(640, 640)):
    return cv2.resize(image, size)
# Функция для обработки изображения
def process_image(image_path, saved_count):
    # Загрузка изображения
    image = cv2.imread(image_path)
    image = resize_image(image)
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
        cv2.putText(image, class_name, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        ls.append(id)
    timestamp = 'SIM'
    # Сохранение измененного изображения
    output_folder = "C:\\Users\\Fortniter\\PycharmProjects\\Kickshering Neyron2.0\\dataset2\\checked_images_with_labels"
    new_image_path = os.path.splitext(image_path)[0] + '_yolo' + os.path.splitext(image_path)[1]
    new_image_path = os.path.join(output_folder, f'{timestamp}_frame1_{saved_count:05d}.jpg')

    if len(grouped_objects) > 0:
        cv2.imwrite(new_image_path, image)
        saved_count += 1
    return saved_count
folder_path = "C:\\Users\\Fortniter\\PycharmProjects\\Kickshering Neyron2.0\\dataset2\\checked_images"
saved_count = 1
for file_name in os.listdir(folder_path):
    if os.path.isfile(os.path.join(folder_path, file_name)):
        saved_count = process_image(f'C:\\Users\\Fortniter\\PycharmProjects\\Kickshering Neyron2.0\\dataset2\\checked_images\\{file_name}', saved_count)