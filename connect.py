#!/usr/bin/env python3
import json
from OpenSSL import crypto, SSL

hostname = ""
port = 000

cert = json.loads(open("./config/cert.json").read())

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

