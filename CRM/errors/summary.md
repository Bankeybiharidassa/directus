/var/log/nucleus/backend.log
PermissionError: [Errno 13] Permission denied: '/opt/nucleus-platform/CRM/logs/integration/tenable.log'
Traceback (most recent call last):
  File "<frozen runpy>", line 198, in _run_module_as_main
  File "<frozen runpy>", line 88, in _run_code
  File "/usr/lib/python3/dist-packages/uvicorn/__main__.py", line 4, in <module>
    uvicorn.main()
  File "/usr/lib/python3/dist-packages/click/core.py", line 1157, in __call__
    return self.main(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3/dist-packages/click/core.py", line 1078, in main
    rv = self.invoke(ctx)
         ^^^^^^^^^^^^^^^^
  File "/usr/lib/python3/dist-packages/click/core.py", line 1434, in invoke
    return ctx.invoke(self.callback, **ctx.params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3/dist-packages/click/core.py", line 783, in invoke
    return __callback(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3/dist-packages/uvicorn/main.py", line 418, in main
    run(
  File "/usr/lib/python3/dist-packages/uvicorn/main.py", line 587, in run
    server.run()
  File "/usr/lib/python3/dist-packages/uvicorn/server.py", line 62, in run
    return asyncio.run(self.serve(sockets=sockets))
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.12/asyncio/runners.py", line 194, in run
    return runner.run(main)
           ^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.12/asyncio/runners.py", line 118, in run
    return self._loop.run_until_complete(task)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "uvloop/loop.pyx", line 1516, in uvloop.loop.Loop.run_until_complete
  File "/usr/lib/python3/dist-packages/uvicorn/server.py", line 69, in serve
    config.load()
  File "/usr/lib/python3/dist-packages/uvicorn/config.py", line 458, in load
    self.loaded_app = import_from_string(self.app)
                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3/dist-packages/uvicorn/importer.py", line 21, in import_from_string
    module = importlib.import_module(module_str)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.12/importlib/__init__.py", line 90, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1331, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 935, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 995, in exec_module
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "/opt/nucleus-platform/CRM/backend/main.py", line 15, in <module>
    from .routes import (
  File "/opt/nucleus-platform/CRM/backend/routes/__init__.py", line 1, in <module>
    from . import (
  File "/opt/nucleus-platform/CRM/backend/routes/assets.py", line 5, in <module>
    from scripts import sophos_sync, tenable_sync
  File "/opt/nucleus-platform/CRM/scripts/tenable_sync.py", line 3, in <module>
    from backend.services import tenable
  File "/opt/nucleus-platform/CRM/backend/services/tenable.py", line 11, in <module>
    handler = logging.FileHandler(log_path)
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.12/logging/__init__.py", line 1231, in __init__
    StreamHandler.__init__(self, self._open())
                                 ^^^^^^^^^^^^
  File "/usr/lib/python3.12/logging/__init__.py", line 1263, in _open
    return open_func(self.baseFilename, self.mode,
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
PermissionError: [Errno 13] Permission denied: '/opt/nucleus-platform/CRM/logs/integration/tenable.log'
Error in sys.excepthook:
Traceback (most recent call last):
  File "/usr/lib/python3/dist-packages/apport_python_hook.py", line 228, in partial_apport_excepthook
    return apport_excepthook(binary, exc_type, exc_obj, exc_tb)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3/dist-packages/apport_python_hook.py", line 114, in apport_excepthook
    report["ExecutableTimestamp"] = str(int(os.stat(binary).st_mtime))
                                            ^^^^^^^^^^^^^^^
FileNotFoundError: [Errno 2] No such file or directory: '/opt/nucleus-platform/CRM/-m'

Original exception was:
Traceback (most recent call last):
  File "<frozen runpy>", line 198, in _run_module_as_main
  File "<frozen runpy>", line 88, in _run_code
  File "/usr/lib/python3/dist-packages/uvicorn/__main__.py", line 4, in <module>
    uvicorn.main()
  File "/usr/lib/python3/dist-packages/click/core.py", line 1157, in __call__
    return self.main(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3/dist-packages/click/core.py", line 1078, in main
    rv = self.invoke(ctx)
         ^^^^^^^^^^^^^^^^
  File "/usr/lib/python3/dist-packages/click/core.py", line 1434, in invoke
    return ctx.invoke(self.callback, **ctx.params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3/dist-packages/click/core.py", line 783, in invoke
    return __callback(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3/dist-packages/uvicorn/main.py", line 418, in main
    run(
  File "/usr/lib/python3/dist-packages/uvicorn/main.py", line 587, in run
    server.run()
  File "/usr/lib/python3/dist-packages/uvicorn/server.py", line 62, in run
    return asyncio.run(self.serve(sockets=sockets))
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.12/asyncio/runners.py", line 194, in run
    return runner.run(main)
           ^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.12/asyncio/runners.py", line 118, in run
    return self._loop.run_until_complete(task)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "uvloop/loop.pyx", line 1516, in uvloop.loop.Loop.run_until_complete
  File "/usr/lib/python3/dist-packages/uvicorn/server.py", line 69, in serve
    config.load()
  File "/usr/lib/python3/dist-packages/uvicorn/config.py", line 458, in load
    self.loaded_app = import_from_string(self.app)
                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3/dist-packages/uvicorn/importer.py", line 21, in import_from_string
    module = importlib.import_module(module_str)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.12/importlib/__init__.py", line 90, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1331, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 935, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 995, in exec_module
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "/opt/nucleus-platform/CRM/backend/main.py", line 15, in <module>
    from .routes import (
  File "/opt/nucleus-platform/CRM/backend/routes/__init__.py", line 1, in <module>
    from . import (
  File "/opt/nucleus-platform/CRM/backend/routes/assets.py", line 5, in <module>
    from scripts import sophos_sync, tenable_sync
  File "/opt/nucleus-platform/CRM/scripts/tenable_sync.py", line 3, in <module>
    from backend.services import tenable
  File "/opt/nucleus-platform/CRM/backend/services/tenable.py", line 11, in <module>
    handler = logging.FileHandler(log_path)
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.12/logging/__init__.py", line 1231, in __init__
    StreamHandler.__init__(self, self._open())
                                 ^^^^^^^^^^^^
  File "/usr/lib/python3.12/logging/__init__.py", line 1263, in _open
    return open_func(self.baseFilename, self.mode,
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
PermissionError: [Errno 13] Permission denied: '/opt/nucleus-platform/CRM/logs/integration/tenable.log'

#
admin_arno@bestanden:~$ ls -al /var/log/nucleus
total 1228
drwxr-xr-x  2 admin_arno admin_arno    4096 Jul  4 13:58 .
drwxrwxr-x 12 root       syslog        4096 Jul  4 13:59 ..
-rw-rw-r--  1 admin_arno admin_arno       0 Jul  4 13:58 acme.log
-rw-rw-r--  1 admin_arno admin_arno   58919 Jul  4 13:59 auth.log
-rw-rw-r--  1 admin_arno admin_arno 1175020 Jul  4 12:32 backend.log
-rw-rw-r--  1 admin_arno admin_arno       0 Jul  4 13:58 crm_sync.log
-rw-rw-r--  1 admin_arno admin_arno       0 Jul  4 13:58 dmarc.log
-rw-rw-r--  1 admin_arno admin_arno     261 Jul  4 13:58 sophos.log
-rw-rw-r--  1 admin_arno admin_arno       0 Jul  4 13:58 tenable.log

#
admin_arno@bestanden:~$ cat /etc/systemd/system/nucleus-backend.service
[Unit]
Description=Nucleus Backend Service
After=network.target

[Service]
Type=simple
WorkingDirectory=/opt/nucleus-platform/CRM
ExecStart=/opt/nucleus-platform/CRM/venv/bin/python -m uvicorn --app-dir /opt/nucleus-platform/CRM backend.main:app --host 0.0.0.0 --port 8000
Restart=on-failure
User=admin_arno
ExecStartPre=/bin/mkdir -p /var/log/nucleus
StandardOutput=append:/var/log/nucleus/backend.log
StandardError=append:/var/log/nucleus/backend.log

[Install]
WantedBy=multi-user.target

#
admin_arno@bestanden:~$ cat /etc/systemd/system/nucleus-auth.service
[Unit]
Description=Nucleus Node Auth Service
After=network.target

[Service]
Type=simple
WorkingDirectory=/opt/nucleus-platform/CRM/node_backend
EnvironmentFile=/opt/nucleus-platform/CRM/.env
ExecStart=/usr/bin/node index.js
Restart=on-failure
User=admin_arno
ExecStartPre=/usr/bin/npm install --production --prefix /opt/nucleus-platform/CRM/node_backend
ExecStartPre=/bin/mkdir -p /var/log/nucleus
StandardOutput=append:/var/log/nucleus/auth.log
StandardError=append:/var/log/nucleus/auth.log

[Install]
WantedBy=multi-user.target
