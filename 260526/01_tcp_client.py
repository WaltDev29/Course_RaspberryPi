# 클라이언트
import socket
import sys

# 소켓을 생성한다
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 서버의 IP와 포트를 설정한다
server_address = ("127.0.0.1", 10000)  # 상대방 IP 접속

# 현재 접속할 서버의 IP와 포트를 콘솔로 출력한다.
print("This is Client. connecting IP: {0} PORT: {1}".format(server_address[0], server_address[1]))

# 서버로 접속을 시도한다
sock.connect(server_address)

# 아래는 서버에 접속할시 처리할 동작을 기술한다
try:
    # 변수 message에 보낼 메세지를 적는다. 
    # 문자열이지만 앞에 b를 붙이면 바이트 타입으로 변환이 가능하다.
    message = b"Hello Server!"
    
    # 현재 보내는 메세지를 표시하기 위해 print에 적어준다. message를 UTF-8 인코딩으로 해석하여 출력한다.
    print("Send a message to the server : " + message.decode("utf-8"))
    
    # send 함수를 통해 소켓에 message를 인자로 넣어 서버로 메세지를 보낸다
    sock.sendall(message)
    
finally:
    print("Closing socket")
    # 접속을 종료한다
    sock.close()