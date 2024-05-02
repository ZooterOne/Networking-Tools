# Networking

Collection of Python scripts for networking.
Based on the book [Black Hat Python](https://nostarch.com/black-hat-python2E).

![LANGUAGE](https://img.shields.io/badge/python-royalblue?style=for-the-badge&logo=python&logoColor=white)
![EDITOR](https://img.shields.io/badge/vscode-coral?style=for-the-badge&logo=visual-studio-code&logoColor=white)
![OS](https://img.shields.io/badge/linux-yellowgreen?style=for-the-badge&logo=linux&logoColor=white)

<br>

## TCPServer

Start a server and receive data using TCP protocol.

```
TCPServer <port> [--all] [--max <n>]
```

&nbsp;&nbsp;&nbsp;&nbsp;_port: The port number._

&nbsp;&nbsp;&nbsp;&nbsp;_--all: Use all network interfaces._

&nbsp;&nbsp;&nbsp;&nbsp;_--max: Maximum simultaneous connections._

__Example:__

&nbsp;&nbsp;TCPServer 5555 --max 3

&nbsp;&nbsp;&nbsp;&nbsp;_Start a server on port 5555 with a maximum of 3 simultaneous connections._

<br>

## TCPClient

Send data to host using TCP protocol.

```
TCPClient <ip> <port> <data>
```

&nbsp;&nbsp;&nbsp;&nbsp;_ip: The IPv4 address to send the data to._

&nbsp;&nbsp;&nbsp;&nbsp;_port: The port number to send the data to._

&nbsp;&nbsp;&nbsp;&nbsp;_data: The data to send._

__Example:__

&nbsp;&nbsp;TCPClient 192.168.1.1 5555 "Hello there!"

&nbsp;&nbsp;&nbsp;&nbsp;_Send 'Hello there!' to the server at 192.168.1.1 on port 5555._

<br>

## Netcat

Netcat utility for networking.

```
Netcat [--target <ip>] [--port <port>] [--command] [--execute <command>] [--listen]
```

&nbsp;&nbsp;&nbsp;&nbsp;_--target: The IPv4 address to connect to._

&nbsp;&nbsp;&nbsp;&nbsp;_--port: The port number to open or connect to._

&nbsp;&nbsp;&nbsp;&nbsp;_--command: Run a command shell._

&nbsp;&nbsp;&nbsp;&nbsp;_--execute: Execute a command._

&nbsp;&nbsp;&nbsp;&nbsp;_--listen: Listen to incoming connections._

__Examples:__

&nbsp;&nbsp;Netcat -p 5555 -l

&nbsp;&nbsp;&nbsp;&nbsp;_Listen to incoming connection (Target mode) on port 5555._

&nbsp;&nbsp;Netcat -t 192.168.1.10 -p 5555 -e="cat /etc/password"

&nbsp;&nbsp;&nbsp;&nbsp;_Execute the command 'cat /etc/password' and send the result to the target at 192.168.1.10 on port 5555._

&nbsp;&nbsp;Netcat -t 192.168.1.10 -p 5555 -c

&nbsp;&nbsp;&nbsp;&nbsp;_Run a shell prompt and connect to the target at 192.168.1.10 on port 5555 to send the results to._

<br>

## TCPProxy

Forward TCP traffic from localhost to target.

```
TCPProxy <port> <target-host> <target-port> [--receiveFirst] [--timeout <seconds>]
```

&nbsp;&nbsp;&nbsp;&nbsp;_port: The port number to redirect._

&nbsp;&nbsp;&nbsp;&nbsp;_target-host: The IPv4 address or hostname to redirect to._

&nbsp;&nbsp;&nbsp;&nbsp;_target-port: The port number to redirect to._

&nbsp;&nbsp;&nbsp;&nbsp;_--receiveFirst: Receive data first when connection is established._

&nbsp;&nbsp;&nbsp;&nbsp;_--timeout: Connection time-out in seconds._

__Examples:__

&nbsp;&nbsp;TCPProxy 21 ftp.sun.ac.za 21 --receiveFirst --timeout 10

&nbsp;&nbsp;&nbsp;&nbsp;_Redirect connection on port 21 to ftp server._
