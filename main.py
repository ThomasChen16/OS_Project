import copy # copying process list for different scheduling algorithms

# Process Scheduling Class Structure
class Process:
    def __init__(self, pid, arrival_time, burst_time, priority=0):
        # pid: Process ID
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.priority = priority
        
        self.remaining_time = burst_time
        self.completion = 0
        self.start = -1

# First-Come, First-Served Scheduling Algorithm   
def fcfs(processes):
    # sort by arrival time
    processes.sort(key = lambda x: x.arrival_time)
    # Current system time
    time = 0
    # Hold start_time, end_time, and pid for each scheduled process
    schedule = []
    
    # for each process, calculate start and end time, and update completion time
    for process in processes:
        # if process arrives after current time, move time forward to arrival time
        if time < process.arrival_time:
            time = process.arrival_time
        
        # start time is current time, end time is start time + burst time
        start = time
        time += process.burst_time
        end = time
        
        # update process completion time
        process.completion = end
        
        # add to schedule
        schedule.append((start, end, process.pid))
        
    print("\nFCFS Schedule:")
    for start, end, pid in schedule:
        print(f"({start} -> {end}) PID: {pid}")
        
    print_metrics(processes)
    return schedule

# Priorioty Scheduling Algorithm
def priority_scheduling(processes):
    # Current system time
    time = 0
    # Hold start_time, end_time, and pid for each scheduled process
    schedule = []
    
    ready = processes.copy()
    
    while ready:
        # get processes that are available
        available = [p for p in ready if p.arrival_time <= time]
        
        # if not available, move time forward
        if not available:
            time += 1
            continue
        
        # pick highest priority (lowest number)
        current = min(available, key=lambda x: x.priority)
        
        # remove from ready queue
        ready.remove(current)
        
        # start time is current time, end time is start time + burst time
        start = time
        time += current.burst_time
        end = time
        
        current.completion = end
        
        # add to schedule
        schedule.append((start, end, current.pid))
        
    print("\nPriority Schedule:")
    for start, end, pid in schedule:
        print(f"({start} -> {end}) PID: {pid}")
            
    print_metrics(processes)
    return schedule

# Output metric calculation for turnaround time and waiting time
def print_metrics(processes):
    total_turnaroundTime = 0
    total_waitTime = 0
    
    # CT = Completion Time, TAT = Turnaround Time, WT = Waiting Time
    print("\nPID | CT | TAT | WT")
    
    
    for p in processes:
        # Calculate Turnaround Time and Waiting Time
        turnaround_time = p.completion - p.arrival_time
        wait_time = turnaround_time - p.burst_time
        
        total_turnaroundTime += turnaround_time
        total_waitTime += wait_time
        
        print(f"{p.pid}  | {p.completion}  | {turnaround_time}   | {wait_time}")
    
    total_processes = len(processes)
    
    print(f"\nAverage Turnaround Time: {total_turnaroundTime / total_processes:.2f}")
    print(f"Average Waiting Time: {total_waitTime / total_processes:.2f}")
    
        

def main():
    # Sample 
    processes = [
        Process("P1", 0, 7, priority=3),
        Process("P2", 1, 4, priority=1),
        Process("P3", 2, 6, priority=4),
        Process("P4", 3, 5, priority=2),
        Process("P5", 4, 3, priority=1),
        Process("P6", 6, 2, priority=5),
    ]
    
    
    fcfs(copy.deepcopy(processes))
    priority_scheduling(copy.deepcopy(processes))
    
if __name__ == "__main__":
    main()
