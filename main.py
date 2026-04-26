import copy # copying process list for different scheduling algorithms

# Process Scheduling Class Structure
class Process:
    def __init__(self, pid, name, arrival_time, burst_time, fuel):
        # pid: Process ID
        self.pid = pid
        self.name = name
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.fuel = fuel
        
        self.priority = self.calculate_priority()
        self.remaining_time = burst_time
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
        
        # pick highest priority and closest arrival_time
        current = min(available, key=lambda x: (x.priority, x.arrival_time))
        
        # remove from ready queue
        ready.remove(current)
        
        # start time is current time, end time is start time + burst time
        start = time
        time += current.burst_time
        end = time
        
        current.completion = end
        
        # add to schedule
        schedule.append((start, end, current.pid))
    
    # print schedule
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
    
    # print schedule
    print_schedule("FCFS Schedule", schedule)    
    
    # print process table  
    print_metrics(processes)
    
    return schedule

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

# scheduling order function gantt chart
def print_schedule(title, schedule):
    print(f"\n======= {title} =======")
    print("Gantt Chart:")
    print("-" * 40)
    
    # loop through schedule to display start time, end time and its pid
    for start, end, pid in schedule:
        print(f"| {start:>2} -> {end:<2} | {pid}")

    print("-" * 40)
    
    
def main():
    # Sample 
    processes = [
        Process("P1", "AB101", 0, 7, fuel=10),
        Process("P2", "BC202", 1, 4, fuel=50),
        Process("P3", "CD303", 2, 6, fuel=25),
        Process("P4", "DE404", 3, 5, fuel=25),
    ]
    
    # Print out processes 
    print("\nInitial Process/Arriving Plane List:")
    print("-" * 40)
    print(f"{'PID':<5}{'Plane':<12}{'AT':<5}{'BT':<5}{'Fuel(PR)':<10}")
    print("-" * 40)
    for p in processes:
        print(f"{p.pid:<5}{p.name:<12}{p.arrival_time:<5}{p.burst_time:<5}{str(p.fuel) + '%':<10}")
    print("-" * 40)
    print()
    
    # priority algorithm
    priority_scheduling(copy.deepcopy(processes))
    
    # fcfs algorithm
    fcfs(copy.deepcopy(processes))
    
    
if __name__ == "__main__":
    main()
