# SESSION: what was really run

**What this is.** The record behind every terminal beat in the film "Logging into AICR with Claude". **Result.** Three real runs from a Claude Code session on macOS, Sun Oct 11 2026, all read-only, one account (`<aicr-username>`). Nothing was submitted, changed or deleted on the cluster.

## Run 1: first login, read-only commands (13:26 EDT)

The agent held no keys before this call (`ssh-add -l`: "The agent has no identities").

```
$ ssh -o BatchMode=yes aicr 'whoami; hostname; date; sinfo -o "%14P %11l %6D"; squeue -u $USER; pwd'
<aicr-username>
login.aicr.ai
Sun Oct 11 13:26:40 EDT 2026
PARTITION      TIMELIMIT   NODES
cpu*           1-00:00:00  5
rtx-batch      1-00:00:00  17
b200-batch     1-00:00:00  25
b200-fullnode  1-00:00:00  4
rtx-devel      4:00:00     2
b200-devel     4:00:00     2
preemptable    1-00:00:00  46
(squeue: header only, no jobs)
/home/<aicr-username>
```

## Run 2: how it authenticated (`ssh -v`, lines filtered)

```
$ ssh -G aicr | grep -iE '^(hostname|user|identityfile|certificatefile|identitiesonly|addkeystoagent|serveraliveinterval) '
user <aicr-username>
hostname login.aicr.ai
identitiesonly yes
serveraliveinterval 60
identityfile ~/.ssh/id_ed25519_aicr
certificatefile ~/.ssh/id_ed25519_aicr-cert.pub
addkeystoagent true

$ ssh-add -l
256 SHA256:<fingerprint> <aicr-username>@aicr.ai (ED25519)        <- the call in Run 1 loaded it

$ ssh -v -o BatchMode=yes aicr true      (filtered)
debug1: get_agent_identities: agent returned 1 keys
debug1: Offering public key: ~/.ssh/id_ed25519_aicr-cert.pub ED25519-CERT SHA256:<fingerprint> explicit
debug1: Server accepts key: ~/.ssh/id_ed25519_aicr-cert.pub ED25519-CERT SHA256:<fingerprint> explicit
Authenticated to login.aicr.ai ([192.69.103.11]:22) using "publickey".
```

## Run 3: the agent-empty test (13:30 EDT)

```
$ ssh-add -l
256 SHA256:<fingerprint> <aicr-username>@aicr.ai (ED25519)

$ ssh-add -D
All identities removed.

$ ssh-add -l
The agent has no identities.

$ ssh -o BatchMode=yes aicr 'whoami; hostname'
<aicr-username>
login.aicr.ai

$ ssh-add -l
256 SHA256:<fingerprint> <aicr-username>@aicr.ai (ED25519)
```

With the agent emptied, `BatchMode=yes` still logged in and the agent had the key again afterwards. That is `AddKeysToAgent` plus the macOS Keychain doing their job: no prompt, no passphrase typed, nothing passed to Claude.

## Certificate (public file, `ssh-keygen -L -f ~/.ssh/id_ed25519_aicr-cert.pub`)

```
Type: ssh-ed25519-cert-v01@openssh.com user certificate
Key ID: "<aicr-username>@aicr.ai"
Valid: forever
Principals: <aicr-username>
Extensions: permit-X11-forwarding permit-agent-forwarding permit-port-forwarding permit-pty permit-user-rc
```

(The AICR docs say certificates are short-lived and can be renewed in OnDemand. This account's certificate is marked `forever`. The guide tells readers to check theirs.)

## Not run

`sbatch`, `scancel`, `srun`, `salloc`, any write on the cluster, and the OnDemand sign-in (human-only). The passphrase and the private key were never read or printed.
