"""
Security module for authentication.
Handles password hashing and JWT token operations.
"""

import secrets
from datetime import datetime, timedelta, timezone
from typing import Any, Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings

# Password hashing context using bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# =====================
# Password Utilities
# =====================

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Generate a bcrypt hash of a password."""
    return pwd_context.hash(password)


# =====================
# JWT Token Utilities
# =====================

def create_access_token(
    subject: int,
    email: str,
    role: str,
    commune_id: Optional[int] = None,
    expires_delta: Optional[timedelta] = None,
) -> str:
    """
    Create a JWT access token.

    Args:
        subject: User ID
        email: User email
        role: User role
        commune_id: Optional commune ID for commune users
        expires_delta: Optional custom expiration time

    Returns:
        Encoded JWT token string
    """
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode = {
        "sub": str(subject),
        "email": email,
        "role": role,
        "commune_id": commune_id,
        "exp": expire,
        "iat": datetime.now(timezone.utc),
        "type": "access",
    }

    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def create_refresh_token(
    subject: int,
    expires_delta: Optional[timedelta] = None,
) -> str:
    """
    Create a JWT refresh token.

    Args:
        subject: User ID
        expires_delta: Optional custom expiration time

    Returns:
        Encoded JWT refresh token string
    """
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES
        )

    to_encode = {
        "sub": str(subject),
        "exp": expire,
        "iat": datetime.now(timezone.utc),
        "type": "refresh",
        "jti": secrets.token_urlsafe(32),  # Unique token ID
    }

    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def decode_token(token: str) -> Optional[dict[str, Any]]:
    """
    Decode and validate a JWT token.

    Args:
        token: JWT token string

    Returns:
        Token payload dict or None if invalid
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        return payload
    except JWTError:
        return None


def verify_access_token(token: str) -> Optional[dict[str, Any]]:
    """
    Verify an access token and return payload.

    Args:
        token: JWT access token string

    Returns:
        Token payload dict or None if invalid
    """
    payload = decode_token(token)
    if payload and payload.get("type") == "access":
        return payload
    return None


def verify_refresh_token(token: str) -> Optional[dict[str, Any]]:
    """
    Verify a refresh token and return payload.

    Args:
        token: JWT refresh token string

    Returns:
        Token payload dict or None if invalid
    """
    payload = decode_token(token)
    if payload and payload.get("type") == "refresh":
        return payload
    return None


def get_token_expiry(token: str) -> Optional[datetime]:
    """
    Get the expiration datetime of a token.

    Args:
        token: JWT token string

    Returns:
        Expiration datetime or None if invalid
    """
    payload = decode_token(token)
    if payload and "exp" in payload:
        return datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
    return None


# =====================
# Utility Functions
# =====================

def generate_password_reset_token(email: str) -> str:
    """
    Generate a password reset token.

    Args:
        email: User email

    Returns:
        Password reset token string
    """
    delta = timedelta(hours=1)  # 1 hour validity
    now = datetime.now(timezone.utc)
    expires = now + delta

    to_encode = {
        "sub": email,
        "exp": expires,
        "iat": now,
        "type": "password_reset",
    }

    return jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )


def verify_password_reset_token(token: str) -> Optional[str]:
    """
    Verify a password reset token and return email.

    Args:
        token: Password reset token string

    Returns:
        Email string or None if invalid
    """
    payload = decode_token(token)
    if payload and payload.get("type") == "password_reset":
        return payload.get("sub")
    return None


def generate_email_verification_token(email: str) -> str:
    """
    Generate an email verification token.

    Args:
        email: User email

    Returns:
        Email verification token string
    """
    delta = timedelta(days=7)  # 7 days validity
    now = datetime.now(timezone.utc)
    expires = now + delta

    to_encode = {
        "sub": email,
        "exp": expires,
        "iat": now,
        "type": "email_verification",
    }

    return jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )


def verify_email_verification_token(token: str) -> Optional[str]:
    """
    Verify an email verification token and return email.

    Args:
        token: Email verification token string

    Returns:
        Email string or None if invalid
    """
    payload = decode_token(token)
    if payload and payload.get("type") == "email_verification":
        return payload.get("sub")
    return None
