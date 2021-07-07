## Functions to help interaction with database

def add_user(data, db):
    db.routes.delete_many({'uid': data['uid']})
    return db.routes.insert_one(data).inserted_id

def update_location(coordinates, userId, db):
    return db.routes.update_one({'uid': userId}, {'$push': {'route': coordinates}})


def user_status(userId, db):
    count = db.routes.count_documents({"uid": userId})
    if count > 0:
        user_info = True
    else:
        user_info = False

    return {"user_info": user_info, "locations": count}

def clear_route(userId, db):
    return db.routes.update_one({'uid': userId}, {'$set': {'route': []}})

def clear_data(userId, db):
    db.routes.delete_many({'uid': userId})
