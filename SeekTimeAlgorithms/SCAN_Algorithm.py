class SCAN_Algorithm:
    def __init__(self, requests, head_position, direction, total_tracks):
        self.requests = requests
        self.head_position = head_position
        self.direction = direction
        self.total_tracks = total_tracks

    def algorithm(self):
        order = [self.head_position]  # Initialize order with an empty list
        seek_time = 0

        if self.direction == "Right":
            # Sort requests and append the head position
            sorted_requests = sorted(self.requests)
            requests_right = [r for r in sorted_requests if r >= self.head_position]
            requests_left = [r for r in sorted_requests if r < self.head_position]
            order += (requests_right + [self.total_tracks - 1] + requests_left[::-1])
        elif self.direction == "Left":
            # Sort requests in reverse order and append the head position
            sorted_requests = sorted(self.requests, reverse=True)
            requests_left = [r for r in sorted_requests if r <= self.head_position]
            requests_right = [r for r in sorted_requests if r > self.head_position]
            order += (requests_left + [0] + requests_right[::-1] )

        for i in range(len(order) - 1):
            seek_time += abs(order[i+1] - order[i])  # Calculating seek time

        return order[1:], seek_time
