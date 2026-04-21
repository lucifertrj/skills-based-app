| name        | computer-vision                                                                                                                                                          |
| ----------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| description | Computer Vision skill — Covers image processing, feature extraction, CNNs, object detection, OpenCV workflows, and practical deep learning pipelines with code examples. |

---

# Computer Vision

## What This Is

Computer Vision is a field of AI that enables machines to interpret and understand visual data like images and videos.

Use this when you're working on:

* Image classification
* Object detection
* Image preprocessing
* Face detection / recognition
* Real-world vision-based ML systems

---

## Installation

```bash
pip install opencv-python matplotlib numpy scikit-learn
pip install tensorflow  # optional for deep learning
```

---

## Quick Start

```python
import cv2

img = cv2.imread("image.jpg")
cv2.imshow("Image", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

---

## Core Concepts

### Image Representation

```python
import cv2

img = cv2.imread("image.jpg")
print(img.shape)  # (height, width, channels)
```

---

### Grayscale Conversion

```python
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
```

---

### Image Resizing

```python
resized = cv2.resize(img, (224, 224))
```

---

### Edge Detection (Canny)

```python
edges = cv2.Canny(img, 100, 200)
```

---

## Feature Extraction

### Histogram of Oriented Gradients (HOG)

```python
from skimage.feature import hog

features = hog(gray)
```

---

### Contours Detection

```python
contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
```

---

## Deep Learning for Vision

### CNN (Image Classification)

```python
import tensorflow as tf

model = tf.keras.Sequential([
    tf.keras.layers.Conv2D(32, (3,3), activation='relu', input_shape=(224,224,3)),
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(10, activation='softmax')
])
```

---

### Image Preprocessing Pipeline

```python
from tensorflow.keras.preprocessing.image import ImageDataGenerator

datagen = ImageDataGenerator(rescale=1./255)

train_data = datagen.flow_from_directory(
    "data/",
    target_size=(224,224),
    batch_size=32
)
```

---

## Object Detection (Basic Idea)

```python
# Using pre-trained Haar Cascade
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

faces = face_cascade.detectMultiScale(gray, 1.3, 5)
```

---

## Visualization

```python
import matplotlib.pyplot as plt

plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.axis('off')
plt.show()
```

---

## Training Workflow

```python
# 1. Load images
# 2. Preprocess (resize, normalize)
# 3. Train CNN
# 4. Evaluate
# 5. Predict

model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

model.fit(train_data, epochs=5)
```

---

## Useful Patterns

### Save / Load Model

```python
model.save("model.h5")
model = tf.keras.models.load_model("model.h5")
```

---

### Prediction

```python
pred = model.predict(image)
```

---

## Performance Notes

* Normalize pixel values (0–255 → 0–1)
* Use data augmentation for better accuracy
* Use GPU for CNN training
* Resize images consistently
* Avoid overfitting with dropout

---

## When to Use What

* OpenCV → preprocessing & real-time tasks
* CNN → image classification
* Haar Cascades → simple object detection
* Transfer Learning → small datasets

---

## References

* https://opencv.org/
* https://docs.opencv.org/
* https://www.tensorflow.org/tutorials/images
* https://keras.io/examples/vision/
* https://scikit-image.org/docs/stable/

---

## Extras (Optional Exploration)

* Transfer Learning (ResNet, MobileNet, VGG16)
* Object Detection (YOLO, SSD)
* Image Segmentation
* Face Recognition systems
* Real-time video processing

```
👉 *“add CV project”*
```
