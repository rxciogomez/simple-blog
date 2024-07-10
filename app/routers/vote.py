from fastapi import FastAPI, Body, HTTPException, status, Response, Depends, APIRouter
from sqlalchemy import and_
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix='/vote',
    tags=['Vote']
)

@router.post('/', status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(get_db),current_user: models.User = Depends(oauth2.get_current_user)):
    
    #Logic to check wether or not a post exists
    post = db.query(models.Post).filter(models.Post.id == vote.post_id ).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id of {vote.post_id} does not exist")
    
    #If post exists we search through the vote table to check if the user has already interacted with the post 
    #trough the voting system
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id )
    existing_vote = vote_query.first()
    
    #If user has already tried to like the existing 
    if (vote.dir == 1):
        if existing_vote :
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f'User {current_user.id} has already voted on post {vote.post_id}')
        
        new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        
        return {'message': 'long live democracy'}
    else:
        if not existing_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User {current_user.id} has never voted on post {vote.post_id}')
        
        vote_query.delete(synchronize_session=False)
        db.commit()
        
        return {'message': 'to regret is to learn'}
