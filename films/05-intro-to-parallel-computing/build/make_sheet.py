#!/usr/bin/env python3
"""make_sheet.py — beat_sheet.json for claude-liam-lecture-intro-to-parallel-computing.

LECTURE (brutalist.art/skills/make/lecture/SKILL.md). Source: hpc/Intro-to-HPC-Scaling-Parallel-Computing-2026/
intro_to_parallel_computing.md ("Introduction to Parallel Computing", Northeastern Research Computing, presenter Ghanghoon
"Will" Paik, HPC Performance Engineer; github.com/northeastern-rc-training/Intro-to-HPC-Scaling-Parallel-Computing-2026).
Its benchmark tables are the data; its code is the code. Fifth film of the series; same cast.
"""
import json
from pathlib import Path
HERE = Path(__file__).resolve().parent
SLUG = HERE.name
TITLE = "Intro to Parallel Computing"
FPS = 30
SPARSE = ("lecture, drawn lane (show-tell drawing laws): one drawn scene on a cream stage with a few labels, the voice "
          "carries the explanation. Only underfill and clustered are waived; edge-bleed, empty-frame and contrast still apply.")


def manim(bid, act, narration, cls, image, show, sparse=False):
    b = {"beat_id": bid, "act": act, "lane": "manim", "proof_gate": "SHOW",
         "narration_text": narration, "estimated_duration_s": round(len(narration.split()) / 2.5, 1),
         "voice": "am_onyx", "engine": "kokoro",
         "shot": {"type": "GRAPHIC", "source": "own", "visual_intent": image, "show": show, "manim": {"class": cls}, "motion_claim": image}}
    if sparse:
        b["qc"] = {"sparse_by_design": True, "sparse_reason": SPARSE}
    return b


def remotion(bid, act, narration, pattern, props, show, gate="SHOW", lane="remotion", **extra):
    b = {"beat_id": bid, "act": act, "lane": lane, "proof_gate": gate,
         "narration_text": narration, "estimated_duration_s": round(len(narration.split()) / 2.5, 1),
         "voice": "am_onyx", "engine": "kokoro",
         "shot": {"type": "REMOTION", "source": "own", "show": show, "remotion": {"pattern": pattern, "props": props}}}
    b.update(extra)
    return b


def shell(bid, act, narration, lines, show, start=20, gap=40, title="ssh — login.explorer.northeastern.edu"):
    return remotion(bid, act, narration, "CCPlainShell", {"title": title, "lines": lines, "startCue": start, "lineGap": gap}, show,
                    motion_claim="The real job scripts and commands land in order.")


def code(bid, act, narration, title, src, spark, show, lang="python"):
    return remotion(bid, act, narration, "ClaudeCodeBeat", {"title": title, "code": src, "language": lang, "largeText": True, "sparkLine": spark},
                    show, motion_claim="The training's own code prints line by line.")


A = ["I · Why Parallel", "II · Flynn's Four Kinds", "III · Shared Or Distributed", "IV · The Speed Limit", "V · The Game Of Life",
     "VI · GPU Computing", "VII · Scaling PyTorch", "VIII · Python, R, MATLAB", "IX · Takeaways"]

OPEN = [
 remotion("BIDEA", "the idea",
    "Namaste! This is Liam, in for Bear. First, a correction. Twice the processors is not twice the speed. The serial "
    "part of your code, and the cost of processors talking to each other, set the limit before the hardware does. This "
    "lecture walks from one core to many GPUs across nodes: why we parallelise, the four kinds of parallel machine, shared "
    "against distributed memory, Amdahl's and Gustafson's laws, a real benchmark of Conway's Game of Life, how GPUs and "
    "PyTorch scale, and the parallel tools in Python, R and MATLAB.",
    "BrutalistHesitantWriter",
    {"text": "Twice the processors,\ntwice the speed", "triggerWords": "twice the speed", "replacementWords": "less than twice the speed",
     "fontSize": 72, "charMs": 62, "hesitateBetween": 6, "hesitateWithin": 1, "mistakeRate": 2, "jitter": 20, "seed": SLUG, "banner": ""},
    [{"at": 0.0, "event": "types the assumption"}, {"at": 0.3, "event": "corrects it"}],
    lane="bookend", lead_silence_s=0.8, motion_claim="The writer types the newcomer's assumption and corrects it.",
    qc={"sparse_by_design": True, "sparse_reason": "Hesitant-writer bookend: the correction is the motion."}),
 remotion("BDEFS", "terms",
    "Six terms. A core: one processing unit that runs instructions on its own. A node: one computer in the cluster, "
    "with its own memory. A thread: a stream of work inside one process, sharing that process's memory. A process: a "
    "running program with its own memory. MPI: the message passing interface, the standard way processes on different "
    "nodes send data to each other. And speedup: serial time divided by parallel time.",
    "ClaudeDefinitions",
    {"title": "Terms In This Lecture",
     "terms": [{"term": "core", "meaning": "one processing unit that runs instructions on its own"},
               {"term": "node", "meaning": "one computer in the cluster, with its own memory"},
               {"term": "thread", "meaning": "a stream of work inside one process, sharing its memory"},
               {"term": "process", "meaning": "a running program with its own memory"},
               {"term": "MPI", "meaning": "message passing: how processes on different nodes exchange data"},
               {"term": "speedup", "meaning": "serial time divided by parallel time"}],
     "folderLabel": "@NikBearBrown"},
    [{"at": 0.08, "event": "core"}, {"at": 0.25, "event": "node"}, {"at": 0.4, "event": "thread"}, {"at": 0.58, "event": "process"}, {"at": 0.72, "event": "MPI"}, {"at": 0.87, "event": "speedup"}],
    gate="CARD", lane="bookend", qc={"sparse_by_design": True, "sparse_reason": "TERMS card: six prerequisites, one line each."}),
]

