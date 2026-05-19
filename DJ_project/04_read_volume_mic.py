import RPi.GPIO as GPIO
import pygame
import os
import time
import smbus
import sounddevice as sd
import numpy as np

# ---------------- GPIO 설정 ----------------
GPIO.setmode(GPIO.BCM)

SW1_PIN = 4
SW2_PIN = 17

GPIO.setup(SW1_PIN, GPIO.IN)
GPIO.setup(SW2_PIN, GPIO.IN)

# ---------------- I2C 설정 ----------------
bus = smbus.SMBus(1)
i2c_address = 0x48
command = 0x44

# ---------------- 오디오 설정 ----------------
os.environ["SDL_AUDIODRIVER"] = "alsa"
os.environ["AUDIODEV"] = "plughw:4,0"

base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, 'test.wav')

pygame.mixer.pre_init(44100, -16, 2, 4096)
pygame.init()

if not os.path.exists(file_path):
    print("파일 없음")
    exit()

sound = pygame.mixer.Sound(file_path)

# ---------------- 마이크 변수 ----------------
mic_volume = 0.0  # 전역처럼 사용할 변수

def audio_callback(indata, frames, time_info, status):
    global mic_volume
    volume_norm = np.linalg.norm(indata) * 10
    mic_volume = volume_norm

# 마이크 스트림 시작 (백그라운드)
stream = sd.InputStream(callback=audio_callback)
stream.start()

# ---------------- 상태 ----------------
is_playing = False

print("SW1=재생 / SW2=정지 / 노브=볼륨 / 마이크=실제 소리")

try:
    while True:
        # ---------------- 버튼 ----------------
        sw1 = GPIO.input(SW1_PIN)
        sw2 = GPIO.input(SW2_PIN)

        if sw1 == 0 and not is_playing:
            print("재생")
            sound.play(-1)
            is_playing = True
            time.sleep(0.3)

        if sw2 == 0 and is_playing:
            print("정지")
            sound.stop()
            is_playing = False
            time.sleep(0.3)

        # ---------------- 노브 ----------------
        adc_data = bus.read_i2c_block_data(i2c_address, command, 5)
        vr_raw = adc_data[1]

        volume = vr_raw / 255.0
        sound.set_volume(volume)

        # ---------------- 마이크 음량 출력 ----------------
        print(f"노브볼륨:{round(volume*100,1)}% | 실제소리:{round(mic_volume,2)}")

        time.sleep(0.1)

finally:
    stream.stop()
    stream.close()
    pygame.mixer.quit()
    GPIO.cleanup()