import cv2

class CameraStreaming:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)

    def update_frame(self, show_todo_list, add_todo_list, blink_selected, current_task_index):
        ret, frame = self.cap.read()
        if ret:
            if show_todo_list:
                frame = add_todo_list(frame, blink_selected, current_task_index)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return frame

    def release(self):
        self.cap.release()
