**Automation**
=================
Some scripts thats automate some routine using python3 (tested on 3.6 version) or bash

**```check_youtube_channel.py```** : check your youtube channel on new video upload and open it if new video exists.

Preconditions:
* Download geckodriver for Firefox or Chromedriver for Google Chrome:
https://github.com/mozilla/geckodriver/releases
http://chromedriver.chromium.org/downloads

* Add path where driver located to System PATH:
```
export PATH=$PATH:/path/to/directory/of/executable/downloaded/in/previous/step
```
* install selenium
```pip install selenium```

* set api_key to https://console.developers.google.com and channel_id inside script


**```rollback_operations_postgre.sh```** : rollback operations of your service (postgre example)

**```cleanup_files.py```** : delete files in directory (screenshots cleanup example)

**```service_names_yaml.py```** : takes yaml file, parse it and store name of services (1st layer) to Excel file
