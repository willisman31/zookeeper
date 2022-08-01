#!/usr/bin/env python3
"""
Actions taken by the server to connect to clients

"""

import sockets

class Server:

    def __init__() --> None:
        self.connections = []
        self.broadcastIP = getBroadcastIP()
        self.port = getPort()

    def getConfigurations() -> None:
        pass

    def getPort() -> int:
        p = open("port.txt")
        port = int(p.read())
        p.close()
        return port

    def listenForBroadcast():
        HOST = ''
        PORT = self.port
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen(1)
            conn, addr = s.accept()
            with conn:
                while True:
                    data = conn.recv(1024)
                    if not data: break
                    conn.sendall(data)

    def getBroadcastIP() -> None:
        hostIP = getHostIP()
        broadcastIP = replaceHostByte(hostIP)
        addConnection("Broadcast", broadcastIP)

    def getHostIP() -> str:
        hostName = socket.gethostname()
        hostIP = socket.gethostbyname(hostName)
        return hostIP

    def replaceHostByte(ipAddress: str) -> str:
        network = ipAddress.rfind(".")
        ipAddress = ipAddress.substring(0,network) + "255"
        return ipAddress
    
    def addConnection(name: str, ip: str) -> None:
        self.connections.append(tuple((name, ip)))

