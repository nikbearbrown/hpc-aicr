# Logging into AICR with Claude

**What this is.** A step-by-step guide to letting Claude Code log into the AICR cluster (`login.aicr.ai`) for you, so it can run commands there. It works for any AICR user on macOS, Linux or Windows. Nothing in it is specific to one machine.

**Why it works.** AICR has no password. You log in with a private key plus a certificate that AICR's own certificate authority signed. Claude Code cannot type a passphrase, and it should never see one. So you unlock the key once, in your own terminal, and let your computer's `ssh-agent` hold it. After that, every `ssh` Claude runs is already unlocked. Claude does the work; the secret never passes through it.

**What was found.** This was done for real on 2026-10-11, and the transcript is in [`SESSION.md`](SESSION.md). Claude Code ran `ssh aicr` with `BatchMode=yes` (which refuses to prompt for anything), and it authenticated and printed the user name, the host and the live partitions. Then the agent was emptied on purpose (`ssh-add -D`), and the same login still worked: the key reloaded itself. That is the test of whether it will keep working after a reboot.

**What you do yourself, and what Claude does.**

| Step | Who |
|---|---|
| Get an AICR account (your PI's proposal, then your institution) | You |
| Sign in at https://ood.aicr.ai and download your key files | You |
| Put the files in `~/.ssh`, set permissions, choose a passphrase | You |
| Unlock the key once so the agent keeps it | You |
| Run `ssh aicr ...` and read the output | Claude |
| Anything that submits, changes or deletes on the cluster | Claude asks first |

---

## 0. Before you start

You need an AICR account. Access comes through a project: a PI's proposal opens it, and your institution's research-computing team creates your user. Your AICR user name looks like `institutionalusername_institutioncode`, for example `jsmith_neu`. It is similar to your campus name but not the same, and it was sent to you when the account was created. Everything below uses `AICR_USERNAME` for it.

You also need Claude Code installed, and a terminal where `ssh` works. macOS and Linux have it. Windows 10 and 11 have OpenSSH built in (PowerShell or Windows Terminal).

## 1. Get your key files (human-only)

1. Open https://ood.aicr.ai and sign in with your institutional credentials. This is the AICR OnDemand portal.
2. Go to **Files → Home Directory**. Download the `aicr_keys` folder (the `...` menu, then **Download**).
3. Unzip it. You should have four files:

| File | What it is |
|---|---|
| `id_ed25519_aicr` | your **private key** (passphrase-protected). Never share it, never paste it anywhere |
| `id_ed25519_aicr.pub` | your public key |
| `id_ed25519_aicr-cert.pub` | your certificate, signed by AICR's certificate authority. This is the credential |
| `.passphrase` | the key's first passphrase |

Signing in is the human step. Do not give Claude your institutional password, and do not ask it to sign in for you.

## 2. Install the files and set a passphrase

macOS or Linux:

```bash
mkdir -p ~/.ssh && chmod 700 ~/.ssh
mv ~/Downloads/aicr_keys/id_ed25519_aicr* ~/.ssh/
chmod 600 ~/.ssh/id_ed25519_aicr
chmod 644 ~/.ssh/id_ed25519_aicr.pub ~/.ssh/id_ed25519_aicr-cert.pub
ssh-keygen -p -f ~/.ssh/id_ed25519_aicr
```

The last command asks for the old passphrase (the one in `.passphrase`) and then a new one. Choose one you will remember. Then delete the downloaded `.passphrase` file.

Windows (PowerShell): put the files in `C:\Users\YOU\.ssh\` and run the same `ssh-keygen -p -f $HOME\.ssh\id_ed25519_aicr`. Under WSL, use the Linux commands inside WSL.

Check that the certificate is the one you expect and when it expires:

```bash
ssh-keygen -L -f ~/.ssh/id_ed25519_aicr-cert.pub
```

Look at **Principals** (it must be your AICR user name) and **Valid** (a date range, or `forever`). When it nears the end, renew it in the OnDemand portal's SSH Certificate app and replace the file.

## 3. Add AICR to your SSH config

Add one block to `~/.ssh/config` (create the file if it is missing). Keep a single `Host aicr` block; two of them work, but the merged result is hard to read.

```
Host aicr
    HostName login.aicr.ai
    User AICR_USERNAME
    IdentityFile ~/.ssh/id_ed25519_aicr
    CertificateFile ~/.ssh/id_ed25519_aicr-cert.pub
    IdentitiesOnly yes
    ServerAliveInterval 60
    AddKeysToAgent yes
    IgnoreUnknown UseKeychain
    UseKeychain yes
```

- `IdentitiesOnly yes` offers only this key, not every key in your agent.
- `ServerAliveInterval 60` stops idle connections dropping.
- `AddKeysToAgent yes` loads the key into the agent the first time it is used.
- `UseKeychain yes` is macOS-only: it lets the macOS Keychain remember the passphrase. `IgnoreUnknown UseKeychain` is what makes Linux and Windows ignore that line instead of failing with "Bad configuration option".

Now `ssh aicr` is the whole command. Optionally add `alias aicr='ssh aicr'` to your shell profile.

## 4. Unlock the key once (this is the step that makes Claude possible)

Claude Code runs commands without a keyboard attached. If `ssh` has to ask for a passphrase, it cannot answer, and the command fails or hangs. The fix is not to give Claude the passphrase. The fix is to unlock the key before Claude arrives, into the `ssh-agent`.

**macOS** (stores the passphrase in the Keychain, so it survives restarts):

```bash
ssh-add --apple-use-keychain ~/.ssh/id_ed25519_aicr
```

**Linux** (one agent per login session):

```bash
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519_aicr
```

Start Claude Code from that same terminal, so it inherits the agent. (A desktop environment that already runs an agent, such as GNOME Keyring, works too.)

**Windows** (PowerShell, run as administrator once):

```powershell
Get-Service ssh-agent | Set-Service -StartupType Automatic
Start-Service ssh-agent
ssh-add $HOME\.ssh\id_ed25519_aicr
```

Each of these asks for your passphrase in your own terminal. Type it there. Confirm the agent holds the key:

```bash
ssh-add -l
```

You should see one line ending in `(ED25519)`, and the comment shows your certificate identity.

## 5. Test the way Claude will use it

First, by hand:

```bash
ssh aicr hostname
```

You should get `login.aicr.ai`. The very first connection to a new machine asks you to confirm the host key; type `yes` yourself. Claude cannot answer that prompt, so do it before handing over.

Then test it the way Claude connects, with no prompting allowed:

```bash
ssh -o BatchMode=yes aicr 'whoami; hostname'
```

`BatchMode=yes` makes `ssh` fail at once instead of asking for anything. If this prints your user name and `login.aicr.ai`, Claude can log in. Then prove it survives an empty agent, which is what a reboot does:

```bash
ssh-add -D                                     # empty the agent
ssh -o BatchMode=yes aicr 'whoami; hostname'   # must still work (macOS Keychain reloads the key)
ssh-add -l                                     # the key is back
```

On Linux and Windows there is no Keychain to reload it, so this test fails until you run `ssh-add` again; that is expected, and it tells you to add the `ssh-add` to your session start. If it prints `Permission denied (publickey)`, the key is not unlocked or the certificate is wrong: see Troubleshooting.

## 6. Ask Claude to log in

Open Claude Code in a terminal and paste something like this:

```
Log into the AICR cluster with `ssh aicr` and run read-only commands only.
Run: whoami, hostname, pwd, sinfo -o "%14P %11l %6D", squeue -u $USER.
Tell me the user name, the host, and which partitions exist.
Do not submit, cancel or change anything, and do not run computation on the login node.
```

Claude should run a command like:

```bash
ssh -o BatchMode=yes aicr 'whoami; hostname; pwd; sinfo -o "%14P %11l %6D"; squeue -u $USER'
```

and report the result. Approve the command when Claude Code asks. Approving each `ssh` command, at least the first few times, is a good habit on a shared system.

A short real example of what comes back (from the 2026-10-11 run, partition list shortened):

```
<aicr-username>
login.aicr.ai
/home/<aicr-username>
PARTITION      TIMELIMIT   NODES
cpu*           1-00:00:00  5
rtx-batch      1-00:00:00  17
b200-batch     1-00:00:00  25
rtx-devel      4:00:00     2
b200-devel     4:00:00     2
```

## 7. Rules for Claude on a shared cluster

Put these in your prompt, or in a `CLAUDE.md` in the project:

1. **Read-only first.** Look before you change: `sinfo`, `squeue -u $USER`, `sacct`, `jobstats JOBID`, `ls`, `module avail`.
2. **Never compute on a login node.** Login nodes are shared and capped at 4 CPU cores and 8 GB of memory per user. Heavy work goes through Slurm: `sbatch`, or `salloc` / `srun` for an interactive session.
3. **Ask before `sbatch`, `scancel`, `rm`, or anything that writes outside your own project.** Jobs use shared GPUs and count against your project.
4. **Never print, copy or upload the private key.** Not `cat`, not `scp`, not into the chat. Claude does not need to read `~/.ssh/id_ed25519_aicr` to use it; the agent does that.
5. **Never put the passphrase in a prompt, a file or a command.** If a command asks for it, stop and unlock the key yourself (step 4).
6. **Use your own account only.** The certificate names you. Do not use it to run work for anyone else.
7. **Mind where files live.** Home is small and recoverable; scratch is large and purged. Check AICR's file-system page before moving data.

## 8. Troubleshooting

| You see | Usually means | Fix |
|---|---|---|
| `Permission denied (publickey)` | The key is not unlocked (by far the most common after a reboot), or the certificate is expired or missing, or the permissions are wrong | Run `ssh-add -l` first: an empty agent looks exactly like an expired certificate. Then `ssh-keygen -L -f ~/.ssh/id_ed25519_aicr-cert.pub` (is it valid?), renew in OnDemand if not, and `chmod 600` the private key |
| Claude's command hangs, or says it needs a passphrase | The key is not in the agent | Do step 4 in your own terminal, then retry. Test with `BatchMode=yes` |
| `Host key verification failed` | The host key changed | `ssh-keygen -R login.aicr.ai`, then connect once yourself and confirm |
| A prompt to confirm a new host key | First connection from this machine | Type `yes` yourself, once, outside Claude |
| `Bad configuration option: usekeychain` | `UseKeychain` is macOS-only | Add `IgnoreUnknown UseKeychain` above it, or remove the line |
| `Connection timed out` | Network or firewall (AICR needs no VPN) | Try another network; check a local firewall |
| Connection drops when idle | No keepalive | `ServerAliveInterval 60` in the config block |
| `ssh-add -l` says the agent has no identities after a restart | The agent forgot the key | macOS: `ssh-add --apple-use-keychain` again. Linux: run `ssh-add` again at the start of each session |

## 9. Where this comes from

- The AICR documentation's SSH page (certificate, key files, config, login-node limits, troubleshooting) and Getting Started page. These are in [`../aicr/`](../aicr/) as saved copies.
- The real run in [`SESSION.md`](SESSION.md).
- The film built from this guide: see `youtube/claude-liam-lecture-logging-into-aicr-with-claude/`.

*Last checked 2026-10-11 against the AICR documentation page dated June 1, 2026. If AICR changes how certificates are issued, the documentation wins over this file.*
