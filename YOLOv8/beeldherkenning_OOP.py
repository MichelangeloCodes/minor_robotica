import cv2
import argparse
import time
from ultralytics import YOLO
import supervision as sv


class YOLOv8Detector:
    def __init__(self, webcam_resolution=(1280, 720), model_path=r"C:\Users\jerom\Downloads\nano_model\best.onnx"):
        
        self.frame_width, self.frame_height = webcam_resolution
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.frame_width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.frame_height)
        if not self.cap.isOpened():
            print("Cannot open camera")
            exit()
            
        self.model = YOLO(model_path, task='detect')
        self.box_annotator = sv.BoxAnnotator(thickness=2, text_thickness=2, text_scale=1)
        self.prev_time = time.time()


    def detect_objects(self):
        while True:
            ret, frame = self.cap.read()
            results = self.model(frame, agnostic_nms=True, conf=0.65)[0]
            detections = sv.Detections.from_ultralytics(results)

            labels = [
                f"{results.names[detections.class_id[class_id]]} {detections.confidence[class_id]:0.2f}"
                for class_id in range(len(detections.class_id))
            ]

            annotated_image = sv.BoundingBoxAnnotator().annotate(scene=frame, detections=detections)
            annotated_image = sv.LabelAnnotator().annotate(scene=annotated_image, detections=detections, labels=labels)

            current_time = time.time()
            fps = 1 / (current_time - self.prev_time)
            self.prev_time = current_time

            cv2.putText(annotated_image, f'FPS: {fps:.0f}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.imshow("yolov8", annotated_image)

            if cv2.waitKey(30) == 27:  # press esc
                break

        self.cap.release()
        cv2.destroyAllWindows()


def main():
    parser = argparse.ArgumentParser(description="YOLOv8 live")
    parser.add_argument("--webcam-resolution", default=(1280, 720), nargs=2, type=int)
    args = parser.parse_args()
    
    detector = YOLOv8Detector(webcam_resolution=(args.webcam_resolution[0], args.webcam_resolution[1]))
    detector.detect_objects()


if __name__ == "__main__":
    main()
