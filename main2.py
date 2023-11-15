from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse

from fastapi.staticfiles import StaticFiles
from typing import List, Union

import uvicorn

from resources.recipes.recipes_resource import RecipeResource
from resources.recipes.recipes_data_service import RecipeDataService
from resources.recipes.recipe_models import RecipeModel, RecipeRspModel

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
# supposedly, this will help serve static files
# if we want to serve HTML files we can do so from here?

def get_data_service():

    config = {
        "data_directory": "data",
        "data_file": "recipes.json"
    }

    ds = RecipeDataService(config)
    return ds

def get_recipe_resource():
    ds = get_data_service()
    config = {
        "data_service": ds
    }
    res = RecipeResource(config)
    return res

recipes_resource = get_recipe_resource()

@app.get("/")
async def root():
    # redirecting to a default page
    return RedirectResponse("/static/index.html")
    #return RedirectResponse("/static/testing.html")

# Retrieve a list of recipes matching the query string 
@app.get("/recipes", response_model=List[RecipeRspModel])
def get_recipes(recipe_id: str = None, title: str = None, author_id: str = None) -> List[RecipeRspModel]:
    result = recipes_resource.get_recipes(recipe_id, title, author_id)
    print(result)
    return result

# Retrieve a specific recipe by ID
@app.get("/recipes/{recipe_id}", response_model=Union[RecipeRspModel, None])
async def get_recipe(recipe_id: str):
    for recipe in recipes_resource.get_recipes():
        if recipe.recipe_id == recipe_id:
            return recipe
    raise HTTPException(status_code=404, detail="Not found")
        
    # result = None
    # result = 
    # if len(result) == 1:
    #     result = result[0]
    # else:
    #     raise HTTPException(status_code=404, detail="Not found")
    
    # return result

# Add a new recipe
@app.post("/recipes", response_model=Union[RecipeRspModel, None])
async def add_recipe(new_recipe: dict):
    print("HERE")
    result = recipes_resource.add_recipe(new_recipe)
    print("HERE2")
    return result

# Update an existing recipe

# # Add a new recipe
# @app.post("/recipes", response_model=dict)
# async def add_recipe(new_recipe: dict):
#     recipes.append(new_recipe)
#     return new_recipe

# # Update an existing recipe
# @app.put("/recipes/{recipe_id}", response_model=dict)
# async def update_recipe(recipe_id: str, updated_recipe: dict):
#     for i, recipe in enumerate(recipes):
#         if recipe["recipe_id"] == recipe_id:
#             recipes[i] = updated_recipe
#             return updated_recipe
#     raise HTTPException(status_code=404, detail="Recipe not found")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8011)