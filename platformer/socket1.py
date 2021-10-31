import socket

client = socket.socket(socket.AF_INET, socket.SOCKET)
client.connect(('www.python.org',80))

#msg = 'hello'
#client.send(msg.encode())

client.send('GET /index.html HTTP/1.0\n\n')
client.recv(1024)

client.close()
