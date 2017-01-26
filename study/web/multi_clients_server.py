import os
import socket
import time
import signal
import errno

SERVER_ADDR = (HOST, POST) = '', 8888
BACKLOG = 5;

def handle_reqeuest(client_conn):
    req = client_conn.recv(1024)
    print(
        'Child PID: {pid}, Parent PID {ppid}'.format(pid=os.getpid(), ppid=os.getppid())
    )
    print(req.decode())

    resp = b"""\
    HTTP/1.1 200 OK

    viva la vida.
    """

    client_conn.sendall(resp)
    time.sleep(5)

def server_forever():
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind(SERVER_ADDR)
    server_sock.listen(BACKLOG)

    print("Server running: Server PID = {pid}\n".format(pid=os.getpid()))

    def grim_reaper(signum, frame):  # 不能够很好处理大量子进程同时关闭时的极限状况
        pid, status = os.wait()
        print("Child {pid} terminated with status {status}.".format(pid=pid, status=status))

    def grim_reaper(signum, frame):  # 等待所有Zombie子进程处理完成
        while True:
            try:
                pid, status = os.waitpid(-1, os.WHOHANG)  # system call
            except OSError:
                return
        if pid == 0:  # no more zombies.
            return

    # 你需要监听系统发出的子进程关闭信号，注册一个callback
    signal.signal(signal.SIGCHLD, grim_reaper)
    while True:
        try:
            client_conn, client_addr = server_sock.accept()
        except IOError as e:
            code, msg = e.args
            # 是否由于处理Child进程关闭，而导致accept被中断
            if code == errno.EINTR:
                continue  # 继续运行
            else:
                raise

        pid = os.fork()
        if pid == 0:  # child process
            server_sock.close()  # 关掉对你而言多余的File Descriptor
            handle_reqeuest(client_conn)
            client_conn.close()
            os._exit(0)
        else:
            client_conn.close()  # 必须关闭，否则导致Server挂起


if __name__ == '__main__':
    server_forever()
