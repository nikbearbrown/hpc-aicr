# Real outputs we captured (read-only), 2026-10-11

**What this is.** Output of read-only commands run on the login nodes of Explorer and AICR on 2026-10-11, in a Claude Code session, with key login and `BatchMode=yes`. Nothing was submitted, changed or deleted; no compute node was requested. **Use:** guides may label a fact "tested by us, 2026-10-11" only if it appears here (or in the film SESSION.md records). **Not tested:** anything that needs a compute node (`srun`, `check-quota`, `project`, `gpu-logs`, `historical-seff`, job submission), Open OnDemand, and other accounts or networks.

## EXPLORER (login node), read-only, 2026-10-11 15:43 EDT
### hostname/os
explorer-02
NAME="Rocky Linux"
VERSION="9.7 (Blue Onyx)"
ID="rocky"
### sinfo -s
PARTITION       AVAIL  TIMELIMIT   NODES(A/I/O/T) NODELIST
gpu                up    8:00:00        21/2/2/25 c[2204-2207],d[1002,1007,1009-1013,1015,1017,1019-1020,1022,1025-1029,4052-4055]
short*             up 2-00:00:00   123/13/116/252 c[0160-0164,0171,0180,0184-0185,0190-0191,0204,0207,0211,0213,0215-0216,0219,0221-0222,0227,0232-0235,0237,0239,0244-0245,0247,0277,0279,0281,0283,0314-0315,0319,0393-0404,0406-0423,0536-0550,0585-0587,0589,0591-0597,0599-0600,0602-0616,0618-0622,0624-0625,0627-0637,0639-0641,0643-0646,0649-0654,0656-0659,0664,0667-0670,0672-0678,0680-0681,0683,0685-0690,0692-0693,3002-3005,3008,3010-3011,3015-3017,3022-3031,3033-3038,3089-3092,3147-3156],d[0002-0005,0012-0014,0020,0022-0024,0026-0039,0064,0076,0085,0097,0100,0105,0110,0113,0126,0139,0142-0147,0149-0150,1027]
sharing            up    1:00:00  158/129/168/455 c[0160-0164,0171,0207,0211,0219,0222,0234,0237,0239,0244,0277,0279,0281,0283,0314,0393-0404,0406-0423,0441-0487,0522,0536-0550,0585-0587,0591-0595,0597,0599-0600,0602-0616,0618-0622,0624-0625,0627-0637,0639,0641,0643-0646,0649-0654,0656-0659,0664,0668-0669,0673-0677,0680,0683,0685,0689-0690,0744-0751,0753-0759,2184-2195,3002-3005,3008,3010-3011,3015-3017,3022-3023,3025-3029,3040,3081-3082,3086,3096-3127,3132,3135,3138,3177-3188,3190-3192,3194-3198,3201-3221,3223-3224,4028-4031,4035,5002],d[0002-0005,0007,0010-0014,0020,0023-0024,0026-0039,0050,0064,0076,0085,0097,0100,0105,0110,0113,0126,0142-0143,0147,0149-0150,1004,1027,3037-3038,3040-3041,3044-3049,3051-3053,3057-3058,3060-3061,3063-3065,3067-3071,3089-3098,3123,3146-3147,3149-3150,3155,3163-3166,3168,3170-3171,3194,3203-3206,3208,3210-3213,3215-3222,3224-3226,3230-3233,3239,4031-4032,4041-4044,4046-4051,4056,4072-4075,4077-4078,4100]
gpu-short          up    2:00:00        21/2/2/25 c[2204-2207],d[1002,1007,1009-1013,1015,1017,1019-1020,1022,1025-1029,4052-4055]
gpu-interactive    up    2:00:00        21/2/2/25 c[2204-2207],d[1002,1007,1009-1013,1015,1017,1019-1020,1022,1025-1029,4052-4055]
### gpu gres (partition gpu)
PARTITION GRES NODES STATE
gpu gpu:v100-sxm2:4(S:0-1) 2 comp
gpu gpu:v100-pcie:2(S:0-7) 1 down*
gpu gpu:v100-sxm2:4(S:0-1) 1 drain
gpu gpu:v100-pcie:2(S:0-1) 3 mix
gpu gpu:v100-sxm2:4(S:0-1) 6 mix
gpu gpu:v100-sxm2:3(S:0-1) 1 mix
gpu gpu:v100-sxm2:3 1 mix
gpu gpu:a100:3 1 mix
gpu gpu:a100:4 2 mix
gpu gpu:h200:8 4 mix
gpu gpu:v100-sxm2:4(S:0-1) 1 alloc
gpu gpu:v100-sxm2:4(S:0-1) 1 idle
gpu gpu:t4:4(S:0-1) 1 idle
### partition limits
PARTITION TIMELIMIT NODES
gpu 8:00:00 25
short* 2-00:00:00 252
sharing 1:00:00 455
gpu-short 2:00:00 25
gpu-interactive 2:00:00 25
### commands present
sbatch           /usr/bin/sbatch
srun             /usr/bin/srun
salloc           /usr/bin/salloc
squeue           /usr/bin/squeue
sinfo            /usr/bin/sinfo
sacct            /usr/bin/sacct
seff             /usr/bin/seff
historical-seff  /shared/EL9/explorer/explorer/bin/historical-seff
gpu-logs         /shared/EL9/explorer/explorer/bin/gpu-logs
check-quota      /shared/EL9/explorer/explorer/bin/check-quota
project          /shared/EL9/explorer/explorer/bin/project
apptainer        /usr/bin/apptainer
module           module
nvidia-smi       MISSING
conda            MISSING
spack            MISSING
### module system
Modules Release 5.3.0 (2023-05-14)
### module avail (selected)
-- cuda
----------------------- /shared/EL9/explorer/modulefiles -----------------------
cuda/12.1.1  cuda/12.3.0  cuda/12.3.0.old  cuda/12.8.0  cuda/13.2.0  
-- miniconda3
----------------------- /shared/EL9/explorer/modulefiles -----------------------
miniconda3/24.11.1  miniconda3/25.9.1  
-- anaconda3
----------------------- /shared/EL9/explorer/modulefiles -----------------------
anaconda3/2024.06  
-- python
----------------------- /shared/EL9/explorer/modulefiles -----------------------
python/3.13.5  
-- gcc
-- openmpi
----------------------- /shared/EL9/explorer/modulefiles -----------------------
OpenMPI/4.1.6  
-- apptainer
-- cmake
----------------------- /shared/EL9/explorer/modulefiles -----------------------
cmake/3.30.2  cmake/4.2.3  cmake/4.4.0  
### apptainer version
apptainer version 1.4.5-3.el9
### my queue
             JOBID PARTITION     NAME     USER ST       TIME  NODES NODELIST(REASON)


