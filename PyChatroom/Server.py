
#python 2.7

import select
import socket
import time
import datetime
import random
from threading import Timer
from Config import *
from Database import UserDatabase

class UserInfo:
    def __init__(self):
        self.startTime = None
        self.onlineTime = None
        self.rollValue = -1

class SocketInfo:
    def __init__(self):
        self.username = None
        self.message = None
        self.state = STATE_OFFLINE

class ChatroomServer:
    def __init__(self):
        self.Clients = {}
        self.OnlineUser = {}
        self.Db = UserDatabase(DATABASE_PATH)
        self.InitSocket()
        self.IsGame = False

    def InitSocket(self):
        self.ServerSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.ServerSocket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self.ServerSocket.bind((SERVER_IP,SERVER_PORT))
        self.ServerSocket.listen(MAX_CLIENT_NUM)
        self.SocketList = [self.ServerSocket]

    def Start(self):
        while True:
            print ('Waiting client connect..')
            rx,_,ex = select.select(self.SocketList,[],[])
            for notified_socket in rx:
                if notified_socket == self.ServerSocket:
                    client_socket,client_addr = self.ServerSocket.accept()
                    self.SocketList.append(client_socket)
                    self.Clients[client_socket] = SocketInfo()
                    client_socket.sendall('>>>Successfully connected to server\r\n$')
                    print ('Accepted new connection from {}'.format(*client_addr))
                else:
                    message = self.Readline(notified_socket)
                    if message is False:
                        self.SocketList.remove(notified_socket)
                        self.HandleLogout(notified_socket)
                    elif self.ParseMessage(notified_socket,message) is False:
                            notified_socket.sendall('>>>Command error!\r\n$')

    def Readline(self,client_socket):
        message = ''
        while True:
            try:
                c = client_socket.recv(BUFFER_SIZE)
                if not c:
                    return False
                elif c == '\r\n':
                    return message
                elif c == '\b':
                    if not message:
                        client_socket.sendall('$')
                    else:
                        message = message[:-1]
                        client_socket.sendall('\x20\x08')
                else:
                    message += c
            except:
                return False

    def ParseMessage(self,client_socket,msg):
        msg = msg.strip().split(' ')
        length = len(msg)
        if length == 3 and msg[0] == MSG_LOGIN:
            self.HandleLogin(client_socket,msg[1],msg[2])
        elif length == 3 and msg[0] == MSG_REGISTER:
            self.HandleRegister(client_socket,msg[1],msg[2])
        elif length > 1 and msg[0] == MSG_CHAT:
            message = ' '.join(msg[1:])
            self.HandleChat(client_socket, message)
        elif length == 2 and msg[0] == MSG_INFO:
            self.HandleInfo(client_socket, msg[1])
        elif length == 2 and msg[0] == MSG_ROLLSTART:
            self.HandleGameStart(client_socket,msg[1])
        elif length == 1 and  msg[0] == MSG_LOGOUT:
            self.HandleLogout(client_socket)
        elif length == 1 and msg[0] == MSG_ROLL:
            self.HandleRoll(client_socket)
        else:
            return False
        return True

    def HandleRegister(self,client_socket,name,password):
        state = self.Clients[client_socket].state
        if state == STATE_ONLINE:
            client_socket.sendall('>>>you need to logout\r\n$')
        elif not self.Db.QueryUserName(name):
            register_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.Db.AddUser(name,password,register_time)
            client_socket.sendall('>>>{} has been created successfully!\r\n$'.format(name))
        else:
            client_socket.sendall('>>>{} already exist!\r\n$'.format(name))


    def HandleLogin(self,client_socket,name,password):
        state = self.Clients[client_socket].state
        if name in self.OnlineUser.keys():
            client_socket.sendall('>>>{} logged in!\r\n$'.format(name))
        elif state == STATE_ONLINE:
            client_socket.sendall('>>>you have logged in another user!\r\n$')
        elif not self.Db.QueryUserLogin(name,password):
            client_socket.sendall('>>>login failed!\r\n$')
        else:
            self.OnlineUser[name] = UserInfo()
            self.OnlineUser[name].onlineTime,_,flag = self.Db.GetUserTimeInfo(name)
            self.OnlineUser[name].startTime = time.time()
            self.Clients[client_socket].username = name
            self.Clients[client_socket].message = password
            self.Clients[client_socket].state = STATE_ONLINE
            self.BroadcastMessage('{} login'.format(name),client_socket)

    def HandleLogout(self,client_socket):
        state = self.Clients[client_socket].state
        if state == STATE_OFFLINE:
            client_socket.sendall('>>>you need to login\r\n$')
        else:
            name = self.Clients[client_socket].username
            self.BroadcastMessage('{} logout'.format(name),client_socket)
            self.Clients[client_socket].state = STATE_OFFLINE
            self.Db.UpdateOnlineTime(name,self.GetOnlineTime(name))
            del self.OnlineUser[name]

    def HandleInfo(self,client_socket,name):
        state = self.Clients[client_socket].state
        if state == STATE_OFFLINE:
            client_socket.sendall('>>>you need to login\r\n$')
        elif not self.Db.QueryUserName(name):
            client_socket.sendall('>>>{} does not exist\r\n$'.format(name))
        else:
            if self.OnlineUser.has_key(name):
                self.Db.UpdateOnlineTime(name,self.GetOnlineTime(name))
            onlineTime, createTime, _ = self.Db.GetUserTimeInfo(name)
            client_socket.sendall('>>>{} info:\r\n'.format(name))
            client_socket.sendall('>>>create time: {}\r\n'.format(createTime))
            client_socket.sendall('>>>online time: {}\r\n$'.format(onlineTime))


    def HandleChat(self,client_socket,message):
        state = self.Clients[client_socket].state
        if state == STATE_OFFLINE:
            client_socket.sendall('>>>you need to login\r\n$')
        else:
            name = self.Clients[client_socket].username
            self.BroadcastMessage('{}:{}'.format(name,message),client_socket)

    def HandleGameStart(self,client_socket,inputTime):
        try:
            state = self.Clients[client_socket].state
            if self.IsGame is True:
                client_socket.sendall('>>>The game has started\r\n$')
            elif state == STATE_OFFLINE:
                client_socket.sendall('>>>you need to login\r\n$')
            else:
                gameTime = int(inputTime)
                Timer(gameTime,self.HandleGameOver).start()
                name = self.Clients[client_socket].username
                message = '{} start a roll game (will end in {} sec)'.format(name,gameTime)
                self.IsGame = True
                self.BroadcastMessage(message,client_socket)

        except ValueError:
            client_socket.sendall('>>>Please enter a proper time\r\n$')


    def HandleGameOver(self):
        winners,flag = self.GetWinner()
        if not flag:
            self.BroadcastMessage('No winner')
        else:
            for winner in winners:
                message = '{}({}) win the roll game!'.format(winner[0],winner[1])
                self.BroadcastMessage(message)
        self.IsGame = False
        self.ClearUserRoll()


    def HandleRoll(self,client_socket):
        state = self.Clients[client_socket].state
        if state == STATE_OFFLINE:
            client_socket.sendall('>>>you need to login\r\n$')
        elif self.IsGame:
            name = self.Clients[client_socket].username
            roll = random.randint(1,100)
            self.OnlineUser[name].rollValue = roll
            self.BroadcastMessage('{} roll:{}'.format(name,str(roll)),client_socket)
        else:
            client_socket.sendall('>>>Game not start\r\n$')

    def BroadcastMessage(self,message,client_socket=''):
        for other_socket in self.Clients.keys():
            state = self.Clients[other_socket].state
            if state == STATE_ONLINE:
                if other_socket != client_socket:
                    other_socket.sendall('\r\n>>>{}\r\n$'.format(message))
                else:
                    other_socket.sendall('>>>{}\r\n$'.format(message))

    def GetWinner(self):
        res = [('',0)]
        flag = True
        for name in self.OnlineUser.keys():
            rollValue = self.OnlineUser[name].rollValue
            if rollValue >= res[-1][1]:
                if rollValue != res[-1][1]:
                    res.pop()
                res.append((name,rollValue))
        if res[-1][0] == '':
            flag = False
        return res,flag

    def ClearUserRoll(self):
        for name in self.OnlineUser.keys():
            self.OnlineUser[name].rollValue = -1

    def GetOnlineTime(self,name):
        startTime = self.OnlineUser[name].startTime
        onlineTime,_,_ = self.Db.GetUserTimeInfo(name)
        curTime = time.time()
        self.OnlineUser[name].startTime = curTime
        return int(curTime - startTime) + onlineTime


if __name__ == '__main__':
    Server = ChatroomServer()
    Server.Start()
