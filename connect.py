#!/usr/bin/env python3
import json
import socket
from OpenSSL import crypto, SSL

cert = json.loads(open("./config/cert.json").read())
network = json.loads(open("./config/network.json").read())

def cert_gen(
    emailAddress=cert['certGen']['emailAddress'],
    commonName=cert['certGen']['commonName'],
    countryName=cert['certGen']['countryName'],
    localityName=cert['certGen']['localityName'],
    stateOrProvinceName=cert['certGen']['stateOrProvinceName'],
    organizationName=cert['certGen']['organizationName'],
    organizationUnitName=cert['certGen']['organizationUnitName'],
    serialNumber=cert['certGen']['serialNumber'],
    validityStartInSeconds=cert['certGen']['validityStartInSeconds'],
    validityEndInSeconds=cert['certGen']['validityEndInSeconds'],
    KEY_FILE = cert['certGen']['KEY_FILE'],
    PUB_FILE = cert['certGen']['PUB_FILE'],
    CERT_FILE= cert['certGen']['CERT_FILE']):
    k = crypto.PKey()
    k.generate_key(crypto.TYPE_RSA, 4096)
    cert = crypto.X509()
    cert.get_subject().C = countryName
    cert.get_subject().ST = stateOrProvinceName
    cert.get_subject().L = localityName
    cert.get_subject().O = organizationName
    cert.get_subject().OU = organizationUnitName
    cert.get_subject().CN = commonName
    cert.get_subject().emailAddress = emailAddress
    cert.set_serial_number(serialNumber)
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(validityEndInSeconds)
    cert.set_issuer(cert.get_subject())
    cert.set_pubkey(k)
    cert.sign(k, 'sha512')
    with open(CERT_FILE, "wt") as f:
        f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert).decode("utf-8"))
    with open(KEY_FILE, "wt") as f:
        f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, k).decode("utf-8"))
    with open(PUB_FILE, "wt") as f:
        f.write(crypto.dump_publickey(crypto.FILETYPE_PEM, k).decode("utf-8"))

def retrieve_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip

def get_broadcast_address():
    ip = retrieve_local_ip()
    ip_split = ip.split('.')[:-1]
    ip_split.append("255")
    return '.'.join(ip_split)

def broadcast(port=network['port']):
    broadcast_ip = get_broadcast_address()
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('', port))
    s.connect((broadcast_ip, port))
    totalSent = 0
    message = "Connect with zookeeper on: " + retrieve_local_ip() + "\n\n"
    msg = bytes(message, "UTF-8")
    while totalSent < len(msg):
        sent = s.send(msg[totalSent:])
        if sent == 0:
            raise RuntimeError("Connection broken")
        totalSent += sent
    s.close()