OMP = """#pragma omp parallel for collapse(2)
for (int i = 1; i <= rows; i++) {
    for (int j = 1; j <= cols; j++) {
        // compute next state for cell (i, j)
    }
}"""
CUDA = """__global__ void MatMulKernel(float *A, float *B,
                             float *C, int N) {
    int row = blockIdx.y * blockDim.y + threadIdx.y;
    int col = blockIdx.x * blockDim.x + threadIdx.x;
    // each thread computes one element of C
}"""
SINGLE = """import torch

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
a = torch.randn(4096, 4096, device=device)
b = torch.randn(4096, 4096, device=device)
c = torch.matmul(a, b)   # runs on the GPU automatically"""
MULTI = """num_gpus = torch.cuda.device_count()
shard_rows = N // num_gpus
shards = []
for i in range(num_gpus):            # a row-shard of A, a full B, per GPU
    device = torch.device(f"cuda:{i}")
    a_shard = torch.randn(shard_rows, N, device=device)
    b_full  = torch.randn(N, N, device=device)
    shards.append((a_shard, b_full))
c_shards = [torch.matmul(a, b) for a, b in shards]   # in parallel
for i in range(num_gpus):
    torch.cuda.synchronize(i)"""
DDP = """import torch.distributed as dist

local_rank = int(os.environ["LOCAL_RANK"])
torch.cuda.set_device(local_rank)
dist.init_process_group(backend="nccl")

tensor = torch.ones(1, device=f"cuda:{local_rank}")
dist.all_reduce(tensor, op=dist.ReduceOp.SUM)
# tensor == world_size means every GPU is talking"""
MPI4PY = """from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

data = rank * 10                      # each rank: its own chunk
result = comm.reduce(data, op=MPI.SUM, root=0)
# launch: mpirun -np 4 python my_script.py"""
RCODE = """library(parallel)
cl <- makeCluster(detectCores() - 1)
results <- parLapply(cl, data_list, my_function)
stopCluster(cl)

library(foreach); library(doParallel)
registerDoParallel(cores = 4)
results <- foreach(i = 1:100) %dopar% { my_function(i) }"""
MATLAB = """parpool('local', 4);
parfor i = 1:1000
    results(i) = my_function(i);
end"""

