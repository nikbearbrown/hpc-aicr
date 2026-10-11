# SESSION: Logging into Explorer with Claude (evidence log, in progress)

**What this is.** Real terminal output from Bear setting up key login to Northeastern's Explorer cluster, saved verbatim for a future film. **Status.** All five steps done and tested 2026-10-11, including by Claude Code itself. Key login works on Explorer, with no Duo prompt. Only public output is kept: no passphrase, no password, no private key.

## Earlier the same day: password login (real)

`ssh <explorer-username>@login.explorer.northeastern.edu` asked the host-key question (answered `yes`), then the Northeastern password, then landed on login node `explorer-01` with a welcome banner. No Duo prompt appeared. The login name that worked was the access form's UserID (`<explorer-username>`), not the email prefix.

## Step 1: make the key (real, Mac)

```
$ ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519_explorer -C "explorer"
Enter same passphrase again:
Your identification has been saved in <home>/.ssh/id_ed25519_explorer
Your public key has been saved in <home>/.ssh/id_ed25519_explorer.pub
The key fingerprint is:
SHA256:<fingerprint> explorer
The key's randomart image is:
+--[ED25519 256]--+
|      o          |
|     + o         |
|  . + o   .      |
|   + .   o .     |
|  . o + S .      |
| o.+ * * o       |
| +Boo * o        |
|B++E+  * .       |
|%=+*+...=.       |
+----[SHA256]-----+
```

(The first passphrase prompt scrolled off; the passphrase itself was typed by Bear and is not recorded.)

## A real mistake worth keeping: the alias was missing

Before the config block existed, the test failed. This is exactly what a reader sees if they skip the config step:

```
$ ssh -o BatchMode=yes explorer 'whoami; hostname'
ssh: Could not resolve hostname explorer: nodename nor servname provided, or not known
```

Cause: `~/.ssh/config` had no `Host explorer` block, so ssh treated `explorer` as a hostname. Fix: add the block (step 3).

## Step 3: the config block (real)

```
Host explorer
    HostName login.explorer.northeastern.edu
    User <explorer-username>
    IdentityFile ~/.ssh/id_ed25519_explorer
    IdentitiesOnly yes
    AddKeysToAgent yes
    UseKeychain yes
    ServerAliveInterval 60
```

## Step 2: install the key on Explorer (real)

```
$ ssh-copy-id -i ~/.ssh/id_ed25519_explorer.pub explorer
/usr/bin/ssh-copy-id: INFO: Source of key(s) to be installed: "<home>/.ssh/id_ed25519_explorer.pub"
/usr/bin/ssh-copy-id: INFO: attempting to log in with the new key(s), to filter out any that are already installed
/usr/bin/ssh-copy-id: INFO: 1 key(s) remain to be installed -- if you are prompted now it is to install the new keys
<explorer-username>@login.explorer.northeastern.edu's password:

Number of key(s) added:        1

Now try logging into the machine, with: "ssh -i <home>/.ssh/id_ed25519_explorer 'explorer'"
and check to make sure that only the key(s) you wanted were added.
```

Asked for the Northeastern password once (typed by Bear, not recorded). No Duo prompt appeared.

## Step 4: unlock the key once (real, Bear's terminal)

```
$ ssh-add --apple-use-keychain ~/.ssh/id_ed25519_explorer
Enter passphrase for <home>/.ssh/id_ed25519_explorer:
Identity added: <home>/.ssh/id_ed25519_explorer (explorer)
```

## Step 5: the BatchMode test (real, Bear's terminal)

```
$ ssh -o BatchMode=yes explorer 'whoami; hostname'
<explorer-username>
explorer-01
```

## Claude Code runs it (real, from the Claude Code session, 2026-10-11, read-only)

```
$ ssh -o BatchMode=yes explorer 'whoami; hostname; pwd; squeue -u <explorer-username>'
<explorer-username>
explorer-01
/home/<explorer-username>
             JOBID PARTITION     NAME     USER ST       TIME  NODES NODELIST(REASON)
```
(`squeue` printed only its header: no jobs.) No password, passphrase or Duo prompt. The agent held the Explorer key (and the AICR one) before the call.

## The empty-agent test (real, Claude Code session)

```
$ ssh-add -D
All identities removed.
$ ssh-add -l
The agent has no identities.
$ ssh -o BatchMode=yes explorer 'whoami; hostname'
<explorer-username>
explorer-01
$ ssh-add -l
256 SHA256:<fingerprint> explorer (ED25519)
```
With the agent emptied, the login still worked and the Explorer key was back in the agent afterwards: the Keychain reloaded it. The AICR key is loaded the same way on its next use.

## Findings

- Explorer accepts key login for this account. No Duo prompt appeared on the key login or on the earlier password login.
- Nothing was run on the cluster beyond whoami, hostname, pwd and squeue (read-only).
- NOT tested: key login from off-campus or on a different network; OnDemand; whether Research Computing permits automated agent access (the policy pages mention none; ask rchelp@northeastern.edu).
