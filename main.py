from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from camera4kivy import Preview
from flask import Flask, Response
import threading
import cv2
import time
import os
from zeroconf import Zeroconf, ServiceInfo
import socket

flask_app = Flask(__name__)
current_frame = None

def gen_frames():
    global current_frame
    while True:
        if current_frame is not None:
            _, jpeg = cv2.imencode('.jpg', current_frame)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')
        time.sleep(0.05)

@flask_app.route('/video')
def video():
    os.system('termux-notification --title "Камера" --content "Компьютер подключился!"')
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

class CameraApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        self.preview = Preview()
        self.status = Label(text="Готов к запуску", size_hint_y=0.15)
        
        start_btn = Button(text="🚀 Запустить камеру и сервер", size_hint_y=0.2)
        start_btn.bind(on_press=self.start_all)
        
        switch_btn = Button(text="🔄 Переключить (передняя/задняя)", size_hint_y=0.15)
        switch_btn.bind(on_press=self.switch_cam)
        
        layout.add_widget(self.preview)
        layout.add_widget(self.status)
        layout.add_widget(start_btn)
        layout.add_widget(switch_btn)
        return layout

    def start_all(self, *args):
        self.preview.connect_camera(camera_id='back', resolution=(640, 480), callback=self.on_frame)
        threading.Thread(target=self.run_server, daemon=True).start()
        self.register_zeroconf()
        self.status.text = "✅ Сервер запущен!\nИщите устройство с компьютера"

    def on_frame(self, frame):
        global current_frame
        current_frame = frame

    def run_server(self):
        flask_app.run(host='0.0.0.0', port=5000, debug=False)

    def register_zeroconf(self):
        try:
            zeroconf = Zeroconf()
            ip = socket.gethostbyname(socket.gethostname())
            info = ServiceInfo(
                "_mycamera._tcp.local.",
                "МойТелефонКамера._mycamera._tcp.local.",
                addresses=[socket.inet_aton(ip)],
                port=5000
            )
            zeroconf.register_service(info)
        except:
            pass

    def switch_cam(self, *args):
        current = self.preview.camera_id
        new = 'front' if current == 'back' else 'back'
        self.preview.connect_camera(camera_id=new, resolution=(640, 480))
        self.status.text = f"📱 Камера: {new.upper()}"

if __name__ == '__main__':
    CameraApp().run()