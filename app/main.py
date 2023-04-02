# from typing import Optional, List
from fastapi import FastAPI  # Body, Response, status, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
# import psycopg
# from psycopg import ClientCursor
# from random import randrange  # just for indexing my_posts elements
# import time
from . import models
from .database import engine  # , get_db
# from .schemas import PostCreate, Post, UserCreate, UserOut
# from sqlalchemy.orm import Session
# from . import utils
from .routers import post, user, auth, vote
from .config import settings

# if we use alembic we don't need this command
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]  # not recommended for security reasons

# middleware is a func that runs before any request
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # what domains should be able to talk to our api
    allow_credentials=True,
    allow_methods=["*"],  # we can allow also only specific http methods
    allow_headers=["*"],
)

# This is a path operation (aka route)
# decorator - function
# async is optional in this case
# the name of the function can be whatever we want but it better be descriptive
# get() is the HTTP method that the user should use
# uvicorn main:app --reload arg lets you udate code without restarting the server to see the updates
# FastAPI works by searching at all the path operations and then execute the first one which matches your request, so order matters!


'''
my_posts = []  # just a variable for debugging until we build a db for storing posts


def find_post(id):  # not efficient, we'll use t until we build a db
    for p in my_posts:
        if p['id'] == id:
            return p


def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i


@app.get('/')
async def root():
    return {'message': 'Hello World'}


@app.get('/posts')
async def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()

    return {'data': posts}

# PostMan is a great tool for testing our api without building a frontend interface
# POST Request: we can send data to the server

# @app.post('/createposts')
# async def create_posts(payLoad: dict = Body(...)):
#     print(payLoad)
#     return {'new_post': f"title: {payLoad['title']}, content: {payLoad['content']}"}


# this is not scalable bc we have to address each field manually and they are not getting validated
# It's better to explicitly define a schema, and there's the Pydantic lib for that
# title str, content str
# each Pydantic model has a dict method that retuns a dict version of the model

@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    
    #post_dict = post.dict()
    #post_dict['id'] = randrange(0, 1000000)
    #my_posts.append(post_dict)
    #return {'data': post_dict}
    
    # cursor.execute(f"") ---> this can lead to SQL injection attacks
    cursor.execute("""INSERT INTO posts(title, content, published) VALUES(%s, %s, %s) RETURNING *""",
                   (post.title, post.content, post.published))
    created_post = cursor.fetchone()
    conn.commit()

    return {'data': created_post}

# CRUD API
# Best practice --> use /posts instead of /post and /users instead of /user
# create must always be a post request
# UPDATE--> we can use either put or patch


# {id} is a path parameter and in FastAPI we can directly pass it to the get_post funct
@app.get('/posts/{id}')
# : int is validation by fastapi, ensures automatic error handling
def get_post(id: int):
    
    #post = find_post(id)
    #if not post:
    #    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                        detail=f"post with id {id} was not found")

    #return {"post_detail": post}

    cursor.execute("""SELECT * FROM posts where id=(%s)""", (str(id),))
    post = cursor.fetchone()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found")
    return {'data': post}

# best practice for 204 is to not send any data back


@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    #index = find_index_post(id)

    #if index == None:
    #    raise HTTPException(status.HTTP_404_NOT_FOUND,
    #                        detail=f"post with id {id} does not exist")

    #my_posts.pop(index)
    
    cursor.execute(
        """DELETE FROM posts WHERE id=(%s) RETURNING *""", (str(id), ))
    deleted_post = cursor.fetchone()

    conn.commit()

    if not deleted_post:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} does not exist")

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put('/posts/{id}')
def update_post(id: int, post: Post):
    #index = find_index_post(id)

    #if index == None:
    #    raise HTTPException(status.HTTP_404_NOT_FOUND,
    #                        detail=f"post with id {id} does not exist")

    #post_dict = post.dict()
    #post_dict['id'] = id            # we have to tell again what the id is
    #my_posts[index] = post_dict

    #return {'data': post_dict}

    cursor.execute("""UPDATE posts SET title=%s,content = %s, published=%s WHERE id=%s RETURNING *""",
                   (post.title, post.content, post.published, str(id),))
    updated_post = cursor.fetchone()
    conn.commit()
    if not updated_post:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} does not exist")

    return {'data': updated_post}

# FastAPI has a built-in support for create documentation. Just go to http://127.0.0.1:8000/docs
# and this can also be used instead of Postman. Also check http://127.0.0.1:8000/redoc

# Section 4 - Databases
# we never talk to the db directly but we access it via a dbms usin SQL statements
# We'll use Postgres: each instance of postgres can be carved into separate databases
#
'''

# Section 5 - ORM
# So far we have seen how to connect to db and make queries but we have to inject SQL statements.
# With ORM we can resort to full Python code

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get('/')
async def root():
    return {'message': 'Hello World'}

'''
@app.get('/posts', response_model=List[Post])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()

    return posts


@app.post('/posts', status_code=status.HTTP_201_CREATED, response_model=Post)
def create_posts(post: PostCreate, db: Session = Depends(get_db)):
    new_post = models.Post(
        **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)  # retrieve and store back in new post

    return new_post


@app.get('/posts/{id}', response_model=Post)
# : int is validation by fastapi, ensures automatic error handling
async def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found")

    return post


@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)

    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found")

    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put('/posts/{id}', response_model=Post)
def update_post(id: int, updated_post: PostCreate, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found")

    post_query.update(updated_post.dict(), synchronize_session=False)

    db.commit()

    return post_query.first()


@app.post('/users', status_code=status.HTTP_201_CREATED, response_model=UserOut)
def create_users(user: UserCreate, db: Session = Depends(get_db)):
    # hash the password - user.password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(
        **user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)  # retrieve and store back in new post

    return new_user


@app.get('/users/{id}', response_model=UserOut)
# : int is validation by fastapi, ensures automatic error handling
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {id} does not exist")

    return user


# This is becoming messy to keep in one file
# Better to separate into two files, one for user and one for posts, but we have to apply routers
'''
