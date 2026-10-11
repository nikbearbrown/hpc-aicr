# SESSION — what was really run for this film

**What this is.** The record behind the one real-output beat (B72). **Result.** One read-only command on login.aicr.ai against Bear's own finished job. No job was submitted; no GPU demo was run.

## jobstats, read-only, Tue Oct 6 12:03:47 EDT 2026

```
$ jobstats 318592
         Job ID: 318592
   User/Account: <aicr-username>/<slurm-account>
       Job Name: f5tune-voice
          State: COMPLETED
          Nodes: 1
      CPU Cores: 8
     CPU Memory: 64GB (8GB per CPU-core)
           GPUs: 1
  QOS/Partition: normal/rtx-batch
     Start Time: Fri Aug 7, 2026 at 9:06 PM
       Run Time: 00:55:09
     Time Limit: 08:00:00

  CPU utilization  [||||||                                         13%]
  CPU memory usage [||||||||||||                                   25%]
  GPU utilization  [||||||||||||||||||||||||||||||||||||||||       80%]
  GPU memory usage [||||||||                                       17%]

  GPU utilization per node:   a0003 (GPU 7): 79.7%
  GPU memory usage per node:  a0003 (GPU 7): 15.9GB/95.6GB (16.6%)

  * This job only needed 11% of the requested time which was 08:00:00. ...
```
B72 re-composes this on cream with bars at exactly 13 / 25 / 80 / 17 and the header rows above.

Also checked: `which jobstats` → /usr/bin/jobstats; `nvitop` and `nsys` are not on the login node's PATH (not shown as output anywhere).

## Not run

The workshop's demo scripts (`scripts/01_gpu_verify.py` … `07_jobstats_guide.py`) need a GPU allocation. Submitting one is a change to the shared cluster that this build is not permitted to make, so no script output is shown; B14 draws the five checks the verify script performs, as the source lists them.
