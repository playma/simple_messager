import socket
import threading
import time
import datetime

bind_ip = "127.0.0.1"
bind_port = 5555

users = ["playma", "scott", "pei"]
passwords = ["playma", "scott", "pei"]

friendList = []
msgbox = []
filebox = []
connection = []

for i in range(len(users)):
    temp = []
    msgbox.append(temp)

for i in range(len(users)):
    temp = []
    friendList.append(temp)

for i in range(len(users)):
    temp = []
    filebox.append(temp)


login_status = [0,0,0]
login_ip = ["127.0.0.1","127.0.0.1","127.0.0.1"]
login_port = [bind_port,bind_port,bind_port]

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
server.bind((bind_ip, bind_port))

server.listen(55555)

print("[*] Listening on "+ bind_ip +":" + str(bind_port))
print("[*] check user uid0 addr:"+ login_ip[0] +":" + str(login_port[0]))
print("[*] check user uid1 addr:"+ login_ip[1] +":" + str(login_port[1]))
print("[*] check user uid2 addr:"+ login_ip[2] +":" + str(login_port[2]))


def getUidByName(name):
    for i in range(len(users)):
        if name == users[i]:
            uid = i
            return uid
    return -1

def getFriendListByUid(uid):
    return friendList[uid]

def clientSocketMsg(client_socket, content):
    msg = content.encode('ascii')
    client_socket.send(msg)

def sendMsg(uid, friendUid, content):
    print("send msg")

def isfriend(uid, friendUid):
    if friendUid in friendList[uid]:
        return 1
    else:
        return 0

def isOnline(uid):
    if login_status[uid] == 1:
        return 1
    else:
        return 0

def addFriendByUid(uid, friendUid):
    friendList[uid].append(friendUid)
    friendList[friendUid].append(uid)

def removeFriendByUid(uid, friendUid):
    friendList[uid].remove(friendUid)
    friendList[friendUid].remove(uid)   

