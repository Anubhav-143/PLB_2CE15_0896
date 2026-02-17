"""
Operating Systems Lab Assignment
This program implements various OS algorithms and concepts including:
1. Process Scheduling Algorithms (FCFS, SJF, Round Robin, Priority)
2. Page Replacement Algorithms (FIFO, LRU, Optimal)
3. Banker's Algorithm for Deadlock Avoidance
4. Disk Scheduling Algorithms (FCFS, SCAN, C-SCAN)
"""

import sys
from collections import deque


class ProcessScheduling:
    """Process Scheduling Algorithms"""
    
    @staticmethod
    def fcfs(processes):
        """First Come First Serve (FCFS) Scheduling"""
        n = len(processes)
        waiting_time = [0] * n
        turnaround_time = [0] * n
        
        # Calculate waiting time
        for i in range(1, n):
            waiting_time[i] = processes[i-1]['burst'] + waiting_time[i-1]
        
        # Calculate turnaround time
        for i in range(n):
            turnaround_time[i] = processes[i]['burst'] + waiting_time[i]
        
        return {
            'waiting_time': waiting_time,
            'turnaround_time': turnaround_time,
            'avg_waiting_time': sum(waiting_time) / n,
            'avg_turnaround_time': sum(turnaround_time) / n
        }
    
    @staticmethod
    def sjf(processes):
        """Shortest Job First (SJF) Scheduling"""
        n = len(processes)
        sorted_processes = sorted(enumerate(processes), key=lambda x: x[1]['burst'])
        waiting_time = [0] * n
        turnaround_time = [0] * n
        
        for i in range(1, n):
            waiting_time[sorted_processes[i][0]] = (
                processes[sorted_processes[i-1][0]]['burst'] + 
                waiting_time[sorted_processes[i-1][0]]
            )
        
        for i in range(n):
            turnaround_time[i] = processes[i]['burst'] + waiting_time[i]
        
        return {
            'waiting_time': waiting_time,
            'turnaround_time': turnaround_time,
            'avg_waiting_time': sum(waiting_time) / n,
            'avg_turnaround_time': sum(turnaround_time) / n,
            'order': [p[1]['pid'] for p in sorted_processes]
        }
    
    @staticmethod
    def round_robin(processes, quantum):
        """Round Robin Scheduling"""
        n = len(processes)
        remaining_burst = [p['burst'] for p in processes]
        waiting_time = [0] * n
        turnaround_time = [0] * n
        current_time = 0
        
        queue = deque(range(n))
        
        while queue:
            i = queue.popleft()
            
            if remaining_burst[i] > quantum:
                current_time += quantum
                remaining_burst[i] -= quantum
                queue.append(i)
            else:
                current_time += remaining_burst[i]
                waiting_time[i] = current_time - processes[i]['burst']
                remaining_burst[i] = 0
        
        for i in range(n):
            turnaround_time[i] = processes[i]['burst'] + waiting_time[i]
        
        return {
            'waiting_time': waiting_time,
            'turnaround_time': turnaround_time,
            'avg_waiting_time': sum(waiting_time) / n,
            'avg_turnaround_time': sum(turnaround_time) / n
        }
    
    @staticmethod
    def priority_scheduling(processes):
        """Priority Scheduling (Lower number = Higher priority)"""
        n = len(processes)
        sorted_processes = sorted(enumerate(processes), key=lambda x: x[1]['priority'])
        waiting_time = [0] * n
        turnaround_time = [0] * n
        
        for i in range(1, n):
            waiting_time[sorted_processes[i][0]] = (
                processes[sorted_processes[i-1][0]]['burst'] + 
                waiting_time[sorted_processes[i-1][0]]
            )
        
        for i in range(n):
            turnaround_time[i] = processes[i]['burst'] + waiting_time[i]
        
        return {
            'waiting_time': waiting_time,
            'turnaround_time': turnaround_time,
            'avg_waiting_time': sum(waiting_time) / n,
            'avg_turnaround_time': sum(turnaround_time) / n,
            'order': [p[1]['pid'] for p in sorted_processes]
        }


