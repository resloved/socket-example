import argparse, socket, sys

##########################
# default   Server Mode -- localhost:50000
# -m/--mode Select Server or Client mode
# -i/--host IP of Server
# -d/--data Data to be sent
# -p/--port Port of Server
##########################
        
parser = argparse.ArgumentParser(description='Send/Recieve UDP Packet(s) over sockets')
parser.add_argument('-m', '--mode', type=str.lower,
                    help='Choose between client and server modes',
                    choices=['server', 'client'])
parser.add_argument('-i', '--host', type=str, default='localhost',
                    help='Address of server you wish to connect to')
parser.add_argument('-d', '--data', type=str.encode,
                    help='Data that will be sent to the server')
parser.add_argument('-p', '--port', type=int, default=50000,
                    help='Port of UDP server')

args = parser.parse_args()
PORT = args.port

##########################
# Client [HOST] [PORT] [DATA]
##########################

if args.mode == 'client':
    if args.data:
        print('Client Mode')
        HOST = args.host
        DATA = args.data
        print('Sending...')
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.settimeout(5)
            try:
                s.sendto(DATA, (HOST, PORT))
            except socket.error:
                sys.exit('error: data could not reach the server')
            try:
                recv, server = s.recvfrom(4096)
                print(recv.decode("utf-8"))
            except socket.error:
                sys.exit('error: no response from the server')
    else:
        sys.exit('error: client mode requires -d/--data to send data')

##########################
# Server [PORT]
##########################
        
else:
    print('Server Mode')
    print('Listening...')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        try:
            s.bind(('', PORT))
        except socket.error:
            sys.exit('error: port already in use')
        try:
            while True:
                recv, addr = s.recvfrom(1024)
                print(addr[0], 'has connected')
                try:
                    s.sendto(str(float(recv) * 2).encode(), addr)
                except ValueError:
                    s.sendto(b'error: input must be a number', addr)
        except KeyboardInterrupt:
            print('Closing Server')
