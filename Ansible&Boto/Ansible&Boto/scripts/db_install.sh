#!/bin/sh


wget http://apache-mirror.rbc.ru/pub/apache/couchdb/source/2.0.0/apache-couchdb-2.0.0.tar.gz

tar -xvzf apache-couchdb-2.0.0.tar.gz
cd apache-couchdb-2.0.0/
./configure && make release


