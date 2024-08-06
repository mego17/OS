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
    def __init__(self, task_name, release_time, period, execution_time, deadline, max_time):
        self.task_name = task_name
        self.release_time = release_time
        self.period = period
        self.execution_time = execution_time
        self.remaining_execution = 0
        self.deadline = deadline
        self.deadline_broken = False
        self.ready_times = [time for time in generate_float_range(self.release_time, max_time+1, self.period)]
        self.ready_times.append(self.ready_times[-1] + period)
        self.deadlines = [time + self.deadline for time in self.ready_times]
        self.execution_times = []
        self.broken_deadlines = []

    def get_deadline(self):
        if self.remaining_execution != 0:
            return self.deadline
        return None

    def update_deadline(self, t):
        for deadline in self.deadlines:
            if deadline > t:
                self.deadline = deadline
                break


class Scheduler:
    def __init__(self, tasks, max_time):
        self.tasks = tasks
        self.max_time = max_time
        self.tasks_deadline_times = []
        self.current_time = 0
        self.execute_list = []
        while self.current_time < max_time:
            min_deadline_task = self.get_min_deadline_task()
            self.execute(min_deadline_task)

    def get_min_deadline_task(self):
        tasks_deadline_time = []
        tasks_ready_times = [(task, task.ready_times[0]) for task in self.tasks]
        for task, ready_time in tasks_ready_times:
            if ready_time <= self.current_time:
                self.execute_list.append(task)
                task.ready_times.pop(0)
                task.remaining_execution = task.execution_time
            tasks_deadline_time.append(task.get_deadline())

        tasks_deadline_time_copy = tasks_deadline_time.copy()
        for task_deadline_time in tasks_deadline_time:
            if task_deadline_time is None:
                tasks_deadline_time_copy.remove(None)

        if not tasks_deadline_time_copy:
            tasks_next_ready_time = [task.ready_times[0] for task in self.tasks]
            self.current_time = min(tasks_next_ready_time)
            self.update_tasks_remaining_execution()
            return self.get_min_deadline_task()

        min_deadline_index = tasks_deadline_time.index(min(tasks_deadline_time_copy))
        self.tasks_deadline_times.append((tasks_deadline_time, self.current_time))

        return self.tasks[min_deadline_index]

    def update_tasks_remaining_execution(self):
        for task in self.tasks:
            if task.ready_times[0] <= self.current_time:
                if task.remaining_execution == 0 or task.deadline_broken:
                    self.execute_list.append(task)
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
            self.execute_list.remove(task)

        self.check_deadline(end_time)
        self.current_time = end_time
        self.update_tasks_remaining_execution()

    def get_time_to_stop(self, task):
        tasks_next_ready_time = [t.ready_times[0] for t in self.tasks]
        nearest_ready_time = min(tasks_next_ready_time)

        if self.current_time + task.remaining_execution < nearest_ready_time:
            return self.current_time + task.remaining_execution
        else:
            return nearest_ready_time

    def check_deadline(self, t):
        for task in self.tasks:
            if task.remaining_execution != 0 and task.deadline <= t:
                if task.deadline not in task.broken_deadlines:
                    task.broken_deadlines.append(task.deadline)
                    task.deadline_broken = True
            else:
                task.deadline_broken = False

    def get_results(self):
        execution = {}
        results = []
        broken_deadlines = {}
        for task in self.tasks:
            execution[task.task_name] = task.execution_times
            broken_deadlines[task.task_name] = task.broken_deadlines
        results.append(execution)
        results.append(self.tasks_deadline_times)
        results.append(broken_deadlines)
    
        return results

