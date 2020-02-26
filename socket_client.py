import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('10.10.11.62', 1024))
s.sendall('Hello')
data = s.recv(1024)
s.close()
#print 'Received', repr(data)
