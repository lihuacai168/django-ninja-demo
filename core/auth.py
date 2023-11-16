# !/usr/bin/python3
# -*- coding: utf-8 -*-
from typing import Dict, Optional, Type, Union

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from ninja import Schema
from ninja_jwt.schema import (
    TokenObtainInputSchemaBase,
    TokenRefreshInputSchema,
    TokenRefreshOutputSchema,
)
from ninja_jwt.tokens import RefreshToken

from core.schemas import StandResponse


class UserSchema(Schema):
    first_name: str
    email: str


class MyTokenObtainPairOutSchema(Schema):
    refresh: str
    access: str
    user: UserSchema


class MyRefreshTokenOutSchema(TokenRefreshOutputSchema):
    def dict(
        self,
        *,
        include: Optional[Union["AbstractSetIntStr", "MappingIntStrAny"]] = None,
        exclude: Optional[Union["AbstractSetIntStr", "MappingIntStrAny"]] = None,
        by_alias: bool = False,
        skip_defaults: Optional[bool] = None,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
    ) -> "DictStrAny":
        return {
            "data": {"access": self.access, "refresh": self.refresh},
            "message": None,
            "success": True,
        }


class MyTokenObtainPairInputSchema(TokenObtainInputSchemaBase):
    @classmethod
    def get_response_schema(cls) -> Type[Schema]:
        # TODO now only work get pair token success
        #  not work at get token fail and refresh
        return StandResponse[MyTokenObtainPairOutSchema]

    @classmethod
    def get_token(cls, user) -> Dict:
        values = {}
        refresh = RefreshToken.for_user(user)
        values["refresh"] = str(refresh)
        values["access"] = str(refresh.access_token)
        values.update(user=UserSchema.from_orm(user))
        return {"data": values}


class MyTokenRefreshInputSchema(TokenRefreshInputSchema):
    @classmethod
    def get_response_schema(cls) -> Type[Schema]:
        return MyRefreshTokenOutSchema


class CustomAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        User = get_user_model()

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None

        if user.check_password(password):
            return user
        else:
            return None
