

# attach the midpoint guard (see ST)
for _cls in (B60_GpuLogs, B72_ParcelsVsCrate, B80_FourHabits, B10_GpuPartitions, B20_FewVsThousands, B21_FerrarisAndBicycles):
    _cls.play = ST.play
