# 서버
import socket
import sys

# TCP/IP 서버 소켓을 생성한다
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# 서버의 IP와 포트를 설정한다
server_address = ("", 10000)

# 서버가 시작시 메세지가 출력된다.
print("The Server is waiting. IP: {0} PORT: {1}".format(server_address[0], server_address[1]))

# 서버 IP와 포트 번호를 고정한다
sock.bind(server_address)
sock.listen(1)
print("Waiting for Client access")

# 클라이언트의 접속을 수용하고, 클라이언트로부터 소켓과 클라이언트 주소를 반환 받는다.
connection, client_address = sock.accept()

try:
    # 접속 위치를 알린다
    print("Connection from", client_address)
    
    # 연결로부터 데이터를 읽는다
    while True:
        data = connection.recv(16)
        print("From Client message : " + data.decode("utf-8"))
        
        if data:
            # 읽어온 데이터를 반송한다 (echo)
            connection.sendall(data)
        else:
            print("no data", client_address)
            break
            
finally:
    print("Closing socket")
    # 접속을 종료한다
    connection.close()