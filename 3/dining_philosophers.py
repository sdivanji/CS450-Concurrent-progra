from __future__ import print_function
from threading import Semaphore, Lock, Thread
from time import sleep
from random import random
import argparse
from timeit import Timer

(THINKING, EATING) = (0, 1) #philosopher states

def left_fork(id):
    return id

def right_fork(id):
    return (id+1) % NUM_PHILOSOPHER

def right(id):
    return (id+1) % NUM_PHILOSOPHER

def left(id):
    return (id+NUM_PHILOSOPHER-1) % NUM_PHILOSOPHER

def get_fork(id):
    global mutex
    global tstate
    global sem

    mutex.acquire()
    tstate[id] = 'hungry'
    test(id)
    mutex.release()
    sem[id].acquire()

def put_fork(id):
    global mutex
    global tstate
    global sem

    mutex.acquire()
    tstate[id] = 'thinking'
    test(right(id))
    test(left(id))
    mutex.release()

def test(id):
    global tstate
    if tstate[id] == 'hungry' and tstate[left(id)] != 'eating' and tstate[right(id)] != 'eating':   
        tstate[id] = 'eating'
        sem[id].release()

def philosophize_footman(id,meal):
    global forks
    global footman
    state = THINKING
    for i in range(meal):
        sleep(random())
        if(state == THINKING):
            msg = "Philosopher " + str(id) + " is thinking."
            #print(msg)
            footman.acquire()
            forks[right_fork(id)].acquire()
            forks[left_fork(id)].acquire()
            state = EATING
        else:
            msg = "Philosopher " + str(id) + " is eating."
            #print(msg)
            forks[right_fork(id)].release()
            forks[left_fork(id)].release()
            state = THINKING
            footman.release()
    print("Finish philosophize_footman")

def philosophize_lefthand(id,meal):
    global forks
    state = THINKING
    for i in range(meal):
        sleep(random())
        if(state == THINKING):
            #define the left hand user.
            if(id == 3):
                forks[left_fork(id)].acquire()
                forks[right_fork(id)].acquire()
                state = EATING
            else:
                forks[right_fork(id)].acquire()
                forks[left_fork(id)].acquire()
                state = EATING
        else:
            if(id == 3):
                forks[left_fork(id)].release()
                forks[right_fork(id)].release()
                state == THINKING   
            else:
                forks[right_fork(id)].release()
                forks[left_fork(id)].release()
                state == THINKING
    print("Finish philosophize_lefthand")

def philosophize_Tanenbaum(id,meal):
    for i in range(meal):
        get_fork(id)
        sleep(random())
        put_fork(id)
    print("Finish philosophize_Tanenbaum")

def run_c():
    global NUM_PHILOSOPHER
    global MEAL
    threads=[]
    for i in range(NUM_PHILOSOPHER):
        phil1 = Thread(target = philosophize_Tanenbaum,args = (i,MEAL))
        phil1.start()
        threads.append(phil1)
    for t in (threads):
        t.join()
def run_a():
    global NUM_PHILOSOPHER
    global MEAL
    threads =[] 
    for m in range(NUM_PHILOSOPHER):
        phil = Thread(target = philosophize_footman, args = (m,MEAL))
        phil.start()
        threads.append(phil)
    for t in (threads):
        t.join()
def run_b():
    global NUM_PHILOSOPHER
    global MEAL
    threads=[]
    for n in range(NUM_PHILOSOPHER):
        phil2 = Thread(target = philosophize_lefthand, args = (n,MEAL))
        phil2.start()
        threads.append(phil2)
    for t in (threads):
        t.join()
        


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Philosopher dining')
    parser.add_argument('--nphi','-n',
                        type = int,
                        default = 0,
                        help = 'add num_phi',
                        metavar = 'number of philosophers')
    parser.add_argument('--meal','-m',
                        type = int,
                        default = 0,
                        help = 'number of meals',
                        metavar = 'meal')
    args = parser.parse_args()
    NUM_PHILOSOPHER = args.nphi #define number fo philosophers
    MEAL = args.meal    #define number of meals
    forks = [Semaphore(1) for i in range(NUM_PHILOSOPHER)]  #defines forks
    sem = [Semaphore(0) for i in range(NUM_PHILOSOPHER)]    #semaphores
    footman = Semaphore(4) #limit the number of philosophers
    mutex = Semaphore(1)    #mutex
    tstate = ['thinking'] * NUM_PHILOSOPHER #T-states


    #run_a()
    #run_b()
    #run_c()
    timer_a = Timer(run_a)
    #print ('time is', timer)
    print("Time for footman: {:0.3f}s".format(timer_a.timeit(1)/1))

    
    #run_a()
    #run_b()
    #run_c()
    timer_b = Timer(run_b)
    #print ('time is', timer)
    print("Time for lefthanded: {:0.3f}s".format(timer_b.timeit(1)/1))

    #run_c()
    #run_b()
    #run_c()
    timer_c = Timer(run_c)
    #print ('time is', timer)
    print("Time for Tanenbaum: {:0.3f}s".format(timer_c.timeit(1)/1))
