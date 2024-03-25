from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field, root_validator


class PaginationDescription(BaseModel):
    class Config:
        allow_population_by_field_name = True

    reuse_previous_request: bool = Field(default=False, alias='reuse-previous-request')
    method: str = ''
    url: str = ''
    modifiers: List[PaginationModifier] = Field(default_factory=list)
    result: str
    has_more: str

    @root_validator
    def validate_fields(cls, values: dict):
        if isinstance(values, PaginationDescription):
            values = values.dict()
        reuse = values.get("reuse-previous-request") or values.get("reuse_previous_request")
        for attr in ['method', 'url']:
            if not reuse and not values[attr]:
                raise ValueError(f"The field '{attr}' is required if 'reuse-previous-request' is False")
        return values


class PaginationModifier(BaseModel):
    op: Optional[str] = 'set'
    param: str
    value: str


PaginationDescription.update_forward_refs()
