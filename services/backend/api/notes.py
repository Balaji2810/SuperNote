from fastapi import APIRouter, status, Request, Query
from pymongo.errors import DuplicateKeyError
from database import Note, SharedNote
from . import schemas
from .schemas import GenericResponse
from auth import auth_required
import json
from fastapi import File, UploadFile
from s3 import S3
from starlette.responses import StreamingResponse
from io import BytesIO

route = APIRouter()


@route.post("/notes")
@auth_required
async def add_note(note:schemas.Note, request: Request, token=None):
    try:
        name = note.name
        note = Note(name=name,owner_id=token)
        await note.create()
        return GenericResponse(data={"id":note.id,"name":note.name})
    except DuplicateKeyError:
        return GenericResponse(status_code=status.HTTP_409_CONFLICT,message="Note name not available!!")


@route.get("/notes")
@auth_required
async def get_note(request: Request, token=None, skip: int = Query(0), limit: int = Query(25)):
    
    notes = await Note.find(Note.owner_id==token).skip(skip).limit(limit).to_list()
    
    return GenericResponse(data=[json.loads(note.model_dump_json()) for note in notes])
    
@route.get("/notes/shared")
@auth_required
async def get_shared_note(request: Request, token=None, skip: int = Query(0), limit: int = Query(25)):
   
    notes = await Note.aggregate([
    {
        "$lookup": {
            "from": SharedNote.get_collection_name(),
            "localField": "_id",
            "foreignField": "note_id",
            "as": "shared_notes"
        }
    },
    {
        "$match": {
            "shared_notes.shared_with": token
        }
    },
    {
        "$project": {
            "id": 1,
            "name": 1
        }
    }
]).to_list()
    
    return GenericResponse(data=[json.loads(json.dumps(note,default=str)) for note in notes])

@route.post("/notes/share")
@auth_required
async def share_note(s_note:schemas.ShareNote, request: Request, token=None):
    
    note = await Note.find(Note.id==s_note.note_id,Note.owner_id==token).first_or_none()
    if not note:
        return GenericResponse(status_code=status.HTTP_403_FORBIDDEN, message="declined")
    note = SharedNote(shared_with=s_note.user_id,owner_id=token,note_id=s_note.note_id)
    await note.create()
    return GenericResponse(data={"id":note.id})
    

@route.post("/notes/{note_id}")
@auth_required
async def push_data(note_id:str,htmldata:schemas.HtmlData, request: Request, token=None):
    note = await Note.find(Note.id==note_id,Note.owner_id==token).first_or_none()
    if not note:
        note = await SharedNote.find(SharedNote.note_id==note_id,SharedNote.owner_id==token).first_or_none()
        if not note:
            return GenericResponse(status_code=status.HTTP_403_FORBIDDEN, message="declined")
    
    if S3.put_data(htmldata.data,note_id):
        return GenericResponse()
    return GenericResponse(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, message="S3 not Reachable")


@route.get("/notes/{note_id}")
@auth_required
async def get_data(note_id:str, request: Request, token=None):
    note = await Note.find(Note.id==note_id,Note.owner_id==token).first_or_none()
    if not note:
        note = await SharedNote.find(SharedNote.note_id==note_id,SharedNote.owner_id==token).first_or_none()
        if not note:
            return GenericResponse(status_code=status.HTTP_403_FORBIDDEN, message="declined")
    data = S3.get_data(note_id)
    if data:
        return GenericResponse(data=data)
    return GenericResponse(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, message="S3 not Reachable")


@route.post("/file/{note_id}")
@auth_required
async def push_file(note_id:str, request: Request, token=None, file_obj: UploadFile = File(...)):
    note = await Note.find(Note.id==note_id,Note.owner_id==token).first_or_none()
    if not note:
        note = await SharedNote.find(SharedNote.note_id==note_id,SharedNote.owner_id==token).first_or_none()
        if not note:
            return GenericResponse(status_code=status.HTTP_403_FORBIDDEN, message="declined")
    
    
    res = S3.upload_file(note_id, file_obj)
    if res:
        return GenericResponse(data=res)
    return GenericResponse(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, message="S3 not Reachable")

@route.get("/file/{key}")
@auth_required
async def get_file(key:str, request: Request, token=None):


    data = S3.download_file(key)
    if data:
        return StreamingResponse(BytesIO(data["file_data"]), media_type="application/octet-stream", 
                                 headers={"Content-Disposition": f"attachment; filename={data['filename']}"})
    return GenericResponse(status_code=status.HTTP_404_NOT_FOUND, message="File not Available")

    