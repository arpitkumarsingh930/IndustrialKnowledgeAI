from pydantic import BaseModel

class ProcessRequest(BaseModel):
    documentId: int
    chunks: list[str]


class Question(BaseModel):
    question: str