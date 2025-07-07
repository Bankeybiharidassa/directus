Investigated backend startup failure due to permission errors on integration log files.
Added call to set_permissions.sh in patch_services.sh and install.sh so service logs are created with correct ownership.
Ran pytest and npm test to verify; all tests pass.
