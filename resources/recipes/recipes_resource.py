from resources.recipes.recipe_models import RecipeRspModel, RecipeModel
from resources.rest_models import Link
from typing import List
from fastapi import HTTPException

class RecipeResource():
    def __init__(self, config):
        self.data_service = config["data_service"]
    
    @staticmethod
    def generate_links(info: dict) -> RecipeRspModel:
        print("INFO IS: ", info)
        keys = ['recipe_id', 'title', 'author_id', 'ingredients', 'steps', 'images']

        if not info:
            return None
        info = {keys[i]: info[i] for i in range(len(keys))}

        self_link = Link(**{
            "rel": "self",
            "href": "/recipes/" + str(info['recipe_id'])
        })

        
        links = [self_link]

        rsp = RecipeRspModel(**info, links=links)
        return rsp

    def get_recipes(self, recipe_id = None, title = None, author_id = None) -> List[RecipeRspModel]:
        print('getting recipes')
        result = self.data_service.get_recipes(recipe_id, title, author_id)
        print('received result:', result)
        final_result = []

        for r in result:
            m = self.generate_links(r)
            final_result.append(m)

        print('final result:', final_result)
        
        return final_result
    
    def get_one_recipe(self, recipe_id):
        print('get one recipe')
        result = self.data_service.get_recipe_by_id(recipe_id)
        final_result = []
        print('got the result from the data service', result)

        m = self.generate_links(result)

        # for r in result:
        #     m = self.generate_links(r)
        #     final_result.append(m)

        return m

    def filter_recipes(self, objects_filter: str):
        print('Getting recipes by query string')
        print('This is the obj filter', objects_filter)

        # Call data service function to filter the recipes and get the result
        result = self.data_service.filter(objects_filter)

        print('The resulting result is:', result)
        final_result = [self.generate_links(r) for r in result]

        return final_result

    
    def add_recipe(self, recipe_info: dict) -> RecipeRspModel:
        # Call the data service method to add the recipe
        print('recipe_info', recipe_info)
        new_recipe_id = self.data_service.add_recipes(recipe_info)
        print("new recipe id: ", new_recipe_id)


        # Retrieve the added recipe by ID -> JSON object
        added_recipe = self.data_service.get_recipe_by_id(new_recipe_id)
        print("json obj: ", added_recipe)

        # Generate links for the added recipe
        recipe_with_links = self.generate_links(added_recipe)

        return recipe_with_links

    def modify_recipe(self, recipe_id, field, new_value):
        if self.data_service.check_id_exists(recipe_id):
            id = self.data_service.modify_recipe_by_field(recipe_id, field, new_value)
            modified_recipe = self.data_service.get_recipe_by_id(id)
            link = self.generate_links(modified_recipe)
            return link
        else:
            raise HTTPException(status_code=500, detail="Recipe ID does not exist")
        
    def delete_recipe(self, recipe_id):
        if self.data_service.check_id_exists(recipe_id):
            result = self.data_service.delete_recipe(recipe_id)
            print('this is what delete returned', result)
            link = self.generate_links(result)
            return link
        else:
            raise HTTPException(status_code=500, detail="Recipe ID does not exist")