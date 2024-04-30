import argparse
import socket
import sys
import textwrap
import threading

from typing import Any, List

# Constants
DATA_BUFFER_SIZE = 4096
HEX_FILTER = ''.join([(len(repr(chr(i))) == 3) and chr(i) or '.' for i in range(256)])

def hexDump(buffer: Any, lineLength: int=16, printResult: bool=True) -> List[str]:
    '''Generate the hexdump (hexadecimal values and ASCII characters) of a buffer.'''
    if isinstance(buffer, bytes):
        buffer = buffer.decode()
    
    results = []
    for i in range(0, len(buffer), lineLength):
        word = str(buffer[i:i+lineLength])
        printable = word.translate(HEX_FILTER)
        hexa = ' '.join([f'{ord(c):02X}' for c in word])
        hexWidth = lineLength * 3
        results.append(f'{i:04X}    {hexa:<{hexWidth}}    {printable}')
    
    if printResult:
        for line in results:
            print(line)
    return results

def receiveDataFrom(connection: socket.socket, timeout: int) -> bytes:
    '''Store received data.'''
    buffer = b''
    connection.settimeout(timeout)
    try:
        while True:
            data = connection.recv(DATA_BUFFER_SIZE)
            if not data:
                break
            buffer += data
    except Exception as ex:
        print(f'[!] Error receiving data: {ex}')
    return buffer

def manageConnection(client: socket.socket, remoteHost: str, remotePort: int, receiveDataFirst: bool, timeout: int) -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as remote:
        try:
            print(f'[*] Connecting to {remoteHost}:{remotePort}.')
            remote.connect((remoteHost, remotePort))
        except Exception as ex:
            print(f'[!] Unable to connect to {remoteHost}:{remotePort}.')
            print(f'[!] Error: {ex}.')
            sys.exit()

        localBuffer = b''
        while True:
            if not receiveDataFirst:
                localBuffer = receiveDataFrom(client, timeout)
                bufferSize = len(localBuffer)
                if bufferSize:
                    print('[==>] Received data from client.')
                    hexDump(localBuffer)
                    print(f'[==>] Sending {bufferSize} bytes to {remoteHost}:{remotePort}.')
                    remote.send(localBuffer)
                    print('[==>] Completed.')

            remoteBuffer = receiveDataFrom(remote, timeout)
            bufferSize = len(remoteBuffer)
            if bufferSize:
                print(f'[<==] Received data from {remoteHost}:{remotePort}.')
                hexDump(remoteBuffer)
                print(f'[<==] Sending {bufferSize} bytes to client.')
                client.send(remoteBuffer)
                print('[<==] Completed.')

            if not receiveDataFirst and (not len(localBuffer) or not len(remoteBuffer)):
                print('[*] No more data. Closing connections.')
                client.close()
                break
            receiveDataFirst = False

def setupServer(port: int, remoteHost: str, remotePort: int, receiveDataFirst: bool, timeout: int) -> None:
    '''Setup server: listen to incoming connection.'''
    ip = socket.gethostbyname(socket.gethostname())
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        try:
            server.bind((ip, port))
        except Exception as ex:
            print(f'[!] Unable to setup proxy on {ip}:{port}.')
            print(f'[!] Error: {ex}.')
            sys.exit()
        print(f'[*] Listening on {ip}:{port}')
        server.listen(5)
        while True:
            try:
                client, address = server.accept()
                print(f'[*] Accepted connection from {address[0]}:{address[1]}')
                clientThread = threading.Thread(target=manageConnection, args=(client, remoteHost, remotePort, receiveDataFirst, timeout))
                clientThread.start()
            except KeyboardInterrupt:
                print(f'[!] Listening on {ip}:{port} terminated.')
                sys.exit()

parser = argparse.ArgumentParser(prog='TCPProxy', 
                                 description='Forward TCP traffic from localhost to target.',
                                 formatter_class=argparse.RawDescriptionHelpFormatter,
                                 epilog=textwrap.dedent('''Examples:
    TCPProxy 5555 192.168.1.10 5555
    TCPProxy 21 ftp.sun.ac.za 21 --receiveFirst --timeout 10
                                 '''))
parser.add_argument('port', type=int, help='The port number to redirect.')
parser.add_argument('targetHost', type=str, help='The IPv4 address or hostname to redirect to.')
parser.add_argument('targetPort', type=int, help='The port number to redirect to.')
parser.add_argument('-r', '--receiveFirst', action='store_true', default=False, help='Receive data first when connection is established.')
parser.add_argument('-t', '--timeout', type=int, default=5, help='Connection time-out in seconds.')

args = parser.parse_args()

setupServer(args.port, args.targetHost, args.targetPort, args.receiveFirst, args.timeout)
