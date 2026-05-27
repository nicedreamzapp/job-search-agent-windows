# Running `job-search-agent` daily on macOS

Schedule `jobscout.py` to run every morning with `launchd`. This is the
macOS native equivalent of cron — survives reboots, runs even when you're
logged out (with the right config), and integrates with the system log.

## 1. Verify a manual run works first

Before automating, confirm the tool works end-to-end:

```bash
cd /path/to/job-search-agent
python3 jobscout.py --dry-run
```

You should see jobs being fetched and a results file written. If
anything fails, fix that first — debugging a LaunchAgent that's failing
silently is much harder than debugging an interactive run.

## 2. Write the plist

Create `~/Library/LaunchAgents/com.example.jobscout.plist`. Customize
the paths and the run time:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.example.jobscout</string>

    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/Users/YOUR_USERNAME/path/to/job-search-agent/jobscout.py</string>
    </array>

    <!-- Run every day at 07:30 local time -->
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>7</integer>
        <key>Minute</key>
        <integer>30</integer>
    </dict>

    <!-- Working dir is the repo so relative imports resolve -->
    <key>WorkingDirectory</key>
    <string>/Users/YOUR_USERNAME/path/to/job-search-agent</string>

    <!-- Optional: feed env vars to the agent -->
    <key>EnvironmentVariables</key>
    <dict>
        <key>JOBSCOUT_CONFIG_DIR</key>
        <string>/Users/YOUR_USERNAME/.config/jobscout</string>
        <key>JOBSCOUT_STATE_DIR</key>
        <string>/Users/YOUR_USERNAME/.local/state/jobscout</string>
        <!-- Uncomment if you want the Anthropic fallback:
        <key>ANTHROPIC_API_KEY</key>
        <string>sk-ant-...</string>
        -->
    </dict>

    <!-- Log files for debugging -->
    <key>StandardOutPath</key>
    <string>/tmp/jobscout.log</string>
    <key>StandardErrorPath</key>
    <string>/tmp/jobscout.err</string>

    <!-- Don't run when the LaunchAgent is first loaded — only on schedule -->
    <key>RunAtLoad</key>
    <false/>
</dict>
</plist>
```

Replace `YOUR_USERNAME` and the path to your clone of this repo.

## 3. Load it

```bash
launchctl unload ~/Library/LaunchAgents/com.example.jobscout.plist 2>/dev/null
launchctl load   ~/Library/LaunchAgents/com.example.jobscout.plist
```

Verify it's registered:

```bash
launchctl list | grep jobscout
```

## 4. Test the schedule fires

You can force an immediate run without waiting for 07:30:

```bash
launchctl kickstart -k gui/$(id -u)/com.example.jobscout
```

Then check the logs:

```bash
tail -n 50 /tmp/jobscout.log /tmp/jobscout.err
```

If the run worked, today's results are in
`$JOBSCOUT_STATE_DIR/results/<today>.json`.

## 5. Optional: read the results in your morning routine

A nice habit: pipe the top results into your terminal motd, your shell
greeting, or a desktop notification when you sit down at the computer.

```bash
# Add to ~/.zshrc or wherever
jq -r '.jobs | sort_by(-.score) | .[0:5] | .[] | "[\(.score)] \(.company_name) — \(.title)"' \
  ~/.local/state/jobscout/results/$(date +%Y-%m-%d).json
```

That prints the day's top 5 with score, company, and title. Two seconds
of attention; you decide what (if anything) to apply to.

## Troubleshooting

- **"command not found: python3"** — LaunchAgents run with a minimal
  PATH. Always use the absolute path `/usr/bin/python3` in
  `ProgramArguments`. If you need a specific Python (homebrew,
  pyenv), use its absolute path.
- **Network access denied** — recent macOS releases prompt for
  network access on first run of a LaunchAgent. Watch System
  Preferences → Privacy & Security the first morning it tries.
- **Nothing in `/tmp/jobscout.log`** — the plist didn't load. Check
  syntax with `plutil ~/Library/LaunchAgents/com.example.jobscout.plist`
  and try `launchctl load` again.
- **Runs but no scores** — the LLM endpoint isn't reachable. Either
  start your local MLX server before 07:30 (or use a `KeepAlive`
  block on a separate LaunchAgent for the server), or set
  `ANTHROPIC_API_KEY` in the plist's `EnvironmentVariables`.