## AICR (login node), read-only, 2026-10-11 15:44 EDT
### hostname/os
login.aicr.ai
NAME="Rocky Linux"
VERSION="9.6 (Blue Onyx)"
ID="rocky"
### sinfo
PARTITION      TIMELIMIT   NODES  GRES
cpu*           1-00:00:00  5      (null)
rtx-batch      1-00:00:00  17     gpu:rtx_pro_6000:8(S:0-1)
b200-batch     1-00:00:00  25     gpu:b200:8(S:0-7)
b200-fullnode  1-00:00:00  4      gpu:b200:8(S:0-7)
rtx-devel      4:00:00     2      gpu:rtx_pro_6000:8(S:0-1)
b200-devel     4:00:00     2      gpu:b200:8(S:0-7)
preemptable    1-00:00:00  17     gpu:rtx_pro_6000:8(S:0-1)
preemptable    1-00:00:00  29     gpu:b200:8(S:0-7)
### commands present
sbatch         /usr/bin/sbatch
srun           /usr/bin/srun
salloc         /usr/bin/salloc
squeue         /usr/bin/squeue
sinfo          /usr/bin/sinfo
sacct          /usr/bin/sacct
seff           /usr/bin/seff
jobstats       /usr/bin/jobstats
nvidia-smi     /usr/bin/nvidia-smi
nvitop         MISSING
nsys           MISSING
ncu            MISSING
apptainer      /usr/bin/apptainer
singularity    /usr/bin/singularity
module         module
conda          MISSING
### module system

