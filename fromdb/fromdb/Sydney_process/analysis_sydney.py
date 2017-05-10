__author__ = 'team12'
# This program uses Elasticsearch to retrieve data from couchdb and the date
#The output file is used in data visualization section.
# This program serves for the topic of SydneyFC and Ausopen
import copy
import json
import time
import pprint
# http://115.146.94.162:5984/_utils/#

from elasticsearch import Elasticsearch


def main():
    start_time = time.time()
    es = Elasticsearch([{'host': '115.146.94.162', 'port': 9200}])
    fp = open("sdyney_output.txt", "w",encoding='utf-8')
    elastic_index = "sydney_test"
    baseQuery = open("base_query.txt").read()

    query_obj = json.loads(baseQuery)
    phrase_obj = query_obj['query']['bool']['should'].pop()

    with open("Ausopen.txt") as tf:
        for term in tf:
            if term.lstrip(' ')[0] == '#':
                continue
            phrase_obj['match_phrase']['text']['query'] = term.rstrip()
            query_obj['query']['bool']['should'].append(copy.deepcopy(phrase_obj))
    query = json.dumps(query_obj)
    res = es.search(index=elastic_index,  body=query, request_timeout=100)
    count, pos, neg, err = 0, 0, 0, 0
    date = "Tue Jan 31"
    for doc in res['hits']['hits']:
        if doc['_source']['created_at'].startswith(date):
            pprint.pprint(doc['_source']['created_at'])
            tweet = doc['_source']
            text = tweet['text']
            label = tweet['label']
            text.encode('GB18030')

            if label == 'pos':
                pos += 1
            elif label == 'neg':
                neg += 1
            else:
                print("Error:", tweet)
                err += 1
                continue
            count += 1
    fp.write(str(date) + '\n'+ str(text) + ':'+str(label) + '\n')
    end_time = time.time()
    elapsed = end_time - start_time

    fp.write("Positive num:" + str(pos)+ '\n')
    fp.write("Negative num:" + str(neg)+ '\n')
    fp.write("Total number:" + str(count))

    print("Runtime:", elapsed, "seconds")
    print("Positive num:", pos)
    print("Negative num:", neg)
    print("Error num:", err)
    print(count)

main()