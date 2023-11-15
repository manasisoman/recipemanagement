import json

class RecipeDataService():
    def __init__(self, config: dict):

        self.data_dir = config['data_directory']
        self.data_file = config["data_file"]
        self.recipes = []
        self.highest_recipe_id = None

        self.load()

    def get_data_file_name(self):
        filename =  self.data_dir + "/" + self.data_file
        return filename
    
    def load(self):
        file_name = self.get_data_file_name()
        with open(file_name, "r") as file:
            self.recipes = json.load(file)
        
        for recipe in self.recipes:
            id = int(recipe.get("recipe_id"))
            if not self.highest_recipe_id or id > self.highest_recipe_id:
                self.highest_recipe_id = id

    def save(self):
        file_name = self.get_data_file_name()
        with open(file_name, "w") as out_file:
            json.dump(self.recipes, out_file)

    def get_recipes(self, recipe_id: str = None, title: str = None, author_id: str = None):
        """
        Get recipes that match a recipe_id, title, and/or an author_id
        """
        result = []

        for r in self.recipes:
            if (recipe_id is None or (r.get("recipe_id", None) == recipe_id)) and \
                    (title is None or (r.get("title", None) == title)) and \
                    (author_id is None or (r.get("author_id", None) == author_id)):
                result.append(r)

        return result
    
    def get_recipe_by_id(self, recipe_id: str = None):
        """
        Get recipes that match a recipe_id
        """
        result = {}

        for r in self.recipes:
            if (recipe_id is None or (r.get("recipe_id", None) == recipe_id)):
                print("this is r", r)
                return r

        return result
    
    
    def add_recipes(self, recipe_info: dict):
        """
        This will add the recipe into the db
        """
        # generate a new, unique recipe_id
        new_recipe_id = self.get_unique_id()
        
        # add the new recipe info to the list
        recipe_info["recipe_id"] = str(new_recipe_id)
        self.recipes.append(recipe_info)
        print('recipe_info')
        print(recipe_info)

        # save the data
        self.save()
        print('save')
        
        # return the new recipe's ID
        return new_recipe_id


    def get_unique_id(self):
        new_id = self.highest_recipe_id + 1
        self.highest_recipe_id = new_id
        print("New id: ", new_id)

        return new_id







        