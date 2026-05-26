import socket
import sys
import threading
import time
from socket import error as socket_error
import smbus
import math

# smbus 모듈을 통해 i2c 모듈에 연결된 AD 모듈을 읽어온다
bus = smbus.SMBus(1)
# 연결된 i2c 모듈의 채널은 0x48이다
i2c_address = 0x48
# PCF8591 칩에서 데이터를 받기위한 명령어다
command = 0x44


# 통신을 위한 서버 소켓 클래스
class ServerSocketClass():
 
    def __init__(self):
        while True:
            try:
                # TCP/IP 서버 소켓을 생성한다
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                
                # 서버의 IP와 포트를 설정한다 (같은 네트워크에 있어야 한다)
                server_address = ('', 10000)
                
                # 서버가 시작시 메세지가 출력된다
                print("The Server is waiting. IP: {0} PORT: {1}".format(server_address[0], server_address[1]))
                
                # 서버 IP와 포트 번호를 고정한다
                self.sock.bind(server_address)
                
                # 클라이언트의 연결을 받을 수 있는 상태를 시작한다
                self.sock.listen(1)
                
                # 클라이언트 대기 메세지를 출력한다
                print("Waiting for Client access..")
                
                # 클라이언트의 접속을 수용하고, 클라이언트로부터 소켓과 클라이언트 주소를 반환 받는다
                self.connection, client_address = self.sock.accept()
                
                # 데이터 전송 스레드 시작
                send = messageSendThread(self.connection)
                send.start()
                
                try:
                    # 접속 위치를 알린다
                    print("Connection from", client_address)
                    
                    # 연결로부터 데이터를 읽는다
                    while True:
                        data = self.connection.recv(4096)
                        # 읽어온 데이터가 존재할시 처리
                        if data:
                            print("\n")
                            print("[Client]: " + data.decode("utf-8"))
                        else:
                            print("Disconnect..from ", client_address)
                            break
                            
                except Exception as err:
                    print(err)
                finally:
                    # 클라이언트 접속을 종료한다
                    self.connection.close()
                    
            except Exception as err:
                print(err)
            finally:
                print("Closing socket END Programs")
                self.sock.close()


# 클라이언트로 메세지를 보낸다 (PSD 센서 데이터 송신)
class messageSendThread(threading.Thread):
    
    def __init__(self, sock):
        threading.Thread.__init__(self)
        self.sock = sock
        
    def run(self):
        try:
            while True:
                # I2C 통신으로 데이터 수신 (명령어 0x44로부터 5바이트 읽기)
                adc_data = bus.read_i2c_block_data(i2c_address, command, 5)
                
                # PSD 거리 센서의 전압 값을 거리(cm) 단위로 계산하는 공식
                psd_value = (adc_data[4] / 255.0 * 3.3) * 3 / 2
                psd_value = 29.988 * math.pow(psd_value, -1.173)
                psd_value = round(psd_value, 2)
                
                # 변수 message에 보낼 메세지를 적는다. 
                message = "PSD,{}".format(psd_value)
                print("Send Message >> " + message) 
                
                # 개행 문자(LF)를 붙여준다
                message += "\n"
                
                # 메세지를 byte로 변환하여 저장한다
                message = message.encode('utf-8')
                
                # send 함수를 통해 소켓에 message를 인자로 넣어 클라이언트로 메세지를 보낸다
                self.sock.sendall(message)
                time.sleep(0.3)
                
        except Exception as err:
            print(err)


# 프로그램의 메인에 해당하는 최상위 구문
if (__name__ == '__main__'):
    try:
        server_socket_instance = ServerSocketClass()  # 클래스 인스턴스 생성
    except KeyboardInterrupt:
        print("Program force quit")
        sys.exit()