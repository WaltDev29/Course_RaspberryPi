import sys
import RPi.GPIO as GPIO
from app import create_app

if __name__ == '__main__':
    try:
        # __init__.py에 정의된 app 생성 함수를 호출하여 실제 실행 객체 확보
        qt_app, gui_window = create_app()
        
        # GUI 윈도우 표시
        gui_window.show()
        
        # 애플리케이션 메인 루프 실행 (블로킹)
        sys.exit(qt_app.exec_())
        
    except Exception as e:
        print(f"Error occurred: {e}")
        
    finally:
        # 종료 시 GPIO 핀 상태 초기화 (다른 애플리케이션 충돌 방지)
        GPIO.cleanup()
