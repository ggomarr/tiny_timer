# tiny_timer
The class provides a timer that help oversee the progress of large loops or parallelized tasks in a very compact way. It will log, once every so much, how many tasks were completed, how long it took, how many tasks are left and how long it should take. It will also raise a flag if suddenly the loop gets stuck for whateve reason, allowing the user code to halt execution if need be.

A normal usage case would be, for example:
- A task will run on a 10k items list and is expected to take 45 minutes. The user wants to know, once every five minutes, how many items were processed and how long it should take until the loop is done
- A group of 1m tasks are being parallelized over multiple cores, and the complete task is expected to take over 8 hours. The user wants to confirm, once every half hour, that the parallelizer is on track and did not get stuck, and terminate the pool if it nothing gets processed for too long

The timer should be initialized right before the loop is launched with the following parameters:
- The total number of tasks (tot)
- Every how many seconds progress should be logged (timer_step=300)
- How many seconds without progress should go by before the stuck flag is raised (max_time_stuck=900)

Once the loop is launched, an update can be requested by calling timer.check_timer(cnt), where cnt is the number of tasks that have been completed. The timer will log the progress if timer_step seconds since the last log have gone by, and return the expected number of seconds left until all tasks are done and a flag letting the user code know whether progress is being made.

Running the file directly from the command line will launch a simulated usage of the timer. On it a timer for a process with 10 steps is declared and a hard coded number of steps are reported completed after a hard coded number of seconds. The output should look like the below.

The log lines added by the timer are labeled 'timer'. The 'Estimated remaining time:' lines are calculated by hand on the sample code, and the '> Time left reported by timer:' and '> Process is stuck flag:' are printed by the sample code using the return from the call to the timer. A stuck flag is raised after making the timer think nothing has been processed for a while.
```
05/14/2017 06:08:44 PM sample_run   INFO     Starting a timer with 10 jobs, step 5s and stuck limit 10s...
05/14/2017 06:08:44 PM sample_run   INFO     Simulating progress to show off the timer's functionality...
05/14/2017 06:08:44 PM sample_run   INFO     ===== Sleeping for 2s =====
05/14/2017 06:08:46 PM sample_run   INFO     Telling the timer that 4 out of 10 jobs were finished
05/14/2017 06:08:46 PM sample_run   INFO     Estimated remaining time: ~3s
05/14/2017 06:08:46 PM sample_run   INFO     > Time left reported by timer: 3.01s
05/14/2017 06:08:46 PM sample_run   INFO     > Process is stuck flag: False
05/14/2017 06:08:46 PM sample_run   INFO     ===== Sleeping for 3s =====
05/14/2017 06:08:49 PM sample_run   INFO     Telling the timer that 5 out of 10 jobs were finished
05/14/2017 06:08:49 PM sample_run   INFO     Estimated remaining time: ~5s
05/14/2017 06:08:49 PM timer        INFO     5 items processed [0:00:05]. 5 items left [0:00:05]
05/14/2017 06:08:49 PM sample_run   INFO     > Time left reported by timer: 5.02s
05/14/2017 06:08:49 PM sample_run   INFO     > Process is stuck flag: False
05/14/2017 06:08:49 PM sample_run   INFO     ===== Sleeping for 3s =====
05/14/2017 06:08:52 PM sample_run   INFO     Telling the timer that 5 out of 10 jobs were finished
05/14/2017 06:08:52 PM sample_run   INFO     Estimated remaining time: ~8s
05/14/2017 06:08:52 PM sample_run   INFO     > Time left reported by timer: 8.04s
05/14/2017 06:08:52 PM sample_run   INFO     > Process is stuck flag: False
05/14/2017 06:08:52 PM sample_run   INFO     ===== Sleeping for 7s =====
05/14/2017 06:08:59 PM sample_run   INFO     Telling the timer that 5 out of 10 jobs were finished
05/14/2017 06:08:59 PM sample_run   INFO     Estimated remaining time: ~15s
05/14/2017 06:08:59 PM timer        INFO     5 items processed [0:00:15]. 5 items left [0:00:15]
05/14/2017 06:08:59 PM sample_run   INFO     > Time left reported by timer: 15.06s
05/14/2017 06:08:59 PM sample_run   INFO     > Process is stuck flag: True
05/14/2017 06:08:59 PM sample_run   INFO     ===== Sleeping for 5s =====
05/14/2017 06:09:04 PM sample_run   INFO     Telling the timer that 10 out of 10 jobs were finished
05/14/2017 06:09:04 PM sample_run   INFO     Estimated remaining time: ~0s
05/14/2017 06:09:04 PM sample_run   INFO     > Time left reported by timer: 0.00s
05/14/2017 06:09:04 PM sample_run   INFO     > Process is stuck flag: False
```
Enjoy, and let me know if you find it useful!