Modules based on Lua: Version 8.7.65 2025-08-05 10:24 -06:00
### module avail (selected)
-- cuda

---------------------------- /apps/neu/modules/all ----------------------------
   CUDA/13.3.0
   NCCL/2.30.4-GCCcore-15.2.0-CUDA-13.3.0
   UCX-CUDA/1.20.0-GCCcore-15.2.0-CUDA-13.3.0

------------------------- /apps/aicr/modulefiles/Core -------------------------
   cuda/13.1.1
   hdf5/1.14.6-gcc-12.5.0-cuda-13.1.1-openmpi-4.1.8
   netcdf-c/4.9.3-gcc-12.5.0-cuda-13.1.1-openmpi-4.1.8
-- miniforge3

------------------------- /apps/aicr/modulefiles/Core -------------------------
   miniforge3/25.3.0-3

If the avail list is too long consider trying:

"module --default avail" or "ml -d av" to just list the default modules.
"module overview" or "ml ov" to display the number of modules for each name.

Use "module spider" to find all possible modules and extensions.
-- python
No module(s) or extension(s) found!
If the avail list is too long consider trying:

"module --default avail" or "ml -d av" to just list the default modules.
"module overview" or "ml ov" to display the number of modules for each name.

Use "module spider" to find all possible modules and extensions.
Use "module keyword key1 key2 ..." to search for all possible modules matching
any of the "keys".

-- gcc

---------------------------- /apps/neu/modules/all ----------------------------
   Autoconf/2.72-GCCcore-15.2.0
   Automake/1.18.1-GCCcore-15.2.0
   Autotools/20250626-GCCcore-15.2.0
   Bison/3.8.2-GCCcore-15.2.0
   GCCcore/15.2.0
   GDRCopy/2.5.2-GCCcore-15.2.0
   M4/1.4.20-GCCcore-15.2.0
   NCCL/2.30.4-GCCcore-15.2.0-CUDA-13.3.0
-- apptainer
No module(s) or extension(s) found!
If the avail list is too long consider trying:

"module --default avail" or "ml -d av" to just list the default modules.
"module overview" or "ml ov" to display the number of modules for each name.

Use "module spider" to find all possible modules and extensions.
Use "module keyword key1 key2 ..." to search for all possible modules matching
any of the "keys".

-- cmake
No module(s) or extension(s) found!
If the avail list is too long consider trying:

"module --default avail" or "ml -d av" to just list the default modules.
"module overview" or "ml ov" to display the number of modules for each name.

Use "module spider" to find all possible modules and extensions.
Use "module keyword key1 key2 ..." to search for all possible modules matching
any of the "keys".

-- openmpi

------------------------- /apps/aicr/modulefiles/Core -------------------------
   hdf5/1.14.6-gcc-12.5.0-cuda-13.1.1-openmpi-4.1.8
   netcdf-c/4.9.3-gcc-12.5.0-cuda-13.1.1-openmpi-4.1.8
   netcdf-cxx4/4.3.1-gcc-12.5.0-cuda-13.1.1-openmpi-4.1.8
   netcdf-fortran/4.6.2-gcc-12.5.0-cuda-13.1.1-openmpi-4.1.8
   openmpi/4.1.8-gcc-12.5.0-cuda-13.1.1

If the avail list is too long consider trying:

-- nvhpc

------------------------- /apps/aicr/modulefiles/Core -------------------------
   nvhpc/26.3

If the avail list is too long consider trying:

