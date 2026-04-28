import copy # copying process list for different scheduling algorithms
from collections import deque # use for round robin queue

# Process Scheduling Class Structure
class Process:
    def __init__(self, pid, name, arrival_time, burst_time, fuel):
        # pid: Process ID
        self.pid = pid
        self.name = name
        self.arrival_time = arrival_time
        # time for process to finish execution excluding wait time
        self.burst_time = burst_time
        self.fuel = fuel
        
        self.priority = self.calculate_priority()
        # time remaining to finish process
        self.remaining_time = burst_time
        # time finished
        self.completion = 0
        self.start = -1
    
    # calculate priority based on fuel left
    def calculate_priority(self):
        # lower fuel = higher priority
        if self.fuel <= 10:
            return 1
        elif self.fuel <= 25:
            return 2
        else:
            return 3

# Priority Scheduling Algorithm
def priority_scheduling(processes):
    # Current system time
    time = 0
    # Hold start_time, end_time, and pid for each scheduled process
    schedule = []
    
    # copy process list to represent ready queue
    ready = processes.copy()
    
    # loop until ready queue is empty
    while ready:
        # get processes that are available
        available = [p for p in ready if p.arrival_time <= time]
        
        # if not available, move time forward
        if not available:
            time += 1
            continue
        
        # pick highest priority and arrival_time as tie-breaker
        current = min(available, key=lambda x: (x.priority, x.arrival_time))
        
        # remove from ready queue
        ready.remove(current)
        
        # start time is current time, end time is start time + burst time
        start = time
        time += current.burst_time
        
        # update process completion time
        end = time
        current.completion = end
        
        # add to schedule
        schedule.append((start, end, current.pid))
    
    # print schedule order
    print_schedule("Priority Schedule", schedule)
    
    # print process table      
    print_metrics(processes)
    
    return schedule

# First-Come, First-Served Scheduling Algorithm   
def fcfs(processes):
    # sort by arrival time
    processes.sort(key = lambda x: x.arrival_time)
    # Current system time
    time = 0
    # Hold start_time, end_time, and pid for each scheduled process
    schedule = []
    
    # loop through each process by arrival time
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
    
    # print schedule order
    print_schedule("FCFS Schedule", schedule)    
    
    # print process table  
    print_metrics(processes)
    
    return schedule

# Round Robin Scheduling Algorithm
def round_robin(processes, quantum):
    # Current system time
    time = 0
   
    # Queue to hold processes that are ready
    ready_queue = deque()
   
    # Hold start_time, end_time, and pid for each scheduled process
    schedule = []
   
    # Sort proccesses by arrival time
    processes.sort(key=lambda x: x.arrival_time)
   
    # Track processes that have been added to the queue
    i = 0
    n = len(processes)
   
    # loop until all processes are completed
    while i < n or ready_queue:
       
        # Add processes that have arrived by current time ot ready_queue
        # Before execution on who is ready right now
        while i < n and processes[i].arrival_time <= time:
            ready_queue.append(processes[i])
            i += 1
       
        # If no process is ready, move time forward
        if not ready_queue:
            time += 1
            continue
       
        # Get next process in queue (First in, First Out)
        current = ready_queue.popleft()
       
        # Record start time
        start = time
       
        # Execute process by either quantum time or remaining time, whether one is smaller
        execution_time = min(quantum, current.remaining_time)
       
        time += execution_time
        current.remaining_time -= execution_time
       
        end = time
       
        # Add to schedule
        schedule.append((start, end, current.pid))
       
        # Add newly arrived processes during execution
        # Proccesses who became ready during the execution time of the previous process
        while i < n and processes[i].arrival_time <= time:
            ready_queue.append(processes[i])
            i += 1
       
        # If proccess is not finished in time, re-add it to queue
        if current.remaining_time > 0:
            ready_queue.append(current)
        else:
            # Process finished, record completion time
            current.completion = time
       
    # Print schedule order
    print_schedule("Round Robin Schedule", schedule, rr=True)
    # Print process table
    print_metrics(processes)
       
    return schedule
            
