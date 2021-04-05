import threading
import time
import sys

# supply the file name which should be in the same directory with command line argument enclosed with double quotes

# GLOBAL VARIABLE
result = 1
threadlist = [4,16,32,64]

# worker class in order to multiply on threads
class Worker:
    # initiating the worker class
    def __init__(self):
        super().__init__()
        self.jobs = []

    # the function that does  the actual multiplying
    def multiplier(self,beg,end,num):
        global result
        #print("\tCalculating from {} to {}".format(beg,end)," : ",result)
        for i in range(beg,end+1):
            result = result * i % num
            #print("\t\tresult updated with *{}:".format(i),result)
        
    
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
    # empty result list 
    result = []
    # deciding to tuple count
    # iterating 
    beginning = 1

    if whole == 0:
        tuple_count = n-1
        for i in range(tuple_count):
            result.append((beginning,beginning))
            beginning += 1
    else:
        tuple_count = t
        increaser = (n-1)//t + 1
        if remainder == 0:
            for i in range(tuple_count):
                result.append((beginning,beginning+whole-1))
                beginning = beginning + whole
        else:
            j = 0
            while j < tuple_count:
                if j == tuple_count-1:
                    result.append((beginning,n-1))
                else: 
                    result.append((beginning,beginning+increaser-2))
                beginning = beginning + increaser -1
                j += 1


    print("### splitup result: ",result,remainder,whole)
    return result

# reads the file and returns the num list
def read_nums():
    num_list = []
    file_name = sys.argv[1]
    with open(file_name,"r") as f:
        for i in f.readlines():
            if i[0] != "#":
                num_list.append(int(i))
    f.close()
    print(num_list)
    return num_list

def write_results(string_list):
    with open("result.txt","w") as f:
        for s in string_list:
            f.write(s)
    f.close()

def execution_per_num(number):
    global threadlist,result
    string_list = []
    for num in number:
        
        for threads in threadlist:
            print("Calculating for: ", str(num)," with thread count: ", str(threads))
            splitted = splitUp(num,threads)
            #creating worker object
            worker = Worker()
            #measuring time
            s = time.time()
            # creating the threads
            for arg in splitted:
                thread = threading.Thread(target=worker.multiplier(arg[0],arg[1],num))
                worker.append_job(thread)

            worker.initiate()
            worker.work()
            e = time.time()

            
            prime = result == num-1 # either 1 or zero 
                
            string = str(num) + ":\t" + ("NOT PRIME","PRIME")[prime] + " result found with {} threads in {} secs\n".format(threads,e-s)
            string_list.append(string)
            result = 1
            print(("NOT PRIME","PRIME")[prime])
        string_list.append("\n")
    write_results(string_list)

if __name__ == "__main__":
    num_list = read_nums()
    #num_list = [1,4,7,10]
    execution_per_num(num_list)


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
