import pymongo
from bson import ObjectId
from datetime import datetime
from datetime import timedelta


class Base():
    def __init__(self,classterMongo):
        self.classterMongo = classterMongo
        self.classter = pymongo.MongoClient(self.classterMongo)


    def regUser(self,usrId,group):
        db = self.classter["AdminBot"]
        User = db["User"]

        post = {"usrId":usrId,
                "group":group,
                "admin":False,
                "activ":False,
                "lvl":0,
                "msgCount":0
                }
        User.insert_one(post)


    def getUser(self,usrId, group):
        db = self.classter["AdminBot"]
        User = db["User"]

        return User.find_one({"usrId":usrId,"group":group})

    def addMsg(self,usrId):
        db = self.classter["AdminBot"]
        User = db["User"]

        User.update_one({"usrId":usrId},{"$set":{"msgCount":User.find_one({"usrId":usrId})["msgCount"]+1}})

    def checkLvl(self,usrId):
        db = self.classter["AdminBot"]
        User = db["User"]
        usr = User.find_one({"usrId":usrId})

        if usr["lvl"]< (usr["msgCount"]//500):
            User.update_one({"usrId": usrId}, {"$set": {"lvl": (usr["msgCount"] // 500)}})
            return 1
        else:
            return 0




    def getAllUser(self,group):
        db = self.classter["AdminBot"]
        User = db["User"]

        return User.find({"group":group})

    def setAdmin(self,usrId,group):
        db = self.classter["AdminBot"]
        User = db["User"]

        User.update_one({"usrId":usrId,"group":group},{"$set":{"admin":True}})