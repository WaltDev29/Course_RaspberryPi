import socket
import sys
import threading
import time

# 채팅을 위한 서버 소켓 클래스
class ServerSocketClass():
    
    def __init__(self):
        while True:
            try:
                # TCP/IP 서버 소켓을 생성한다
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                
                # 서버의 IP와 포트를 설정한다 (같은 네트워크에 있어야 한다)
                server_address = ('', 10000)
                
                # 서버가 시작시 메세지가 출력된다.
                print("The Server is waiting. IP: {0} PORT: {1}".format(server_address[0], server_address[1]))
                
                # 서버 IP와 포트 번호를 고정한다
                self.sock.bind(server_address)
                
                # 클라이언트의 연결을 받을 수 있는 상태를 시작한다
                self.sock.listen(1)
                
                # 클라이언트 대기 메세지를 출력한다
                print("Waiting for Client access..")
                
                # 클라이언트의 접속을 수용하고, 클라이언트로부터 소켓과 클라이언트 주소를 반환 받는다.
                self.connection, client_address = self.sock.accept()
                
                # 메시지 전송 스레드 시작
                send = messageSendThread(self.connection)
                send.start()

                try:
                    # 접속 위치를 알린다
                    print("Connection from", client_address)
                    
                    # 연결로부터 데이터를 읽는다 (수신 대기)
                    while True:
                        data = self.connection.recv(4096)
                        print("\n")
                        if data:
                            print("[Client]: " + data.decode("utf-8"))
                        else:
                            print("Disconnect..from ", client_address)
                            break
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


# 서버로 메세지를 보낸다
# 클라이언트의 메세지 샌드 스레드와 거의 유사하다
class messageSendThread(threading.Thread):
    
    def __init__(self, connection):
        threading.Thread.__init__(self)
        self.connection = connection
        
    def run(self):
        try:
            while True:
                # 변수 message에 보낼 메세지를 적는다. 
                # input을 통해 사용자로부터 데이터를 받는다
                message = input()
                
                # input을 통해 받은 message를 byte로 변환하여 저장한다
                message = message.encode('utf-8')
                
                # send 함수를 통해 소켓에 message를 인자로 넣어 클라이언트로 메세지를 보낸다
                self.connection.sendall(message)
                print("\n")
        except Exception as err:
            print(err)


# 프로그램의 메인에 해당하는 최상위 구문
if (__name__ == '__main__'):
    try:
        server_socket_instance = ServerSocketClass()  # 클래스 인스턴스 생성
    except KeyboardInterrupt:
        print("Program force quit")
        sys.exit()