import RPi.GPIO as GPIO
import pygame
import os
import time

# ---------------- GPIO 설정 ----------------
GPIO.setmode(GPIO.BCM)

SW1_PIN = 4   # 재생 버튼
SW2_PIN = 17  # 정지 버튼

GPIO.setup(SW1_PIN, GPIO.IN)
GPIO.setup(SW2_PIN, GPIO.IN)

# ---------------- 오디오 설정 ----------------
os.environ["SDL_AUDIODRIVER"] = "alsa"
os.environ["AUDIODEV"] = "plughw:4,0"  # 안정성 ↑

pygame.mixer.pre_init(44100, -16, 2, 4096)
pygame.init()

# 오디오 파일 경로 지정
base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, 'test.wav')

if not os.path.exists(file_path):
    print("파일 없음")
    exit()

sound = pygame.mixer.Sound(file_path)

# 상태 변수 (중복 재생 방지)
is_playing = False

print("시작: SW1=재생 / SW2=정지")

try:
    while True:
        sw1 = GPIO.input(SW1_PIN)
        sw2 = GPIO.input(SW2_PIN)

        # 버튼은 눌리면 0 (LOW)
        if sw1 == 0 and not is_playing:
            print("재생")
            sound.play(-1)  # -1 = 무한 반복
            is_playing = True
            time.sleep(0.3)  # 디바운싱

        if sw2 == 0 and is_playing:
            print("정지")
            sound.stop()
            is_playing = False
            time.sleep(0.3)

        time.sleep(0.05)

finally:
    pygame.mixer.quit()
    GPIO.cleanup()