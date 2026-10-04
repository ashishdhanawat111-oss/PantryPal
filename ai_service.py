import os
import json

from dotenv import load_dotenv
from huggingface_hub import InferenceClient
from datetime import date, datetime


# Load variables from the .env file
load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")


def ask_gemma(message):

    if not HF_TOKEN:
        return "Error: HF_TOKEN was not found."

    try:

        client = InferenceClient(
            provider="auto",
            api_key=HF_TOKEN
        )

        response = client.chat.completions.create(
            model="google/gemma-3-4b-it",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are PantryPal, a friendly "
                        "AI kitchen assistant."
                    )
                },
                {
                    "role": "user",
                    "content": message
                }
            ],
            max_tokens=1200
        )

        return response.choices[0].message.content

    except Exception as error:

        return f"AI Error: {error}"

def get_meal_suggestions(
    pantry_items,
    meal_type,
    servings,
    preference
):

    if len(pantry_items) == 0:
        return (
            "Your pantry is empty. "
            "Add some ingredients first."
        )

    pantry_text = ""

    for ingredient in pantry_items:

        name = ingredient[1]
        quantity = ingredient[2]
        unit = ingredient[3]

        pantry_text += (
            f"- {name}: {quantity:g} {unit}\n"
        )

    prompt = f"""
You are PantryPal, a practical AI kitchen assistant.

The user currently has these ingredients:

{pantry_text}

The user wants:
Meal type: {meal_type}
Servings: {servings}
Preference: {preference}

Recommend exactly 3 suitable dishes.

IMPORTANT RULES:

1. Prioritize ingredients already available in the pantry.
2. Do not claim an ingredient is available if it is not listed.
3. Consider the quantities available.
4. Clearly mention any important missing ingredients.
5. Prefer simple and realistic home-cooked meals.
6. Keep the answer concise.
7. Do not invent pantry quantities.
8. Do not tell the user to buy ingredients unless they are actually needed.

For each dish use this format:

### Dish Name

Why it works:
Short explanation.

Uses from pantry:
- ingredient
- ingredient

Missing:
- ingredient
OR
None

Quick method:
Short cooking instructions.
"""

    return ask_gemma(prompt)


def estimate_cooked_ingredients(
    meal_description,
    pantry_items
):

    if meal_description.strip() == "":
        return None

    pantry_text = ""

    for ingredient in pantry_items:

        name = ingredient[1]
        quantity = ingredient[2]
        unit = ingredient[3]

        pantry_text += (
            f"- {name}: {quantity:g} {unit}\n"
        )

    prompt = f"""
You are PantryPal, an AI kitchen assistant.

The user says they cooked:

"{meal_description}"

Their current pantry contains:

{pantry_text}

Estimate which pantry ingredients were probably used
and approximately how much was used.

IMPORTANT RULES:

1. Only include ingredients that exist in the pantry.
2. Use the same ingredient names as the pantry.
3. Use realistic quantities.
4. Use only these units:
   kg, g, L, ml, pieces, packets, tbsp, tsp
5. Do not subtract anything yourself.
6. The user will review your estimates before anything changes.
7. Return ONLY valid JSON.
8. Do not use markdown.
9. Do not wrap the JSON in ```json.

Return exactly this structure:

{{
    "dish": "dish name",
    "ingredients": [
        {{
            "name": "ingredient name",
            "quantity": 1,
            "unit": "pieces"
        }}
    ]
}}
"""

    response = ask_gemma(prompt)

    try:

        cleaned_response = response.strip()

        if cleaned_response.startswith("```json"):
            cleaned_response = cleaned_response[7:]

        elif cleaned_response.startswith("```"):
            cleaned_response = cleaned_response[3:]

        if cleaned_response.endswith("```"):
            cleaned_response = cleaned_response[:-3]

        data = json.loads(
            cleaned_response.strip()
        )

        return data

    except Exception:

        return None


def get_structured_meal_suggestions(
    pantry_items,
    meal_type,
    servings,
    preference
):

    if len(pantry_items) == 0:
        return None

    pantry_text = ""

    for ingredient in pantry_items:

        name = ingredient[1]
        quantity = ingredient[2]
        unit = ingredient[3]

        pantry_text += (
            f"- {name}: {quantity:g} {unit}\n"
        )

    expiring_soon = []

    for ingredient in pantry_items:

        name = ingredient[1]
        expiry_date = ingredient[6]

        if expiry_date:

            try:

                expiry = datetime.strptime(
                    expiry_date,
                    "%Y-%m-%d"
                ).date()

                days_left = (
                    expiry - date.today()
                ).days

                if 0 <= days_left <= 3:

                    expiring_soon.append({
                        "name": name,
                        "days_left": days_left
                    })

            except ValueError:

                pass
    expiry_priority_text = ""

    if (
        preference
        == "Use ingredients that may expire soon"
    ):

        if len(expiring_soon) > 0:

            expiry_priority_text = (
                "\nPRIORITY INGREDIENTS:\n"
            )

            for item in expiring_soon:

                expiry_priority_text += (
                    f"- {item['name']} "
                    f"(expires in "
                    f"{item['days_left']} days)\n"
                )

            expiry_priority_text += """
Strongly prioritize these ingredients when creating
the recipes so the user can use them before they expire.
"""

        else:

            expiry_priority_text = """
There are currently no pantry ingredients expiring
within the next 3 days.
"""

    prompt = f"""
You are PantryPal, a practical AI kitchen assistant.

The user's pantry contains:

{pantry_text}

The user wants:

Meal type: {meal_type}
Servings: {servings}
Preference: {preference} 

{expiry_priority_text}

Recommend exactly 3 realistic dishes.

IMPORTANT RULES:

1. Prioritize ingredients already in the pantry.
2. Consider the available quantities.
3. You may suggest a small number of missing ingredients.
4. Never claim a missing ingredient is in the pantry.
5. Use realistic ingredient quantities.
6. Return ONLY valid JSON.
7. Do not use markdown.
8. Do not wrap the response in ```json.
9. Use only these units:
   kg, g, L, ml, pieces, packets, tbsp, tsp.

Return exactly this structure:

{{
    "recipes": [
        {{
            "name": "Recipe Name",
            "servings": {servings},
            "ingredients": [
                {{
                    "name": "Ingredient",
                    "quantity": 1,
                    "unit": "pieces",
                    "available": true
                }}
            ],
            "missing": [
                "Missing Ingredient"
            ],
            "instructions": "Short cooking instructions"
        }}
    ]
}}
"""

    response = ask_gemma(prompt)

    try:

        cleaned_response = response.strip()

        if cleaned_response.startswith("```json"):
            cleaned_response = cleaned_response[7:]

        elif cleaned_response.startswith("```"):
            cleaned_response = cleaned_response[3:]

        if cleaned_response.endswith("```"):
            cleaned_response = cleaned_response[:-3]

        data = json.loads(
            cleaned_response.strip()
        )

        if "recipes" not in data:
            return None

        return data

    except Exception as error:

        print("STRUCTURED AI ERROR:")
        print(error)

        print("\nRAW GEMMA RESPONSE:")
        print(response)

        return None