# scheduling order function gantt chart
def print_schedule(title, schedule, rr=False):
    print(f"\n======= {title} =======")
    print("Gantt Chart:")
    print("-" * 40)
    
    # loop through schedule to display start time, end time and its pid
    for start, end, pid in schedule:
        print(f"| {start:>2} -> {end:<2} | {pid}")

    print("-" * 40)
    
    # for round robin, add context switches output
    if rr:
        # Number of times the CPU stops running one process and starts/switch to running another process
        print(f"Context Switches: {len(schedule) - 1}")
    
# Output metric calculation for turnaround time and waiting time
def print_metrics(processes):
    total_turnaroundTime = 0
    total_waitTime = 0
    
    # Sort by PID for consistent output
    processes.sort(key=lambda p: p.pid)
    
    
    print("\nProcess Table: ")
    print("-" * 40)
    
    # CT = Completion Time, TAT = Turnaround Time, WT = Waiting Time
    print(f"{'PID':<5}{'AT':<5}{'BT':<5}{'PR':<5}{'CT':<5}{'TAT':<7}{'WT':<5}")
    print("-" * 40)
    
    
    for p in processes:
        # Calculate Turnaround Time and Waiting Time
        turnaround_time = p.completion - p.arrival_time
        wait_time = turnaround_time - p.burst_time
        
        total_turnaroundTime += turnaround_time
        total_waitTime += wait_time
        
        # 
        print(f"{p.pid:<5}{p.arrival_time:<5}{p.burst_time:<5}{p.priority:<5}{p.completion:<5}{turnaround_time:<7}{wait_time:<5}")
    
    total_processes = len(processes)
    
    print("-" * 40)
    print(f"Average Turnaround Time: {total_turnaroundTime / total_processes:.2f}")
    print(f"Average Waiting Time: {total_waitTime / total_processes:.2f}")

    
def main():
    # Data
    arriving_processes = [
        Process("P1", "AB101", 0, 7, fuel=50),  # low priority, arrives first
        Process("P2", "BC202", 0, 4, fuel=10),  # high priority, arrives same time as P1
        Process("P3", "CD303", 2, 6, fuel=25),  # medium
        Process("P4", "DE404", 3, 5, fuel=25),  # same priority as P3 (tie case)
        Process("P5", "EF505", 4, 3, fuel=10),  # another high priority
    ]
    
    # fuel does not matter for the rr
    departing_proccesses = [
        Process("D1", "EF505", arrival_time=0, burst_time=4, fuel=0),
        Process("D2", "FG606", arrival_time=0, burst_time=2, fuel=0),
        Process("D3", "GH707", arrival_time=1, burst_time=6, fuel=0),  # long burst time
        Process("D4", "HI808", arrival_time=2, burst_time=3, fuel=0),
    ]
    
    
    
    # Print out processes 
    print("\nArriving Plane List:")
    print("-" * 40)
    print(f"{'PID':<5}{'Plane':<12}{'AT':<5}{'BT':<5}{'Fuel(PR)':<10}")
    print("-" * 40)
    for p in arriving_processes:
        print(f"{p.pid:<5}{p.name:<12}{p.arrival_time:<5}{p.burst_time:<5}{str(p.fuel) + '%':<10}")
    print("-" * 40)
    
    # priority algorithm
    priority_scheduling(copy.deepcopy(arriving_processes))
    
    # fcfs algorithm
    fcfs(copy.deepcopy(arriving_processes))
    
    print("\nDeparting Plane List:")
    print("-" * 40)
    print(f"{'PID':<5}{'Plane':<12}{'AT':<5}{'BT':<5}{'Fuel(PR)':<10}")
    print("-" * 40)
    for p in departing_proccesses:
        print(f"{p.pid:<5}{p.name:<12}{p.arrival_time:<5}{p.burst_time:<5}{str(p.fuel) + '%':<10}")
    print("-" * 40)
    
    
    # round robin algorithm
    round_robin(copy.deepcopy(departing_proccesses), quantum=4)
    
    
if __name__ == "__main__":
    main()
