import base64

from langchain_core.tools import tool
from openai import OpenAI
from supabase import create_client

from recipes_agent.constants import IMAGES_URL, SUPABASE_KEY, SUPABASE_URL
from recipes_agent.schemas.recipe import Recipe

supabase = create_client(supabase_url=SUPABASE_URL, supabase_key=SUPABASE_KEY)
openai = OpenAI()


@tool(description="Generates a recipe")
def generate_recipe(details: str):
    """
    Args
    ----
    details: str
        The details of the recipe to be generated.
    """

    prompt = f"""
    Crea una receta, siguiendo las siguientes instrucciones:
    - Evita SIEMPRE los caracteres '```json' y usa comillas dobles para los nombres de las claves y los valores. 
    - Los valores extraídos deben estar traducidos al español de España.
    - La respuesta debe ser un JSON válido. 
    - No pongas saltos de línea de tu respuesta. Debe ir todo el texto en una sola línea.
    - El nombre de la receta sólo debe tener mayúscula la primera letra.
    - Tu respuesta debe tener el siguiente esquema: {Recipe.model_json_schema()} 
    La receta que debes crear es la siguiente: '{details}'
    """

    response = openai.chat.completions.create(
        model="gpt-4o-mini", messages=[{"role": "user", "content": prompt}]
    )

    recipe = response.choices[0].message.content
    return recipe


@tool(description="Generates a realistic picture and uploads it to the database")
def generate_recipe_image(recipe_name: str):
    """
    Args
    ----
    recipe_name: str
        The name of the recipe to be generated.
    """

    response = openai.images.generate(
        model="dall-e-3",
        prompt=f"Create una imagen realista de la siguiente receta: '{recipe_name}'",
        n=1,
        response_format="b64_json",
        size="1024x1024",
    )

    image_base64 = response.data[0].b64_json
    image_bytes = base64.b64decode(image_base64)

    file_name = f"{recipe_name.lower()}.png"  # .replace(" ", "-")
    supabase.storage.from_("images").upload(file=image_bytes, path=file_name)

    return f"{IMAGES_URL}/{file_name}"


TOOLS = [generate_recipe, generate_recipe_image]
