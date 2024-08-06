def generate_float_range(start, end, step):
    float_range_list = [start]
    if step != 0:
        while True:
            start += step
            if start > end:
                break
            float_range_list.append(round(start, 2))
    return float_range_list

class TaskScheduler:
    def __init__(self, name, release_time, period, execution_time, deadline, max_time):
        self.name = name
        self.release_time = release_time
        self.period = period
        self.execution_time = execution_time
        self.remaining_execution = 0
        self.deadline = deadline
        self.deadline_broken = False
        self.max_time = max_time
        self.priority = None
        self.ready_times = [time for time in generate_float_range(release_time, max_time + 1, period)]
        self.ready_times.append(self.ready_times[-1] + period)
        self.deadlines = [ready_time + deadline for ready_time in self.ready_times]
        self.execution_times = []
        self.broken_deadlines = []

    def update_deadline(self, t):
        for deadline in self.deadlines:
            if deadline > t:
                self.deadline = deadline
                break

class Scheduler:
    def __init__(self, tasks, max_time):
        self.tasks = tasks
        self.max_time = max_time
        self.current_time = 0
        self.set_priorities()
        self.execution_list = []
        while self.current_time < self.max_time:
            task = self.get_task_to_execute()
            self.execute(task)

    def set_priorities(self):
        tasks_periods = []
        for task in self.tasks:
            tasks_periods.append(task.period)

        count = 1
        tasks_priorities = []
        for deadline1 in tasks_periods:
            for deadline2 in tasks_periods:
                if deadline1 > deadline2:
                    count += 1
            tasks_priorities.append(count)
            count = 1

        for index, task in enumerate(self.tasks):
            task.priority = tasks_priorities[index]

    def get_task_to_execute(self):
        if not self.execution_list:
            tasks_ready_time = [(task, task.ready_times[0]) for task in self.tasks]

            for task, ready_time in tasks_ready_time:
                if ready_time <= self.current_time:
                    task.remaining_execution = task.execution_time
                    self.execution_list.append(task)
                    task.ready_times.pop(0)

            if not self.execution_list:
                self.current_time = min(tasks_ready_time, key=lambda ready_time: ready_time[1])[1]
                self.update_tasks_remaining_execution()
                return self.get_task_to_execute()

        priorities = []
        for task in self.execution_list:
            priorities.append(task.priority)

        highest_priority_index = priorities.index(min(priorities))

        return self.execution_list[highest_priority_index]

    def update_tasks_remaining_execution(self):
        for task in self.tasks:
            if task.ready_times[0] <= self.current_time:
                if task.remaining_execution == 0 or task.deadline_broken:
                    self.execution_list.append(task)
                    task.remaining_execution = task.execution_time
                    task.ready_times.pop(0)
                task.update_deadline(self.current_time)

    def execute(self, task):
        start_time = self.current_time
        end_time = self.get_time_to_stop(task)

        task.remaining_execution -= (end_time - start_time)
        if end_time > self.max_time:
            task.execution_times.append([start_time, self.max_time])
        else:
            task.execution_times.append([start_time, end_time])

        if task.remaining_execution == 0:
            self.execution_list.remove(task)

        self.check_deadline(end_time)
        self.current_time = end_time
        self.update_tasks_remaining_execution()

    def get_time_to_stop(self, task):
        tasks_ready_time = [t.ready_times[0] for t in self.tasks]
        nearest_ready_time = min(tasks_ready_time)

        if self.current_time + task.remaining_execution < nearest_ready_time:
            return self.current_time + task.remaining_execution
        else:
            return nearest_ready_time

    def check_deadline(self, t):
        for task in self.tasks:
            if task.remaining_execution != 0 and task.deadline <= t:
                if task.name == "T3":
                    print(f"t: {t}, rt: {task.remaining_execution}")
                if task.deadline not in task.broken_deadlines:
                    task.broken_deadlines.append(task.deadline)
                    task.deadline_broken = True
            else:
                task.deadline_broken = False

    def get_results(self):
        execution = {}
        tasks_priorities = {}
        results = []
        broken_deadlines = {}
        for task in self.tasks:
            execution[f"{task.name}"] = task.execution_times
            broken_deadlines[f"{task.name}"] = task.broken_deadlines
            tasks_priorities[f"{task.name}"] = task.priority
        results.append(execution)
        results.append(tasks_priorities)
        results.append(broken_deadlines)
        for task in self.tasks:
            print(f"{task.name} execute times (from, to): {task.execution_times}")
            if task.broken_deadlines:
                print(f"{task.name} broken deadlines: {task.broken_deadlines}")
        return results
