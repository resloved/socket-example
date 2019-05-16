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
                s.connect((HOST, PORT))
            except socket.error:
                sys.exit('error: connection could not be made')
            try:
                s.send(DATA)
            except socket.error:
                sys.exit('error: data could not reach the server')
            try:
                recv = s.recv(4096)
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
        s.bind(('', PORT))
        s.listen(1)
        try:
            while True:
                conn, addr = s.accept()
                with conn:
                    print(addr[0], 'has connected')
                    recv = conn.recv(1024)
                    try:
                        conn.send(str(float(recv) * 2).encode())
                    except ValueError:
                        conn.send(b'error: input must be a number')
        except KeyboardInterrupt:
            print('Closing Server')
