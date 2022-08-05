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
                "verif":False
                }
        User.insert_one(post)


    def getUser(self,usrId):
        db = self.classter["AdminBot"]
        User = db["User"]

        return User.find_one({"usrId":usrId})

    def getAllUser(self,group):
        db = self.classter["AdminBot"]
        User = db["User"]

        return User.find({"group":group})

    def setAdmin(self,usrId):
        db = self.classter["AdminBot"]
        User = db["User"]

        User.update_one({"usrId":usrId},{"$set":{"admin":True}})