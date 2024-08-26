from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from src.auth.models import Authenticate

from src.user.models import UserModel

from src.database import DBAdapter

router = APIRouter()


@router.post("/")
def authenticate(request: Authenticate):

    try:
        with DBAdapter().get_session() as session: 
            user_model = session.query(UserModel).filter_by(username=request.username).first()
            
            if not user_model: 
                return JSONResponse(status_code=201, content=False)
            
            if user_model.password != request.password: 
                return JSONResponse(status_code=201, content=False)
            
            return JSONResponse(status_code=200, content=True)
    except Exception as e: 
        raise HTTPException(status_code=500, detail={e}) from e         
 
        
        
        
    
    
