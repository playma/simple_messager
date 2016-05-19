import socket
import threading
import sys
import os
import logging

exit = 0
filename = ""

def handle_send():
    while True:
        content = input()
        
        msg = content.encode('ascii')
        if exit == 1:
            break;
        else:
            client.send(msg)
            if content[:8] == "sendfile": 
                command = content[9:]
                cmd_split = command.split(" ", 1)
                if(len(cmd_split)==2):
                    global filename
                    filename = cmd_split[1]


def handle_receive():
    while True:
        response = client.recv(4096)
        re = response.decode('ascii')
        print(re)

        if re == "password:":
            os.system("stty -echo")
            response = client.recv(4096)
            re = response.decode('ascii')
            print(re)
            if re == "Wrong password!":
                os.system("stty echo")
            elif re == "Login sucess !":
                os.system("stty echo")
            else:
                os.system("stty echo")

        elif re == "### Agree to transmite file.":
            global filename
            print(filename)
            f = open(filename,'rb')
            l = f.read(1024)
            maxval = 100
                
            while (l):
                client.send(l)
                l = f.read(1024)

            f.close()
            print("end of file transmission")

        elif re[0:15] == "### Denied from":
            filename = ""

        elif re == "### Start to transimate file.":
            file = open('myTransfer', 'wb')
            #while True:
            data = client.recv(4096)
            if data:
                print(data)
                file.write(data)
                #else:
                file.close()
                print("finished.")
                    #break

        elif re=="### Goodbye !":
            global exit
            exit = 1
            print("exit")
            break;


server_host = "127.0.0.1"
server_port = 5555

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
client.connect((server_host, server_port))

exit = 0
   
send_handler = threading.Thread(target=handle_send, args=())
send_handler.start()

receive_handler = threading.Thread(target=handle_receive, args=())
receive_handler.start()


while True:
    if exit == 1:
        sys.exit()
