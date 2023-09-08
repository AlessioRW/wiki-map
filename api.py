from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from search import get_connections
app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/search/{start}/{target}/{max_depth}')
def search(start: str, target: str, max_depth: int):
    print('{} --> {} (Max Depth: {})'.format(start, target, str(max_depth)))

    connections = get_connections(start, target, max_depth)
    

    return 200,connections