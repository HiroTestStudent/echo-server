import socket
import sys
import traceback


def server(log_buffer=sys.stderr):

    address = ('127.0.0.1', 10000)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)

    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Question to Vamsi: Is this OK?

    print("making a server on {0}:{1}".format(*address), file=log_buffer)

    sock.bind(address)
    sock.listen(1)

    try:

        print('waiting for a connection', file=log_buffer)
        while True:

            conn, addr = sock.accept()

            try:
                print('connection - {0}:{1}'.format(*addr), file=log_buffer)

                while True:

                    buffer_size = 16 
                    data = conn.recv(buffer_size)
                    print('received "{0}"'.format(data.decode('utf8')))

                    conn.sendall(data)
                    print('sent "{0}"'.format(data.decode('utf8')))                    

                    if len(data) < 16:
                        break

            except Exception as e:
                traceback.print_exc()
                sys.exit(1)
            finally:
           
                print(
                    'echo complete, client connection closed', file=log_buffer
                )

                conn.close()
                sys.exit(0) # Question to Vamsi: Is this OK?

    except KeyboardInterrupt:

        conn.close() # Question to Vamsi: Is this OK?
        sock.close()
        print('quitting echo server', file=log_buffer)
        sys.exit(0) # Question to Vamsi: Is this OK?


if __name__ == '__main__':
    server()
    sys.exit(0)
