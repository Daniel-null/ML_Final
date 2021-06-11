from pycoral.utils.dataset import read_label_file
from sense_hat import SenseHat
import vision

sense = SenseHat()

r = (255, 0, 0)
g = (0, 255, 0)
b = (0, 0, 255)
k = (0, 0, 0)
w = (255, 255, 255)
c = (0, 255, 255)
y = (255, 255, 0)
o = (255, 128, 0)
n = (255, 128, 128)
p = (128, 0, 128)
d = (255, 0, 128)
l = (128, 255, 128)
f = (120, 120, 120)
rr = (145, 0, 0)
gg = (0, 128, 0)

idle = [k, k, r, g, gg, g, k, k,
        k, r, g, k, g, g, g, g,
        k, k, w, w, g, g, g, g,
        k, r, w, w, g, g, g, g,
        k, k, r, f, w, w, w, k,
        gg, r, gg, gg, f, f, gg, k,
        k, gg, g, gg, f, f, gg, gg,
        k, k, r, r, k, rr, rr, k
]

sense.set_pixels(idle)

# Main program ------------------------

# Load the neural network model
detector = vision.Detector(vision.OBJECT_DETECTION_MODEL)
labels_d = read_label_file(vision.OBJECT_DETECTION_LABELS)
classifier = vision.Classifier(vision.CLASSIFICATION_MODEL)
labels = read_label_file(vision.CLASSIFICATION_LABELS) #renders labels for objects detected


# Run a loop to get images and process them in real-time
for frame in vision.get_frames():
    classes = classifier.get_classes(frame)
    # Get list of all recognized objects in the frame
    label_id = classes[0].id
    score = classes[0].score
    label = labels.get(label_id)
    #label = labels[classes[0].id] optimized version remove label_id variable
    #label = labels[label_id]    #could also use this code for label
    print(label_id, label, score)
  # Draw the label name on the video
    #vision.draw_objects()

    objects = detector.get_objects(frame, threshold=0.2)
    vision.draw_objects(frame, objects, labels_d)