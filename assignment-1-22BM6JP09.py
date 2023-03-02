import os
import threading
import re
import sys
import time


# exceptions... 
if len(sys.argv)!=5:
    print("Number of arguments not sufficient to run the program")
    exit()
if int(sys.argv[2]) == 0:
    print("Number of threads cannot be zero ")
    exit()
if int(sys.argv[3]) == 0:
    print("Number of grams cannot be zero")
    exit()
if int(sys.argv[4]) == 0:
    print(" k cannot be zero")
    exit()


# getting the input variable 
data_path = sys.argv[1]
no_thread = min(int(sys.argv[2]),len(os.listdir(data_path)))
no_gram = int(sys.argv[3])
no_k = int(sys.argv[4])

# creating some global variable to accessed by all functions below ...
regex = '[^a-zA-Z0-9]+'
lines = {}
n_gram = {}
score = {}


"""
function to read files and extract words
"""
def data_util(batch):
    for c in batch:
        lines[c] = []
        files = os.listdir(os.path.join(data_path,c))
        for file in files:
            with open(os.path.join(data_path,c,file),encoding="latin-1") as f:
                lines[c].append(re.split(regex,f.read().lower()))

"""
function to create and score the ngrams 
"""
def ngram_score(batch):
    for c in batch:
        score[c] = {}
        for file in lines[c]:
            for i in range(len(file)-no_gram+1):
                gram = " ".join(file[i:i+no_gram])
                if gram in score[c]:
                    score[c][gram] = score[c][gram] + 1
                else:
                    score[c][gram] = 1
        for key,value in score[c].items():
            score[c][key] = value/len(lines[c])

"""
function to sort and print Top_k ngrams
"""
def result_topk():
    for c in score.keys():
        for gram in score[c].keys():
            if gram not in n_gram.keys():
                n_gram[gram] = score[c][gram]
            else:
                n_gram[gram] = max(n_gram[gram],score[c][gram])
    sorted_n_gram = sorted(n_gram.items(), reverse=True, key= lambda x: x[1])
    for i,topk in zip(range(no_k),sorted_n_gram[:no_k]):
        print("Top-{}".format(i+1,no_gram),"-",topk)


# main function to execute everything 
def main():
    folders = os.listdir(data_path)
    batches = []
    for i in range(0,len(folders),no_thread):
        folder = []
        for j in range(i,i+no_thread):
            folder.append(folders[j])
        batches.append(folder)
    thread_list = []
    for i,batch in enumerate(batches):
        thread = threading.Thread(target=data_util,args=([batch])) 
        thread.start()
        thread_list.append(thread)
    for t in thread_list:
        t.join()
    for i,batch in enumerate(batches):
        thread = threading.Thread(target=ngram_score,args=([batch])) 
        thread.start()
        thread_list.append(thread)
    for t in thread_list:
        t.join()
    result_topk()

# calculating the time taken for multithreading 
startTime = time.time()
main()
endTime = time.time()
print("Time taken by the program - {}s".format(int((endTime-startTime))))

