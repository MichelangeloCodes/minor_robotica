import cv2
import argparse
import time  # Add the 'time' module for frame rate calculation

from ultralytics import YOLO
import supervision as sv


# set resolution camera
def parse_argument() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="YOLOv8 live")
    parser.add_argument("--webcam-resolution", default=(1280, 720), nargs=2, type=int)
    args = parser.parse_args()
    return args


def main():
    args = parse_argument()
    frame_width, frame_height = args.webcam_resolution
    
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)
    
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    
    # NANO model
    model = YOLO(r"C:\Users\jerom\Downloads\nano_model\best.onnx", task='detect', )
    
    # box properties
    box_annotator = sv.BoxAnnotator(
        thickness=2,
        text_thickness=2,
        text_scale=1
    )
    
    prev_time = time.time()  # Initialize the variable for frame rate calculation
    
    while True:
        ret, frame = cap.read()
        
        results = model(frame, agnostic_nms=True, conf=0.65)[0]
        detections = sv.Detections.from_ultralytics(results)

        # string output
        for class_id in range(len(detections.class_id)):
            class_name = results.names[detections.class_id[class_id]]
            confidence = detections.confidence[class_id]
            
            if class_name == "radish":
                print("RADISH")
            elif class_name == "lettuce":
                print("LETTUCE")
            elif class_name == "carrot":
                print("CARROT")
            elif class_name == "beetroot":
                print("BEETROOT")
        
        bounding_box_annotator = sv.BoundingBoxAnnotator()
        label_annotator = sv.LabelAnnotator()

        labels = [
            f"{results.names[detections.class_id[class_id]]} {detections.confidence[class_id]:0.2f}"
            for class_id in range(len(detections.class_id))
        ]
        
        annotated_image = bounding_box_annotator.annotate(
            scene=frame, detections=detections)
        annotated_image = label_annotator.annotate(
            scene=annotated_image, detections=detections, labels=labels)
        
        # Calculate frames
        current_time = time.time()
        fps = 1 / (current_time - prev_time)
        prev_time = current_time

        # Display frames 
        cv2.putText(annotated_image, f'FPS: {fps:.0f}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        cv2.imshow("yolov8", annotated_image)        
        
        if cv2.waitKey(30) == 27: #press esc
            break
    
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
