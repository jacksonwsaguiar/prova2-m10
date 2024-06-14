
from fastapi import FastAPI, Request,Response
from pydantic import BaseModel
from logging_config import LoggerSetup
import logging

logger_setup = LoggerSetup()

LOGGER = logging.getLogger(__name__)

app = FastAPI()

blog_posts = []

class BlogPost(BaseModel):
    # def __init__(self, id, title, content):
        id :int
        title: str
        content: str
    # def __str__(self) -> str:
    #     return f'{self.id} - {self.title} - {self.content}'
    
    # def toJson(self):
    #     return Response({'id': self.id, 'title': self.title, 'content': self.content})

@app.post('/blog', status_code=201)
def create_blog_post(post: BlogPost,response: Response):
    LOGGER.info({"message": "Acessando a rota /blog", "method": "POST", "post": post.dict()})
    try:
        # data = request.get_json()
        blog_posts.append(post)
        return {'status':'sucess'}
    except KeyError:
        response.status_code = 400
        return {'error': 'Invalid request'}
    except Exception as e:
        response.status_code = 500
        return {'error': str(e)}


@app.get('/blog',status_code=200)
def get_blog_posts():
    LOGGER.info({"message": "Acessando a rota /blog", "method": "GET"})
    return {"posts":blog_posts }


@app.get('/blog/{id}',status_code=200)
def get_blog_post(id: int,response: Response):
    LOGGER.info({"message": "Acessando a rota /blog/id", "method": "GET","post_id": id})
    for post in blog_posts:
        if post.id == id:
            return {'post': post.__dict__}
    response.status_code = 404
    LOGGER.warning({"message": "rota /blog - post not found", "method": "GET","post_id": id})
    return {'error': 'Post not found'}

@app.delete('/blog/{id}',status_code=200)
def delete_blog_post(id: int,response: Response):
    LOGGER.info({"message": "Acessando a rota /blog/id", "method": "DELETE","post_id": id})
    for post in blog_posts:
        if post.id == id:
            blog_posts.remove(post)
            return {'status':'sucess'}
    response.status_code = 404
    LOGGER.warning({"message": "rota /blog/id - post not found", "method": "DELETE","post_id": id})
    return {'error': 'Post not found'}

@app.put('/blog/{id}', status_code=200)
def update_blog_post(id: int, updatePost: BlogPost,response: Response):
    LOGGER.info({"message": "Acessando a rota /blog/id", "method": "PUT","post_id": id, "post": updatePost.dict()})
    try:
        # data = request.get_json()
        for post in blog_posts:
            if post.id == id:
                post.title = updatePost.title
                post.content = updatePost.content
                return {'status':'sucess'}
        response.status_code = 404
        return {'error': 'Post not found'}
    except KeyError:
        response.status_code = 400
        return {'error': 'Invalid request'}
    except Exception as e:
        response.status_code = 500
        return {'error': str(e)}

# if __name__ == '__main__':
    # app.run(debug=True)
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)