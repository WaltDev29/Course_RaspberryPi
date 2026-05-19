import pygame
import os
import time

# 1. 환경 변수 설정 (4번 카드, 0번 장치인 USB 오디오 지목)
# 이 설정은 pygame.mixer.init() 호출 전에 수행해야 함
os.environ["SDL_AUDIODRIVER"] = "alsa"
os.environ["AUDIODEV"] = "hw:4,0"

# 2. 믹서 사전 설정 (스피커가 요구하는 16비트로 강제 고정)
# frequency: 44100Hz, size: -16 (Signed 16-bit), channels: 2
pygame.mixer.pre_init(44100, -16, 2, 4096)
pygame.init()

# 3. 오디오 파일 경로 지정
base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, 'test.wav')

if os.path.exists(file_path):
    try:
        # 사운드 객체 생성
        # Pygame 믹서가 32비트 파일을 16비트 하드웨어에 맞춰 변환 시도
        sound_effect = pygame.mixer.Sound(file_path)
        
        print("USB 스피커를 통해 출력을 시작합니다.")
        sound_effect.play()
        
        # 재생 시간만큼 대기 (음악 길이를 자동으로 계산)
        time.sleep(sound_effect.get_length())
        print("출력이 완료되었습니다.")
        
    except pygame.error as error_msg:
        print(f"재생 중 오류가 발생했습니다: {error_msg}")
    finally:
        pygame.mixer.quit()
else:
    print("지정된 경로에 파일이 존재하지 않습니다.")