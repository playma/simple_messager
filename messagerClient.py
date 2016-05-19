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
        response = client.recv(1024)
        re = response.decode('ascii')
        print(re)

        if re == "password:":
            os.system("stty -echo")
            response = client.recv(1024)
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
            
            fileSize = os.path.getsize(filename)
            print ("filesize: " + str(fileSize))
            f = open(filename,'rb')
            l = f.read(1024)
            i = 0
            print("0% of " + filename + " transmitted....\r", end="")
            while (l):
                client.send(l)
                l = f.read(1024)
                i = i + 1
                percent = 1024*i / fileSize * 100
                if 1024*i > fileSize: 
                    percent = 100
                print( str(percent) + "% of filename transmitted....\r", end="")
            print( "100% of filename transmitted....")
            f.close()
            stop = "EOF"
            stop = stop.encode('ascii')
            client.send(stop)
            print("end of file transmission")

        elif re[0:15] == "### Denied from":
            filename = ""

        elif re == "### Start to transimate file.":
            file = open('myTransfer', 'wb')
            while True:
                ##print("in loop")
                data = client.recv(1024)
                msg = data.decode('ascii')
                ##print("client receiveve: " + msg)
                if msg == "EOF":  
                    print("match eof")
                    break;
                print("writefile")

                file.write(data)
            
            file.flush()  
            file.close() 
            print("download finished") 


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
