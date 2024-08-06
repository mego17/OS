class CLOOK_Algorithm:
    def __init__(self, requests, head_position, direction, total_tracks):
        self.requests = requests
        self.head_position = head_position
        self.direction = direction
        self.total_tracks = total_tracks

    def algorithm(self):
        order = [self.head_position]  # Initialize order with the initial head position
        seek_time = 0

        if self.direction == "Right":
            order += sorted([r for r in self.requests if r >= self.head_position])
            order += sorted([r for r in self.requests if r < self.head_position])
        elif self.direction == "Left":
            order += sorted([r for r in self.requests if r <= self.head_position], reverse=True)
            order += sorted([r for r in self.requests if r > self.head_position], reverse=True)

        for i in range(len(order) - 1):
            seek_time += abs(order[i+1] - order[i])  # Calculating seek time

        return order[1:], seek_time
