"""Authentication routes."""

from fastapi import APIRouter, HTTPException, status, Request
from slowapi import Limiter
from slowapi.util import get_remote_address
import httpx
import os
import sys

sys.path.append('/app')
from common.models import UserLoginRequest, UserRegisterRequest, TokenResponse
from common.auth import create_access_token
from loguru import logger

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)

CMS_MOCK_URL = os.getenv("CMS_API_URL", "http://cms-mock:3001")

@router.post("/login", response_model=TokenResponse)
@limiter.limit("5/minute")
async def login(request: Request, login_request: UserLoginRequest):
    """
    User login endpoint.
    
    Rate limit: 5 requests per minute per IP
    """
    try:
        # Forward to CMS mock for authentication
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{CMS_MOCK_URL}/api/auth/login",
                data={
                    "username": login_request.email,
                    "password": login_request.password
                },
                timeout=10.0
            )
            
            if response.status_code == 200:
                user_data = response.json()
                
                # Generate JWT token
                token = create_access_token(
                    data={
                        "userId": user_data["id"],
                        "email": user_data["email"],
                        "role": user_data.get("role", "client")
                    }
                )
                
                logger.info(f"User logged in: {user_data['email']}")
                
                return TokenResponse(
                    token=token,
                    user=user_data
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid credentials"
                )
    
    except httpx.TimeoutException:
        logger.error("CMS service timeout")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Authentication service unavailable"
        )
    except Exception as e:
        logger.error(f"Login error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed"
        )

@router.post("/register", response_model=TokenResponse)
@limiter.limit("3/hour")
async def register(request: Request, register_request: UserRegisterRequest):
    """
    User registration endpoint.
    
    Rate limit: 3 requests per hour per IP
    """
    try:
        # Forward to CMS mock for registration
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{CMS_MOCK_URL}/api/customers",
                json={
                    "name": register_request.name,
                    "email": register_request.email,
                    "password": register_request.password,
                    "phone": register_request.phone or "",
                    "company": register_request.company or "",
                    "status": "active",
                    "role": "client"
                },
                timeout=10.0
            )
            
            if response.status_code == 200:
                user_data = response.json()
                
                # Generate JWT token
                token = create_access_token(
                    data={
                        "userId": user_data["id"],
                        "email": user_data["email"],
                        "role": user_data.get("role", "client")
                    }
                )
                
                logger.info(f"New user registered: {user_data['email']}")
                
                return TokenResponse(
                    token=token,
                    user=user_data
                )
            else:
                error_detail = response.json().get("detail", "Registration failed")
                raise HTTPException(
                    status_code=response.status_code,
                    detail=error_detail
                )
    
    except httpx.TimeoutException:
        logger.error("CMS service timeout")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Registration service unavailable"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Registration error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed"
        )