B = [
 # I
 manim("B10", A[0],
    "Start with why. Simulations, data processing, model training: sooner or later one core isn't fast enough, so we "
    "split the work. Think of laundry. Serial: wash, dry, fold one load, then the next waits. Nine steps for three "
    "loads. Pipelining: while load one dries, load two washes. Five steps. Data parallelism: three washers, three "
    "dryers, three loads at once. Three steps. Most of today is data parallelism: cut a big problem into small ones "
    "and solve them simultaneously.",
    "B10_Laundry",
    "Three timeline grids build one after another from the source's tables: serial (3 loads across 9 time slots, one block per slot), pipelined (5 slots, staggered), data-parallel (3 slots, stacked); each slot is a kraft block labelled wash / dry / fold; the slot count lands as a numeral beside each grid (9 · 5 · 3). Act title top-left.",
    [{"at": 0.25, "event": "serial: 9"}, {"at": 0.5, "event": "pipelined: 5"}, {"at": 0.7, "event": "data parallel: 3"}, {"at": 0.9, "event": "cut a big problem into small ones"}]),
 # II
 manim("B20", A[1],
    "Flynn's taxonomy sorts machines by how instructions and data flow. Single or multiple instruction; single or "
    "multiple data. SISD is an ordinary single core. SIMD is one instruction over many data points at once: that is a GPU. "
    "MISD is rare, fault-tolerant hardware. And MIMD is many instructions over many data: a multi-node cluster, each "
    "task on its own data. Today's two are SIMD, the GPU, and MIMD, the cluster.",
    "B20_Flynn",
    "A 2×2 grid draws with axes 'instruction: single · multiple' and 'data: single · multiple'; each cell lands with its acronym and a tiny cast picture (one core; a GPU block over a row of data squares; a faded cell for MISD; three racks each with its own data box); SIMD and MIMD get the terracotta dot. Act title top-left.",
    [{"at": 0.2, "event": "axes"}, {"at": 0.35, "event": "SISD"}, {"at": 0.5, "event": "SIMD = GPU"}, {"at": 0.62, "event": "MISD"}, {"at": 0.75, "event": "MIMD = cluster"}, {"at": 0.92, "event": "the two that matter"}]),
 # III
 manim("B30", A[2],
    "How processors reach memory decides which tool you use. Shared memory: the cores of one node read one pool of RAM, "
    "any core any address. Easier to program; the tool is OpenMP; the limit is one machine. Distributed memory: each node "
    "has its own RAM, and node A can't read node B's. Programs send data over the network; the tool is MPI; the gain is "
    "that you scale across nodes. Most real HPC codes are hybrid: MPI between nodes, OpenMP inside each.",
    "B30_SharedVsDistributed",
    "Left: one node drawn as a plinth with four core pads all cabled to one memory slab ('RAM'), label 'OpenMP'; right: three nodes each with their own memory slab, joined by a network belt, labels 'MPI'; then 'hybrid' lands as both pictures combine: each node's cores share its slab, and belts link the nodes. Act title top-left.",
    [{"at": 0.15, "event": "shared: one RAM, many cores"}, {"at": 0.4, "event": "OpenMP"}, {"at": 0.55, "event": "distributed: own memory, a network"}, {"at": 0.75, "event": "MPI"}, {"at": 0.9, "event": "hybrid"}]),
 manim("B31", A[2],
    "This maps straight onto Slurm. n tasks is the number of processes, the MPI ranks. CPUs per task is the cores each "
    "process gets for its threads. They multiply: four tasks per node, five CPUs per task, is twenty cores per node. Pure "
    "OpenMP is one task with twenty CPUs. Pure MPI is twenty tasks with one CPU each. Hybrid sits between.",
    "B31_TasksTimesCpus",
    "A node plinth with 20 core pads arranged 4 × 5; four process boxes land, each spanning 5 pads ('--ntasks-per-node=4 · --cpus-per-task=5 · 20'); then the same 20 pads regroup under one box ('1 × 20: OpenMP'), then as twenty single boxes ('20 × 1: MPI'); mono flags beside each arrangement.",
    [{"at": 0.3, "event": "4 × 5 = 20"}, {"at": 0.6, "event": "1 × 20"}, {"at": 0.78, "event": "20 × 1"}]),
 # IV
 manim("B40", A[3],
    "Now the speed limit. Not everything parallelises: reading data, writing results, steps that depend on the last. "
    "Amdahl's law: speedup equals one over S plus P over N, where S is the serial fraction, P the parallel fraction, and N "
    "the number of processors. If ten percent of your code is serial, the most you can ever get is ten times, however "
    "many processors you add. The curve climbs, then flattens. This is strong scaling: the same problem, more cores.",
    "B40_Amdahl",
    "The formula typeset (MathTex: Speedup = 1/(S + P/N), S, P = 1 − S); axes 'processors N' (1…64) and 'speedup'; the S = 0.1 curve draws and bends toward a dashed ceiling at 10 ('10× at most'); a dashed ideal diagonal for contrast; label 'strong scaling'. Act title top-left.",
    [{"at": 0.25, "event": "the formula"}, {"at": 0.55, "event": "S = 0.1: the curve"}, {"at": 0.72, "event": "ceiling at 10×"}, {"at": 0.92, "event": "strong scaling"}]),
 manim("B41", A[3],
    "Gustafson asked the other question: what if the problem grows with the cores? A researcher with a hundred cores "
    "doesn't finish a ten-minute problem in six seconds. They solve a problem a hundred times larger in the same ten "
    "minutes. Speedup equals S plus P times N. That is weak scaling, and it's how most real HPC work gets done. Both laws "
    "are right; they answer different questions. One tip before any code: plan what can be parallel. Retrofitting "
    "parallelism onto finished serial code is painful.",
    "B41_Gustafson",
    "The formula typeset (MathTex: Speedup = S + P·N); the same axes, and a near-straight line climbs beside Amdahl's flattening curve; a clock holding at '10 min' while a problem block grows 100× ('100 cores · 100× the problem'); label 'weak scaling'; a small planning page with a check lands on 'plan what can be parallel'.",
    [{"at": 0.15, "event": "the question"}, {"at": 0.4, "event": "100× the problem, same 10 minutes"}, {"at": 0.55, "event": "S + P·N, near-linear"}, {"at": 0.7, "event": "weak scaling"}, {"at": 0.9, "event": "plan first"}]),
 # V
 manim("B50", A[4],
    "Now a real case. Conway's Game of Life: a grid where each cell's next state depends on its eight neighbours. It is "
    "embarrassingly parallel, because within one time step every cell is independent of every other. A single core "
    "walks the grid row by row. Many cores can take the rows at once.",
    "B50_GameOfLife",
    "A grid of cells; a glider pattern steps forward twice; one cell's eight neighbours ring; then a cursor sweeps the grid row by row ('serial'); then the rows split into four bands that each sweep at once ('parallel'). Act title top-left.",
    [{"at": 0.15, "event": "the glider steps"}, {"at": 0.4, "event": "eight neighbours"}, {"at": 0.6, "event": "independent per step"}, {"at": 0.8, "event": "row by row, then bands at once"}]),
 code("B51", A[4],
    "With OpenMP, one directive above the loop asks the compiler to spread it across the cores of a node. The pragma "
    "collapses the two loops into one parallel space; the compiler creates and distributes the threads.",
    "life_openmp.cpp", OMP, "One pragma; the compiler does the threads.",
    [{"at": 0.1, "event": "the loop prints"}], lang="cpp"),
 shell("B52", A[4],
    "Submitting it: one node, one task, twenty CPUs per task, and the thread count set from Slurm's variable. Ten "
    "thousand by ten thousand cells, five hundred generations.",
    ["#SBATCH -p short", "#SBATCH -N 1", "#SBATCH --ntasks=1", "#SBATCH --cpus-per-task=20", "",
     "export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK", "./life_openmp --rows 10000 --cols 10000 --gens 500"],
    [{"at": 0.1, "event": "one task, twenty CPUs"}, {"at": 0.6, "event": "threads from Slurm"}], start=20, gap=28, title="openmp.sbatch"),
 manim("B53", A[4],
    "When the grid outgrows one node's memory, split it across nodes: domain decomposition. The grid is cut into "
    "horizontal strips, one per MPI rank. But a cell on the edge of a strip needs neighbours from the strip next door, "
    "on another node. So before each step the ranks swap their boundary rows with MPI send and receive. Those borrowed "
    "rows are the halo, or ghost zone.",
    "B53_HaloExchange",
    "The grid splits into four horizontal strips that slide apart onto four node plinths; the top and bottom rows of each strip are highlighted; copies of the boundary rows travel across the gaps to the neighbouring strips and land as ghost rows (dashed outline); labels 'rank 0 … rank 3', 'halo', mono 'MPI_Send / MPI_Recv'.",
    [{"at": 0.2, "event": "strips onto nodes"}, {"at": 0.5, "event": "the edge needs the neighbour"}, {"at": 0.75, "event": "rows swap: the halo"}]),
 shell("B54", A[4],
    "The hybrid job: four nodes, four ranks per node, five threads per rank. Four times four times five is eighty cores, "
    "launched with m p i run and the task count from Slurm.",
    ["#SBATCH -p long", "#SBATCH -N 4", "#SBATCH --ntasks-per-node=4", "#SBATCH --cpus-per-task=5", "",
     "export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK", "mpirun -np $SLURM_NTASKS ./life_mpi_omp \\", "    --rows 10000 --cols 10000 --gens 500",
     "# 4 nodes × 4 ranks × 5 threads = 80 cores"],
    [{"at": 0.1, "event": "four nodes, four ranks, five threads"}, {"at": 0.7, "event": "80 cores"}], start=20, gap=24, title="hybrid.sbatch"),
 manim("B55", A[4],
    "The real numbers, same grid, five hundred iterations. Serial: two hundred fifty seconds. OpenMP on two cores, "
    "two point two times faster. Four cores, four point three. Eight, eight and a half. Twelve, only seven and a half, "
    "slower than eight. Sixteen, ten times. Twenty, twelve point four. Then across nodes with MPI: forty cores, "
    "twenty-five times. Sixty, thirty-seven. Eighty, forty-four. Inside one node the scaling is close to ideal, with no "
    "network in the way. Across nodes the communication cost shows, and the curve bends under the ideal line, exactly as "
    "Amdahl predicted.",
    "B55_Benchmark",
    "Axes 'cores' (1…80) and 'speedup'; a dashed ideal diagonal; the ten real points land one by one as spoken (1:1.0, 2:2.2, 4:4.3, 8:8.5, 12:7.5, 16:10.0, 20:12.4, 40:25.1, 60:36.9, 80:44.0), joined by an ink line, OpenMP points grey, MPI points dark; the 12-core dip gets a small ring; the gap to the ideal line at 80 is bracketed 'communication'; a wall-time column (250.7 s → 5.7 s) ticks beside.",
    [{"at": 0.1, "event": "serial 250 s"}, {"at": 0.3, "event": "OpenMP points climb"}, {"at": 0.42, "event": "the dip at 12"}, {"at": 0.6, "event": "MPI points: 40, 60, 80"}, {"at": 0.85, "event": "the gap to ideal"}]),
 # VI
 manim("B60", A[5],
    "GPUs. A CPU is built for low latency: tens of complex cores, good at sequential logic and branching. A GPU is built "
    "for throughput: thousands of simple cores doing the same operation across a large array. A few professional chefs "
    "cooking complicated dishes, against a thousand line cooks each doing one simple task for a buffet.",
    "B60_CpuVsGpu",
    "A two-column drawn table builds: design goal (latency · throughput), core count (tens, complex · thousands, simple), best for (sequential logic · same operation on large arrays), with a small CPU block and GPU block as the column heads; the GPU's dense grey core grid fills. Act title top-left.",
    [{"at": 0.2, "event": "latency vs throughput"}, {"at": 0.45, "event": "tens vs thousands"}, {"at": 0.65, "event": "best for"}, {"at": 0.85, "event": "chefs vs line cooks"}]),
 manim("B61", A[5],
    "Every GPU program follows four steps. Allocate memory on the device. Copy the data from host to device, CPU to GPU. "
    "Launch a kernel: thousands of threads run the same function on different data. Then copy the results back. Host is "
    "the CPU; device is the GPU.",
    "B61_FourSteps",
    "Left a grey CPU block ('host'), right a dark GPU block ('device'); step 1: a memory slab appears on the device ('cudaMalloc'); step 2: data boxes ride a cable host → device ('cudaMemcpy'); step 3: a grid of terracotta sparks lights across the device ('kernel'); step 4: result boxes ride back ('cudaMemcpy'). Mono step labels land in order.",
    [{"at": 0.2, "event": "allocate"}, {"at": 0.4, "event": "copy in"}, {"at": 0.6, "event": "launch the kernel"}, {"at": 0.8, "event": "copy back"}]),
 code("B62", A[5],
    "A matrix-multiply kernel. Each thread works out its own row and column from its block and thread indices, and "
    "computes exactly one element of the result. For a thousand-by-thousand matrix that is over a million threads, in "
    "parallel. You may never write Kooda yourself: PyTorch, CuPy and RAPIDS do it for you. But this is what they do.",
    "matmul.cu", CUDA, "One thread, one element of C.",
    [{"at": 0.1, "event": "the kernel prints"}], lang="cpp"),
 # VII
 code("B70", A[6],
    "In PyTorch the pattern is: put the tensors on the device, and the library calls the Kooda kernels for you. Two "
    "four-thousand-square matrices and one matmul. Submitted with one GPU on the gpu partition.",
    "single_gpu.py", SINGLE, "Tensors on the device; PyTorch calls the kernels.",
    [{"at": 0.1, "event": "the single-GPU code prints"}]),
 code("B71", A[6],
    "More than one GPU on a node: split one big operation across them. Partition A by rows, give every GPU its shard and "
    "a full copy of B, launch the matmuls, they run in parallel because kernel launches are asynchronous, then "
    "synchronise each device. Submitted with two GPUs on the multigpu partition.",
    "multi_gpu.py", MULTI, "Row shards of A, a full B each, parallel matmuls.",
    [{"at": 0.1, "event": "the sharded code prints"}]),
 code("B72", A[6],
    "Across nodes, PyTorch uses Distributed Data Parallel. The vocabulary: the backend is NCCL, NVIDIA's communication "
    "library, MPI's cousin for GPUs. World size is the total number of GPUs. Rank is each GPU's ID. Local rank is its "
    "index inside its node. The communication test: every GPU holds a one, all-reduce sums them, and if the result equals "
    "the world size, every GPU is talking.",
    "ddp_test.py", DDP, "all_reduce: every GPU contributes, every GPU gets the sum.",
    [{"at": 0.1, "event": "the DDP test prints"}]),
 manim("B73", A[6],
    "The GPU benchmark: a four-thousand-square matmul, a hundred times. One GPU, eleven point seven seconds. Two GPUs on "
    "one node, five and a half seconds: two point one times, near linear over the fast in-node link. Four GPUs across two "
    "nodes, five point one seconds: only two point three times. At this size each GPU gets a tiny shard, and the "
    "cross-node sync costs more than the maths. The computation-to-communication ratio decides how far you can scale.",
    "B73_GpuBench",
    "Three bars grow with their real wall times (11.73 s, 5.48 s, 5.08 s) under labels '1 GPU', '2 GPUs · 1 node', '4 GPUs · 2 nodes'; speedup numerals land (1.0× · 2.1× · 2.3×); a bracket between bars 2 and 3 labelled 'sync > maths'; a small ratio scale 'compute : communication'.",
    [{"at": 0.2, "event": "11.73 s"}, {"at": 0.4, "event": "5.48 s, 2.1×"}, {"at": 0.6, "event": "5.08 s, 2.3×"}, {"at": 0.85, "event": "sync > maths"}]),
 # VIII
 code("B80", A[7],
    "You don't need C or Kooda to go parallel. In Python, mpi4py gives you MPI: a communicator, your rank and the size of "
    "the world, each rank working on its own chunk, and a reduce to rank zero. Launch it with m p i run. Also worth "
    "knowing: multiprocessing for one node, concurrent futures, Dask and Ray.",
    "my_script.py", MPI4PY, "MPI from Python.",
    [{"at": 0.1, "event": "mpi4py prints"}]),
 code("B81", A[7],
    "In R, the parallel package ships with base R: make a cluster of all cores but one, par l apply over your list, stop "
    "the cluster. Or for-each with do-parallel for embarrassingly parallel loops: register four cores and swap do for "
    "do-par.",
    "parallel.rmd", RCODE, "makeCluster, parLapply, or foreach %dopar%.",
    [{"at": 0.1, "event": "the R code prints"}], lang="r"),
 code("B82", A[7],
    "In MATLAB, parpool opens a pool of workers and parfor replaces a for loop. MATLAB distributes the iterations.",
    "parallel.mlx", MATLAB, "parfor replaces for.",
    [{"at": 0.1, "event": "parfor prints"}], lang="matlab"),
 manim("B83", A[7],
    "Choosing the tool. OpenMP: shared memory, loop-level parallelism on one node. MPI: distributed, multi-node "
    "simulations. mpi4py for multi-node Python. multiprocessing for single-node Python tasks. PyTorch DDP for training. "
    "Dask or Ray for big data and pipelines, both memory models. R's parallel and foreach, and MATLAB's parfor, for "
    "embarrassingly parallel loops on one node.",
    "B83_ToolTable",
    "A drawn table builds row by row from the source's eight rows: tool (mono) · memory model · best for; shared rows get a single-slab icon, distributed rows a three-node icon, Dask/Ray both; rows land as spoken. Act title top-left.",
    [{"at": 0.15, "event": "OpenMP"}, {"at": 0.3, "event": "MPI"}, {"at": 0.42, "event": "mpi4py"}, {"at": 0.52, "event": "multiprocessing"}, {"at": 0.62, "event": "PyTorch DDP"}, {"at": 0.72, "event": "Dask / Ray"}, {"at": 0.88, "event": "R, MATLAB"}]),
 # IX
 manim("B90", A[8],
    "Four things to keep. Profile first: find the bottleneck before you parallelise. Choose the level: shared memory on "
    "one node, MPI across nodes, GPUs for data-parallel maths. Communication costs are real: more nodes are not always "
    "faster. And plan for parallelism from the start. Questions: r c help at northeastern dot e d u, or office hours.",
    "B90_Takeaways",
    "Four checkbox rows tick in order (profile first · choose the level · communication costs · plan for parallelism), each with a small cast icon (magnifier · a node slab / three nodes / a GPU block in a row · a belt with a cost tag · a planning page); then 'rchelp@northeastern.edu' lands in mono. Act title top-left.",
    [{"at": 0.1, "event": "profile first"}, {"at": 0.3, "event": "choose the level"}, {"at": 0.55, "event": "communication costs"}, {"at": 0.75, "event": "plan"}, {"at": 0.92, "event": "rchelp"}]),
 shell("B91", A[8],
    "And the three Slurm recipes to keep. OpenMP: one node, one task, twenty CPUs. MPI plus OpenMP: four nodes, four ranks "
    "each, five threads each. GPU: one node, two GPUs.",
    ["# OpenMP: one node, 20 cores", "#SBATCH -N 1", "#SBATCH --ntasks=1", "#SBATCH --cpus-per-task=20", "./my_openmp_program",
     "# MPI + OpenMP: 4 nodes × 4 ranks × 5 threads", "#SBATCH -N 4", "#SBATCH --ntasks-per-node=4", "#SBATCH --cpus-per-task=5",
     "mpirun -np $SLURM_NTASKS ./my_mpi_program", "# GPU: one node, 2 GPUs", "#SBATCH -N 1", "#SBATCH --gres=gpu:2", "python my_training.py"],
    [{"at": 0.1, "event": "OpenMP recipe"}, {"at": 0.45, "event": "MPI + OpenMP recipe"}, {"at": 0.8, "event": "GPU recipe"}], start=15, gap=24, title="recipes.sbatch"),
]

