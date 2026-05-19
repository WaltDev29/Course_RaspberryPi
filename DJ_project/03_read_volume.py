import RPi.GPIO as GPIO
import pygame
import os
import time
import smbus
import wave
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

# ---------------- 🔥 음량 분석 (추가) ----------------
wf = wave.open(file_path, 'rb')
frames = wf.readframes(wf.getnframes())
data = np.frombuffer(frames, dtype=np.int16)

sample_rate = wf.getframerate()
chunk_size = int(sample_rate * 0.1)  # 0.1초 단위

volume_levels = []

for i in range(0, len(data), chunk_size):
    chunk = data[i:i+chunk_size]
    if len(chunk) > 0:
        rms = np.sqrt(np.mean(chunk**2))
        volume_levels.append(rms)

# 정규화 (0~1)
max_rms = max(volume_levels)
volume_levels = [v / max_rms for v in volume_levels]

# ---------------- 상태 ----------------
is_playing = False
start_time = 0

print("SW1=재생 / SW2=정지 / 노브=볼륨")

try:
    while True:
        # 버튼
        sw1 = GPIO.input(SW1_PIN)
        sw2 = GPIO.input(SW2_PIN)

        if sw1 == 0 and not is_playing:
            print("재생")
            sound.play(-1)
            is_playing = True
            start_time = time.time()
            time.sleep(0.3)

        if sw2 == 0 and is_playing:
            print("정지")
            sound.stop()
            is_playing = False
            time.sleep(0.3)

        # 노브 볼륨
        adc_data = bus.read_i2c_block_data(i2c_address, command, 5)
        vr_raw = adc_data[1]
        volume = vr_raw / 255.0
        sound.set_volume(volume)

        # ---------------- 🔥 현재 음악 음량 ----------------
        if is_playing:
            elapsed = time.time() - start_time
            index = int(elapsed / 0.1)

            if index < len(volume_levels):
                music_level = volume_levels[index]
                print(f"볼륨:{round(volume*100,1)}% | 음악세기:{round(music_level,2)}")
            else:
                start_time = time.time()  # 루프 재생 대응

        time.sleep(0.1)

finally:
    pygame.mixer.quit()
    GPIO.cleanup()