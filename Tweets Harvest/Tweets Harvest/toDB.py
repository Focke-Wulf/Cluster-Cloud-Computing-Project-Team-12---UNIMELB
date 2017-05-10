from config import token_pool,couchdb_admin,couch_server,db_name,locations,geocode
import json,tweepy,couchdb,sys,re
import sentiment_analysis as sa


def main():
    classifier = sa.ta_classifier()
    db = get_db(0, True)
    num_saved = 0
    with open("bigTwitter.json") as f:
        print("9")
        for num, line in enumerate(f):
            if bool(re.search(r'"full_name":"Melbourne', line)):
                num_saved += 1
                line = json.loads(line[:-2])
                tweet = line['json']
                tweet['_id'] = line['meta']['id']
                print(num)
                try:
                    label = sa.predict(classifier, tweet['text'])
                    tweet['label'] = label
                    db.save(tweet)
                    print(num_saved, "saved")
                except:
                    print("save failed")








def get_auth(name):
    if name not in token_pool:
        sys.exit("user name is incorrect")
    else:
        consumer_key, consumer_secret =token_pool[name].c_key,token_pool[name].c_sec
        access_token_key, access_token_secret=token_pool[name].a_token,token_pool[name].a_sec
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token_key, access_token_secret)
        return auth


def get_db(node_id, ini=False):
    db_user, db_pwd=couchdb_admin["admin"],couchdb_admin["password"]
    server=couch_server[node_id]
    couch = couchdb.Server("http://" + db_user + ":" + db_pwd + "@" + server)
    try:
        db = couch[db_name]
        return db
    except:
        if ini:
            db = couch.create(db_name)
            return db
        else:
            sys.exit('Database does not exist')


def get_location(loc_id):
    try:
        return locations[loc_id]
    except:
        sys.exit("Location Index does not exit")


def get_geocode():
        return geocode

if __name__ == '__main__':
    main()