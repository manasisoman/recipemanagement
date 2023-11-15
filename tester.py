from resources.recipes.recipes_data_service import RecipeDataService
import uuid

def generate_unique_recipe_id(used_recipe_ids):
    new_recipe_id = str(uuid.uuid4())  # Generate a new UUID

    # Ensure the generated ID is unique
    while new_recipe_id in used_recipe_ids:
        new_recipe_id = str(uuid.uuid4())

    return new_recipe_id

def main():
    used_recipe_ids = {'abc123', 'def456', 'ghi789'}  # Set of used recipe IDs
    new_recipe_id = generate_unique_recipe_id(used_recipe_ids)
    print(new_recipe_id)
        

if __name__ == "__main__":
    main()