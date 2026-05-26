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
                server_address = ("127.0.0.1", 10000)
                
                print("This is Client. connecting IP: {0} PORT: {1}".format(server_address[0], server_address[1]))
                self.sock.connect(server_address)
                
                # 메시지 전송 스레드 시작
                send = messageSendThread(self.sock)
                send.start()
                
                # 서버로부터 메시지 수신 대기
                while True:
                    data = self.sock.recv(4096)
                    if data:
                        print("\n")
                        print("[Server]: " + data.decode("utf-8"))
                    else:
                        print("Disconnect")
                        break
                        
            # 서버가 열려 있지 않을 시 3초 동안 대기한다
            except socket_error as serr:
                print(serr)
                time.sleep(3)
            except Exception as err:
                print(err)
            finally:
                print("Closing socket")
                # 접속을 종료한다
                self.sock.close()


# 서버로 메세지를 보낸다
# 클라이언트의 메세지 샌드 스레드와 거의 유사하다
class messageSendThread(threading.Thread):
    
    def __init__(self, sock):
        threading.Thread.__init__(self)
        self.sock = sock
        
    def run(self):
        try:
            while True:
                # 변수 message에 보낼 메세지를 적는다. 
                # input을 통해 사용자로부터 데이터를 받는다.
                message = input()
                
                # input을 통해 받은 message를 byte로 변환하여 저장한다.
                message = message.encode('utf-8')
                
                # send 함수를 통해 소켓에 message를 인자로 넣어 서버로 메세지를 보낸다.
                self.sock.sendall(message)
                print("\n")
        except Exception as err:
            print(err)


# 프로그램의 메인에 해당하는 최상위 구문
if (__name__ == '__main__'):
    try:
        client_socket_instance = ClientSocketClass() # 클래스 인스턴스 생성
    except KeyboardInterrupt:
        print("Program force quit")
        sys.exit()