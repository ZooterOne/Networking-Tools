import argparse
import socket
import sys

parser = argparse.ArgumentParser(prog='TCPClient', 
                                 description='Send data to host using TCP protocol.',
                                 epilog='Example: TCPClient 192.168.1.1 111 "Hello there!"')
parser.add_argument('ip', type=str, help='The IPv4 address to send the data to.')
parser.add_argument('port', type=int, help='The port number to send the data to.')
parser.add_argument('data', type=str, help='The data to send.')

args = parser.parse_args()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
    try:
        print(f'[*] Connecting to {args.ip}:{args.port}.')
        client.connect((args.ip, args.port))
    except OSError as msg:
        print(f'[!] Unable to connect to {args.ip}:{args.port}.')
        print(f'[!] Error: {msg}.')
        sys.exit()
    dataAsBytes = bytes(map(ord, args.data))
    print(f'[*] Sending data.')
    client.send(dataAsBytes)
    response = client.recv(4096)
    print(f'[*] Received response from server: {response.decode()}.')
