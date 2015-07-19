#!/usr/bin/env python
import sys
import json
from urllib2 import Request, urlopen
import os, glob
import hashlib
import shutil
import time
from pydub import AudioSegment

cachepath=os.path.abspath(os.path.join(os.path.dirname(__file__), 'cache'))
jinglepath=os.path.abspath(os.path.join(os.path.dirname(__file__), 'jingle'))
hashtxt = hashlib.md5(sys.argv[1]+sys.argv[2]).hexdigest()
hashfile = hashtxt+'.mp3'
filename=os.path.join(cachepath,hashfile)
found = 0
try:
    os.stat(cachepath)
except:
    os.mkdir(cachepath)
for filefound in os.listdir(cachepath):
    if str(hashfile) == str(filefound) :
        found=1
        break

if found == 0 :

    req = Request(url='http://translate.google.com/translate_tts')
    req.add_header('User-Agent', 'My agent !') #Needed otherwise return 403 Forbidden
    req.add_data("tl=FR&q="+sys.argv[7]+"&ie=UTF-8")
    fin = urlopen(req)
    mp3 = fin.read()
    fout = file(filename, "wb")
    fout.write(mp3)
    fout.close()
    song = AudioSegment.from_mp3(filename)
    jinglename=os.path.join(jinglepath,sys.argv[10]+'.mp3')
    jingle= AudioSegment.from_mp3(jinglename)
    songmodified = jingle+song
    songmodified.export(filename, format="mp3", bitrate="128k", tags={'albumartist': 'Alerte', 'title': 'TTS', 'artist':'Alerte'}, parameters=["-ar", "44100","-vol", "800"])

cmd = ['mplayer']
cmd.append(filename)
with open(os.devnull, 'wb') as nul:
    subprocess.call(cmd, stdin=nul)