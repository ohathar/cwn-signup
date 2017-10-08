# Signup Site thing

[![License](https://img.shields.io/github/license/mashape/apistatus.svg)](https://opensource.org/licenses/MIT)

This signup thing was built in order to get an idea of how many people would be attending a CodeWarz live event.

Since dillinger.io already has some tab things set out, i will now add a few bullet type things about it

  - Written for Python3.5 (may work in 2, i dunno?)
  - Uses MySQL only for backend db at present
  - <3 flask so we're using flask

# Making it "go"

  - Recommend using virtualenv, clone this repo into app dir, install deps
 ```sh
 $ virtualenv -p python3 signup-site
 $ . signup-site/bin/activate
 (signup-site) $ cd signup-site
 (signup-site) $ git clone https://github.com/ohathar/cwn-comp-signup app
 (signup-site) $ cd app
 (signup-site) $ pip install -r requirements.txt
 ```
   - edit sql file to reflect admin user/pass combo you want (passlib.hash.bcrypt.encrypt)
   - Get the provided sql db stuff into a db somehow
   - copy config.txt.example to config.txt and edit to suite
   - run app.py
```sh
 (signup-site) $ ./app.py
  * Running on http://0.0.0.0:1301/ (Press CTRL+C to quit)
  * Restarting with stat
  * Debugger is active!
  * Debugger PIN: zzz-yyy-xxx
```

# Contributing
   - clone the repo
   - work in dev branch
   - make PR
   - i'll probably merge it