RECAP = ["Pipelining and data parallelism; today is data parallelism.",
         "SIMD is the GPU; MIMD is the cluster. Shared memory: OpenMP. Distributed: MPI.",
         "Amdahl: 10% serial caps you at 10×. Gustafson: grow the problem with the cores.",
         "Game of Life: 12.4× on 20 cores, 44× on 80 across nodes; communication bends the curve.",
         "GPU: allocate, copy in, launch the kernel, copy back. 2 GPUs 2.1×, 4 across nodes 2.3×.",
         "Profile first, choose the level, count communication, plan for parallelism."]
VERDICT = remotion("BVDT", "recap",
    "Let's recap with Claude. Pipelining and data parallelism, and today was data parallelism. SIMD is the GPU, MIMD is "
    "the cluster; shared memory means OpenMP, distributed means MPI. Amdahl: ten percent serial caps you at ten times. "
    "Gustafson: grow the problem with the cores. The Game of Life ran twelve times faster on twenty cores and forty-four "
    "times on eighty across nodes, with communication bending the curve. A GPU program allocates, copies in, launches the "
    "kernel and copies back; two GPUs gave two point one times, four across nodes only two point three. Profile first, "
    "choose the level, count the communication, and plan for parallelism.",
    "ClaudeVerdictArtifact", {"artifactTitle": "Recap", "artifactHeading": TITLE, "artifactLines": RECAP},
    [{"at": 0.0, "event": "artifact page opens"}, {"at": 0.1, "event": "six recap lines land"}],
    lane="bookend", lead_silence_s=0.5, qc={"sparse_by_design": True, "sparse_reason": "Mandated ClaudeVerdictArtifact bookend."})

