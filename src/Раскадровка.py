import cv2
import os
import time
folder_path = ""
frame_count = 6007
saved_count = 6007
for file_name in os.listdir(folder_path):
    if os.path.isfile(os.path.join(folder_path, file_name)):
        # Путь к видеофайлу
        video_path = f"{file_name}"
        # Папка для сохранения изображений
        output_folder = ''
        # Интервал между кадрами (каждый n-й кадр будет сохранен)
        frame_interval = 4  # Можно изменить на 2, 5 и т.д.

        os.makedirs(output_folder, exist_ok=True)

        # Открытие видеофайла
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print(f"Ошибка открытия видеофайла: {video_path}")
            exit()


        while True:
            ret, frame = cap.read()
            if not ret:
                break

            if frame_count % frame_interval == 0:
                # Получение текущего времени в виде временной метки
                timestamp = int(time.time() * 1000)  # Используем миллисекунды для большей точности
                output_path = os.path.join(output_folder, f'{timestamp}_frame1_{saved_count:05d}.jpg')
                cv2.imwrite(output_path, frame)
                print(f"Сохранено: {output_path}")
                saved_count += 1

            frame_count += 1

        cap.release()
        print("Разделение видео на фотографии завершено.")