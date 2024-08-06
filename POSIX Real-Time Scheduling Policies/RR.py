class TaskScheduler:
    def __init__(self, name, release_time, period, execution_time, deadline, max_time):
        self.name = name
        self.release_time = release_time
        self.period = period
        self.execution_time = execution_time
        self.deadline = deadline
        self.max_time = max_time
        self.NextReleaseTime = release_time
        self.remaining_execution = execution_time  # Remaining execution time for the current job
        self.JobNumber = 1
        self.execution_times = []
        self.priority = 1
        self.broken_deadlines = []  


class Scheduler:
    def __init__(self, tasks, max_time, slot_time):
        self.tasks = tasks
        self.max_time = max_time
        self.slot_time = slot_time
        self.current_time = 0
        self.ready_list = []

    def schedule(self):
        while not self.get_time_to_stop() and self.current_time < self.max_time:
            for task in self.tasks:
                if self.current_time >= task.NextReleaseTime:
                    task.deadline += task.period + task.release_time
                    self.ready_list.insert(0, task)  
                    task.NextReleaseTime += task.period

            if self.ready_list:  
                running_task = self.ready_list.pop(0)  
                self.execute_task(running_task, self.slot_time)

            self.current_time += self.slot_time  

    def execute_task(self, task, slot_time):
        task.remaining_execution -= slot_time
        task.execution_times.append([self.current_time, self.current_time + slot_time])

        if task.remaining_execution <= 0:
            task.remaining_execution = task.execution_time
            task.JobNumber += 1

            if self.current_time + slot_time > task.deadline:
                task.broken_deadlines.append(self.current_time + slot_time)

        else:
            self.ready_list.append(task)

    def get_time_to_stop(self):
        return all(task.remaining_execution <= 0 for task in self.tasks)

    def get_results(self):
        execution = {}
        task_priorities = {}
        broken_deadlines = {}

        results = []

        for task in self.tasks:
            execution[f"{task.name}"] = task.execution_times
            task_priorities[f"{task.name}"] = task.priority
            broken_deadlines[f"{task.name}"] = task.broken_deadlines


        results.append(execution)
        results.append(task_priorities)
        results.append(broken_deadlines)

        return results

