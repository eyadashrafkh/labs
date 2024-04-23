import heapq


class PQ:
    def __init__(self, size):
        self.pointers = [0 for _ in range(size)]
        self.heap = []
        self.count = 0

    def append(self, priority, item):
        """Append item to the heap without heapifying"""
        self.pointers[item] = [priority, self.count, item]
        self.heap.append(self.pointers[item])
        self.count += 1

    def push(self, priority, item):
        """Push item to the heap and heapify"""
        self.pointers[item] = [priority, self.count, item]
        heapq.heappush(self.heap, self.pointers[item])
        self.count += 1

    def heapify(self):
        """Heapify the heap"""
        heapq.heapify(self.heap)

    def update(self, item, priority):
        """Update the priority of item without heapifying"""
        print("update", item, priority)
        print(self.pointers[item])
        self.pointers[item][0] = priority

    def pop(self):
        """Pop item from the heap and heapify"""
        if len(self.heap) == 0:
            return None

        return heapq.heappop(self.heap)[-1]

    def __len__(self):
        return len(self.heap)
