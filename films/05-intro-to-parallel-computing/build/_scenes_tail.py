

# attach the midpoint guard (see ST)
for _cls in (B40_Amdahl, B41_Gustafson, B53_HaloExchange, B55_Benchmark, B73_GpuBench, B60_CpuVsGpu, B61_FourSteps, B83_ToolTable, B90_Takeaways, B10_Laundry, B20_Flynn, B30_SharedVsDistributed, B31_TasksTimesCpus, B50_GameOfLife):
    _cls.play = ST.play
