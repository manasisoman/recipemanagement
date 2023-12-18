from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import RedirectResponse

from fastapi.staticfiles import StaticFiles
from typing import List, Union

import uvicorn

from resources.recipes.recipes_resource import RecipeResource
from resources.recipes.recipes_data_service import RecipeDataService
from resources.recipes.recipe_models import RecipeModel, RecipeRspModel

#added by manasi
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

#added by manasi
origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

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

# Retrieve a list of recipes matching the query string OR given parameters
@app.get("/recipes", response_model=List[RecipeRspModel])
def get_recipes(recipe_id: str = None, 
                title: str = None, 
                author_id: str = None, 
                objects_filter: str = Query(default='')) -> List[RecipeRspModel]:
    if objects_filter:
        filtered_recipes = recipes_resource.filter_recipes(objects_filter)
        return filtered_recipes
    
    result = recipes_resource.get_recipes(recipe_id, title, author_id)
    return result

# Retrieve a specific recipe by ID
@app.get("/recipes/{recipe_id}", response_model=Union[RecipeRspModel, None])
async def get_recipe(recipe_id: str):
    recipe = recipes_resource.get_recipe_by_id(recipe_id)
    print('recipe returned:', recipe)
    return recipe
        
# Add a new recipe
@app.post("/recipes", response_model=Union[RecipeRspModel, None])
async def add_recipe(new_recipe: dict):
    print("HERE")
    result = recipes_resource.add_recipe(new_recipe)
    print("HERE2")
    return result

# Update an existing recipe
@app.put("/recipes/{recipe_id}", response_model=RecipeRspModel)
async def modify_recipe(recipe_id: str, field: str, new_value: Union[str, list]):
    result = recipes_resource.modify_recipe(recipe_id, field, new_value)
    return result

# Delete a recipe
@app.delete("/recipes", response_model=RecipeRspModel)
async def delete_recipe(recipe_id: str):
    result = recipes_resource.delete_recipe(recipe_id)
    return result

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8011)