#!/usr/bin/python

import os
import sys
from glob import glob as ls

dict = {}
for file in ls('*.php'):
    if os.path.isfile('9/%s' % file):
        for line in open(file):
            if line.find('=>') != -1:
                field = line.split('=>')[0].strip()
                for anotherline in open('pt-br/%s' % file.replace('en-US','pt-BR')):
                    if anotherline.find(field) != -1:
                        dict.update({field: "".join(anotherline.split('=>')[1:])})

        newfile = open('final/%s' % file.replace('en-US','pt-BR'), 'w')
        for line in open(file):
            field = line.split('=>')[0].strip()
            if dict.has_key(field):
                newfile.write("%s => %s" % (line.split('=>')[0], dict[field]))
            else:
                newfile.write(line)
        newfile.close()

#for file in *.php 
#do
#    for field in $( cat $file | awk '/=>/ { print $1 }' ) ; do 
#        if [ -f 9/$file ] ; then
#            novo=$( grep -w $field pt-br/${file/en-US/pt-BR} | awk -F'=>' '{print $2}')
#            #grep -w $field $file 9/$file
#            sed -n "/${field//\'}/s/ => .*/ => $novo/p" $file
#        fi
#    done
#done
