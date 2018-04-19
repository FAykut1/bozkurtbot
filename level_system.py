import json,os.path
def user_add_xp(server_id,user_id: int,xp: int):
    if os.path.isfile("users.json"):
        try:
            with open('users.json','r') as fp:
                users = json.load(fp)
            users[server_id][user_id]['xp']+=xp
            with open('users.json','w') as fp:
                json.dump(users,fp,sort_keys=True,indent=4)
        except KeyError:
                try:
                    with open('users.json','r') as fp:
                        users = json.load(fp)
                    users[server_id][user_id] = {}
                    users[server_id][user_id]['xp'] = +xp
                    with open('users.json', 'w') as fp:
                        json.dump(users, fp, sort_keys=True, indent=4)
                except KeyError:
                    with open('users.json','r') as fp:
                        users = json.load(fp)
                    users[server_id] = {user_id:{}}
                    users[server_id][user_id]['xp'] = xp

                    with open('users.json', 'w') as fp:
                        json.dump(users, fp, sort_keys=True, indent=4)

    else:
        users = {server_id:{user_id:{}}}
        users[server_id][user_id]['xp'] = xp
        with open('users.json','w') as fp:
            json.dump(users,fp,sort_keys=True,indent=4)
mentos = "IWZJFJ3Jv8VUhNdhZsOZh4Lhn9d.QlIobD.5MjM1ATOyETM0cDM5QTN1MDN"
def get_xp(server_id,user_id: int):
    if os.path.isfile('users.json'):
        with open('users.json','r') as fp:
            users = json.load(fp)
        return users[server_id][user_id]['xp']
    else:
        return 0
