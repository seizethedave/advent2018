from collections import defaultdict
import heapq

NUM_WORKERS = 5

class Worker(object):
    def __init__(self, name):
        self.name = name
        self.available_time = 0
        self.current_task = None

    def __lt__(self, other):
        return self.available_time < other.available_time

    def __repr__(self):
        return "<{} finished at {}>".format(self.current_task, self.available_time)

def task_time(task_char):
    return ord(task_char) - ord('A') + 1 + 60

def go():
    dependents = defaultdict(set)
    indegree = defaultdict(int)

    with open("advent07.txt", "r") as f:
        for line in f:
            prerequisite, dependent = line[5], line[36]
            dependents[prerequisite].add(dependent)
            indegree.setdefault(prerequisite, 0)
            indegree[dependent] += 1

    heap = [step for step, deg in indegree.iteritems() if deg == 0]
    heapq.heapify(heap)

    idle_workers = [Worker(name="Worker {}".format(i)) for i in range(NUM_WORKERS)]
    active_workers = []
    now = 0

    while heap or active_workers:
        if active_workers:
            worker = heapq.heappop(active_workers)
            now = worker.available_time
            print "finished {} at {}".format(worker.current_task, now)

            if worker.current_task is not None:
                for next_task in dependents[worker.current_task]:
                    indegree[next_task] -= 1
                    if indegree[next_task] == 0:
                        # Only add to heap when all of its prerequisites are complete.
                        heapq.heappush(heap, next_task)

            worker.current_task = None
            worker.available_time = -1
            idle_workers.append(worker)

        while heap and idle_workers:
            task = heapq.heappop(heap)
            worker = idle_workers.pop()
            worker.current_task = task
            worker.available_time = now + task_time(task)
            heapq.heappush(active_workers, worker)

if __name__ == "__main__":
    go()

"""
--- Part Two ---
As you're about to begin construction, four of the Elves offer to help. "The sun
will set soon; it'll go faster if we work together." Now, you need to account
for multiple people working on steps simultaneously. If multiple steps are
available, workers should still begin them in alphabetical order.

Each step takes 60 seconds plus an amount corresponding to its letter: A=1, B=2,
C=3, and so on. So, step A takes 60+1=61 seconds, while step Z takes 60+26=86
seconds. No time is required between steps.

To simplify things for the example, however, suppose you only have help from one
Elf (a total of two workers) and that each step takes 60 fewer seconds (so that
step A takes 1 second and step Z takes 26 seconds). Then, using the same
instructions as above, this is how each second would be spent:

Second   Worker 1   Worker 2   Done
   0        C          .
   1        C          .
   2        C          .
   3        A          F       C
   4        B          F       CA
   5        B          F       CA
   6        D          F       CAB
   7        D          F       CAB
   8        D          F       CAB
   9        D          .       CABF
  10        E          .       CABFD
  11        E          .       CABFD
  12        E          .       CABFD
  13        E          .       CABFD
  14        E          .       CABFD
  15        .          .       CABFDE

Each row represents one second of time. The Second column identifies how many
seconds have passed as of the beginning of that second. Each worker column shows
the step that worker is currently doing (or . if they are idle). The Done column
shows completed steps.

Note that the order of the steps has changed; this is because steps now take
time to finish and multiple workers can begin multiple steps simultaneously.

In this example, it would take 15 seconds for two workers to complete these
steps.

With 5 workers and the 60+ second step durations described above, how long will
it take to complete all of the steps?
"""
