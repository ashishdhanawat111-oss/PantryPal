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
Prefer recipes that naturally use these ingredients.
Do NOT force an expiring ingredient into a dish where
it would taste strange or be unrealistic.
"""

        else:

            expiry_priority_text = """
There are currently no pantry ingredients expiring
within the next 3 days.
"""

    prompt = f"""
You are PantryPal, a practical home-cooking assistant.

Your job is to recommend meals that a normal person
would realistically cook and enjoy.

USER'S PANTRY:

{pantry_text}

REQUEST:

Meal type: {meal_type}
Servings: {servings}
Preference: {preference}

{expiry_priority_text}

Recommend exactly 3 realistic and recognizable dishes.

VERY IMPORTANT RECIPE RULES:

1. Recommend familiar, realistic home-cooked dishes.
   Do not invent unusual dishes or strange ingredient
   combinations just to use pantry ingredients.

2. Pantry ingredients should be the main basis of recipes,
   but only combine ingredients that naturally belong
   together in that dish.

3. Use realistic quantities for exactly {servings} serving(s).
   Think carefully about normal portion sizes before choosing
   each quantity.

4. Avoid excessive quantities. For example, a simple meal
   for 2 people should normally not require hundreds of grams
   of several different main ingredients unless appropriate.

5. Never use more of a pantry ingredient than the user
   currently has available.

6. Prefer recipes requiring few missing ingredients.
   If the pantry cannot make a complicated meal, recommend
   a simpler realistic meal instead.

7. Include ALL ingredients required to actually cook the dish.
   This includes things such as oil, salt, water, spices,
   seasonings and sauces when they are needed.

8. Never mention an ingredient in the instructions unless
   that ingredient also appears in the "ingredients" list.

9. Do not write vague instructions such as:
   "add spices",
   "season as needed",
   "cook normally",
   or "prepare the mixture".

   Instead, state what to add and approximately how much.

10. Write instructions for a BEGINNER who may not know
    how to cook.

11. Instructions should explain the cooking process in a
    clear order. Include useful details such as approximate
    cooking time, heat level, or amount of water when needed.

12. Keep the instructions reasonably short. They should be
    detailed enough to cook the dish but not unnecessarily long.

13. If an ingredient required for the recipe is not in the
    pantry, include it in the ingredients list with
    "available": false.

14. Also include every unavailable required ingredient by
    name in the "missing" array.

15. If an ingredient exists in the pantry and enough quantity
    is available, mark "available": true.

16. Basic cooking ingredients are NOT automatically available.
    If oil, salt, spices, sauces or similar ingredients are
    not listed in the pantry, mark them unavailable.

17. Water may be included as an ingredient when needed for
    cooking. Water does not need to be present in the pantry
    and should use ml or L.

18. Respect the requested meal type and preference.

19. When expiry priority is active, use an expiring ingredient
    only when it naturally fits the dish. Never create a strange
    recipe merely to consume it.

20. Before returning the answer, mentally check each recipe:
    - Is this a real and sensible dish?
    - Are the quantities reasonable for {servings} serving(s)?
    - Could a beginner follow these instructions?
    - Is every ingredient mentioned in the instructions also
      present in the ingredients list?
    If not, correct the recipe before returning it.

PORTION AND UNIT RULES:

For normal meals serving 1 to 4 people:

- Rice should normally be about 60 to 120 g per person.
- Dal, chana and other pulses should normally be about
  50 to 100 g per person.
- Potato should normally be about 100 to 250 g per person.
- Tomato should normally be about 50 to 200 g per person.
- Other vegetables should normally be about
  50 to 250 g per person.
- Eggs should normally be about 1 to 3 pieces per person.
- Cooking oil should normally be measured in tbsp or tsp.
- Salt and spices should normally be measured in tsp,
  not grams or kilograms.
- Water should normally be measured in ml or L.

These are approximate cooking guidelines, not targets.
Use culinary judgment depending on the dish.

For recipes serving 1 to 4 people, NEVER use kg for ordinary
amounts of rice, dal, pulses, vegetables, spices or seasonings.
Use g instead.

NEVER use hundreds of grams of spices or masala.

Before returning each recipe, verify that the quantities are
reasonable for exactly {servings} serving(s).

CRITICAL CONSISTENCY RULE:

Read the final cooking instructions after writing them.
Every food, spice, seasoning, oil, sauce or other ingredient
mentioned in the instructions MUST appear in the ingredients
array.

If you mention onion, garlic, ginger, chilli, oil, salt,
spices or anything else in the instructions, it MUST be
listed as an ingredient.

If it is not available in the pantry, set "available": false
and include its name in "missing".

ALLOWED UNITS ONLY:

kg
g
L
ml
pieces
packets
tbsp
tsp

OUTPUT RULES:

Return ONLY valid JSON.
Do not write explanations before or after the JSON.
Do not use markdown.
Do not use ```json or code fences.

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
            "instructions": "Short practical cooking instructions."
        }}
    ]
}}

The "recipes" array MUST contain exactly 3 recipes.
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

        if len(data["recipes"]) != 3:
            return None

        return data

    except Exception:

        return None