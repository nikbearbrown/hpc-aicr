

# attach the midpoint guard (see ST)
for _cls in (B10_LaptopVsCluster, B11_LoginNodeAndFilesystem, B21_WhatModuleLoadDoes, B31_CondaPitfalls, B40_TheSpackSpec, B51_ThreeFlagsToModulefile, B52_SpackVsEasyBuild, B61_SourceBuildPipeline, B63_PersonalModuleStack, B70_ApptainerVsDocker, B80_SixToolsTable, B81_DecisionOrder):
    _cls.play = ST.play
