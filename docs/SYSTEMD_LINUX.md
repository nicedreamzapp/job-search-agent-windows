# Running `job-search-agent` daily on Linux

Schedule `jobscout.py` to run every morning with a `systemd` user timer.
This is the Linux equivalent of macOS launchd or classic cron — survives
reboots, integrates with `journalctl`, and runs without root.

## 1. Verify a manual run works first

Before automating, confirm the tool works end-to-end:

```bash
cd /path/to/job-search-agent
python3 jobscout.py --dry-run
```

You should see jobs being fetched and a results file written. If
anything fails, fix that first — debugging a systemd unit that's
failing silently is much harder than debugging an interactive run.

## 2. Write the service unit

Create `~/.config/systemd/user/jobscout.service`. Customize the
`ExecStart` path and the environment variables to match your install:

```ini
[Unit]
Description=job-search-agent — daily LLM-scored job briefing
Documentation=https://github.com/USER/job-search-agent
After=network-online.target
Wants=network-online.target

[Service]
Type=oneshot
WorkingDirectory=%h/path/to/job-search-agent
ExecStart=/usr/bin/python3 %h/path/to/job-search-agent/jobscout.py

# Feed env vars to the agent
Environment=JOBSCOUT_CONFIG_DIR=%h/.config/jobscout
Environment=JOBSCOUT_STATE_DIR=%h/.local/state/jobscout
# Uncomment if you want the Anthropic fallback:
# Environment=ANTHROPIC_API_KEY=sk-ant-...

# Log to the journal — view with `journalctl --user -u jobscout`
StandardOutput=journal
StandardError=journal
```

`%h` expands to the user's home directory. No need to hard-code
`/home/yourname`.

## 3. Write the timer unit

Create `~/.config/systemd/user/jobscout.timer`. This is what actually
schedules the service to run:

```ini
[Unit]
Description=Run job-search-agent every morning at 07:30
Documentation=https://github.com/USER/job-search-agent

[Timer]
# Daily at 07:30 local time
OnCalendar=*-*-* 07:30:00

# If the machine was off at 07:30, run as soon as it's back up
Persistent=true

# Spread the wake-up across a 5-minute window so a hundred copies of
# this timer don't all hit the same ATS endpoint at once
RandomizedDelaySec=300

[Install]
WantedBy=timers.target
```

## 4. Enable and start the timer

```bash
# Reload systemd's view of your user units
systemctl --user daemon-reload

# Enable the timer so it survives reboots, and start it now
systemctl --user enable --now jobscout.timer
```

Verify it's registered and scheduled:

```bash
systemctl --user list-timers --all | grep jobscout
```

You should see the next scheduled run.

## 5. Allow it to run when you're logged out (optional)

By default, user services only run while you're logged in. To let them
run even when you're not at a session, enable lingering for your user:

```bash
sudo loginctl enable-linger "$USER"
```

Now the timer fires at 07:30 whether or not you're logged in. Useful on
a server or always-on workstation.

## 6. Test the schedule fires

Force an immediate run without waiting for the next scheduled time:

```bash
systemctl --user start jobscout.service
```

Watch the logs:

```bash
journalctl --user -u jobscout.service -f
```

If the run worked, today's results are in
`$JOBSCOUT_STATE_DIR/results/<today>.json`.

## 7. Optional: read the results in your morning routine

A nice habit: pipe the top results into your shell greeting or a desktop
notification when you sit down at the computer.

```bash
# Add to ~/.bashrc, ~/.zshrc, ~/.profile, etc.
jq -r '.jobs | sort_by(-.score) | .[0:5] | .[] | "[\(.score)] \(.company_name) — \(.title)"' \
  ~/.local/state/jobscout/results/$(date +%Y-%m-%d).json 2>/dev/null
```

That prints the day's top 5 with score, company, and title. Two seconds
of attention; you decide what (if anything) to apply to.

## Troubleshooting

- **"python3: command not found"** — systemd runs with a minimal `PATH`.
  Always use an absolute path in `ExecStart` (`/usr/bin/python3`,
  `/usr/local/bin/python3.11`, or the output of `which python3`).
- **Service ran but produced no scores** — the LLM endpoint isn't
  reachable. Either start your local server before 07:30 (or run it as
  its own systemd user service), or set `ANTHROPIC_API_KEY` in the
  service unit's `Environment=` lines.
- **Timer never fires** — check `systemctl --user list-timers`. If the
  timer isn't listed, you forgot `systemctl --user daemon-reload` after
  editing. If it's listed but `NEXT` is in the past, the schedule
  expression in `OnCalendar` is malformed — validate with
  `systemd-analyze calendar "*-*-* 07:30:00"`.
- **Runs on a headless box but no network at boot** — make sure the
  `[Unit]` block has `After=network-online.target` and
  `Wants=network-online.target`; otherwise the connectors race the
  network and fail.
- **Stops running when I log out** — see step 5; you need
  `loginctl enable-linger` for user units to survive logout.

## Why not classic `cron`?

You can absolutely use cron — `30 7 * * * /usr/bin/python3 /path/to/jobscout.py`
in `crontab -e` is one line and works fine. systemd timers give you
journal integration, on-resume catch-up via `Persistent=true`, and
`RandomizedDelaySec` for free; for a daily personal job that's gravy
but not required. Pick whichever fits your stack.
