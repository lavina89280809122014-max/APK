from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.camera import Camera
from flask import Flask, Response
import threading
import time
import os
from zeroconf import Zeroconf, ServiceInfo
import socket

flask_app = Flask(__name__)

class CameraApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        self.cam = Camera(play=True, resolution=(640, 480))
        self.status = Label(text="Готов", size_hint_y=0.15)
        
        start_btn = Button(text="🚀 Запустить сервер", size_hint_y=0.2)
        start_btn.bind(on_press=self.start_server)
        
        switch_btn = Button(text="🔄 Переключить камеру", size_hint_y=0.15)
        switch_btn.bind(on_press=self.switch_cam)
        
        layout.add_widget(self.cam)
        layout.add_widget(self.status)
        layout.add_widget(start_btn)
        layout.add_widget(switch_btn)
        return layout

    def start_server(self, *args):
        threading.Thread(target=self.run_flask, daemon=True).start()
        self.register_zeroconf()
        self.status.text = "✅ Сервер запущен"

    def run_flask(self):
        flask_app.run(host='0.0.0.0', port=5000)

    def register_zeroconf(self):
        try:
            zeroconf = Zeroconf()
            ip = socket.gethostbyname(socket.gethostname())
            info = ServiceInfo("_mycamera._tcp.local.", "МойТелефонКамера._mycamera._tcp.local.", 
                             addresses=[socket.inet_aton(ip)], port=5000)
            zeroconf.register_service(info)
        except:
            pass

    def switch_cam(self, *args):
        self.status.text = "Переключение камеры (ограничено)"

if __name__ == '__main__':
    CameraApp().run()
