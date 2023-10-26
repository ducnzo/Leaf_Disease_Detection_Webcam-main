import cv2
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.efficientnet import preprocess_input


# Load the pre-trained model
# model = load_model('mobileNetV2_model.h5')
# class_labels = ["anthracnose", "downy_mildew", "fresh_leaf", "powdery_mildew"]

# Nếu dùng data Plant Village thì download file .h5 về và dùng code dưới đây. 
model = load_model('MobileNetV2_PlantVillage.h5') # Chú ý đường dẫn tới file .h5 xem có đúng không nhé.
class_labels = ["Apple___Apple_scab", "Apple___Black_rot", "Apple___Cedar_apple_rust", "Apple___healthy", "Background_without_leaves"]

# Start the webcam
cap = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    # assert cap.isOpened(), 'Cannot capture source'
    # cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    # cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    # print(ret)
    frame = cv2.flip(frame, 1)

    # Preprocess the image for the model
    img = cv2.resize(frame, (224, 224))
    img = np.expand_dims(img, axis=0)
    img = preprocess_input(img)

    # Make a prediction
    preds = model.predict(img)
    pred_class = np.argmax(preds[0])
    pred_label = class_labels[pred_class]


    # Display the resulting frame with the prediction
    cv2.putText(frame, f'Disease: {pred_label}', (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow('Leaf Diseases Detection', frame)
    print(pred_label)

    # Break the loop on 'q' press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture and destroy windows
cap.release()
cv2.destroyAllWindows()
