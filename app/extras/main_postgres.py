""" This is the main file of the application. It contains all the routes and the database connection.
    This is a proxy to app/main.py where it uses psycopg2, a PostgresSQL driver, to connect to the database and perform CRUD operations.
"""


from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
import psycopg2
import time
from typing import Optional
from psycopg2.extras import RealDictCursor


while True:
    try:
        connection = psycopg2.connect(
            host="localhost",
            database="fastapi",
            user="postgres",
            password="root",
            cursor_factory=RealDictCursor,
        )
        cursor = connection.cursor()
        print("Connected to database")
        break
    except Exception as e:
        print("Error: ", e)
        time.sleep(2)

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: Optional[bool] = False


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/posts", status_code=status.HTTP_200_OK)
async def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    print(posts)
    return {"posts": posts}


@app.get("/posts/{id}", status_code=status.HTTP_200_OK)
def get_post(id: int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    post = cursor.fetchone()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found"
        )

    return {"post": post}


@app.post("/createpost", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    cursor.execute(
        """INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
        (post.title, post.content, post.published),
    )
    new_post = cursor.fetchone()
    connection.commit()
    return {"post": new_post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    delete_post = cursor.fetchone()
    connection.commit()

    if not delete_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found"
        )

    return None


@app.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_post(id: int, post: Post):
    cursor.execute(
        """UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
        (post.title, post.content, post.published, str(id)),
    )
    update_post = cursor.fetchone()
    connection.commit()

    if not update_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found"
        )

    return {"post": update_post}
