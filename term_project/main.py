import sys
import RPi.GPIO as GPIO
from app import create_app, cleanup_app

if __name__ == '__main__':
    try:
        # __init__.py에 정의된 app 생성 함수를 호출하여 tkinter root 객체 확보
        root, gui_window = create_app()
        
        # 애플리케이션 메인 루프 실행 (블로킹)
        root.mainloop()
        
    except Exception as e:
        print(f"Error occurred: {e}")
        
    finally:
        # 애플리케이션 종료 시 안전하게 하드웨어 및 플레이어 스레드/메모리 해제
        cleanup_app()
        # 종료 시 GPIO 핀 상태 초기화 (다른 애플리케이션 충돌 방지)
        GPIO.cleanup()
