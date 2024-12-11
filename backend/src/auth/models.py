from sqlmodel import SQLModel

class Authenticate(SQLModel): 
    username: str 
    password: str 
    