from __future__ import annotations
from pydantic import BaseModel
from typing import List

from resources.rest_models import Link

class RecipeModel(BaseModel):
    recipe_id: int
    title: str
    author_id: str
    ingredients: str
    steps: str
    images: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "recipe_id": 1,
                    "title": "Chocolate Chip Pancakes",
                    "author_id": "sarah_m",
                    "ingredients": '"flour", "sugar", "eggs", "milk", "chocolate chips"',
                    "steps": '"Mix the ingredients in a bowl.", "Pour the batter into a hot pan.", "Cook until golden brown."',
                    "images": '"pancakes_image.jpg"'
                }
            ]
        }
    }

class RecipeRspModel(RecipeModel):
    links: List[Link] = None
    