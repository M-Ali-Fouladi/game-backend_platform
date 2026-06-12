from pydantic import BaseModel, EmailStr


class PlayerCreate(BaseModel):
    username: str
    email: EmailStr


class PlayerResponse(BaseModel):
    id: int
    username: str
    email: str
    xp: int
    mmr: int

    class Config:
        from_attributes = True


class XPUpdate(BaseModel):
    amount: int


class MMRUpdate(BaseModel):
    amount: int