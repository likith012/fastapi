from pydantic import BaseModel, EmailStr, conint
from datetime import datetime

# Users
class UserBase(BaseModel):
    username: str
    email: EmailStr
    
class UserCreateIn(UserBase):
    password: str

class UserCreateOut(UserBase):
    user_id: int
    created_at: datetime
    
    class Config():
        orm_mode = True
        
class UserGetOut(UserCreateOut):
    pass


# Posts Request
class RequestBase(BaseModel):
    title: str
    content: str
    published: bool = False
    
class RequestCreate(RequestBase):
    pass

class RequestUpdate(RequestBase):
    published: bool # Required field rather than optional

# Posts Response
class ResponseBase(BaseModel):
    post_id: int
    title: str
    content: str
    published: bool
    created_at: datetime
    owner_id: int
    owner: UserCreateOut
    
    class Config():
        orm_mode = True

        
class ResponseOut(BaseModel):
    Post: ResponseBase
    Likes: int
    
    class Config():
        orm_mode = True
        

# Votes
class VoteBase(BaseModel):
    post_id: int
    like: conint(ge=0, le=1)
        
class VoteCreate(VoteBase):
    pass
        
# OAuth2
class AccessToken(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    user_id: str