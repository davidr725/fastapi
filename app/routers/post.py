from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
import models
import schemas
from database import get_db
from typing import List
import oauth2
from typing import Optional


router = APIRouter(prefix="/posts", tags=['Posts'])


@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db),
              limit: int = 10,
              skip: int = 0,
              search: Optional[str] = ""):
    posts = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.User, models.Post.owner_id == models.User.id)
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .group_by(models.Post.id, models.User.id)
        .filter(models.Post.title.contains(search))
        .limit(limit)
        .offset(skip)
        .all()
    )
    return [
        schemas.PostOut(
            id=post.id,
            title=post.title,
            content=post.content,
            published=post.published,
            created_at=post.created_at,
            owner_id=post.owner_id,
            owner=schemas.UserOut(
                id=post.owner.id,
                email=post.owner.email,
                created_at=post.owner.created_at,
            ),
            votes=votes
        )
        for post, votes in posts
    ]


@router.get('/{id}', response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db),
             current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id)))
    # post = cursor.fetchone()
    # posts = db.query(models.Post).filter(models.Post.id == id).first()
    posts = (db.query(models.Post, func.count(models.Vote.post_id)
                      .label("votes"))
             .join(models.User, models.Post.owner_id == models.User.id)
             .join(models.Vote, models.Vote.post_id == models.Post.id,
                   isouter=True)
             .group_by(models.Post.id, models.User.id)
             .first())
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")

    return schemas.PostOut(
        id=posts.Post.id,
        title=posts.Post.title,
        content=posts.Post.content,
        published=posts.Post.published,
        created_at=posts.Post.created_at,
        owner_id=posts.Post.owner_id,
        owner=schemas.UserOut(
            id=posts.Post.owner.id,
            email=posts.Post.owner.email,
            created_at=posts.Post.owner.created_at,
        ),
        votes=posts.votes or 0
    )


@router.post("/", status_code=status.HTTP_201_CREATED,
             response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db),
                 current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts (title, content, published)
    #                VALUES (%s, %s, %s) RETURNING * """,
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post = models.Post(owner_id=current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):

    # cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING *""",
    #                (str(id)))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform request action")

    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate,
                db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):

    # cursor.execute(""" UPDATE posts SET title = %s, content = %s,
    #                published = %s WHERE id = %s RETURNING *;""",
    #                (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform request action")

    post_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()
    return post_query.first()