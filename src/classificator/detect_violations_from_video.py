from ultralytics import YOLO

from src.classificator.detect_violation import detect_violation
from src.classificator.detection_video import detection_video
from src.classificator.model_object import Violation


def detect_violations_from_video(path_to_video: str, path_to_model: str, save_path: str = "./detected_videos",
                                 show: bool = False, save_json: bool = False, save_text: bool = False) -> dict[
    int, set[Violation]]:
    """
    :param path_to_video: Путь до видео.
    :param path_to_model: Путь до модели.
    :param save_path: Путь каталога котором будет сохранено видео, jsonl и text файлы
    :param show: Bool переменная, true если нужно отобразить видео, false иначе, по умолчанию false
    :param save_json: Bool переменная, true если нужно сохранить jsonl file, false иначе, по умолчанию false (сохранение как {save_path}/*.jsonl)
    :param save_text: Bool переменная, true если нужно сохранить text file, false иначе, по умолчанию false (сохранение как {save_path}/labels/*.txt)
    :return: Возвращает словарь, вида {id: Violation}
    """
    result = detection_video(path_to_video, path_to_model, save_path=save_path, show=show, save_json=save_json,
                             save_text=save_text)
    violations: dict[int, set[Violation]] = dict()
    for image in result:
        image_violations = detect_violation(image)
        if not image_violations: continue
        for object, viol in image_violations.items():
            if object.id not in violations:
                violations[object.id] = viol
            else:
                violations[object.id] = violations[object.id].union(viol)

    return violations

# detection_video(r"dataset/test_video/video_2025-10-27_12-59-32.mp4", r"models/besty.pt", show=True, save_json=False)
