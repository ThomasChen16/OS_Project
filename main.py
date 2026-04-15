# Process Scheduling Class Structure
class Process:
    def __init__(self, pid, arrival_time, burst_time, priority=0):
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
    
    time = 0
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
    for s in schedule:
        print(f"Time {s}")
        
    return schedule

def main():
    # Sample 
    processes = [
        Process(pid=1, arrival_time=0, burst_time=5),
        Process(pid=2, arrival_time=2, burst_time=3),
        Process(pid=3, arrival_time=4, burst_time=1)
    ]
    
    print(fcfs(processes))
    
if __name__ == "__main__":
    main()