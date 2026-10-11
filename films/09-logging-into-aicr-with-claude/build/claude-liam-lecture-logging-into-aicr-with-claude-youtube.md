Logging into AICR with Claude

How to let Claude Code log into the AICR cluster for you and run commands there, while your key and your passphrase never leave your hands. Video 9 of 13 in the series Research Computing on Explorer and AICR. New here? Start with Video 1 · AICR Introduction. Liam, in for Bear, narrates.

Chapters
0:00 Opening
0:12 The idea
0:26 Terms in this lecture
0:47 I · What AICR Checks
2:08 II · Unlock Once
3:36 III · Do It For Real
5:17 IV · Rules For A Shared Cluster
6:36 V · When It Fails
7:40 Recap
8:02 Your turn

Your turn. Paste this into Claude:
Log into the AICR cluster with `ssh aicr` and run read-only commands only. Run: whoami, hostname, pwd, sinfo -o "%14P %11l %6D", squeue -u $USER. Tell me the user name, the host, and which partitions exist. Do not submit, cancel or change anything, and do not run computation on the login node.
Then check two things yourself: did Claude run only read-only commands, nothing that submits or changes? did Claude ever ask for, or print, your passphrase or key? It should not.

Sources
The AICR documentation SSH page (certificate authentication, key files, login-node limits, troubleshooting) and a real, read-only Claude Code session on a Mac, recorded for this film. Every terminal line on screen is copied from that session.

Made with the brutalist.art toolkit: Manim, Remotion and Kokoro, free and local. Narration is synthetic (Liam, in for Bear). This is an independent educational film, not an official Northeastern or AICR publication. Every factual claim in this video was checked against primary sources before rendering.

#AICR #AIComputeResource #ClaudeCode #SSH #sshagent #SSHcertificate #BatchMode #NortheasternUniversity
