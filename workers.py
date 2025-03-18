import multiprocessing
import time

def square(num):
    return num * num

def worker(function, queue_in, queue_out):
    while not queue_in.empty():
        args = queue_in.get()
        if args is None:
            break
        result = function(args)
        queue_out.put(result)

def create_queue(items = []):
    queue = multiprocessing.Manager().Queue()
    for item in items:
        queue.put(item)
    return queue

def create_workers(function, queue_in, queue_out, workers = multiprocessing.cpu_count()):
    processes = []
    print("Worker count:", workers)    
    for _ in range(workers):
        process = multiprocessing.Process(target=worker, args=(function, queue_in, queue_out))
        processes.append(process)
    return processes

def run_processes(processes):
    for process in processes:
        process.start()
    for process in processes:
        process.join()
    

def main():
    queue_in = create_queue(items = range(160))
    queue_out = create_queue()
    processes = create_workers(square, queue_in, queue_out)

    start = time.time()
    run_processes(processes)
    end = time.time()
    print(f"Execution time {end - start:.2f}")

    seznam = []
    while not queue_out.empty():
        seznam.append(queue_out.get())
    print(seznam)

if __name__ == '__main__':
    main()