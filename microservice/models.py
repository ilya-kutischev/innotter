from pydantic import BaseModel, Field


class Statistics(BaseModel):
    id: int
    posts: int = 0
    likes: int = 0
    followers: int = 0
    follow_requests: int = 0

