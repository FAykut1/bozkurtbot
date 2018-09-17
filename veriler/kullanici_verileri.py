import os,json


"""
Şuana kadar oluşturduğum Kullanıcı Verileri:

{
    name        > Kullanıcının ismi
    ID          > kullanıcının ID 'si
    servers     > kullanıcının bulunduğu sunucular
    praise      > övgü puanları
    praiseUsers > övgü atan kişiler
    afkDesc     > afk açıklaması
    dmCheck     > Dm check eder
}

"""


def check_user(user):
    userID = user.id 
    if os.path.isfile("./veriler/kullanicilar/"+ str(userID) + ".json"):
        return True
    else:
        return False


def check_user_and_add(user,server):
    userID = user.id 
    if os.path.isfile("./veriler/kullanicilar/"+ str(userID) + ".json"):
        return True
    else:
        add_user(user,server)


def add_user(user,server):
    userID = user.id
    userName = user.name
    serverID = server.id
    if check_user(user):
        return
    userData = {}
    userData["Name"] = userName
    userData["ID"] = userID
    userData["servers"] = {}
    userData["servers"][serverID] = {}
    userData["servers"][serverID]["name"] = server.name
    with open("./veriler/kullanicilar/"+ str(userID) + ".json","w") as fp:
        json.dump(userData,fp,indent=4)


def delete_user(user):
    userID = user.id
    if check_user(user):
        os.remove("./veriler/kullanicilar/"+ str(userID) + ".json")


def get_user_data(user,server,datas):
    userID = user.id
    check_user_and_add(user,server)
    with open("./veriler/kullanicilar/"+ str(userID) + ".json","r") as fp:
        userData = json.load(fp)
    try:
        return userData[datas]
    except KeyError:
        return None


def get_all_data(user,server):
    userID = user.id
    check_user_and_add(user,server)
    with open("./veriler/kullanicilar/"+ str(userID) + ".json","r") as fp:
        userData = json.load(fp)
    try:
        return userData
    except KeyError:
        return None   

def add_user_data(user,server,key,value):
    userID = user.id
    check_user_and_add(user,server)
    with open("./veriler/kullanicilar/"+ str(userID) + ".json","r") as fp:
        userData = json.load(fp)
    userData[key] = value
    with open("./veriler/kullanicilar/"+ str(userID) + ".json","w") as fp:
        json.dump(userData,fp,indent=4)


def add_list_user_data(user,server,key,value):
    userID = user.id
    check_user_and_add(user,server)
    with open("./veriler/kullanicilar/"+ str(userID) + ".json","r") as fp:
        userData = json.load(fp)
    if key in list(userData.keys()):
        userData[key].append(value)
        with open("./veriler/kullanicilar/"+ str(userID) + ".json","w") as fp:
            json.dump(userData,fp,indent=4)
    else:
        userData[key] = []
        userData[key].append(value)
        with open("./veriler/kullanicilar/"+ str(userID) + ".json","w") as fp:
            json.dump(userData,fp,indent=4)


def add_user_server_data(user,server,key=None,value=None):
    userID = user.id
    if check_user_and_add(user,server):
        with open("./veriler/kullanicilar/"+ str(userID) + ".json","r") as fp:
            userData = json.load(fp)
        if key == None:
            if str(server.id) in list(userData["servers"]):
                return
            else:
                userData["servers"][server.id] = {}
                userData["servers"][server.id]["name"] = server.name
        else:
            if server.id in list(userData["servers"].keys()):
                userData["servers"][server.id][key] = value
            else:
                userData["servers"][server.id] = {}
                userData["servers"][server.id]["name"] = server.name
                userData["servers"][server.id][key] = value
        with open("./veriler/kullanicilar/"+ str(userID) + ".json","w") as fp:
            json.dump(userData,fp,indent=4)
    else:
        with open("./veriler/kullanicilar/"+ str(userID) + ".json","r") as fp:
            userData = json.load(fp)
        if key == None:
            return
        else:
            userData["servers"][server.id][key] = value
        with open("./veriler/kullanicilar/"+ str(userID) + ".json","w") as fp:
            json.dump(userData,fp,indent=4)

