

# attach the midpoint guard (see ST)
for _cls in (B10_ClusterShape, B11_ExplorerNumbers, B12_Plumbing, B20_TwoDoors, B30_TwoWaysIn, B60_LeaveTheLoginNode, B40_FourPlaces, B41_Quotas, B62_Partitions, B63_WhichPartition, B80_Seff):
    _cls.play = ST.play
