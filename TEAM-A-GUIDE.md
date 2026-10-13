# Teammate A: current cloud handoff

The OpenCode Droplet replaces the earlier Hermes/Harness Runtime setup. The [previous detailed guide](archive/TEAM-A-GUIDE-HARNESS-RUNTIME.md) is historical. Follow [BUILD-GUIDE.md](BUILD-GUIDE.md) for the active workflow.

## Already working

- Droplet ID 608613396, public IP 134.209.114.233.
- SSH access; OpenCode 1.18.27 at /root/.opencode/bin/opencode.
- Workspace /root/research-workbench.
- Default provider model digitalocean/router:general; actual response and file tools verified.
- Source, compressed file and notes backed up locally.

## Remaining handoff checks

1. Record hosting-team usable balance, actual Droplet size/rate and credit eligibility. Do not assume the cheaper size was selected.
2. Inspect general router policy and available request usage; record facts without changing it unnecessarily.
3. Verify native Evaluations access; teammate C checks dataset preview and fixed model/judge settings.
4. Keep secrets out of shared notes, exports and screenshots. Never print auth.json.
5. Preserve outputs locally. Powering off does not stop Droplet billing; destruction needs a separate instruction.

Read WALKTHROUGH.md for the simple explanation and tasks/todo.md for live progress. The assistant owns research preparation and integration; teammate C can operate native evaluation while A confirms account details. No additional cloud resources are required.