class PageReplacement:
    """Page Replacement Algorithms"""
    
    @staticmethod
    def fifo(pages, frame_count):
        """First In First Out (FIFO) Page Replacement"""
        frames = []
        page_faults = 0
        hits = 0
        
        for page in pages:
            if page not in frames:
                page_faults += 1
                if len(frames) < frame_count:
                    frames.append(page)
                else:
                    frames.pop(0)
                    frames.append(page)
            else:
                hits += 1
        
        return {
            'page_faults': page_faults,
            'hits': hits,
            'hit_ratio': hits / len(pages) if pages else 0
        }
    
    @staticmethod
    def lru(pages, frame_count):
        """Least Recently Used (LRU) Page Replacement"""
        frames = []
        page_faults = 0
        hits = 0
        recent_use = {}
        
        for i, page in enumerate(pages):
            if page not in frames:
                page_faults += 1
                if len(frames) < frame_count:
                    frames.append(page)
                else:
                    # Find least recently used page (minimum timestamp)
                    lru_page = min(frames, key=lambda x: recent_use[x])
                    frames.remove(lru_page)
                    frames.append(page)
            else:
                hits += 1
            
            recent_use[page] = i
        
        return {
            'page_faults': page_faults,
            'hits': hits,
            'hit_ratio': hits / len(pages) if pages else 0
        }
    
    @staticmethod
    def optimal(pages, frame_count):
        """Optimal Page Replacement"""
        frames = []
        page_faults = 0
        hits = 0
        
        for i, page in enumerate(pages):
            if page not in frames:
                page_faults += 1
                if len(frames) < frame_count:
                    frames.append(page)
                else:
                    # Find page that will be used farthest in future
                    future_use = {}
                    for frame_page in frames:
                        try:
                            future_use[frame_page] = pages[i+1:].index(frame_page)
                        except ValueError:
                            future_use[frame_page] = float('inf')
                    
                    page_to_replace = max(frames, key=lambda x: future_use[x])
                    frames.remove(page_to_replace)
                    frames.append(page)
            else:
                hits += 1
        
        return {
            'page_faults': page_faults,
            'hits': hits,
            'hit_ratio': hits / len(pages) if pages else 0
        }


class BankersAlgorithm:
    """Banker's Algorithm for Deadlock Avoidance"""
    
    def __init__(self, available, maximum, allocation):
        self.available = available
        self.maximum = maximum
        self.allocation = allocation
        self.need = [[maximum[i][j] - allocation[i][j] 
                     for j in range(len(maximum[0]))] 
                     for i in range(len(maximum))]
    
    def is_safe(self):
        """Check if the system is in a safe state"""
        work = self.available[:]
        finish = [False] * len(self.allocation)
        safe_sequence = []
        
        while len(safe_sequence) < len(self.allocation):
            found = False
            for i in range(len(self.allocation)):
                if not finish[i]:
                    if all(self.need[i][j] <= work[j] for j in range(len(work))):
                        # Process can complete
                        for j in range(len(work)):
                            work[j] += self.allocation[i][j]
                        finish[i] = True
                        safe_sequence.append(i)
                        found = True
                        break
            
            if not found:
                return False, []
        
        return True, safe_sequence
    
    def request_resources(self, process_id, request):
        """Request resources for a process"""
        # Check if request is valid
        if any(request[i] > self.need[process_id][i] for i in range(len(request))):
            return False, "Request exceeds need"
        
        if any(request[i] > self.available[i] for i in range(len(request))):
            return False, "Resources not available"
        
        # Try allocation
        for i in range(len(request)):
            self.available[i] -= request[i]
            self.allocation[process_id][i] += request[i]
            self.need[process_id][i] -= request[i]
        
        # Check if safe
        safe, sequence = self.is_safe()
        
        if not safe:
            # Rollback
            for i in range(len(request)):
                self.available[i] += request[i]
                self.allocation[process_id][i] -= request[i]
                self.need[process_id][i] += request[i]
            return False, "Unsafe state"
        
        return True, f"Request granted. Safe sequence: {sequence}"


