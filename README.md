# Line Server Problem

### Where is solution and how to try it

This is a very simple django-based web application. URL to use is [http://katyrumshisky.pythonanywhere.com/lines](http://katyrumshisky.pythonanywhere.com/lines). To build this app I used public service [PythonAnywhere](https://www.pythonanywhere.com) - an online integrated development environment and web hosting service based on the Python programming language. I chose it because I don't have other available resources at hand: my home PC would require a lot of tinkering with environment and for obvious reasons I couldn't use work resources.
But from using public domain come serious restrictions. I paid $5 for a basic account and it gets me the following:
 * 1 web app on their domain name 
 * enough power to withstand 100,000 hit/day website
 * 1GB disk space
With all that in hand I made the app.

### How does it work?
The top directory ```newlinepr``` contains everything I need. From the command line from this directory I do:
```
python manage.py runserver 0:8880
```
to start up my web server. During the startup it will read big_file, also sitting in top directory, and split it into small chunks and create a dictionary, with the entry for each line (key - line index, value - path to file chunk and offset). This preprocessing allows to access lines of text fast when users request them.

### How well does it perform

This app is a a POC at best. I used django development tools to quickly make a working project. As it is said in [django docs](https://docs.djangoproject.com/en/2.0/intro/tutorial01/)
```
You’ve started the Django development server, a lightweight Web server written purely in Python. We’ve included this with Django so you can develop things rapidly, without having to deal with configuring a production server – such as Apache – until you’re ready for production.
```
By no means it is suposed to accept production volumes. Plus, adding the restrictions of PythonAnywhere, here is what we have.
I couldn't test with even 1GB file - it was my total memory limit - on almost 28MB and 5 users it's fast. PythonAnywhere promises to allow 100,000 hits per day. With original file size getting bigger, the size of the chunk needs to be adjusted, i.e. increased ```newlinepr/lines/local_settings.py```.

Suppose I pay for more memory: then I believe the app would hold well up to 10G file size. Django supports multithreading and together with promised 100K hits per day it should be OK. Bigger files, like 100G, would slow down the app - both at startup and at serving.

_NOTE_: if database can't be used, then splitting large file in chunks is the way to speed things up, and in real situation we should be talking not only of splitting the file, but of sharding the chunks between servers, having a dispatcher to keep track of which shard has what parts; plus getting multiple servers and load balancers to serve from these shards (and of course keep multiple copies of all all sharded data...).

### What did I use?

 1. Public platform  [PythonAnywhere](https://www.pythonanywhere.com), their domain and services, pre-installed environment:
      * bash shell
      * Python 2.7
      * django 1.10
 2. [django documentation](https://docs.djangoproject.com/en/1.10/intro/)
 3. [Stack Overflow](https://stackoverflow.com/)
 