YT_PROMPT = ("Here is a serial program I want to run faster on a cluster: [describe it and paste the main loop]. First, mark which "
             "parts are inherently serial and estimate my Amdahl ceiling. Then tell me which level fits: threads on one node, "
             "MPI across nodes, or a GPU, and why. Finally, write the Slurm header for that choice with --ntasks and --cpus-per-task "
             "explained.")
YOURTURN = remotion("BHTF", "your turn",
    "Your turn. Paste this into Claude: " + YT_PROMPT + " Then check two things yourself. Did it name the serial part before "
    "it promised a speedup? And do its n tasks times CPUs per task equal the cores you'd actually get?",
    "ClaudeComposerAsk",
    {"greeting": "Your turn.", "topic": "CLAUDE · YOUR TURN", "segment": "Find Your Ceiling, Then Your Level", "command": YT_PROMPT,
     "runningText": "paste this into Claude…",
     "output": ["Check: did it name the serial part before it promised a speedup?", "Check: do ntasks × cpus-per-task equal the cores you'd get?"],
     "folderLabel": "@NikBearBrown", "modelLabel": "Opus 5.5", "effortLabel": "High"},
    [{"at": 0.0, "event": "Composer opens"}, {"at": 0.1, "event": "the prompt types in full"}, {"at": 0.8, "event": "two check lines land"}],
    lane="bookend")

