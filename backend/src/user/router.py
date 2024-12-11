from fastapi import APIRouter, HTTPException

from src.user.models import UserCreate, UserModel, UserGet
from src.database import DBAdapter

router = APIRouter()


@router.post("/")
def create_user(request: UserCreate) -> UserGet:
    user_model = UserModel(name=request.name, username=request.username, password=request.password)
    
    try:
        with DBAdapter().get_session() as session: 
            session.add(user_model)
            
            session.commit() 
            
            user_get = UserGet(id=user_model.id, name=user_model.name, username=user_model.username)
            
            return user_get
    except Exception as e: 
        raise HTTPException(status_code=400, detail="Create user failed") from e
    

@router.get("/{id}")
def get_user(id: str) -> UserGet: 
    
    try: 
        with DBAdapter().get_session() as session: 
            user_model = session.query(UserModel).filter_by(id=id).first()
    
            if not user_model: 
                return None 
            
            user_get = UserGet(
                id=user_model.id, 
                name=user_model.name, 
                username=user_model.username,
            )
            
            return user_get 
    except Exception as e: 
        raise HTTPException(status_code=400, detail=e) from e 
    