import os,json

"""
Şuana kadar eklediğim veriler
{
    Name
    ID
    MainChat
    Adblock
    BadWordBlock
    Otorol
    praiseUsers
    praise
    hgmesaji
}


"""
def check_server(server):
    # Sunucu kaydını tespit etme.
    serverID = server.id
    if os.path.isfile("./veriler/sunucular/" + str(serverID) + ".json"):
        return True
    else:
        return False


def check_server_and_add(server):
    # Sunucu kaydını tespit etme, kayıt yoksa ekleme.
    serverID = server.id
    if os.path.isfile("./veriler/sunucular/" + str(serverID) + ".json"):
        return True
    else:
        add_server(server)


def add_server(server):
    # Sunucu ekleme.
    serverName = server.name
    serverID = server.id
    if check_server(server) == True:
        print("Sunucu var")
        return
    serverData = {}
    serverData["Name"] = serverName
    serverData["ID"] = serverID
    with open("./veriler/sunucular/" + str(serverID) + ".json","w") as fp:
        json.dump(serverData,fp,indent=4)


def delete_server(server):
    # Sunucu silme
    serverID = server.id
    if check_server(server) == True:
        os.remove("./veriler/sunucular/" + str(serverID) + ".json")
    else:
        print("dosya yok")


def get_data(server,datas):
    # Veri çekme
    serverID = server.id
    if not check_server(server):
        return None
    with open("./veriler/sunucular/" + str(serverID) + ".json","r") as fp:
        allDatas = json.load(fp)
    try:
        return allDatas[datas]
    except KeyError:
        return None


def add_data(server,key,value):
    # Sunucu verisi ekleme
    check_server_and_add(server)
    serverID = server.id  
    with open("./veriler/sunucular/" + str(serverID) + ".json","r") as fp:
        allDatas = json.load(fp)
    allDatas[key] = value
    with open("./veriler/sunucular/" + str(serverID) + ".json","w") as fp:
        json.dump(allDatas,fp,indent=4)


def add_list_data(server,key,value):
    serverID = server.id 
    check_server_and_add(server)
    with open("./veriler/sunucular/"+ str(serverID) + ".json","r") as fp:
        serverData = json.load(fp)
    if key in list(serverData.keys()):
        serverData[key].append(value)
        with open("./veriler/sunucular/"+ str(serverID) + ".json","w") as fp:
            json.dump(serverData,fp,indent=4)
    else:
        serverData[key] = []
        serverData[key].append(value)
        with open("./veriler/sunucular/"+ str(serverID) + ".json","w") as fp:
            json.dump(serverData,fp,indent=4)