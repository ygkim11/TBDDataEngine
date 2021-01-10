from multiprocessing import Process, Queue, cpu_count

def create_queues(count):
    q_list = []
    for i in range(count):
        q_list.append(Queue())
    return tuple(q_list)

def create_processes(queues, func):
    p_list = []
    for i in range(len(queues)):
        p_list.append(Process(target=func, args=(i, queues[i])))
    return tuple(p_list)

def start_processes(processes):
    return tuple([p.start() for p in processes])

def send_to_queues(queues, message):
    return tuple([q.put(message) for q in queues])

def join_processes(processes):
    return tuple([p.join() for p in processes])