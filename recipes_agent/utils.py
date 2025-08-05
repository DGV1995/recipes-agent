import re


def parse_recipe(raw):
    result = {}

    # Extraer nombre (hasta la primera coma)
    name, rest = raw.split(",", 1)
    result["name"] = name.strip()

    # Extraer ingredients
    ingredients_match = re.search(r"ingredients:\[(.*?)\]", rest)
    if ingredients_match:
        ingredients_raw = ingredients_match.group(1)
        ingredient_list = re.findall(r"\{(.*?)\}", ingredients_raw)
        ingredients = []
        for item in ingredient_list:
            parts = [kv.strip() for kv in item.split(",")]
            ing = {}
            for part in parts:
                key, value = part.split(":", 1)
                ing[key.strip()] = try_cast(value.strip())
            ingredients.append(ing)
        result["ingredients"] = ingredients

    # Extract cooking_time
    cooking_match = re.search(r"cooking_time:\s*(\d+)", rest)
    if cooking_match:
        result["cooking_time"] = int(cooking_match.group(1))

    # Extract instructions
    instructions_match = re.search(r"instructions:\s*\[(.*?)\]", rest)
    if instructions_match:
        instructions_raw = instructions_match.group(1)
        instructions = [instr.strip() for instr in instructions_raw.split(",")]
        result["instructions"] = instructions

    # Extract category
    category_match = re.search(r"category:\s*([^,]+)", rest)
    if category_match:
        result["category"] = category_match.group(1).strip()

    # Extract types
    types_match = re.search(r"types:\s*\[(.*?)\]", rest)
    if types_match:
        types_raw = types_match.group(1)
        result["types"] = [t.strip() for t in types_raw.split(",")]

    # Extract macros
    macros = {}
    for macro in ["proteins", "carbs", "fats", "calories"]:
        pattern = rf"{macro}:\s*\{{(.*?)\}}"
        match = re.search(pattern, rest)
        if match:
            kvs = match.group(1)
            parts = [kv.strip() for kv in kvs.split(",")]
            macros[macro] = {}
            for part in parts:
                key, value = part.split(":", 1)
                macros[macro][key.strip()] = try_cast(value.strip())
    result["macros"] = macros

    return result


def try_cast(val):
    try:
        return int(val)
    except Exception:
        return val.strip('"')
