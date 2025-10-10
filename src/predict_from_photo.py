import json

from ultralytics import YOLO


def predict_from_phot(path_to_video: str, path_to_model: str):
    model = YOLO(path_to_model)
    results = model(path_to_video)
    file_name = path_to_video.split('/')[-1]
    for result in results:
        boxes = result.boxes
        masks = result.masks
        keypoints = result.keypoints
        probs = result.probs
        obb = result.obb
        # result.show()
        image_bin = json.loads(result.to_json())
        jsn = json.dumps(image_bin, indent=4)
        with open(f"dataset/output_json/results_{file_name}.json", "w") as outfile:
            outfile.write(jsn)


predict_from_phot(r"dataset/output_images/SIM_frame1_00001.jpg")
