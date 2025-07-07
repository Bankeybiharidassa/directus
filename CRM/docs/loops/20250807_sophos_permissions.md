Backend failed due to unwritable /var/log/nucleus/sophos.log.
Reverted log fallback and updated set_permissions.sh to create the file with
correct ownership. Tests pass and log saved in logs/codex_loop_run_20250807-0000.log.
