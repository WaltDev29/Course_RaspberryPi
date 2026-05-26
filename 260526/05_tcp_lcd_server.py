import socket
import sys
import threading
import time
import RPi_I2C_driver

# RPi_I2C_driver 모듈을 사용하는 예제
textLcd = RPi_I2C_driver.lcd()
textLcd.lcd_clear()

class ServerSocketClass():
 
    def __init__(self):
        while True:
            try:
                # [수정] 이전 부저 코드의 pwm 설정 흔적이 남아있어 주석 처리했습니다.
                # 필요하다면 상단에 pwm 객체를 생성하고 주석을 해제하세요.
                # pwm.start(100) 
                # pwm.ChangeDutyCycle(100) 
                
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
                            
                            # [수정] 특수문자 따옴표(’)를 표준 따옴표(')로 수정했습니다.
                            msg = removeLf.split(',')

                            # textlcd,1,hello 형태로 들어올 시 길이는 3이다.
                            if len(msg) == 3:
                                # textlcd 가 아니면 동작하지 않는다.
                                if msg[0] == "textlcd":
                                    line = int(msg[1])
                                    
                                    if line >= 1 and line <= 2:
                                        # 화면을 공백으로 한 번 지우고 새로운 메시지 출력
                                        textLcd.lcd_display_string("                ", line) 
                                        # 16자 이내 아스키코드, 1은 첫 번째 줄이고 2는 두 번째 줄이다
                                        textLcd.lcd_display_string(msg[2], line)
                                        print(" line:{} / message:{}".format(msg[1], msg[2]))
                                        
                                        self.connection.sendall("OK.".encode('utf-8'))
                                    else:
                                        # [수정] 코드 끝에 있던 중복 괄호 ')'를 제거했습니다.
                                        self.connection.sendall("fail!".encode('utf-8')) 
                        else:
                            print("Disconnect")
                            break
                            
                        time.sleep(0.1)
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
        # [수정] 변수 이름 중복으로 클래스가 덮어씌워지는 문제를 방지했습니다.
        server_socket_instance = ServerSocketClass() 
    except KeyboardInterrupt:
        print("Program force quit")
        
        # [수정] 이 코드에는 부저(buzzer)나 GPIO 설정이 없으므로 깔끔하게 정리만 하고 종료합니다.
        textLcd.lcd_clear()
        sys.exit()