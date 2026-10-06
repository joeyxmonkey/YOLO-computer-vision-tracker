import cv2
from ultralytics import YOLO
model = YOLO("yolo26m.pt")

def distance_fun(center_x,center_y,prev_x,prev_y):
    return float(((center_x - prev_x) ** 2 + (center_y - prev_y) ** 2) ** 0.5)
    
video = cv2.VideoCapture("Sample2.mp4")

tracked_objects = {}
next_id = 0
max_distance = 50

while True:
    success, frame = video.read()
    if not success:
        break
    else:
        results = model(frame)
        boxes = results[0].boxes

        for i, coords in enumerate(boxes.xyxy):
            x1 = int(coords[0])
            y1 = int(coords[1])
            x2 = int(coords[2])
            y2 = int(coords[3])


            center_x = (x1+x2)//2
            center_y = (y1+y2)//2

            closest_id = None
            closest_distance = float("inf")

            for object_id, (prev_x, prev_y) in tracked_objects.items():

                distance = distance_fun(center_x,center_y,prev_x,prev_y)

                if distance < closest_distance:
                    closest_distance = distance
                    closest_id = object_id

            if closest_id is not None and closest_distance < max_distance:
                chosen_id = closest_id
            else:
                chosen_id = next_id
                next_id += 1

            tracked_objects[chosen_id] = (center_x, center_y)

            cv2.circle(frame,(center_x,center_y), 12, (0, 255 , 0), 3)

            class_id = int(boxes.cls[i])
            confidence = float(boxes.conf[i])

            class_name = model.names[class_id]
            text = f"{class_name} #{chosen_id} {confidence:.0%}"

            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 120, 50), 3, 1)
            cv2.putText(frame,
                    text,
                    (x1, y1-10),
                    cv2.FONT_HERSHEY_COMPLEX,
                    0.7,
                    (0, 255, 0),
                    2
                     )
        small_frame = cv2.resize(frame, (1920, 1080))
        cv2.imshow("Sample2", small_frame)
        cv2.waitKey(30)


video.release()
cv2.destroyAllWindows()

