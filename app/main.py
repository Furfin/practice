from ultralytics import YOLO
from collections import defaultdict

import cv2

from ultralytics import YOLO

# Loop through the video frames
from collections import defaultdict

import cv2
import numpy as np

from ultralytics import YOLO



model = YOLO("yolo11l.pt")
global idx
idx = 0

def track(filename):
    # Open the video file
    global idx
    video_path = filename
    cap = cv2.VideoCapture(video_path)
    width= int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height= int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    out = cv2.VideoWriter(f'static/out{idx}.mp4', cv2.VideoWriter_fourcc(*'h264'), 20.0, (width,height))
    track_history = defaultdict(lambda: [])

    while cap.isOpened():
        success, frame = cap.read()

        if success:
            result = model.track(frame, persist=True, classes=[28], conf=0.2,verbose=False)[0]
            if result.boxes and result.boxes.id is not None:
                boxes = result.boxes.xywh.cpu()
                track_ids = result.boxes.id.int().cpu().tolist()
                frame = result.plot()
                for box, track_id in zip(boxes, track_ids):
                    x, y, w, h = box
                    track = track_history[track_id]
                    track.append((float(x), float(y)))
                    if len(track) > 30:
                        track.pop(0)
                    points = np.hstack(track).astype(np.int32).reshape((-1, 1, 2))
                    cv2.polylines(frame, [points], isClosed=False, color=(230, 230, 230), thickness=10)
            out.write(frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        else:
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()
    idx+=1
    print(len(track_history))
    return f'out{idx-1}.mp4', len(track_history)

track('test.mp4')