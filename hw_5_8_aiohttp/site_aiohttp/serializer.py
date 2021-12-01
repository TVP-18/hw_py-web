import pydantic


class AdSerializer(pydantic.BaseModel):
    title: str
    text: str
    id_owner: int
