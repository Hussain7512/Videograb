from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
import threading
import subprocess
import sys

class VideoGrabApp(App):
    def build(self):
        self.title = "VideoGrab"
        self.yt_dlp_ready = False
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        title = Label(text="VideoGrab", font_size=40, size_hint=(1, 0.15))
        layout.add_widget(title)
        
        self.link_input = TextInput(
            hint_text="Yahan video ka link paste karein",
            multiline=False,
            size_hint=(1, 0.12)
        )
        layout.add_widget(self.link_input)
        
        self.quality = TextInput(
            text="1",
            hint_text="Quality (1=Best, 2=720p, 3=480p, 4=360p, 5=Audio)",
            multiline=False,
            size_hint=(1, 0.12)
        )
        layout.add_widget(self.quality)
        
        self.btn = Button(
            text="Download",
            size_hint=(1, 0.15),
            background_color=(0, 0.7, 1, 1)
        )
        self.btn.bind(on_press=self.start_download)
        layout.add_widget(self.btn)
        
        self.status = Label(
            text="Setup ho raha hai... pehli baar 1-2 minute lagenge",
            size_hint=(1, 0.3)
        )
        layout.add_widget(self.status)
        
        Clock.schedule_once(lambda dt: threading.Thread(target=self.setup_ytdlp).start(), 1)
        
        return layout
    
    def setup_ytdlp(self):
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "yt-dlp"])
            self.yt_dlp_ready = True
            Clock.schedule_once(lambda dt: setattr(self.status, 'text', 'Taiyar hai! Link paste karein'))
        except Exception as e:
            Clock.schedule_once(lambda dt: setattr(self.status, 'text', f'Setup fail: {e}'))
    
    def start_download(self, instance):
        if not self.yt_dlp_ready:
            self.status.text = "Setup abhi chal raha hai, intezar karein..."
            return
        
        link = self.link_input.text.strip()
        choice = self.quality.text.strip()
        
        if not link:
            self.status.text = "Pehle link paste karein!"
            return
        
        self.status.text = "Download shuru ho raha hai..."
        threading.Thread(target=self.download_video, args=(link, choice)).start()
    
    def download_video(self, link, choice):
        import yt_dlp
        
        if choice == '1':
            fmt = 'best[ext=mp4]/best'
        elif choice == '2':
            fmt = 'best[height<=720][ext=mp4]/best'
        elif choice == '3':
            fmt = 'best[height<=480][ext=mp4]/best'
        elif choice == '4':
            fmt = 'best[height<=360][ext=mp4]/best'
        elif choice == '5':
            fmt = 'bestaudio/best'
        else:
            fmt = 'best[ext=mp4]/best'
        
        ydl_opts = {
            'outtmpl': '/storage/emulated/0/Download/%(title).50s.%(ext)s',
            'format': fmt,
            'concurrent_fragment_downloads': 10,
            'extractor_args': {
                'youtube': {
                    'player_client': ['android', 'web']
                }
            },
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([link])
            Clock.schedule_once(lambda dt: setattr(self.status, 'text', '✅ Download mukammal! Download folder mein hai'))
        except Exception as e:
            Clock.schedule_once(lambda dt: setattr(self.status, 'text', f'❌ Masla: {e}'))

if __name__ == '__main__':
    VideoGrabApp().run()