class DiskScheduling:
    """Disk Scheduling Algorithms"""
    
    @staticmethod
    def fcfs(requests, head):
        """First Come First Serve Disk Scheduling"""
        seek_count = 0
        current = head
        sequence = [head]
        
        for request in requests:
            seek_count += abs(current - request)
            current = request
            sequence.append(current)
        
        return {
            'seek_count': seek_count,
            'avg_seek': seek_count / len(requests) if requests else 0,
            'sequence': sequence
        }
    
    @staticmethod
    def scan(requests, head, disk_size, direction='right'):
        """SCAN (Elevator) Disk Scheduling"""
        seek_count = 0
        current = head
        sequence = [head]
        
        left = sorted([r for r in requests if r < head])
        right = sorted([r for r in requests if r >= head])
        
        if direction == 'right':
            # Move right first
            for request in right:
                seek_count += abs(current - request)
                current = request
                sequence.append(current)
            
            if right and current != disk_size - 1:
                seek_count += abs(current - (disk_size - 1))
                current = disk_size - 1
                sequence.append(current)
            
            # Then move left
            for request in reversed(left):
                seek_count += abs(current - request)
                current = request
                sequence.append(current)
        else:
            # Move left first
            for request in reversed(left):
                seek_count += abs(current - request)
                current = request
                sequence.append(current)
            
            if left and current != 0:
                seek_count += abs(current - 0)
                current = 0
                sequence.append(current)
            
            # Then move right
            for request in right:
                seek_count += abs(current - request)
                current = request
                sequence.append(current)
        
        return {
            'seek_count': seek_count,
            'avg_seek': seek_count / len(requests) if requests else 0,
            'sequence': sequence
        }
    
    @staticmethod
    def cscan(requests, head, disk_size):
        """C-SCAN (Circular SCAN) Disk Scheduling
        
        In C-SCAN, the head moves from one end to the other servicing requests,
        then returns to the beginning without servicing requests on return.
        """
        seek_count = 0
        current = head
        sequence = [head]
        
        left = sorted([r for r in requests if r < head])
        right = sorted([r for r in requests if r >= head])
        
        # Move right
        for request in right:
            seek_count += abs(current - request)
            current = request
            sequence.append(current)
        
        # Go to end if not already there
        if right and current != disk_size - 1:
            seek_count += abs(current - (disk_size - 1))
            current = disk_size - 1
            sequence.append(current)
        
        # Return to beginning (circular jump) and service remaining requests
        if left:
            # In C-SCAN, we jump back to start - count the full movement
            seek_count += current  # Distance from current to 0
            current = 0
            sequence.append(current)
            
            # Service remaining requests
            for request in left:
                seek_count += abs(current - request)
                current = request
                sequence.append(current)
        
        return {
            'seek_count': seek_count,
            'avg_seek': seek_count / len(requests) if requests else 0,
            'sequence': sequence
        }


def demonstrate_scheduling():
    """Demonstrate Process Scheduling Algorithms"""
    print("=" * 70)
    print("PROCESS SCHEDULING ALGORITHMS")
    print("=" * 70)
    
    processes = [
        {'pid': 'P1', 'burst': 5, 'priority': 2},
        {'pid': 'P2', 'burst': 3, 'priority': 1},
        {'pid': 'P3', 'burst': 8, 'priority': 3},
        {'pid': 'P4', 'burst': 6, 'priority': 2}
    ]
    
    print("\nProcess Details:")
    print(f"{'Process':<10} {'Burst Time':<15} {'Priority':<10}")
    print("-" * 35)
    for p in processes:
        print(f"{p['pid']:<10} {p['burst']:<15} {p['priority']:<10}")
    
    # FCFS
    print("\n1. First Come First Serve (FCFS):")
    print("-" * 35)
    result = ProcessScheduling.fcfs(processes)
    print(f"Average Waiting Time: {result['avg_waiting_time']:.2f}")
    print(f"Average Turnaround Time: {result['avg_turnaround_time']:.2f}")
    
    # SJF
    print("\n2. Shortest Job First (SJF):")
    print("-" * 35)
    result = ProcessScheduling.sjf(processes)
    print(f"Execution Order: {' -> '.join(result['order'])}")
    print(f"Average Waiting Time: {result['avg_waiting_time']:.2f}")
    print(f"Average Turnaround Time: {result['avg_turnaround_time']:.2f}")
    
    # Round Robin
    print("\n3. Round Robin (Quantum = 2):")
    print("-" * 35)
    result = ProcessScheduling.round_robin(processes, 2)
    print(f"Average Waiting Time: {result['avg_waiting_time']:.2f}")
    print(f"Average Turnaround Time: {result['avg_turnaround_time']:.2f}")
    
    # Priority
    print("\n4. Priority Scheduling:")
    print("-" * 35)
    result = ProcessScheduling.priority_scheduling(processes)
    print(f"Execution Order: {' -> '.join(result['order'])}")
    print(f"Average Waiting Time: {result['avg_waiting_time']:.2f}")
    print(f"Average Turnaround Time: {result['avg_turnaround_time']:.2f}")


def demonstrate_page_replacement():
    """Demonstrate Page Replacement Algorithms"""
    print("\n" + "=" * 70)
    print("PAGE REPLACEMENT ALGORITHMS")
    print("=" * 70)
    
    pages = [7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2, 1, 2, 0, 1, 7, 0, 1]
    frame_count = 3
    
    print(f"\nPage Reference String: {pages}")
    print(f"Number of Frames: {frame_count}")
    
    # FIFO
    print("\n1. FIFO (First In First Out):")
    print("-" * 35)
    result = PageReplacement.fifo(pages, frame_count)
    print(f"Page Faults: {result['page_faults']}")
    print(f"Hits: {result['hits']}")
    print(f"Hit Ratio: {result['hit_ratio']:.2%}")
    
    # LRU
    print("\n2. LRU (Least Recently Used):")
    print("-" * 35)
    result = PageReplacement.lru(pages, frame_count)
    print(f"Page Faults: {result['page_faults']}")
    print(f"Hits: {result['hits']}")
    print(f"Hit Ratio: {result['hit_ratio']:.2%}")
    
    # Optimal
    print("\n3. Optimal Page Replacement:")
    print("-" * 35)
    result = PageReplacement.optimal(pages, frame_count)
    print(f"Page Faults: {result['page_faults']}")
    print(f"Hits: {result['hits']}")
    print(f"Hit Ratio: {result['hit_ratio']:.2%}")


