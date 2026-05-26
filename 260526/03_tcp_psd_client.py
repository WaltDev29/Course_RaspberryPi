import socket
import sys
import threading
import time
from socket import error as socket_error

class ClientSocketClass():
    
    def __init__(self):
        while True:
            try:
                # 소켓을 생성한다
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                
                # 서버의 IP와 포트를 설정한다
                server_address = ("127.0.0.1", 10000) # 본인 장비 IP 입력
                
                # 현재 접속할 서버의 IP와 포트를 콘솔로 출력한다.
                print("This is Client. connecting IP: {0} PORT: {1}".format(server_address[0], server_address[1]))
                
                # 서버로 접속을 시도한다
                self.sock.connect(server_address)
                
                while True:
                    # 아래는 서버에 접속할시 처리할 동작을 기술한다
                    data = self.sock.recv(4096)
                    if data:
                        msgStr = data.decode("utf-8")
                        removeLf = msgStr.split('\n')[0]
                        msg = removeLf.split(',')
                        
                        if len(msg) == 2:
                            if msg[0] == "PSD":
                                print("RECEIVE Message >> [Sensor]:{} [Value]:{}cm".format(msg[0], msg[1]))
                    else:
                        print("Disconnect")
                        break
                        
            # 서버가 열려 있지 않을시 3초 동안 대기한다
            except socket_error as serr:
                print(serr)
                time.sleep(3)
            except Exception as err:
                print(err)
            finally:
                try:
                    self.sock.close()
                    print("Closing socket")
                except Exception as sockerr:
                    pass


# 프로그램의 메인에 해당하는 최상위 구문
if (__name__ == '__main__'):
    try: 
        # 클래스 인스턴스를 생성한다
        client_socket_instance = ClientSocketClass()
    except KeyboardInterrupt:
        print("Program force quit")
        sys.exit()