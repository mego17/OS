class FCFS_Algorithm:
    def __init__(self, requests, head_position):
        self.requests = requests
        self.head_position = head_position

    def algorithm(self):
        order = [self.head_position]  # Initialize order with the initial head position
        seek_time = 0

        for i in range(len(self.requests)):
            seek_time += abs(order[-1] - self.requests[i])  # Calculating seek time
            order.append(self.requests[i])  # Add the request to the order

        return order[1:], seek_time