OUTRO = {"beat_id": "BOUT", "act": "outro", "lane": "bookend", "proof_gate": "SHOW",
         "narration_text": f"{TITLE}. At Nik Bear Brown.", "estimated_duration_s": 4.0, "voice": "am_onyx", "engine": "kokoro",
         "shot": {"type": "REMOTION", "source": "own", "show": [{"at": 0.0, "event": "title restates; handle; mascot"}],
                  "remotion": {"pattern": "ClaudeTitleOutro", "props": {"title": TITLE, "slug": SLUG, "handle": "@NikBearBrown", "subline": ""}}},
         "kind": "outro_voice", "tail_silence_s": 1.0}

# Gate V underfill on drawn beats that build progressively (31% / 46% at the sampled midpoint on the first 4K run).
for b in B:
    if b["beat_id"] in {"B10", "B61"} and "qc" not in b:
        b["qc"] = {"sparse_by_design": True, "sparse_reason": SPARSE + " Progressive drawing: the midpoint frame holds only part of the final picture."}
BOPEN = {"beat_id": "BOPEN", "act": "Opening", "lane": "bookend", "proof_gate": "CARD",
         "narration_text": "Research Computing on Explorer and AICR. Intro to Parallel Computing. Threads, processes and scaling across nodes: how work gets split up, and when that actually makes it faster.",
         "estimated_duration_s": 10.0, "voice": "am_onyx", "engine": "kokoro",
         "shot": {"type": "CARD", "source": "own", "template": "lecture-title-slide-16x9", "narration_contract": "playlist-title-summary-v1",
                  "motion": "hold", "visual_intent": "Film identity and short teaching description, visible immediately; Liam speaks playlist, title, summary",
                  "show": [{"at": 0, "event": "Complete portrait/title/series card visible"}]}}
