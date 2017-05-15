import logging
import datetime

class tiny_timer():
    def __init__(self,tot,timer_step=300,max_time_stuck=900,log_level=logging.DEBUG):
        self.tot=tot
        self.cnt=0
        self.step=1
        self.timer_step=timer_step
        self.max_time_stuck=max_time_stuck
        self.stuck_start=datetime.datetime.now()
        self.global_start=datetime.datetime.now()
        self.logger=logging.getLogger('timer')
        self.logger.setLevel(log_level)
    def check_timer(self,cnt):
        very_stuck=False
        if self.tot>cnt:
            if self.cnt<cnt:
                self.stuck_start=datetime.datetime.now()
            else:
                stuck_time=datetime.datetime.now()-self.stuck_start
                if stuck_time.total_seconds()>=self.max_time_stuck:
                    very_stuck=True
            elapsed_time=datetime.datetime.now()-self.global_start
            if cnt>0:
                time_left=elapsed_time/cnt*(self.tot-cnt)
            else:
                time_left=elapsed_time*self.tot
            if elapsed_time.total_seconds()>=self.step*self.timer_step:
                self.logger.info('{} items processed [{}]. '.format(cnt,str(elapsed_time).split('.')[0]) + \
                                 '{} items left [{}]'.format(self.tot-cnt,str(time_left).split('.')[0]))
                self.step=int(elapsed_time.total_seconds()/self.timer_step)+1
            seconds_left=time_left.total_seconds()
        else:
            seconds_left=0
        self.cnt=cnt
        return seconds_left,very_stuck

if __name__ == '__main__':
    import time
    def setup_logger(log_level=logging.DEBUG):
        logger=logging.getLogger()
        formatter=logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s','%m/%d/%Y %I:%M:%S %p')
        handler_stream=logging.StreamHandler()
        handler_stream.setLevel(log_level)
        handler_stream.setFormatter(formatter)
        logger.addHandler(handler_stream)
        return logger
    setup_logger()
    logger=logging.getLogger('sample_run')
    logger.setLevel(logging.DEBUG)
    tot_jobs=10
    timer_step=5
    max_time_stuck=10
    progress_lst=[[2,4],
                  [3,5],
                  [3,5],
                  [7,5],
                  [5,10]]
    logger.info('Starting a timer with {} jobs, '.format(tot_jobs) + \
                'step {}s and stuck limit {}s...'.format(timer_step,max_time_stuck))
    timer=tiny_timer(tot=tot_jobs,timer_step=5,max_time_stuck=10)
    total_time=0
    logger.info('Simulating progress to show off the timer\'s functionality...')
    for progress in progress_lst:
        sleep_time=progress[0]
        total_time=total_time+sleep_time
        jobs_done=progress[1]
        logger.info('===== Sleeping for {}s ====='.format(sleep_time))
        time.sleep(sleep_time)
        logger.info('Telling the timer that {} out of 10 jobs were finished'.format(jobs_done))
        logger.info('Estimated remaining time: ~{}s'.format(int(1.0*(tot_jobs-jobs_done)/jobs_done*total_time)))
        seconds_left,very_stuck=timer.check_timer(jobs_done)
        logger.info('> Time left reported by timer: {:0.2f}s'.format(seconds_left))
        logger.info('> Process is stuck flag: {}'.format(very_stuck))

# Expected output
# 05/14/2017 06:08:44 PM sample_run   INFO     Starting a timer with 10 jobs, step 5s and stuck limit 10s...
# 05/14/2017 06:08:44 PM sample_run   INFO     Simulating progress to show off the timer's functionality...
# 05/14/2017 06:08:44 PM sample_run   INFO     ===== Sleeping for 2s =====
# 05/14/2017 06:08:46 PM sample_run   INFO     Telling the timer that 4 out of 10 jobs were finished
# 05/14/2017 06:08:46 PM sample_run   INFO     Estimated remaining time: ~3s
# 05/14/2017 06:08:46 PM sample_run   INFO     > Time left reported by timer: 3.01s
# 05/14/2017 06:08:46 PM sample_run   INFO     > Process is stuck flag: False
# 05/14/2017 06:08:46 PM sample_run   INFO     ===== Sleeping for 3s =====
# 05/14/2017 06:08:49 PM sample_run   INFO     Telling the timer that 5 out of 10 jobs were finished
# 05/14/2017 06:08:49 PM sample_run   INFO     Estimated remaining time: ~5s
# 05/14/2017 06:08:49 PM timer        INFO     5 items processed [0:00:05]. 5 items left [0:00:05]
# 05/14/2017 06:08:49 PM sample_run   INFO     > Time left reported by timer: 5.02s
# 05/14/2017 06:08:49 PM sample_run   INFO     > Process is stuck flag: False
# 05/14/2017 06:08:49 PM sample_run   INFO     ===== Sleeping for 3s =====
# 05/14/2017 06:08:52 PM sample_run   INFO     Telling the timer that 5 out of 10 jobs were finished
# 05/14/2017 06:08:52 PM sample_run   INFO     Estimated remaining time: ~8s
# 05/14/2017 06:08:52 PM sample_run   INFO     > Time left reported by timer: 8.04s
# 05/14/2017 06:08:52 PM sample_run   INFO     > Process is stuck flag: False
# 05/14/2017 06:08:52 PM sample_run   INFO     ===== Sleeping for 7s =====
# 05/14/2017 06:08:59 PM sample_run   INFO     Telling the timer that 5 out of 10 jobs were finished
# 05/14/2017 06:08:59 PM sample_run   INFO     Estimated remaining time: ~15s
# 05/14/2017 06:08:59 PM timer        INFO     5 items processed [0:00:15]. 5 items left [0:00:15]
# 05/14/2017 06:08:59 PM sample_run   INFO     > Time left reported by timer: 15.06s
# 05/14/2017 06:08:59 PM sample_run   INFO     > Process is stuck flag: True
# 05/14/2017 06:08:59 PM sample_run   INFO     ===== Sleeping for 5s =====
# 05/14/2017 06:09:04 PM sample_run   INFO     Telling the timer that 10 out of 10 jobs were finished
# 05/14/2017 06:09:04 PM sample_run   INFO     Estimated remaining time: ~0s
# 05/14/2017 06:09:04 PM sample_run   INFO     > Time left reported by timer: 0.00s
# 05/14/2017 06:09:04 PM sample_run   INFO     > Process is stuck flag: False
