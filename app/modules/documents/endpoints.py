from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from app.db.debs import get_db
from app.core.permission_dependancy import require_permission
from app.modules.users.model import User
from .usecases import create_document_usecase, get_document_usecase, delete_document_usecase, update_document_usecase
from .schemas import CreateDocumentRequest, DocumentDepthLevel, UpdateDocumentRequest

# Router initialization
router = APIRouter(
    prefix="/departments/{department_id}/documents",
    tags=["Documents"]
)

# Dependencies
db = Annotated[AsyncSession, Depends(get_db)]

# Endpoint to create a new document
@router.post("")
async def create_document_endpoint(db: db, department_id: str, request: CreateDocumentRequest, current_user: User = Depends(require_permission("documents.create"))):
    resp = await create_document_usecase(db, department_id, request)
    return resp

# Endpoint to get a document
@router.get("/{node_id}")
async def get_document_endpoint(department_id: str, node_id: str, depth: DocumentDepthLevel = Query(DocumentDepthLevel.ZERO), db: AsyncSession = Depends(get_db), current_user=Depends(require_permission("document.read"))):
    return await get_document_usecase(db, department_id, node_id, depth.value)

# Endpoint to update a document
@router.put("/{node_id}")
async def update_document_endpoint(department_id: str, node_id: str, request: UpdateDocumentRequest, db: AsyncSession = Depends(get_db), current_user=Depends(require_permission("document.update"))):
    return await update_document_usecase(db, department_id, node_id, request)

# Endpoint to delete a document
@router.delete("/{node_id}")
async def delete_document_endpoint(department_id: str, node_id: str, db: AsyncSession = Depends(get_db), current_user=Depends(require_permission("document.delete"))):
    return await delete_document_usecase(db, department_id, node_id)