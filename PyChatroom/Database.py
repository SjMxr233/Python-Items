import sqlite3

class Database(object):
    def __init__(self,path):
        self.Con = sqlite3.connect(path)
        self.Cursor = self.Con.cursor()

    def DatabaseGet(self,command):
        self.Cursor.execute(command)
        command_result = self.Cursor.fetchone()
        if not command_result:
            return False
        return command_result

    def DatabaseSet(self,command):
        self.Cursor.execute(command)
        self.Con.commit()

class UserDatabase(Database):
    def __init__(self,path):
        super(UserDatabase, self).__init__(path)

    def GetUserTimeInfo(self,username):
        query = "SELECT onlineTime,createTime FROM user WHERE name = '{}'".format(username)
        result = self.DatabaseGet(query)
        if not result:
            return None,None,False
        else:
            return result[0],result[1],True

    def QueryUserName(self,username):
        query = "SELECT * FROM user WHERE name = '{}'".format(username)
        return self.DatabaseGet(query)

    def QueryUserLogin(self,username,password):
        query = "SELECT * FROM user WHERE name = '{}' AND password = '{}' ".format(username,password)
        return self.DatabaseGet(query)

    def UpdateOnlineTime(self, name, onlineTime):
        update = "UPDATE user SET onlineTime = {} WHERE name = '{}'".format(onlineTime,name)
        self.DatabaseSet(update)

    def AddUser(self,username,password,createTime):
        insert = "insert into user (name,password,onlineTime,createTime) " \
                 "values ('{}','{}',0,'{}')".format(username,password,createTime)
        self.Db.DatabaseSet(insert)