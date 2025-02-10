from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import SessionLocal
from models import Post
from schemas import PostCreate, PostUpdate, PostResponse
from dependencies import get_current_user  # 이 줄을 추가

router = APIRouter(prefix="/api/posts", tags=["Posts"])

# 비동기 DB 세션 의존성 주입
async def get_db():
    async with SessionLocal() as session:
        yield session

# ✅ 게시글 생성 (POST)
@router.post("/", response_model=PostResponse)
async def create_post(
    post: PostCreate,
    current_user: int = Depends(get_current_user),  # 여기서 user_id를 자동으로 가져옴
    db: AsyncSession = Depends(get_db)
):
    new_post = Post(user_id=current_user, title=post.title, content=post.content)
    db.add(new_post)
    await db.commit()
    await db.refresh(new_post)
    return new_post

# ✅ 게시글 목록 조회 (GET)
@router.get("/", response_model=list[PostResponse])
async def get_posts(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Post))
    posts = result.scalars().all()
    return posts

# ✅ 특정 게시글 조회 (GET)
@router.get("/{post_id}", response_model=PostResponse)
async def get_post(post_id: int, db: AsyncSession = Depends(get_db)):
    post = await db.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

# ✅ 게시글 수정 (PUT)
@router.put("/{post_id}", response_model=PostResponse)
async def update_post(post_id: int, post_update: PostUpdate, db: AsyncSession = Depends(get_db)):
    post = await db.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    post.title = post_update.title
    post.content = post_update.content
    await db.commit()
    await db.refresh(post)
    return post

# ✅ 게시글 삭제 (DELETE)
@router.delete("/{post_id}")
async def delete_post(post_id: int, db: AsyncSession = Depends(get_db)):
    post = await db.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    await db.delete(post)
    await db.commit()
    return {"message": "Post deleted successfully"}
