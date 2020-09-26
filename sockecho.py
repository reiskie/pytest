#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket  
import time

MYHOST = '192.168.3.202'
MYPORT = 8008

# send back what's received.

s_lsn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s_lsn.bind((MYHOST, MYPORT)) 
s_lsn.listen(1) 

print('Now i\'m listening on %s:%d' % (MYHOST, MYPORT))


conn_in, addr = s_lsn.accept()  
print('Receive connection from %s !' % str(addr))  

cnt=0

while True:

    data = conn_in.recv(16384)
    print('# %d, Receive data from %s:\n %s' % (cnt, str(addr), data))
    print('This data will be sent back to client %s.' % str(addr))
    conn_in.send(data) 

    cnt=cnt+1
    if cnt >= 3:
        break;
 
conn_in.close()

