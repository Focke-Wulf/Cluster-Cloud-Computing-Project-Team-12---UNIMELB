#!/bin/bash
screen python3 twitter_harvest_multi_thread.py auth_streaming auth_timeline auth_followers auth_friends auth_rest couchlogin "115.146.94.129:5984/" "melbourne_tweet" "144.52,-34.43,144.49,-37.52" "Melbourne" "-37.813628,144.963058,15km"
