from src.classificator.detect_violations_from_video import detect_violations_from_video


def main() -> None:
    print(detect_violations_from_video("../dataset/test_video/DSC_0052.MOV", "../models/best.pt", show=True))


if __name__ == "__main__":
    main()
