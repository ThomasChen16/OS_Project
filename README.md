# OS_Project
Operating System Project

## Overview
Air Traffic Control
The air traffic controller has a large influx of arriving planes that need to land on the runway and dock at an available terminal, and departing planes that need to take off from the same runway, at around the same time. In this scenario, a priority algorithm will need to be created to determine which arriving planes can land on the runway based on the amount of fuel, starting with the arriving planes that have the least amount of fuel left over. Additionally, we need to create a queueing algorithm that will allow arriving planes that land on the runway first to dock at a terminal first, and another queueing algorithm that will give departing planes a fixed amount of time on the runway to fully take off.


## Algorithms Implemented
# Non-preemptive Priority Scheduling:
This algorithm has been implemented for the arrival of planes and will give priority to those that have the lowest fuel percentage. This algorithm works by giving the lowest fueled plane the highest priority, then it'll select the plane with the highest priority to be processed so it can land and if there are multiple planes with the same level of priority it'll use FCFS to determine which plane goes next. Finally after the plane is processed and lands it'll loop back and process the next plaen until the list is complete. 
Input: Plane ID, Arrival Time, Burst time, Fuel (Percentage based)
Output: Turn Around Time, Waiting Time

# First Come First Serve Scheduling:
This algorithm has also been implemented for after the planes land and are needed to be processed to a terminal to dock. This processes all planes by order of arrival, meaning that none of the planes are given priority in this instance, making it a fair process even if some planes can be processed faster than others. If some planes do somehow arrive at the same time the plane that arrived first in the list would be given priority.
Input: Plane ID, Arrival Time, Burst time, Fuel (Is ignored in this instance)
Output: Turn Around Time, Waiting Time

# Round Robin Scheduling: 
The algorithm was chosen and implemented for the departure of the planes, it entirely ignores the fuel percentage of each plane and processes them in a FIFO order, however this makes sure that each of the planes are all processed in a fixed quantum time so that all of the planes have departed within a certain amount of time. If a plane is not able to depart within the given quantum it is then placed in the back of the queue so the other planes can be processed in time.
Input: Plane ID, Arrival Time, Burst time, Fuel (Percentage based), Quantum is fixed to 4 minutes
Output: Turn Around Time, Waiting Time
