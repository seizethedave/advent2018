from collections import defaultdict
import heapq

def go():
    dependents = defaultdict(set)
    indegree = defaultdict(int)

    with open("advent07.txt", "r") as f:
        for line in f:
            prerequisite, dependent = line[5], line[36]
            dependents[prerequisite].add(dependent)
            indegree.setdefault(prerequisite, 0)
            indegree[dependent] += 1

    roots = [step for step, deg in indegree.iteritems() if deg == 0]
    heap = []

    for root in roots:
        heapq.heappush(heap, root)

    ordering = []

    while heap:
        step = heapq.heappop(heap)
        ordering.append(step)

        for next_step in dependents[step]:
            indegree[next_step] -= 1
            if indegree[next_step] == 0:
                # Only add to heap when all of its prerequisites are complete.
                heapq.heappush(heap, next_step)

    print "".join(ordering)


if __name__ == "__main__":
    go()
