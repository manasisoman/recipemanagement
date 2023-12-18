import json
import mysql.connector

class RecipeDataService():
    def __init__(self):
        self.connection = self.get_connection()

    def get_connection(self):
        return mysql.connector.connect(
            user="admin",
            password="cloudymeatball",
            host="recipediadb.c52h6qfa4sj1.us-east-1.rds.amazonaws.com",
            port="3306",
            database="recipesDB"
        )

    # def get_data_file_name(self):
    #     filename =  self.data_dir + "/" + self.data_file
    #     return filename
    
    # def load(self):
    #     file_name = self.get_data_file_name()
    #     with open(file_name, "r") as file:
    #         self.recipes = json.load(file)
        
    #     for recipe in self.recipes:
    #         id = int(recipe.get("recipe_id"))
    #         if not self.highest_recipe_id or id > self.highest_recipe_id:
    #             self.highest_recipe_id = id

    # def save(self):
    #     file_name = self.get_data_file_name()
    #     with open(file_name, "w") as out_file:
    #         json.dump(self.recipes, out_file)
    
    def get_recipes(self, recipe_id: int = None, title: str = None, author_id: str = None):
        """
        Get recipes that match a recipe_id, title, and/or an author_id
        """
        try:
            query = "SELECT * FROM recipes WHERE "
            conditions = []
            params = []
            if recipe_id is not None:
                conditions.append("recipe_id = %s")
                params.append(recipe_id)

            if title is not None:
                conditions.append("title = %s")
                params.append(title)

            if author_id is not None:
                conditions.append("author_id = %s")
                params.append(author_id)
            
            if conditions:
                query += " AND ".join(conditions)
            else:
                query = query.replace(" WHERE ", "")  # if no conditions, remove WHERE clause

            cursor = self.connection.cursor()
            cursor.execute(query, tuple(params))
            recipes = cursor.fetchall()
            print(recipes)
            cursor.close()
            return recipes
        except mysql.connector.Error as e:
            print("Error fetching recipes:", e)
            return []

    def get_recipe_by_id(self, recipe_id):
        """
        Get recipes that match a recipe_id
        """
        if recipe_id is None:
            return None  # or you can choose to return an empty dict {}

        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM recipes WHERE recipe_id = %s", (recipe_id,))
            recipe = cursor.fetchone()
            print(recipe)
            cursor.close()
            return recipe
        except mysql.connector.Error as e:
            print("Recipe ID", e)
            print("Error in fetching recipe by id:", e)
            return None

    def get_all_recipes(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM recipes")
            recipes = cursor.fetchall()
            cursor.close()
            print(recipes)
            return recipes
        except mysql.connector.Error as e:
            print("Error fetching all recipes", e)

    def check_id_exists(self, recipe_id):
        """
        Checks if a given recipe_id exists in the database.
        """
        try:
            cursor = self.connection.cursor()
            query = "SELECT COUNT(*) FROM recipes WHERE recipe_id = %s"
            cursor.execute(query, (recipe_id,))
            (count,) = cursor.fetchone()
            cursor.close()
            return count > 0
        except mysql.connector.Error as e:
            print("Error checking if ID exists:", e)
            return False
    
    def add_recipes(self, recipe_info: dict):
        """
        Adds the recipe into the database.
        """
        try:
            cursor = self.connection.cursor()
            new_id = self.get_unique_id()
            if new_id is None:
                raise Exception("Failed to generate a unique ID.")
            query = """
                INSERT INTO recipes (recipe_id, title, author_id, ingredients, steps, images)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            values = (
                new_id,
                recipe_info['title'],
                recipe_info['author_id'],
                recipe_info['ingredients'],
                recipe_info['steps'],
                recipe_info['images']
            )
            cursor.execute(query, values)
            self.connection.commit()  # Commit the transaction
            cursor.close()
            return new_id
        except mysql.connector.Error as e:
            print("Error adding recipe to the database:", e)
            return None
        
    def modify_recipe_by_field(self, recipe_id, field, new_value):
        """
        Modifies a field of a recipe in the database.
        """
        try:
            cursor = self.connection.cursor()

            # Prepare the SQL query for updating the field
            query = "UPDATE recipes SET {} = %s WHERE recipe_id = %s".format(field)
            cursor.execute(query, (new_value, recipe_id))

            # Check if the update was successful
            if cursor.rowcount == 0:
                raise Exception("No rows were updated. The recipe might not exist, or the field is invalid.")

            self.connection.commit()
            cursor.close()
            return recipe_id
        except mysql.connector.Error as e:
            print("Error modifying the recipe in the database:", e)
            return None
        except Exception as e:
            print(e)
            return None
    
    def delete_recipe(self, recipe_id):
        """
        Deletes a recipe from the database.
        """
        try:
            cursor = self.connection.cursor()

            # First, optionally, fetch the recipe to be deleted (if you want to return it)
            cursor.execute("SELECT * FROM recipes WHERE recipe_id = %s", (recipe_id,))
            removed_recipe = cursor.fetchone()

            # Then, perform the delete operation
            cursor.execute("DELETE FROM recipes WHERE recipe_id = %s", (recipe_id,))
            self.connection.commit()

            cursor.close()
            return removed_recipe  # or just return True to indicate success
        except mysql.connector.Error as e:
            print("Error deleting recipe from the database:", e)
            return None  # or False to indicate failure

    def filter(self, objects_filter):
        filter_mappings = {
            'title': 'title',
            'author': 'author_id',
            'ingredient': 'ingredients'
        }

        filters = objects_filter.split(',')
        query = "SELECT * FROM recipes"
        conditions = []
        params = []

        for f in filters:
            filter_parts = f.split(':')
            if len(filter_parts) == 2 and filter_parts[0] in filter_mappings:
                field = filter_mappings[filter_parts[0]]
                value = filter_parts[1].lower()

                if field in ['title', 'author_id', 'ingredients']:
                    conditions.append(f"LOWER({field}) LIKE %s")
                    params.append(f"%{value}%")

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            filtered_recipes = cursor.fetchall()
            cursor.close()
            return filtered_recipes
        except mysql.connector.Error as e:
            print("Error in filtering recipes", e)
            return []
    
    def get_unique_id(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT MAX(recipe_id) FROM recipes")
            result = cursor.fetchone()
            max_id = result[0] if result[0] is not None else 0
            new_id = max_id + 1
            return new_id
        except mysql.connector.Error as e:
            print("Error getting unique ID:", e)
            return None
        finally:
            cursor.close()

def main():
    print("----------------------------------------------")
    db = RecipeDataService()
    print("----------------------------------------------")
    print("Get recipe by id")
    db.get_recipe_by_id(1)
    print("----------------------------------------------")
    print("Get recipes")
    db.get_recipes()
    print("----------------------------------------------")
    print("Get all recipes")
    db.get_all_recipes()




if __name__ == "__main__":
    main()

        