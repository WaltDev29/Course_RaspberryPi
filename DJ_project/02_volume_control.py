import RPi.GPIO as GPIO
import pygame
import os
import time
import smbus

# ---------------- GPIO 설정 ----------------
GPIO.setmode(GPIO.BCM)

SW1_PIN = 4   # 재생
SW2_PIN = 17  # 정지

GPIO.setup(SW1_PIN, GPIO.IN)
GPIO.setup(SW2_PIN, GPIO.IN)

# ---------------- I2C 설정 (노브) ----------------
bus = smbus.SMBus(1)
i2c_address = 0x48
command = 0x44

# ---------------- 오디오 설정 ----------------
os.environ["SDL_AUDIODRIVER"] = "alsa"
os.environ["AUDIODEV"] = "plughw:4,0"

# 오디오 파일 경로 지정
base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, 'test.wav')

pygame.mixer.pre_init(44100, -16, 2, 4096)
pygame.init()

if not os.path.exists(file_path):
    print("파일 없음")
    exit()

sound = pygame.mixer.Sound(file_path)

is_playing = False

print("SW1=재생 / SW2=정지 / 노브=볼륨")

try:
    while True:
        # ---------------- 버튼 입력 ----------------
        sw1 = GPIO.input(SW1_PIN)
        sw2 = GPIO.input(SW2_PIN)

        if sw1 == 0 and not is_playing:
            print("재생")
            sound.play(-1)  # 반복 재생
            is_playing = True
            time.sleep(0.3)

        if sw2 == 0 and is_playing:
            print("정지")
            sound.stop()
            is_playing = False
            time.sleep(0.3)

        # ---------------- 노브 (볼륨) ----------------
        adc_data = bus.read_i2c_block_data(i2c_address, command, 5)
        vr_raw = adc_data[1]  # 0~255

        volume = vr_raw / 255.0  # 0.0 ~ 1.0

        sound.set_volume(volume)

        print(f"볼륨: {round(volume*100,1)}%")

        time.sleep(0.1)

finally:
    pygame.mixer.quit()
    GPIO.cleanup()