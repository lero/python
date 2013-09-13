#!/opt/local/bin/python2.7

jump=0
old=None
for line in open('zbx_hosts_export.xml'):
   if line.find('znfs') != -1:
       jump=1
   if line.find('nfs.alive') != -1:
       jump=1
   if line.find('sr-mount') != -1:
       jump=1
   old=line
   if jump == 0:
       print old[:-1]
   if line.find('</item>') != -1:
       jump=0