BEATS = [BOPEN] + OPEN + B + [VERDICT, YOURTURN, OUTRO]
sheet = {"metadata": {
    "slug": SLUG, "title": TITLE, "topic": "RESEARCH COMPUTING · PARALLEL COMPUTING", "skill": "lecture", "style_preset": "lecture",
    "channel": "claude-liam", "persona": "Liam (in for Bear)", "voice": "am_onyx", "voice_kokoro": "am_onyx", "engine": "kokoro",
    "clock": "narration", "palette": "claude", "register": "Teardown", "fps": 24, "aspect_ratio": "16:9", "width": 3840, "height": 2160,
    "caption_policy": "none", "greeting_language": "Hindi (Namaste)",
    "audience": "Researchers and students scaling code from one core to many GPUs on a cluster; assumes no other film",
    "source_doc": "hpc/Intro-to-HPC-Scaling-Parallel-Computing-2026/intro_to_parallel_computing.md (Northeastern Research Computing training, "
                  "presenter Ghanghoon 'Will' Paik; github.com/northeastern-rc-training/Intro-to-HPC-Scaling-Parallel-Computing-2026), read 2026-10-06",
    "playlist": "Explorer", "chapter_number": 4,
    "series_title": "Research Computing on Explorer and AICR", "series_video_number": 5, "series_video_count": 13, "series_entry_video": "Video 1 · AICR Introduction",
    "lecture_opening_description": "Threads, processes and scaling across nodes",
    "tags": ["parallel computing", "HPC", "Amdahl's law", "Gustafson's law", "OpenMP", "MPI", "Slurm", "Game of Life", "CUDA", "PyTorch DDP",
             "mpi4py", "Explorer cluster", "Northeastern", "Research Computing", "Nik Bear Brown"]},
    "beats": BEATS}

old = {}
p = HERE / "beat_sheet.json"
if p.exists():
    for ob in json.load(open(p))["beats"]:
        old[ob["beat_id"]] = ob
for b in BEATS:
    ob = old.get(b["beat_id"])
    if ob and ob.get("narration_text") == b["narration_text"]:
        for k in ("actual_duration_s", "audio_file"):
            if k in ob:
                b[k] = ob[k]
    dur = b.get("actual_duration_s")
    props = (b["shot"].get("remotion") or {}).get("props")
    if dur and props is not None:
        pat = b["shot"]["remotion"]["pattern"]
        if pat in ("ClaudeDefinitions", "BrowserCapture", "LibraryIconRow", "CCPlainShell", "ClaudeCodeBeat"):
            props["durationSeconds"] = dur
p.write_text(json.dumps(sheet, indent=2, ensure_ascii=False) + "\n")
print(len(BEATS), "beats; est", round(sum(b.get("actual_duration_s") or b["estimated_duration_s"] for b in BEATS)), "s")
