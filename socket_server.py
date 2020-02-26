# Server
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('10.10.11.62', 1024))
s.listen(1)
conn, addr = s.accept()
while 1:
    data = conn.recv(1024)
    print (data)
    if not data:
        break
    conn.sendall(data)
conn.close()
