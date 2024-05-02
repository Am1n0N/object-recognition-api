from flask import Flask, request, send_file
import os
from ultralytics import YOLO
import cv2
import io
import numpy as np


app = Flask(__name__)

@app.route('/process_image', methods=['POST'])
def process_image():
    # Get the uploaded image file
    image_file = request.files.get('image', None)

    if not image_file:
        return 'No image file provided', 400

    # Read the image file
    image_bytes = image_file.read()
    image = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)

    # Load the model
    model_path = os.path.join('.', 'best.pt')
    model = YOLO(model_path)
    threshold = 0.5

    # Process the image
    results = model(image)[0]
    for result in results.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = result
        if score > threshold:
            cv2.rectangle(image, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 4)
            cv2.putText(image, results.names[int(class_id)].upper(), (int(x1), int(y1 - 10)),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3, cv2.LINE_AA)

    # Convert the processed image to bytes
    output_image = cv2.imencode('.jpg', image)[1].tobytes()

    # Return the processed image
    return send_file(io.BytesIO(output_image), mimetype='image/jpeg')


if __name__ == "__main__": 
    app.run()