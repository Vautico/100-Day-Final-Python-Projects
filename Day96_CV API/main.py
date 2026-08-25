from numpy.f2py.auxfuncs import show
# from onnx import save
from ultralytics import YOLO
import torch

# # Create a new YOLO model from scratch
# model = YOLO("yolo26n.yaml")

# Load a pretrained YOLO model (recommended for training)
model = YOLO("yolo26n.pt")
#
# # Train the model using the 'coco8.yaml' dataset for 3 epochs
# results = model.train(data="coco8.yaml", epochs=20)
#
# # Evaluate the model's performance on the validation set
# results = model.val()
#
# # Perform object detection on an image using the model
# results = model("https://ultralytics.com/images/bus.jpg")
#
# # Export the model to ONNX format
# success = model.export(format="onnx")

results = model(source=0, show=True, conf=0.6, save=True)

