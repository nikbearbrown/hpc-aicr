

# attach the midpoint guard (see ST)
for _cls in (B50_ThreeByThree, B51_DecodeTheLine, B71_TheToolbelt, B10_LinuxFamily, B20_PathsAndColours, B32_RemoveIsForever):
    _cls.play = ST.play
