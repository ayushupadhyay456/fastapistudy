import threading #inbuilt in python
import time
import concurrent.futures #used to run thredapoolexecutor that helps in making a pool of threads,distributes task in threads
#allows to define max_workers of threads so as to avoid CPU Crash.If i will keep max_worker=10000000000 CPu will crash

def hello_world():
    thread_name=threading.current_thread().name
    time.sleep(1)
    print(f"Hello from {thread_name}")

def task(n):
    print(f"starting{n}")
    time.sleep(n)
    return f"Done{n}"


if __name__=='__main__':
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        futures={executor.submit(task,i): i for i in range(1,4)}
        for future in concurrent.futures.as_completed(futures):
            print((future.result()))
    t1=threading.Thread(target=hello_world,name="thread1")
    t2=threading.Thread(target=hello_world,name="thread2")

    t1.start()
    t2.start()
    t1.join()
    t2.join()












