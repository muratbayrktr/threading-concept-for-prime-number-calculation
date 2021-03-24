import threading
import time

# GLOBAL VARIABLE
result = 1

# worker class in order to multiply on threads
class Worker:
    # initiating the worker class
    def __init__(self):
        super().__init__()
        self.jobs = []

    # the function that does  the actual multiplying
    def multiplier(self,beg,end):
        global result
        for i in range(beg,end+1):
            result*= i
            #print("\tresult updated with *{}:".format(i),result)
        #print("Calculating from {} to {}".format(beg,end)," : ",result)
    
    # appending threads to the object
    def append_job(self,job):
        self.jobs.append(job)

    # function that is to see the threads
    def see_jobs(self):
        return self.jobs

    # initiating the threads
    def initiate(self):
        for j in self.jobs:
            j.start()

    # finalizing and joining the threads
    def finalize(self):
        for j in self.jobs:
            j.join()

    # controlling the threads by blocking them untill all threads are asleep
    def work(self):
        while True:
            if 0 == len([t for t in self.jobs if t.is_alive()]):
                self.finalize()
                break
                
# this is the function to split the factorial into several threads
def splitUp(n,t):
    # defining the remainder and the whole 
    remainder, whole = (n-1) % t, (n-1) // t
    # deciding to tuple count
    tuple_count = whole if remainder == 0 else whole + 1
    # empty result list 
    result = []
    # iterating 
    beginning = 1
    end = (n-1) // t 
    for i in range(1,tuple_count+1):
        if i == tuple_count:
            result.append((beginning,n-1)) # if we are at the end, just append all to end
        else:
            result.append((beginning,end*i))
        beginning = end*i + 1
    return result

if __name__ == "__main__":
    threads = 32
    number = 743
    splitted = splitUp(number,threads)

    worker = Worker()
    #print(worker.see_jobs())

    s = time.time()
    # creating the threads
    for arg in splitted:
        thread = threading.Thread(target=worker.multiplier(arg[0],arg[1]))
        worker.append_job(thread)

    worker.initiate()
    worker.work()
    e = time.time()
    print("result found with {} threads in {} secs\n".format(threads,e-s))
    if result % number == number-1:
        print("PRIME")
    else:
        print("NOT PRIME")

""" 
--------------------  REPORT  ------------------------

result found with 2 threads in 6.162530899047852 secs
result found with 4 threads in 0.29897499084472656 secs
result found with 16 threads in 0.009003162384033203 secs
result found with 32 threads in 0.0060007572174072266 secs
result found with 64 threads in 0.0029952526092529297 secs

note that: these results may differ from machine to machine
-------------------------------------------------------
"""
