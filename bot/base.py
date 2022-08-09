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
                "ban":False,
                "lvl":0,
                "balCount":0
                }
        User.insert_one(post)

    def setBan(self,usrId,group,ban):
        db = self.classter["AdminBot"]
        User = db["User"]
        User.update_one({"usrId":usrId,"group":group},{"$set":{"ban":ban}})

    def getUser(self,usrId, group):
        db = self.classter["AdminBot"]
        User = db["User"]

        return User.find_one({"usrId":usrId,"group":group})

    def addBall(self,usrId,count,group):
        db = self.classter["AdminBot"]
        User = db["User"]

        User.update_one({"usrId":usrId,"group":group},{"$set":{"balCount":User.find_one({"usrId":usrId})["balCount"]+count}})

    def checkLvl(self,usrId,group):
        db = self.classter["AdminBot"]
        User = db["User"]
        usr = User.find_one({"usrId":usrId,"group":group})

        if usr["lvl"]< (usr["balCount"]//500):
            User.update_one({"usrId": usrId,"group":group}, {"$set": {"lvl": (usr["balCount"] // 500)}})
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

    def DelAll(self):
        db = self.classter["AdminBot"]
        User = db["User"]

        User.delete_one({})
