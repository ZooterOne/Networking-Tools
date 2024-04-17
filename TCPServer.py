import argparse
import socket
import threading
import sys

def handleClientConnection(client: socket.socket) -> None:
    '''Handle connection with client.'''
    with client:
        response = client.recv(4096)
        print(f'[*] Received: {response.decode()}')
        client.send(b'ACK')

parser = argparse.ArgumentParser(prog='TCPServer', 
                                 description='Start a server and receive data using TCP protocol.',
                                 epilog='Example: TCPServer 9998 --max 5')
parser.add_argument('port', type=int, help='The port number.')
parser.add_argument('--all', action='store_true', default=False, help='Use all network interfaces.')
parser.add_argument('--max', type=int, default=5, help='Maximum simultaneous connections.')

args = parser.parse_args()

ip = '0.0.0.0' if args.all else socket.gethostbyname(socket.gethostname())

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    try:
        server.bind((ip, args.port))
    except OSError as msg:
        print(f'[!] Unable to setup {ip}:{args.port}.')
        print(f'[!] Error: {msg}.')
        sys.exit()
    print(f'[*] Listening on {ip}:{args.port}')
    server.listen(args.max)
    while True:
        try:
            client, address = server.accept()
            print(f'[*] Accepted connection from {address[0]}:{address[1]}')
            clientThread = threading.Thread(target=handleClientConnection, args=(client,))
            clientThread.start()
        except KeyboardInterrupt:
            print(f'[!] Listening on {ip}:{args.port} terminated.')
