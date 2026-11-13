from datetime import datetime

from pydantic import BaseModel, Field, ValidationError


class Ponto(BaseModel):
    x: int = Field(ge=0, le=10)
    quando: datetime


p = Ponto.model_validate({"x": "7", "quando": "2024-01-15T10:30:00"})
print(p.x, type(p.x), p.quando, type(p.quando))
try:
    Ponto.model_validate({"x": 99, "quando": "ontem"})
except ValidationError as e:
    print(e.error_count())
    for err in e.errors():
        print(err["loc"], err["msg"])