"""Authentication utilities and role based access control."""

import fnmatch
import ipaddress
import secrets
import socket

import pyotp
from fastapi import Depends, Header, HTTPException, Request, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import base64
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Role, User, UserRole, WhitelistedIP

security = HTTPBasic(auto_error=False)


def authenticate(
    request: Request,
    credentials: HTTPBasicCredentials | None = Depends(security),
    x_totp: str | None = Header(default=None),
    db: Session = Depends(get_db),
):
    """Validate user credentials and enforce MFA and IP whitelist."""
    if credentials is None or credentials.username is None:
        cookie = request.cookies.get("auth")
        if cookie:
            try:
                decoded = base64.b64decode(cookie).decode()
                usern, pw = decoded.split(":", 1)
                credentials = HTTPBasicCredentials(username=usern, password=pw)
            except Exception:
                credentials = None
    if credentials is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    user = db.query(User).filter(User.username == credentials.username).first()
    if not user or not secrets.compare_digest(credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )
    if user.mfa_enabled:
        totp = pyotp.TOTP(user.mfa_secret)
        if not x_totp or not totp.verify(x_totp):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="MFA required"
            )
    if db.query(WhitelistedIP).count():
        client_ip = request.headers.get("X-Client-IP", request.client.host)
        client_fqdn = request.headers.get("X-Client-FQDN", "")

        def is_local(addr: str) -> bool:
            try:
                ip_obj = ipaddress.ip_address(addr)
                return ip_obj.is_private or ip_obj.is_loopback
            except ValueError:
                return False

        if not is_local(client_ip):
            entries = [e.pattern for e in db.query(WhitelistedIP).all()]

            def matches(pattern: str) -> bool:
                try:
                    if "/" in pattern:
                        net = ipaddress.ip_network(pattern, strict=False)
                        return ipaddress.ip_address(client_ip) in net
                    ipaddress.ip_address(pattern)
                    return client_ip == pattern
                except ValueError:
                    fqdn = client_fqdn
                    if not fqdn:
                        try:
                            fqdn = socket.gethostbyaddr(client_ip)[0]
                        except (socket.herror, OSError):
                            fqdn = ""
                    return fnmatch.fnmatch(fqdn, pattern)

            if not any(matches(p) for p in entries):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="IP/FQDN not allowed",
                )
    return user


def require_role(role: str):
    """Ensure the authenticated user has the specified role."""

    def checker(
        current_user: User = Depends(authenticate),
        db: Session = Depends(get_db),
    ):
        roles = (
            db.query(Role)
            .join(UserRole, Role.id == UserRole.role_id)
            .filter(UserRole.user_id == current_user.id)
            .all()
        )
        if not any(r.name == role for r in roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden"
            )
        return current_user

    return checker


def require_roles(roles: list[str]):
    """Check that the user has at least one role from the provided list."""

    def checker(
        current_user: User = Depends(authenticate),
        db: Session = Depends(get_db),
    ):
        assigned = (
            db.query(Role)
            .join(UserRole, Role.id == UserRole.role_id)
            .filter(UserRole.user_id == current_user.id)
            .all()
        )
        if not any(r.name in roles for r in assigned):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden"
            )
        return current_user

    return checker
