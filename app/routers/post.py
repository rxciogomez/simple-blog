from typing import List
from fastapi import FastAPI, Body, HTTPException, status, Response, Depends, APIRouter
from fastapi.encoders import jsonable_encoder
from .. import models, schemas, oauth2
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func, join
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@router.get('/mine', response_model=list[schemas.PostOut])
def get_my_posts(db:Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user),
                limit: int = 10, skip: int = 0, search: str = None):
    
    query = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Post.id == models.Vote.post_id).group_by(models.Post.id).filter(models.Post.owner_id == current_user.id)
    
    if search:
        query = query.filter(or_(
                                models.Post.title.contains(search),
                                models.Post.content.contains(search))
                            )
    
    posts = query.limit(limit).offset(skip).all()
    
    return posts

@router.get('/', response_model=list[schemas.PostOut])
def get_all_posts(db:Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user),
                limit: int = 10, skip: int = 0, search: str = None):
    query = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id)

    if search:
        query = query.filter(or_(
                                models.Post.title.contains(search),
                                models.Post.content.contains(search))
                            )
    
    posts = query.limit(limit).offset(skip).all()
    

    return posts


@router.post('/', status_code= status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db:Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    
    new_post = models.Post(owner_id = current_user.id,**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return new_post

@router.get('/{id}', response_model=schemas.PostOut)
def get_post_by_id(id: int, db:Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    
    result = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()    
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Item of id {id} not found")

    return result

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db:Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    #cursor.execute("""DELETE FROM posts where id = %s RETURNING *""", (id,))
    #Get post
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    
    #If there is no post with the required id
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id}  does not exist")
    
    #If current user is not the owner of the post
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="Current user does not have the permits needed to execute this action.")
    
    #Everything all right? Delete post 
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put('/{id}',response_model=schemas.Post)
def edit_post(id: int, post: schemas.PostBase, db:Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    #Get post
    post_query = db.query(models.Post).filter(models.Post.id == id)
    current_post = post_query.first()
    
    #If there is no post
    if current_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id}  does not exist")
    
    #If current user is not og poster
    if current_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Current user does not have the permits needed to execute this action.")
    
    #Update post on the data base
    post_query.update(post.model_dump(), synchronize_session=False)
    #Save changes 
    db.commit()
    
    return post_query.first() 