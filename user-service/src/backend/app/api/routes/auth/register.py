from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from backend.app.core.db import get_session
from backend.app.core.logging import get_logger
from backend.app.auth.schema import UserCreateSchema, UserReadSchema
from backend.app.api.services.user_auth import user_auth_service

logger = get_logger()

router = APIRouter(prefix="/auth")


@router.post(
    "/register", response_model=UserReadSchema, status_code=status.HTTP_201_CREATED
)
async def register_user(
    user_data: UserCreateSchema, session: AsyncSession = Depends(get_session)
):
    try:
        # email check
        if await user_auth_service.check_user_email_exists(user_data.email, session):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "status": "error",
                    "message": "Email already exists",
                    "action": "Please use a different email address",
                },
            )

        # id_no check
        if await user_auth_service.check_user_id_no_exists(user_data.id_no, session):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this ID number already exists",
            )

        # create user
        new_user = await user_auth_service.create_user(user_data, session)
        logger.info(
            f"User {new_user.email} registered successfully, Awaiting email verification..."
        )

        return new_user

    except HTTPException as http_exp:
        await session.rollback()
        raise http_exp
    except Exception as err:
        await session.rollback()
        logger.error(f"Error registering user: {str(err)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )
