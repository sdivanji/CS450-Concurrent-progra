from __future__ import print_function
from threading import Thread, Semaphore
from time import sleep
import io
import logging
import argparse
from collections import deque
from timeit import Timer
import random

parser = argparse.ArgumentParser(description='Dance mixer simulator')
parser.add_argument('--leader', '-l',
                        default='0',
                        help='number of leaders')

parser.add_argument('--follower', '-f',
                        default='0',
                        help='no of followers')
                        
args = parser.parse_args()


global leader
global follower

leaderQueue=Semaphore(0)
followerQueue=Semaphore(0)
mutex=Semaphore(1)

leader= int (args.leader)
follower= int (args.follower)

leadercount=0
followercount=0

rng = random.Random()
rng.seed(100)

print ('No. of leaders', leader) 
print ('No. of followers',follower) 


def start_music(music):
    print('**Band leader started playing',music,'**') 
def end_music(music):
    print('**Band leader stopped playing',music,'**')

def band():
    for music in list(['waltz', 'tango', 'foxtrot']):
        mutex.acquire()
        start_music(music)
        sleep(5)
        end_music(music)
        mutex.release()

def dance():
    global leadercount
    global followercount
    for i in range(leadercount):
        temp=followercount
        print('temp is',temp)
        for j in range(followercount):
            followercount-=1
            print('leader', i ,'and follower', j ,'are dancing')
            print('follower', j, 'is leaving')
        print('leader',i,'is leaving')
        followercount=temp
        print('follower count is',followercount)
        leadercount-=1
        

def leader_dance():
    global leadercount
    global followercount
    leadercount=0
    followercount=0
    for i in range(leader):
        print ('Leader', i ,'is entering floor')
        followerQueue.release()
        leadercount+=1
        leaderQueue.acquire()
         

def follower_dance():
    global leadercount
    global followercount
    for i in range(follower):
        print('Follower', i, 'is entering floor')
        leaderQueue.release()
        followercount+=1
        followerQueue.acquire()
            
while (True):
    t=Thread(target=band)
    t.start()
    sleep(1)
    t=Thread(target=leader_dance)
    t.start()
    rng.seed(100)
    prng=rng.random()
    sleep (prng)
    t=Thread(target=follower_dance)
    t.start()
    rng.seed(100)
    prng=rng.random()
    sleep (prng)
    t=Thread(target=dance)
    t.start()
    rng.seed(100)
    prng=rng.random()
    sleep (prng)



        



