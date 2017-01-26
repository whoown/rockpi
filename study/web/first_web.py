# from _socket import AF_INET
# import socket
#
# HOST, PORT = '', 8787
#
# listen_socket = socket.socket(AF_INET, socket.SOCK_STREAM)
# listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# listen_socket.bind((HOST, PORT))
# listen_socket.listen(1)
# print 'Servering Http on port %s. ' % PORT
#
# while True:
#     client_conn, client_addr = listen_socket.accept()
#     request = client_conn.recv(1024)
#     print 'request is ', request
#     http_resp = """\
# HTTP/1.1 200 OK
#
# Hello, World~
# """
#     client_conn.sendall(http_resp)
#     client_conn.close()

