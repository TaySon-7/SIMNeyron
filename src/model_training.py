import os
from ultralytics import YOLO

current_dir = os.path.dirname(os.path.abspath(__file__))

data_path = os.path.join(current_dir, 'data.yaml')
model = YOLO(os.path.join(current_dir, 'yolov11n.pt'))

epochs = 500
batch = 64
imgsz = 640
if __name__ == '__main__':
    results = model.train(data=data_path,
                          epochs=epochs,
                          batch=batch,
                          imgsz=imgsz,
                          name='red',
                          device='cpu')
