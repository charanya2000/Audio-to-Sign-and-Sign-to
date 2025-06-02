import os
import cv2
import numpy as np
import tensorflow as tf
import pyttsx3

EMOTIONS = ['angry', 'disgusted', 'fearful', 'happy', 'sad', 'surprised', 'neutral']
PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))

# Load the model once
model = tf.keras.models.load_model(os.path.join(PROJECT_PATH, 'models', 'emotion_detection_model_advanced.h5'))

def predict_emotion(image):
    """Predict the emotion of a given image using the trained model."""
    image = cv2.resize(image, (48, 48)) / 255.0
    image = np.expand_dims(image, axis=-1)  # Ensure the shape is (48, 48, 1)
    image = np.expand_dims(image, axis=0)   # Model expects (1, 48, 48, 1)
    prediction = model.predict(image)
    return EMOTIONS[np.argmax(prediction)]

def speak_message(emotion):
    """Convert emotion text to speech."""
    engine = pyttsx3.init()
    engine.say(emotion)
    engine.runAndWait()

def facialexpression_model():
    """Real-time facial expression detection using webcam."""
    cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    face_cascade = cv2.CascadeClassifier(cascade_path)

    cap = cv2.VideoCapture(0)
    print("Press 'q' to quit.")

    last_emotion = None  # Track last emotion

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.3, minNeighbors=5)

        for (x, y, w, h) in faces:
            roi_gray = gray_frame[y:y+h, x:x+w]
            emotion = predict_emotion(roi_gray)

            if emotion != last_emotion:  # Speak only if the emotion changes
                speak_message(emotion)
                last_emotion = emotion  # Update last detected emotion

            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.putText(frame, emotion, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow('Facial Expression Detection', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
