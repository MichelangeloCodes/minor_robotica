from ultralytics import YOLO

model = YOLO(r"C:\Users\jerom\Downloads\nano_model\best.onnx", task='detect')
#model = YOLO(r"C:\Users\jerom\Downloads\medium_model\best.onnx", task='detect')

results = model(source=0, show=True, conf=0.5)