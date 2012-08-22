'''
Created on 16 Aug 2012

@author: i046533
'''

import hashlib
import time
import random
string = "abcdefghijklmnopqrstuvwxyz1234567890"

while True :
    rnum= str(random.randint(-1000000000000, 1000000000000))
    #print rnum
    encrptint =  hashlib.md5(rnum).hexdigest()
    encrptstr =  hashlib.md5(string).hexdigest()
   # print encrptint
    #print encrptstr
    encrptstr =''
   
    
    #time.sleep(0.0001)
           
   

if __name__ == '__main__':
    pass