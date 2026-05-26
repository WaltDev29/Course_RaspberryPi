import socket
import sys
import threading
import time
import RPi.GPIO as GPIO

# GPIO 설정
GPIO.setmode(GPIO.BCM)
buzzer = 12

# 4옥타브 도레미~ 5옥타브 도 주파수 배열 및 딕셔너리
SCALE = [261, 294, 330, 349, 392, 440, 493]
SCALE_STR = {'do': 0, 're': 1, 'mi': 2, 'fa': 3, 'sol': 4, 'la': 5, 'ti': 6}

# Buzzer핀의 GPIO를 출력으로 설정
GPIO.setup(buzzer, GPIO.OUT) 
pwm = GPIO.PWM(buzzer, 100)


class ServerSocketClass():
 
    def __init__(self):
        while True:
            try:
                # PWM 시작 및 초기 듀티 사이클 설정 (100%는 소리가 나지 않는 상태)
                pwm.start(100) 
                pwm.ChangeDutyCycle(100) 
                
                # TCP/IP 서버 소켓 생성 및 설정
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                
                server_address = ('', 10000)
                print("The Server is waiting. IP: {0} PORT: {1}".format(server_address[0], server_address[1]))
                
                self.sock.bind(server_address)
                self.sock.listen(1)
                print("Waiting for Client access..")
                
                self.connection, client_address = self.sock.accept()
                
                try:
                    print("Connection from", client_address)
                    while True:
                        data = self.connection.recv(4096)
                        if data:
                            msgStr = data.decode("utf-8")
                            removeLf = msgStr.split('\n')[0]
                            msg = removeLf.split(',')
                            
                            # buzzer,do 형태로 들어올 시 길이는 2이다.
                            if len(msg) == 2:
                                try:
                                    # buzzer 명령어가 맞을 때만 동작
                                    if msg[0] == "buzzer":
                                        # dutycycle 50%로 소리를 출력 상태로 변경
                                        pwm.ChangeDutyCycle(50)
                                        # 음계 명령문을 사용해서 해당하는 주파수로 변경
                                        pwm.ChangeFrequency(int(SCALE[SCALE_STR[msg[1]]])) 
                                        print("RECEIVE Message >> [Sensor]:{} [Value]:{}".format(msg[0], msg[1]))
                                        time.sleep(0.5)
                                except KeyError as err:
                                    print("invalid command : {}".format(err))
                                
                                # 연주가 끝나면 듀티 사이클을 100%로 만들어 소리를 끈다.
                                pwm.ChangeDutyCycle(100) 
                        else:
                            print("Disconnect")
                            break
                        
                        time.sleep(0.1)  # 루프 과열 방지를 위해 소폭 조절 (기존 1초에서 반응성 향상)
                        
                except Exception as err:
                    print(err)
                finally:
                    # 접속을 종료한다
                    self.connection.close()
                    
            except Exception as err:
                print(err)
            finally:
                print("Closing socket END Programs")
                self.sock.close()


if (__name__ == '__main__'):
    try:
        server_socket_instance = ServerSocketClass()  # 클래스 인스턴스 생성
    except KeyboardInterrupt:
        print("Program force quit")
        
        # 종료 시 GPIO 및 PWM 깔끔하게 정리
        pwm.stop()
        GPIO.output(buzzer, GPIO.LOW)
        GPIO.cleanup()
        sys.exit()