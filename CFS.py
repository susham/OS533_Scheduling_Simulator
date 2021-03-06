from Jobs import Job
from collections import deque


class CFS:
    queue = deque()
    queue1 = deque()
    cfs_jobs = []
    cfs_throughput = 0

    def sort_job(self, jobList):

        """ Sort the job list based on execution time
       :param job_list:Jobs
       :return:
       """
        sorted_job_list = sorted(jobList, key=lambda x: x.execution_time, reverse=False)
        for x in range(0, len(sorted_job_list)):
            sorted_job_list[x].arrival_time = 0
            sorted_job_list[x].cpu_burst = 0
        return sorted_job_list

    def convert_to_queue(self, sortedList):
        """
       Convert the input list to queue
       :param sortedList: list sorted according to priorities
       :return:
       """
        for i in range(len(sortedList)):
            CFS.queue.append(sortedList[i])
        return CFS.queue

    def calculate_times(self, queue, num_jobs, cpu_slice):
        """
        This definition is responsible to run the CFS scheduling algorithm and
        calculate waiting time, completion time, turnaround time for each process and
        total turnaround time and throughput.
        :param queue: queue containing jobs, sorted according to execution.
        num_jobs: number of jobs
        cpu_slice: cpu time slice for which jobs can run.
        :return:
        """
        total_completion = 0
        completion_time = 0.0
        number_of_jobs = num_jobs
        while(len(queue)>0):
            flag = 0
            temp_slice = (cpu_slice / number_of_jobs)
            for i in range(number_of_jobs):
                running = CFS.queue.pop()

                running.execution_time = running.execution_time - temp_slice
                running.cpu_burst = running.cpu_burst + temp_slice
                if (running.execution_time > 0):
                    CFS.queue.appendleft(running)
                    completion_time = completion_time + temp_slice

                elif running.execution_time <= 0 :
                    flag =flag+1
                    completion_time = completion_time + (temp_slice - abs(running.execution_time))
                    # running.completion_time = completion_time

                    #total_completion = total_completion + completion_time

                    # set completeion time of running job
                    Job.set_completion_time(running, completion_time)

                    # set turnaround time of running job
                    Job.set_turnaround_time(running, Job.get_completion_time(running))

                    waitingTime =Job.get_completion_time(running) - running.cpu_burst
                    # running.waiting_time = waitingTime

                    # set waiting time of running job
                    Job.set_waiting_time(running, waitingTime)

                    CFS.cfs_jobs.append(running)

                    print("JobId:", running.JobId)
                    print("Completion time", running.completion_time)
                    print("Turnaround time", running.completion_time-running.arrival_time)
                    print("Waiting ", running.waiting_time)
                    print("-----------------------------------------------------------------")

            if flag>0:
                number_of_jobs = number_of_jobs - flag

        print("CFS Completion time:",completion_time)

        CFS.cfs_throughput = num_jobs / completion_time
        print("Throughput ", self.cfs_throughput)

        # calculate total turnaround time
        total_TurnarounTime = completion_time / num_jobs

        print("Average Turn around time ", total_TurnarounTime)
        print("-----------------------------------------------------------------")

        return CFS.cfs_jobs

    def execute_priority(self, num_of_jobs, cpu_slice, job_List):
        sorted_job_list = self.sort_job(job_List)
        for i in range(len(sorted_job_list)):
            CFS.queue.append(sorted_job_list[i])
        # print(CFS.queue)
        CFS.cfs_jobs = CFS.calculate_times(self, CFS.queue, num_of_jobs, cpu_slice)
        return CFS.cfs_jobs