# PLB_2CE15_0896 - Operating Systems Lab Assignment

## Overview
This repository contains a comprehensive Python implementation of various Operating Systems algorithms and concepts, including:

- **Process Scheduling Algorithms** (FCFS, SJF, Round Robin, Priority)
- **Page Replacement Algorithms** (FIFO, LRU, Optimal)
- **Banker's Algorithm** (Deadlock Avoidance)
- **Disk Scheduling Algorithms** (FCFS, SCAN, C-SCAN)

## Requirements
- Python 3.x

## Usage

Run the program:
```bash
python3 os_lab.py
```

## Features

### 1. Process Scheduling Algorithms
The program implements four major CPU scheduling algorithms:

- **FCFS (First Come First Serve)**: Processes are executed in the order they arrive
- **SJF (Shortest Job First)**: Process with shortest burst time is executed first
- **Round Robin**: Each process gets a fixed time quantum in cyclic order
- **Priority Scheduling**: Processes are executed based on priority (lower number = higher priority)

Each algorithm calculates:
- Waiting time for each process
- Turnaround time for each process
- Average waiting time
- Average turnaround time

### 2. Page Replacement Algorithms
Three page replacement strategies are implemented:

- **FIFO (First In First Out)**: Oldest page in memory is replaced
- **LRU (Least Recently Used)**: Page that hasn't been used for longest time is replaced
- **Optimal**: Page that won't be used for longest time in future is replaced (theoretical)

For each algorithm, the program calculates:
- Total page faults
- Number of hits
- Hit ratio

### 3. Banker's Algorithm
Implements the Banker's Algorithm for deadlock avoidance:
- Determines if system is in safe state
- Finds safe sequence if one exists
- Handles resource requests from processes
- Validates requests and checks for safety before granting

### 4. Disk Scheduling Algorithms
Three disk head scheduling algorithms:

- **FCFS**: Requests are serviced in arrival order
- **SCAN (Elevator)**: Head moves in one direction servicing requests, then reverses
- **C-SCAN (Circular SCAN)**: Head moves in one direction, jumps back to start

Each algorithm provides:
- Seek sequence
- Total seek count
- Average seek time

## Example Output

The program provides detailed output for each algorithm with:
- Input parameters
- Execution steps
- Results and metrics
- Performance comparisons

Sample execution:
```
======================================================================
PROCESS SCHEDULING ALGORITHMS
======================================================================

Process Details:
Process    Burst Time      Priority  
-----------------------------------
P1         5               2         
P2         3               1         
P3         8               3         
P4         6               2         

1. First Come First Serve (FCFS):
-----------------------------------
Average Waiting Time: 7.25
Average Turnaround Time: 12.75
...
```

## Educational Purpose
This program is designed for educational purposes to understand and demonstrate fundamental Operating Systems concepts and algorithms used in:
- Process management
- Memory management
- Disk management
- Deadlock handling

## Author
Operating Systems Lab Assignment - PLB_2CE15_0896
