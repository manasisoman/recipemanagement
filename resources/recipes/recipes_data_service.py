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
    
    def get_all_recipes(self):
        result = []
        for r in self.recipes:
            result.append(r)
        return result


    def check_id_exists(self, recipe_id):
        for r in self.recipes:
            if r.get("recipe_id", None) == recipe_id:
                return True
        
        return False
    
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
    
    def modify_recipe_by_field(self, recipe_id, field, new_value):
        """
        This will modify the recipe in the DB
        """
        old_recipe = {}
        # pull the recipe from the DB
        for r in self.recipes:
            if r.get("recipe_id") == recipe_id:
                old_recipe = r
                self.recipes.remove(r)
                break

        # Handle special case for field with lists
        if field == "steps" or field == "ingredients" or field == "images":
            if isinstance(new_value, str):
                # Convert a string to a list separated by commas (for example)
                new_value = new_value.split(",")  # You might need a different delimiter
            elif not isinstance(new_value, list):
                # If it's neither a string nor a list, handle accordingly
                new_value = [new_value]  # Put the single value into a list

        # modify the field, update, and save
        old_recipe[field] = new_value
        self.recipes.append(old_recipe)
        self.save()

        return recipe_id
    
    def delete_recipe(self, recipe_id):
        removed_recipe = {}
        for r in self.recipes:
            if r.get("recipe_id") == recipe_id:
                removed_recipe = r
                self.recipes.remove(r)
                self.save()

        return removed_recipe

    
    def filter(self, objects_filter):
        filter_mappings = {
            'title': 'title',
            'author': 'author_id',
            'ingredient': 'ingredients'
        }

        filters = objects_filter.split(',') # go through each of the possible fields 
        filtered_recipes = self.recipes

        for f in filters:
            filter_parts = f.split(':')
            if len(filter_parts) == 2 and filter_parts[0] in filter_mappings:
                field = filter_mappings[filter_parts[0]]
                value = filter_parts[1].lower()
                print('field', field, 'value', value)

                if field == 'ingredients':
                    filtered_recipes = [r for r in filtered_recipes if any(value in ing.lower() for ing in r.get('ingredients'))]
                elif field == 'author_id':
                    filtered_recipes = [r for r in filtered_recipes if value in r.get('author_id', '').lower()]
                elif field == 'title':
                    filtered_recipes = [r for r in filtered_recipes if value in r.get('title', '').lower()]

        return filtered_recipes


    def get_unique_id(self):
        new_id = self.highest_recipe_id + 1
        self.highest_recipe_id = new_id
        print("New id: ", new_id)

        return new_id







        