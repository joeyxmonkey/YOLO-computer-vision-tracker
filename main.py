import cv2
from ultralytics import YOLO
model = YOLO("yolo26m.pt")
 
video = cv2.VideoCapture("sample.mp4")

while True:
    success, frame = video.read()
    if not success:
        break
    else:
        results = model.track(
            frame,
            persist=True,
            tracker="bytetrack.yaml",
            conf=0.1,
            verbose=False,
        )
        boxes = results[0].boxes

        if boxes is not None and boxes.id is not None:
            for i, coords in enumerate(boxes.xyxy):
                chosen_id = int(boxes.id[i].item())
                x1 = int(coords[0])
                y1 = int(coords[1])
                x2 = int(coords[2])
                y2 = int(coords[3])


                center_x = (x1+x2)//2
                center_y = (y1+y2)//2


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
        cv2.imshow("sample", small_frame)
        cv2.waitKey(30)


video.release()
cv2.destroyAllWindows()

