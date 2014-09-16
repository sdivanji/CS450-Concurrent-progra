from __future__ import print_function
from threading import Thread, Semaphore
from time import sleep
import io
import logging
import argparse
from collections import deque
from timeit import Timer
import random

parser = argparse.ArgumentParser(description='Concurrent golfer simulator')
parser.add_argument('--golfer', '-g',
                        default='0',
                        help='number of golfers')

parser.add_argument('--stash', '-s',
                        default='0',
                        help='no of balls in stash')

parser.add_argument('--bucket', '-b',
                        default='0',
                        help='no. of balls per bucket')
                        
args = parser.parse_args()


global golfer
global stash
global bucket

golfer= int (args.golfer)
stash= int (args.stash)
bucket=int (args.bucket)
balls_on_field=0
print ('No. of golfers', golfer) 
print ('No. of balls in stash',stash) 
print ('No. of balls per bucket',bucket) 

##Initialize semaphores
stash_sem=Semaphore(stash/bucket)
mutex=Semaphore(1)
rng = random.Random()
rng.seed(100)

##generate methods for golfer equal to the no. of golfers in args
for i in range(0,golfer):
    def golf(i=i):
        global stash
        ##Each time a golfer calls for bucket the stash is reduced by the quantity          of bucket
        stash=stash-bucket
        #wait
        stash_sem.acquire()
        print ('Golfer', i, 'calling for bucket')
        print ('Golfer', i, 'got', bucket, 'balls',':''Stash is',stash)
        j=0
        while (True):
            j=(j+1)%bucket
            global balls_on_field
            mutex.acquire()
            balls_on_field+=1
            mutex.release()
            #print('balls on field is',balls_on_field)
            print('Golfer', i, 'hit' ,j ,'ball')
            if(j==bucket-1):
                print ('Golfer', i, 'calling for bucket')
                if(stash>=bucket):
                    stash=stash-bucket
                    print ('Golfer', i, 'got', bucket, 'balls',':''Stash is',stash)
                    mutex.acquire()
                    balls_on_field+=1
                    mutex.release()
                    #print('balls on field is',balls_on_field)
                    j=0
                    print('Golfer', i, 'hit' ,j ,'ball')
                    global prng
                    global rng
                    prng=rng.random()
                    sleep (prng)
            prng=rng.random()
            sleep (prng)
            
           
for i in range(golfer):
    t=Thread(target=golf,args=[i])
    t.start()
    rng.seed(i*100)
    prng=rng.random()
    sleep (prng)
    


def cart():
    global stash
    global balls_on_field
    mutex.acquire()
    print('######################################')
    print('stash=', stash, 'gathering balls on field')
    stash+=balls_on_field
    balls_on_field=0
    #signal
    stash_sem.release()
    print('done stash=', stash, 'return')
    print('#####################################')
    mutex.release()
while(True):        
    t=Thread(target=cart)
    if(stash<bucket):
        mutex.acquire()
        t.start()
        mutex.release()
        rng.seed(50)
        prng=rng.random()
        sleep (prng)
