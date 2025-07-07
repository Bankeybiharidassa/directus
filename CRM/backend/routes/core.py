import socket

import httpx
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from scripts import security_scan

from ..database import SessionLocal
from ..security.auth import require_role

router = APIRouter(prefix="/core", tags=["core"])


def get_local_ip() -> str:
    """Return primary local IP address for the server."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    except OSError:
        return "127.0.0.1"
    finally:
        s.close()


@router.get("/log/export", summary="Export logs")
def log_export(_user=Depends(require_role("admin"))):
    return {"status": "exported"}


@router.post("/config/reload", summary="Reload configuration")
def config_reload(_user=Depends(require_role("admin"))):
    return {"status": "reloaded"}


@router.get("/check/bs", summary="Run BS check")
def bs_check():
    return {"bs": "0%"}


@router.get("/status", summary="Service status")
def service_status():
    db = SessionLocal()
    try:
        db.execute(text("SELECT 1"))
        db_status = "ok"
    except SQLAlchemyError:
        db_status = "error"
    finally:
        db.close()

    try:
        resp = httpx.get("http://localhost:3001/status", timeout=1)
        node_status = "ok" if resp.status_code == 200 else "error"
    except httpx.HTTPError:
        node_status = "down"

    return {"database": db_status, "node_auth": node_status}


@router.get("/security/scan", summary="Run security scan")
def run_security_scan(_user=Depends(require_role("admin"))):
    """Expose security scan results for admin UI."""
    return security_scan.scan_system()


@router.get("/login", response_class=HTMLResponse, include_in_schema=False)
def admin_login_page(request: Request, role: str | None = None):
    """Serve a minimal HTML login form posting to the Node auth service."""
    host_header = request.headers.get("host", "")
    server_host = host_header.split(":")[0]
    if server_host in ("localhost", "0.0.0.0", ""):
        server_host = get_local_ip()
    node_url = f"http://{server_host}:3001/login"
    heading = f"{role.title()} Login" if role else "Login"
    role_input = f"<input type='hidden' name='role' value='{role}'/>" if role else ""
    return f"""
    <html>
      <body>
        <h2>{heading}</h2>
        <form method='post' action='{node_url}'>
          {role_input}
          <input type='text' name='username' placeholder='Username'/><br/>
          <input type='password' name='password' placeholder='Password'/><br/>
          <input type='text' name='otp' placeholder='OTP (optional)'/><br/>
          <button type='submit'>Login</button>
        </form>
      </body>
    </html>
    """


@router.get("/frontpage", response_class=HTMLResponse, include_in_schema=False)
def public_frontpage():
    """Serve a simple public landing page."""
    return """
    <html>
      <body>
        <h2>Welcome to Nucleus CRM</h2>
        <p>Please <a href='/core/login'>log in</a> to continue.</p>
      </body>
    </html>
    """


@router.get("/admin", response_class=HTMLResponse, include_in_schema=False)
def admin_page(_user=Depends(require_role("admin"))):
    """Serve a basic admin dashboard placeholder."""
    return """
    <html>
      <body>
        <div style='position:absolute;top:10px;right:10px'>
          <a href='#profile'>Profile</a> |
          <a href='#security'>Security</a>
        </div>
        <h2>Admin Dashboard</h2>
        <p>You are logged in as an administrator.</p>
        <section id='profile'>
          <h3>Profile</h3>
          <p>Update administrator details here.</p>
        </section>
        <section id='security'>
          <h3>Security</h3>
          <p>Manage passwords and MFA settings.</p>
        </section>
      </body>
    </html>
    """


@router.get("/support", response_class=HTMLResponse, include_in_schema=False)
def support_page(_user=Depends(require_role("support"))):
    """Serve a basic support dashboard placeholder."""
    return """
    <html>
      <body>
        <div style='position:absolute;top:10px;right:10px'>
          <a href='#profile'>Profile</a> |
          <a href='#security'>Security</a>
        </div>
        <h2>Support Dashboard</h2>
        <p>You are logged in as a supporter.</p>
        <section id='profile'>
          <h3>Profile</h3>
          <p>Edit your support account settings.</p>
        </section>
        <section id='security'>
          <h3>Security</h3>
          <p>Update password or enable MFA.</p>
        </section>
      </body>
    </html>
    """


@router.get("/distributor", response_class=HTMLResponse, include_in_schema=False)
def distributor_page(_user=Depends(require_role("distributor"))):
    """Serve a basic distributor dashboard placeholder."""
    return """
    <html>
      <body>
        <div style='position:absolute;top:10px;right:10px'>
          <a href='#profile'>Profile</a> |
          <a href='#security'>Security</a>
        </div>
        <h2>Distributor Dashboard</h2>
        <p>You are logged in as a distributor.</p>
        <section id='profile'>
          <h3>Profile</h3>
          <p>View distributor organization info.</p>
        </section>
        <section id='security'>
          <h3>Security</h3>
          <p>Configure login policies.</p>
        </section>
      </body>
    </html>
    """


@router.get("/partner", response_class=HTMLResponse, include_in_schema=False)
def partner_page(_user=Depends(require_role("partner"))):
    """Serve a basic partner dashboard placeholder."""
    return """
    <html>
      <body>
        <div style='position:absolute;top:10px;right:10px'>
          <a href='#profile'>Profile</a> |
          <a href='#security'>Security</a>
        </div>
        <h2>Partner Dashboard</h2>
        <p>You are logged in as a partner.</p>
        <section id='profile'>
          <h3>Profile</h3>
          <p>Partner account settings.</p>
        </section>
        <section id='security'>
          <h3>Security</h3>
          <p>MFA and key management.</p>
        </section>
      </body>
    </html>
    """

@router.get("/company", response_class=HTMLResponse, include_in_schema=False)
def company_page(_user=Depends(require_role("company"))):
    """Serve a basic company dashboard placeholder."""
    return """
    <html>
      <body>
        <div style='position:absolute;top:10px;right:10px'>
          <a href='#profile'>Profile</a> |
          <a href='#security'>Security</a>
        </div>
        <h2>Company Dashboard</h2>
        <p>You are logged in as an employee.</p>
        <section id='profile'>
          <h3>Profile</h3>
          <p>Update employee details here.</p>
        </section>
        <section id='security'>
          <h3>Security</h3>
          <p>Manage passwords and MFA settings.</p>
        </section>
      </body>
    </html>
    """


@router.get("/enduser", response_class=HTMLResponse, include_in_schema=False)
def enduser_page(_user=Depends(require_role("enduser"))):
    """Serve a basic end user dashboard placeholder."""
    return """
    <html>
      <body>
        <div style='position:absolute;top:10px;right:10px'>
          <a href='#profile'>Profile</a> |
          <a href='#security'>Security</a>
        </div>
        <h2>End User Dashboard</h2>
        <p>You are logged in as an end user.</p>
        <section id='profile'>
          <h3>Profile</h3>
          <p>Personal account info.</p>
        </section>
        <section id='security'>
          <h3>Security</h3>
          <p>Change password or enable MFA.</p>
        </section>
      </body>
    </html>
    """