def demonstrate_bankers():
    """Demonstrate Banker's Algorithm"""
    print("\n" + "=" * 70)
    print("BANKER'S ALGORITHM FOR DEADLOCK AVOIDANCE")
    print("=" * 70)
    
    available = [3, 3, 2]
    maximum = [
        [7, 5, 3],
        [3, 2, 2],
        [9, 0, 2],
        [2, 2, 2],
        [4, 3, 3]
    ]
    allocation = [
        [0, 1, 0],
        [2, 0, 0],
        [3, 0, 2],
        [2, 1, 1],
        [0, 0, 2]
    ]
    
    print("\nAvailable Resources: A=3, B=3, C=2")
    print("\nAllocation and Maximum Matrices:")
    print(f"{'Process':<10} {'Allocation':<20} {'Maximum':<20} {'Need':<20}")
    print("-" * 70)
    
    banker = BankersAlgorithm(available, maximum, allocation)
    
    for i in range(len(allocation)):
        alloc_str = f"({allocation[i][0]}, {allocation[i][1]}, {allocation[i][2]})"
        max_str = f"({maximum[i][0]}, {maximum[i][1]}, {maximum[i][2]})"
        need_str = f"({banker.need[i][0]}, {banker.need[i][1]}, {banker.need[i][2]})"
        print(f"P{i:<9} {alloc_str:<20} {max_str:<20} {need_str:<20}")
    
    safe, sequence = banker.is_safe()
    print(f"\nSystem is {'SAFE' if safe else 'UNSAFE'}")
    if safe:
        print(f"Safe Sequence: P{' -> P'.join(map(str, sequence))}")
    
    # Test a resource request
    print("\n\nTesting Resource Request:")
    print("Process P1 requests (1, 0, 2)")
    success, message = banker.request_resources(1, [1, 0, 2])
    print(f"Result: {message}")


def demonstrate_disk_scheduling():
    """Demonstrate Disk Scheduling Algorithms"""
    print("\n" + "=" * 70)
    print("DISK SCHEDULING ALGORITHMS")
    print("=" * 70)
    
    requests = [98, 183, 37, 122, 14, 124, 65, 67]
    head = 53
    disk_size = 200
    
    print(f"\nDisk Queue: {requests}")
    print(f"Initial Head Position: {head}")
    print(f"Disk Size: {disk_size}")
    
    # FCFS
    print("\n1. FCFS (First Come First Serve):")
    print("-" * 35)
    result = DiskScheduling.fcfs(requests, head)
    print(f"Seek Sequence: {' -> '.join(map(str, result['sequence']))}")
    print(f"Total Seek Count: {result['seek_count']}")
    print(f"Average Seek: {result['avg_seek']:.2f}")
    
    # SCAN
    print("\n2. SCAN (Elevator Algorithm):")
    print("-" * 35)
    result = DiskScheduling.scan(requests, head, disk_size, 'right')
    print(f"Seek Sequence: {' -> '.join(map(str, result['sequence']))}")
    print(f"Total Seek Count: {result['seek_count']}")
    print(f"Average Seek: {result['avg_seek']:.2f}")
    
    # C-SCAN
    print("\n3. C-SCAN (Circular SCAN):")
    print("-" * 35)
    result = DiskScheduling.cscan(requests, head, disk_size)
    print(f"Seek Sequence: {' -> '.join(map(str, result['sequence']))}")
    print(f"Total Seek Count: {result['seek_count']}")
    print(f"Average Seek: {result['avg_seek']:.2f}")


def main():
    """Main function to demonstrate all OS algorithms"""
    print("\n")
    print("*" * 70)
    print("*" + " " * 68 + "*")
    print("*" + " " * 15 + "OPERATING SYSTEMS LAB ASSIGNMENT" + " " * 21 + "*")
    print("*" + " " * 68 + "*")
    print("*" * 70)
    
    try:
        demonstrate_scheduling()
        demonstrate_page_replacement()
        demonstrate_bankers()
        demonstrate_disk_scheduling()
        
        print("\n" + "=" * 70)
        print("ALL DEMONSTRATIONS COMPLETED SUCCESSFULLY!")
        print("=" * 70 + "\n")
        
    except Exception as e:
        print(f"\nError: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
