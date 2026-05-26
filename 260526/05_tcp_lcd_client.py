import socket
import sys
import threading
import time
from socket import error as socket_error

# 채팅을 위한 클라이언트 소켓 클래스
# 포트는 10000 이다
class ClientSocketClass():
    
    def __init__(self):
        while True:
            try:
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                # [수정] 웹 특수문자 따옴표(“)를 표준 따옴표(")로 수정했습니다.
                server_address = ("127.0.0.1", 10000)
                
                print("This is Client. connecting IP: {0} PORT: {1}".format(server_address[0], server_address[1]))
                self.sock.connect(server_address)
                
                # 메시지 전송 스레드 시작
                send = messageSendThread(self.sock)
                send.start()
                
                while True:
                    # 아래는 서버에 접속할시 처리할 동작을 기술한다
                    data = self.sock.recv(4096)
                    if data:
                        print("\n")
                        print("[Server]: " + data.decode("utf-8"))
                    else:
                        print("Disconnect")
                        break
                        
            except socket_error as serr:
                print(serr)
                time.sleep(3)
            except Exception as err:
                print(err)
            finally:
                print("Closing socket")
                # 접속을 종료한다
                self.sock.close()


class messageSendThread(threading.Thread):
    
    def __init__(self, sock):
        threading.Thread.__init__(self)
        self.sock = sock
        
    def run(self):
        print("==== Send Message. ex)'textlcd,1,Hello World!' ====")
        try:
            while True:
                # 변수 message에 보낼 메세지를 적는다. 
                # input을 통해 사용자로부터 데이터를 받는다.
                message = input("Send Message >> ")
                
                # input을 통해 받은 message를 byte로 변환하여 저장한다
                message = message.encode('utf-8')
                
                # send 함수를 통해 소켓에 message를 인자로 넣어 서버로 메세지를 보낸다
                self.sock.sendall(message)
                print("\n")
        except Exception as err:
            print(err)


# 프로그램의 메인에 해당하는 최상위 구문
if (__name__ == '__main__'):
    try:
        # [수정] 변수명과 클래스명이 겹치는 문제를 방지하기 위해 변수명을 수정했습니다.
        client_socket_instance = ClientSocketClass() 
    except KeyboardInterrupt:
        print("Program force quit")
        sys.exit()