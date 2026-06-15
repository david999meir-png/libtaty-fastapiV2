from fastapi import APIRouter, HTTPException
from mysql.connector import IntegrityError
from database.members_db import MemberDAL
from pydantic import BaseModel, Field


class Member(BaseModel):
    name: str = Field(max_length=50)
    email: str = Field(max_length=255)

class MemberUP(BaseModel):
    name: str | None = Field(max_length=50, default=None)
    email: str |None = Field(max_length=255, default=None)


router = APIRouter()


@router.post("", status_code=201)
def add_member(member: Member):
    try:
        new_id = MemberDAL.create_member(member.model_dump())
        return {"msg": f"added, new id {new_id}"}
    
    except IntegrityError as e:
        if e.errno == 1062:
            raise HTTPException(status_code=409, detail=f"memer alrady exists")
        

@router.get("")
def get_all_members():
    return MemberDAL.get_all_members()


@router.get("/{id}")
def get_member_by_id(id: int):
    found = MemberDAL.get_member_by_id(id)
    if not found:
        raise HTTPException(status_code=404, detail=f"member id {id} not found.")
    return found


@router.patch("/{id}")
def update_member(id: int, data: MemberUP):
    found = MemberDAL.get_member_by_id(id)
    if not found:
        raise HTTPException(status_code=404, detail=f"member id {id} not found.")
    
    updated = MemberDAL.update_member(id, data.model_dump(exclude_none=True))
    if not updated:
        raise HTTPException(status_code=400, detail=f"member id {id} not updated")
    
    return {"msg": f"member id {id} updated."}


@router.patch("/{id}/deactivate")
def deacrive_member(id: int):
    found = MemberDAL.get_member_by_id(id)
    if not found:
        raise HTTPException(status_code=404, detail=f"member id {id} not found.")
    
    changed = MemberDAL.deactivate_member(id)
    if not changed:
        raise HTTPException(status_code=400, detail=f"member is alrady deactive")
    
    return {"msg": f"member id {id} become deactive"} 


@router.patch("/{id}/activate")
def acrive_member(id: int):
    found = MemberDAL.get_member_by_id(id)
    if not found:
        raise HTTPException(status_code=404, detail=f"member id {id} not found.")
    
    changed = MemberDAL.activate_member(id)
    if not changed:
        raise HTTPException(status_code=400, detail=f"member is alrady active")
    
    return {"msg": f"member id {id} become active"} 

