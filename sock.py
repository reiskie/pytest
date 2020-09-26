#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket  
import time

DBHOST = '192.168.1.201'
DBPORT = 60000

MYHOST = '192.168.1.202'
MYPORT = 8007

# work as an agent beteen db2 client and db2 server.

s_lsn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s_lsn.bind((MYHOST, MYPORT)) 
s_lsn.listen(1) 

print('Now i\'m listening on %s:%d' % (MYHOST, MYPORT))

conn_out = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn_out.connect((DBHOST, DBPORT))
print("Connect to DB %s:%d OK" % (DBHOST, DBPORT))


while True:
    #time.sleep(1)
    #continue
    conn_in, addr = s_lsn.accept()  
    print('Receive connection from %s !' % str(addr))  

    cnt=1
    while True:
        print('====== [%d] round ======' % cnt)

        data = conn_in.recv(16384)
        print('Receive request from %s:\n %s' % (str(addr), data))
        print('These data will be sent to DB %s:%d' % (DBHOST, DBPORT))
        conn_out.send(data) 

        if cnt < 10:
            data1 = conn_out.recv(16384)
            print('Receive response from DB (%s:%d):\n %s' % (DBHOST, DBPORT, data1))
            print('These data will be sent to client %s.' % str(addr))
            conn_in.send(data1)
  
        cnt=cnt+1

    conn_in.close()

conn_out.close()




