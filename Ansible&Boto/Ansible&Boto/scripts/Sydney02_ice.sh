#!/bin/bash
screen python3 twitter_harvest_multi_thread.py auth_streaming auth_timeline auth_followers auth_friends auth_rest couchlogin "115.146.94.129:5984/" "sydney" "150.935,-34.12,151.37,-33.57" "Sydney, New South Wales" "-33.868820,151.209296,15km"
