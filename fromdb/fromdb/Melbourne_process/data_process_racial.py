__author__ = 'team12'
# This program uses Elasticsearch to retrieve data from couchdb and uses googlemap to get the suburb of the tweet.
#The output file is used in data visualization section.
# This program serves for the topic of racial issue
import copy
import json
import time
import googlemaps
from elasticsearch import Elasticsearch
from  melbourne_config import host_ip, host_port, e_index, topic_file, base_query_file, g_key, suburbs_file


def get_suburbs():
    sub_dic = {}
    with open(suburbs_file) as sf:
        for suburb in sf:
            sub_dic[suburb.rstrip("\n")] = [0, 0]
    return sub_dic

#retrieve data from couchdb
def get_tweet_topic():
    es = Elasticsearch([{'host': host_ip, 'port': host_port}])
    elastic_index = e_index
    baseQuery = open(base_query_file).read()
    query_obj = json.loads(baseQuery)
    phrase_obj = query_obj['query']['bool']['should'].pop()
    with open(topic_file) as tf:
        for term in tf:
            if term.lstrip(' ')[0] == '#':
                continue
            phrase_obj['match_phrase']['text']['query'] = term.rstrip()
            query_obj['query']['bool']['should'].append(copy.deepcopy(phrase_obj))
    query = json.dumps(query_obj)
    res = es.search(index=elastic_index,  body=query, request_timeout=100)
    return res


def main():
    suburb_set = get_suburbs()
    gmaps = googlemaps.Client(key=g_key)
    start_time = time.time()
    res = get_tweet_topic()
    count, pos, neg, err = 0, 0, 0, 0
    print(suburb_set)
    for doc in res['hits']['hits']:
        tweet = doc['_source']
        text = tweet['text']
        label = tweet['label']

        coordinates = tweet['geo']['coordinates']
        if coordinates == [0, 0]:
            continue
        coordinate_tup = tuple(coordinates)
        #print(label)
        reverse_geocode_result = gmaps.reverse_geocode(coordinate_tup)
        for i in reverse_geocode_result[0]['address_components']:
            if i['types'] == ['locality', 'political']:
                subname = i['long_name']
                subname = subname.upper()
                #print(subname)
        if label == 'pos':
            pos += 1
            try:
                suburb_set[subname][1] += 1
            except:
                print("Lack:", subname)
                continue
        elif label == 'neg':
            neg += 1
            try:
                suburb_set[subname][1] += 1
            except:
                print("Lack:", subname)
                continue
        else:
            print("Error:", tweet)
            err += 1
            continue
        count += 1
        resultDict = {'polarity': label, 'coordinates': coordinates}
    print(count)
    newD = {}
    print(suburb_set)
    for item in suburb_set:
        v = suburb_set.get(item)[1]
        print(v)
        newD.update({item:round((v/count),2)})
    print(newD)
    with open('racially.txt', 'w') as fpp:
        fpp.write(str(newD))

    end_time = time.time()
    elapsed = end_time - start_time
    print("Runtime:", elapsed, "seconds")
    print("Positive num:", pos)
    print("Negative num:", neg)
    print("Error num:", err)
    print(count)
    print(suburb_set)

if __name__ == '__main__':
    main()