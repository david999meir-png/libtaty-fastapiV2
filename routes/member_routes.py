from fastapi import APIRouter, HTTPException
from database.members_db import MemberDAL



router = APIRouter()


@router.post("", status_code=201)
def add_member(member):
    pass


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
def update_member(data):
    pass


@router.patch("/{id}/deactivate ")
def deacrive_member(id: int):
    found = MemberDAL.get_member_by_id(id)
    if not found:
        raise HTTPException(status_code=404, detail=f"member id {id} not found.")
    
    return MemberDAL.deactivate_member(id)


@router.patch("/{id}/activate ")
def acrive_member(id: int):
    found = MemberDAL.get_member_by_id(id)
    if not found:
        raise HTTPException(status_code=404, detail=f"member id {id} not found.")
    
    return MemberDAL.activate_member(id)

