# from typing import Optional
#
# from fastapi import Form
#
# class OAuth2PasswordRequestFormWithClient:
#     def __init__(
#         self,
#         username: str = Form(...),
#         password: str = Form(...),
#         client_id: Optional[str] = Form(None),
#         client_secret: Optional[str] = Form(None),
#         # client_id: str = Form(...),
#         # client_secret: str = Form(...),
#     ):
#         self.username = username
#         self.password = password
#         self.client_id = client_id
#         self.client_secret = client_secret

from fastapi import Form
from fastapi.security import OAuth2PasswordRequestForm
from typing import Optional, List

class OAuth2PasswordRequestFormWithClient(OAuth2PasswordRequestForm):
    def __init__(
        self,
        grant_type: str = Form(None),
        username: str = Form(...),
        password: str = Form(...),
        scope: str = Form(""),
        client_id: Optional[str] = Form(None),
        client_secret: Optional[str] = Form(None),
    ):
        # Store values like original parent class
        self.grant_type = grant_type
        self.username = username
        self.password = password
        self.scopes = scope.split() if scope else []
        self.client_id = client_id
        self.client_secret = client_secret
