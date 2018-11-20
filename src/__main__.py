from src.protocol.iec101 import IEC101
from src.server.tornado import TCPServer

if __name__ == '__main__':
    print("Server start ......")
    server = TCPServer()
    server.protocol = IEC101
    server.run_forever(8000)
