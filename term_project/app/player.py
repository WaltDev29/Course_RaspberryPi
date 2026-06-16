import os
import pygame
import random
import time

class MusicPlayer:
    _instance = None
    
    def __new__(cls):
        if not cls._instance:
            cls._instance = super(MusicPlayer, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
        
    def __init__(self):
        if self._initialized:
            return
            
        # ALSA 드라이버 설정 (Raspberry Pi 오디오 환경 대응)
        try:
            os.environ["SDL_AUDIODRIVER"] = "alsa"
            os.environ["AUDIODEV"] = "hw:4,0"
            pygame.mixer.pre_init(44100, -16, 2, 4096)
            pygame.mixer.init()
        except Exception:
            # 로컬 환경(윈도우 등)에서 에러 발생 시 환경 변수 없이 재시도 (테스트 편의성)
            if "SDL_AUDIODRIVER" in os.environ:
                del os.environ["SDL_AUDIODRIVER"]
            if "AUDIODEV" in os.environ:
                del os.environ["AUDIODEV"]
            pygame.mixer.init()
            
        # 오디오 파일 기본 경로 설정 (term_project/audio)
        self.audio_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'audio')
        if not os.path.exists(self.audio_dir):
            os.makedirs(self.audio_dir)
            
        self.playlist = []
        self.current_index = 0
        self.is_playing = False
        self.is_paused = False
        self._load_playlist()
        
        self.start_time = 0
        self.pause_time = 0
        
        self._initialized = True
        
    def _load_playlist(self):
        self.playlist = []
        if os.path.exists(self.audio_dir):
            for f in os.listdir(self.audio_dir):
                if f.endswith('.wav') or f.endswith('.mp3'):
                    self.playlist.append(os.path.join(self.audio_dir, f))
        self.playlist.sort()
        
    def get_current_song_name(self):
        if not self.playlist:
            return ""
        base_name = os.path.basename(self.playlist[self.current_index])
        return os.path.splitext(base_name)[0]
        
    def add_and_play(self, filepath):
        """외부에서 파일을 직접 선택했을 때 플레이리스트에 추가하고 즉시 재생"""
        if filepath not in self.playlist:
            self.playlist.append(filepath)
        self.current_index = self.playlist.index(filepath)
        self.is_paused = False
        
        # 새로 선택한 곡이므로 강제로 다시 로드하기 위해 pause 초기화
        pygame.mixer.music.load(filepath)
        pygame.mixer.music.play()
        self.is_playing = True
        self.start_time = time.time()
        
    def play(self):
        if not self.playlist:
            return
            
        if self.is_paused:
            pygame.mixer.music.unpause()
            self.is_paused = False
            self.is_playing = True
            # 일시정지되었던 시간을 빼서 시작 시간을 보정
            self.start_time += time.time() - self.pause_time
            return
            
        song_path = self.playlist[self.current_index]
        pygame.mixer.music.load(song_path)
        pygame.mixer.music.play()
        self.is_playing = True
        self.is_paused = False
        self.start_time = time.time()
        
    def pause(self):
        if self.is_playing:
            pygame.mixer.music.pause()
            self.is_playing = False
            self.is_paused = True
            self.pause_time = time.time()
            
    def toggle_play(self):
        if self.is_playing:
            self.pause()
        else:
            self.play()
            
    def next_song(self):
        if not self.playlist:
            return
        self.current_index = (self.current_index + 1) % len(self.playlist)
        self.is_paused = False
        self.play()
        
    def prev_song(self):
        if not self.playlist:
            return
            
        # 5초 이상 재생된 상태면 현재 곡의 처음으로 돌아감 (요구사항 반영)
        if self.is_playing and (time.time() - self.start_time) > 5.0:
            self.is_paused = False
            self.play() 
        else:
            self.current_index = (self.current_index - 1) % len(self.playlist)
            self.is_paused = False
            self.play()
            
    def shuffle(self):
        if not self.playlist:
            return
            
        if len(self.playlist) > 1:
            idx = self.current_index
            while idx == self.current_index:
                idx = random.randint(0, len(self.playlist) - 1)
            self.current_index = idx
            
        self.is_paused = False
        self.play()
        
    def set_volume(self, volume_percent):
        """0 ~ 100 퍼센트 볼륨 설정"""
        pygame.mixer.music.set_volume(volume_percent / 100.0)
        
    def get_progress(self):
        """현재 곡 진행 시간(초) 반환"""
        if not self.is_playing and not self.is_paused:
            return 0
        if self.is_paused:
            return self.pause_time - self.start_time
        return time.time() - self.start_time
