# diary_module/video_recording.py

import cv2
import threading
from datetime import datetime
import os
import pyaudio
import wave
from moviepy.editor import VideoFileClip, AudioFileClip, vfx
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap
import time

class VideoRecording:
    def __init__(self):
        self.setup_video_recording()

    def setup_video_recording(self):
        self.recording = False
        self.cap = cv2.VideoCapture(0)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)
        self.audio_frames = []

    def start_recording(self):
        if not self.recording:
            self.recording = True
            self.audio_frames = []
            self.audio_thread = threading.Thread(target=self.record_audio)
            self.audio_thread.start()
            time.sleep(1)  # 1초 대기 후 비디오 녹화 시작
            self.video_filename = self.get_unique_filename('avi')
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            self.out = cv2.VideoWriter(self.video_filename, fourcc, 20.0, (640, 480))
            self.red_dot_timer.start(500)
            print("Recording started...")

    def stop_recording(self):
        if self.recording:
            self.recording = False
            self.red_dot_timer.stop()
            self.audio_thread.join()
            self.out.release()
            self.combine_audio_video()
            print("Recording stopped.")

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.flip(frame, 1)  # 좌우 반전
            frame = self.add_timestamp(frame)
            if self.recording:
                self.out.write(frame)
                frame = self.add_red_dot(frame)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            if self.show_todo_list:
                frame = self.add_todo_list(frame)
            h, w, ch = frame.shape
            bytes_per_line = ch * w
            converted_frame = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
            self.label.setPixmap(QPixmap.fromImage(converted_frame))

    def get_unique_filename(self, ext):
        date_str = datetime.now().strftime("%Y%m%d")
        base_filename = f"assets/diary/video_{date_str}"
        counter = 1
        filename = f"{base_filename}.{ext}"
        while os.path.exists(filename):
            filename = f"{base_filename}_{counter}.{ext}"
            counter += 1
        return filename

    def record_audio(self):
        self.audio_filename = self.get_unique_filename('wav')
        audio = pyaudio.PyAudio()
        stream = audio.open(format=pyaudio.paInt16, channels=1,
                            rate=44100, input=True, input_device_index=1,
                            frames_per_buffer=1024)
        print("Recording Audio...")
        while self.recording:
            data = stream.read(1024)
            self.audio_frames.append(data)
        print("Finished Recording Audio.")
        stream.stop_stream()
        stream.close()
        audio.terminate()

        wf = wave.open(self.audio_filename, 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        wf.setframerate(44100)
        wf.writeframes(b''.join(self.audio_frames))
        wf.close()

    def combine_audio_video(self):
        video_clip = VideoFileClip(self.video_filename)
        audio_clip = AudioFileClip(self.audio_filename)

        video_duration = video_clip.duration
        audio_duration = audio_clip.duration

        # Adjust the speed of the video to match the audio length
        if video_duration > audio_duration:
            speed_factor = video_duration / audio_duration
            final_video_clip = video_clip.fx(vfx.speedx, speed_factor)
        else:
            final_video_clip = video_clip

        final_clip = final_video_clip.set_audio(audio_clip)
        final_filename = self.get_unique_filename('mp4')
        final_clip.write_videofile(final_filename, codec='libx264', audio_codec='aac')

        print(f"Video and audio have been combined successfully into {final_filename}.")

    def add_timestamp(self, frame):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        height, width, _ = frame.shape
        text_size, _ = cv2.getTextSize(timestamp, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)
        text_w, text_h = text_size
        cv2.putText(frame, timestamp, (width - text_w - 10, height - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        return frame