def handle_client(client_socket, client_ip, client_port):
    login_check = 0
    conversation_lock = 0;

    while login_check != 1:
        content = "### Login: "
        msg = content.encode('ascii') 
        client_socket.send(msg)
        
        response = client_socket.recv(1024)
        re = response.decode('ascii')
        username = re
        print("### login: " + re)

        uid = getUidByName(re)
        
        if(uid != -1):
            content = "### password: "
            msg = content.encode('ascii')
            client_socket.send(msg)
   
            response = client_socket.recv(1024)
            re = response.decode('ascii')

            if re == passwords[uid]:
                login_check = 1
                content = "### Login success!"
                msg = content.encode('ascii')
                client_socket.send(msg)

                login_status[uid] = 1
                login_ip[uid] = client_ip
                login_port[uid] = client_port

                print("### user " + users[uid] + " login success!")
                clientSocketMsg(client_socket, "### Welcome " + username )
                client_listener = threading.Thread(target=handle_listen, args=(client_socket, uid))
                client_listener.start()
            else:
                # wrong password
                login_check = 3
                content = "### Wrong passowrd!"
                msg = content.encode('ascii')
                client_socket.send(msg)
        else:
            # user not exist
            login_check = 2
            content = "### User not exist!"
            msg = content.encode('ascii')
            client_socket.send(msg)
            
 
    # Logined
    
    while True:
        response = client_socket.recv(4096)
        re = response.decode('ascii')
        #print("# Received: " + re)

        if re == "friend list":

            print("# " + username +  "\tshow friend list.")
            #friendList = getFriendListByUid(uid)
            print(friendList)
            if not friendList[uid]:
                clientSocketMsg(client_socket, "### Sorry, you don't have any friend!")
                print("# return no any friend")
            else:
                clientSocketMsg(client_socket, "### Your friend list.")
                content = ""
                for friendUid in friendList[uid]:
                    content += "\n### " + users[friendUid] + "\t"
                    content += 'online' if login_status[friendUid]==1 else 'offline'
                clientSocketMsg(client_socket, content)

        elif re[0:10] == "friend add":
            print("# " + username +  "\tadd friend.")
            friendName = re[11:]
            friendUid = getUidByName(friendName)
            
            if(friendUid != -1) and isfriend(uid, friendUid)==0:
                addFriendByUid(uid, friendUid)
                clientSocketMsg(client_socket, "### " + friendName + " added into the friend list.")
                print("# " + username + " added friend " + friendName + " successfully.")
            else:
                clientSocketMsg(client_socket, "### Add friend " + friendName + " failed")
                print("# " + username +  " added friend " + friendName + " failed")
        elif re[0:9] == "friend rm":
            friendName = re[10:]
            friendUid = getUidByName(friendName)
    
            if(friendUid != -1) and isfriend(uid, friendUid)==1:
                removeFriendByUid(uid, friendUid)
                clientSocketMsg(client_socket, "### " + friendName + " removed from the friend list.")
                print("# " + username + " removed friend " + friendName + " successfully.")
            else:
                clientSocketMsg(client_socket, "### Removed friend " + friendName + " failed, not found this user.")
                print("# " + username +  " removed friend " + friendName + " failed, not found user.")
        
        elif re[0:8] == "sendfile":
            command = re[9:]
            cmd_split = command.split(" ", 1)

            if(len(cmd_split)==2):
                friendName = cmd_split[0]
                fileName = cmd_split[1]
                friendUid = getUidByName(friendName)

                if(friendUid != -1):
                    if isfriend(uid, friendUid) == 1:
                        if isOnline(friendUid) == 1:
                            #conversation_lock = 1
                            print("# user " + username +  " send file to with " + friendName + ".")
                            clientSocketMsg(client_socket, "### Send file to " + friendName + ".")
                            clientSocketMsg(client_socket, "##############################################")
                            currentTime = str(datetime.datetime.now())
                            msgbox[friendUid].append([currentTime, uid, "I want to send file to you.(storefile/deny)"])
                            
                            flag = 0
                            while True:
                                print("in while loop")
                                
                                if flag == 1:
                                    print("break2")
                                    break;
                                if msgbox[uid]:               
                                    for msg in msgbox[uid]:
                                        print("in for loop")

                                        if msg[1]==friendUid:
                                            if msg[2] == "storefile":
                                                clientSocketMsg(client_socket,  "### Agree to transmite file.")
                                                
                                                while True:
                                                    data = client_socket.recv(1024)
                                                    if data:
                                                        data = data.decode('ascii')
                                                        print(data)
                                                        filebox[friendUid].append(data)
                                                        #client_socket.send(data)
                                                    else:
                                                        break;
                                                flag = 1
                                                #msgbox[uid].pop(0)
                                            elif msg[2] == "deny":
                                                #msgbox[uid].pop(0)
                                                clientSocketMsg(client_socket,  "### Denied from " + users[friendUid])                         
                                                flag = 1
                                                break;

                                                
                        else:
                            clientSocketMsg(client_socket, "### Send file to " + friendName + " failed, " + friendName + " is Offline.")
                            print("# " + username +  " send file to " + friendName + " failed, " + friendName + " is Offline.")
                    else:
                        clientSocketMsg(client_socket, "### Send file to " + friendName + " failed, " + friendName + " is not your friend.")
                        print("# " + username +  " send file to " + friendName + " failed, " + friendName + " is not your friend.")
                else:
                    clientSocketMsg(client_socket, "### Send file to " + friendName + " failed, not found this user.")
                    print("# " + username +  " send file to " + friendName + " failed, not found this user.")

            else:
                clientSocketMsg(client_socket, "### Too few arguments.")
                print("# Too few arguments.")

        elif re[0:4] == "send":
            command = re[5:]
            cmd_split = command.split(" ", 1)
            if(len(cmd_split)==2):
                friendName = cmd_split[0]
                content = cmd_split[1]
                friendUid = getUidByName(friendName)   
                currentTime = str(datetime.datetime.now())
                if(friendUid != -1):
                    if isfriend(uid, friendUid) == 1:
                        msgbox[friendUid].append([currentTime, uid, content])
                        print("# user " + username +  " send\t" + content + "\t to " + friendName)
                    else:
                        clientSocketMsg(client_socket, "### Send msg to " + friendName + " failed, " + friendName + " is not your friend.")
                        print("# " + username +  " send msg to " + friendName + " failed, " + friendName + " is not your friend.")

                else:
                    clientSocketMsg(client_socket, "### Send msg to " + friendName + " failed, not found this user.")
                    print("# " + username +  " send msg to " + friendName + " failed, not found this user.")

                
            else:
                clientSocketMsg(client_socket, "### Too few arguments.")
                print("# Too few arguments.")

        elif re[0:4] == "talk":
            friendName = re[5:]
            friendUid = getUidByName(friendName)
            if(friendUid != -1):
                if isfriend(uid, friendUid) == 1:
                    if isOnline(friendUid) == 1:
                        #conversation_lock = 1

                        print("# user " + username +  " start conversion with " + friendName + ".")
                        clientSocketMsg(client_socket, "### Start conversion with " + friendName + ".")
                        clientSocketMsg(client_socket, "##############################################")
                        while True:
                            response = client_socket.recv(4096)
                            re = response.decode('ascii')
                            if re == "end conversion":
                                print("# user " + username +  " end conversion with " + friendName + ".")
                                clientSocketMsg(client_socket, "### End conversion with " + friendName + ".")
                                break;
                            else:
                                currentTime = str(datetime.datetime.now())
                                content = re
                                msgbox[friendUid].append([currentTime, uid, content])                            
                        
                    else:
                        clientSocketMsg(client_socket, "### Start conversion with " + friendName + " failed, " + friendName + " is Offline.")
                        print("# " + username +  " start conversion with " + friendName + " failed, " + friendName + " is Offline.")
                else:
                    clientSocketMsg(client_socket, "### Start conversion with " + friendName + " failed, " + friendName + " is not your friend.")
                    print("# " + username +  " start conversion with " + friendName + " failed, " + friendName + " is not your friend.")
            else:
                clientSocketMsg(client_socket, "### Start conversion with " + friendName + " failed, not found this user.")
                print("# " + username +  " start conversion with " + friendName + " failed, not found this user.")
            
        elif re == "logout":
            print("# user " + username +  "\tlogout")
            clientSocketMsg(client_socket, "### Goodbye !" )
            #client.socket.close()
            login_status[uid] = 0;
            break;
        else:
            clientSocketMsg(client_socket, "### Opps! Something wrong." )
            print(" Opps! Something wrong.")




                    

def handle_listen(client_socket, uid):
    print("start listen to " + users[uid])
    while True:
        if msgbox[uid]:
            for msg in msgbox[uid]:
                clientSocketMsg(client_socket, "### " + msg[0] + "\tMessage from  " +  users[msg[1]] + "\t" + msg[2])
                msgbox[uid].pop(0)

        if filebox[uid]:
            clientSocketMsg(client_socket, "### Start to transimate file.")
            for block in filebox[uid]:
                clientSocketMsg(client_socket, block)
                filebox[uid].pop(0)



while True:
 
    client_socket, addr = server.accept()
    print("Accept connection from:" + addr[0] + ":" + str(addr[1]))

    client_handler = threading.Thread(target=handle_client, args=(client_socket, addr[0], addr[1]))
    client_handler.start()

