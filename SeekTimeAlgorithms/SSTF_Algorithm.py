class SSTF_Algorithm:
    def __init__(self, requests, head_position):
        self.requests = requests
        self.head_position = head_position

    def algorithm(self):
        order = [self.head_position]  # Initialize order with the initial head position
        seek_time = 0

        while self.requests:
            closest_request = min(self.requests, key=lambda x: abs(x - order[-1]))  # Find the closest request
            order.append(closest_request)  # Add the closest request to the order
            self.requests.remove(closest_request)  # Remove the processed request
            seek_time += abs(order[-1] - order[-2])  # Update seek time

        return order[1:], seek_time
