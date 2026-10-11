

# attach the midpoint guard (see ST); the classes stay literal `(Scene)` for run.sh scene discovery
for _cls in (B21_TwoGauges, B22_TwoAxes, B30_FourLayers, B31_DevelToBatch, B33_ReadTheTrace, B40_Factory, B42_FortyFiveNine, B10_SilentFailures, B11_PartitionTable, B13_RamVsVram, B14_VerifyFive, B15_VisibleDevices, B16_IdleCancel, B20_NvidiaSmi, B44_FourKnobs, B50_TwoMeters, B51_DecisionTable, B52_BinarySearch, B54_BitLadder, B55_MixedSafetyNet, B60_EightyRule, B61_AllReduce, B63_ScalingEfficiency, B70_TheLoop, B71_DecisionTree, B72_Jobstats, B73_Checklist):
    _cls.play = ST.play
