## Functions to help interaction with database

def add_user(data, db):
    db.routes.delete_many({'username': data['username']})
    return db.routes.insert_one(data).inserted_id

def update_location(coordinates, userName, db):
    return db.routes.update_one({'username': userName}, {'$push': {'route': coordinates}})


def user_status(userName, db):
    count = db.routes.count_documents({"username": userName})
    if count > 0:
        user_info = True
    else:
        user_info = False

    return {"user_info": user_info, "locations": count}

def clear_route(userName, db):
    return db.routes.update_one({'username': userName}, {'$set': {'route': []}})

def clear_data(userName, db):
    db.routes.delete_many({'username': userName})
