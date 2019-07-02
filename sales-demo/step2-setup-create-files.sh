sed -i '' 's/"host":"[^"]*"/"host":"'"$API_HOST"'"/g' index.html

# Create an initial folder
python demodata.py --api $API_CREDS --op file_list --folder "/NYC Project" --files '{"file":"NewYork.jpg", "size":0.88}, {"file":"New-York-New-York.flac", "size":2.24}, {"file":"Statue-of-Liberty.mov", "size":4.48}, {"file":"Times-Sqaure-Scene1.mov", "size":2.72}, {"file":"Times-Sqaure-Scene2.mov", "size":0.4}, {"file":"Times-Sqaure-Scene3.mov", "size":0.56}, {"file":"Times-Sqaure-Scene4.mov", "size":3.12}, {"file":"Central-Park.jpg", "size":3.28}'

# Create the initial tree with ~150 megabytes of files. You can change the 150 to the number of megabytes you'd like created.
# This takes a few minutes on a sim cluster, but under one minute on an OVA
python demodata.py --api $API_CREDS --op create --size 130 --threads 4
