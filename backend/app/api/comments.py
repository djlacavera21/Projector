from fastapi import APIRouter, HTTPException, status

from app.models.comment import Comment, CommentCreate, new_comment_id
from app.services.comments import create_comment, list_comments
from app.services.videos import get_video

router = APIRouter(prefix="/videos/{video_id}/comments", tags=["comments"])


@router.get("", response_model=list[Comment])
async def get_comments(video_id: str) -> list[Comment]:
    if get_video(video_id) is None:
        raise HTTPException(status_code=404, detail="Video not found")
    return list_comments(video_id)


@router.post("", response_model=Comment, status_code=status.HTTP_201_CREATED)
async def post_comment(video_id: str, payload: CommentCreate) -> Comment:
    try:
        return create_comment(
            Comment(
                id=new_comment_id(),
                video_id=video_id,
                author=payload.author,
                body=payload.body,
                parent_id=payload.parent_id,
            )
        )
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
