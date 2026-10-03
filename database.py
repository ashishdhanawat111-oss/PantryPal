import sqlite3


# Connect to our SQLite database
def connect_db():
    return sqlite3.connect("pantry.db")


# Create pantry table if it doesn't already exist
def create_table():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pantry (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            quantity REAL NOT NULL,
            unit TEXT NOT NULL,
            category TEXT,
            low_stock REAL DEFAULT 0,
            expiry_date TEXT
        )
    """)

    conn.commit()
    conn.close()


# Add a new ingredient
def add_ingredient(
    name,
    quantity,
    unit,
    category,
    low_stock,
    expiry_date
):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO pantry
        (name, quantity, unit, category, low_stock, expiry_date)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        name,
        quantity,
        unit,
        category,
        low_stock,
        expiry_date
    ))

    conn.commit()
    conn.close()


# Get every ingredient from pantry
def get_ingredients():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM pantry")

    ingredients = cursor.fetchall()

    conn.close()

    return ingredients


# Find an ingredient by name and unit
def find_ingredient(name, unit):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM pantry
        WHERE LOWER(name) = LOWER(?)
        AND unit = ?
    """, (name, unit))

    ingredient = cursor.fetchone()

    conn.close()

    return ingredient


# Change the quantity of an ingredient
def update_quantity(ingredient_id, new_quantity):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE pantry
        SET quantity = ?
        WHERE id = ?
    """, (
        new_quantity,
        ingredient_id
    ))

    conn.commit()
    conn.close()


# Delete an ingredient
def delete_ingredient(ingredient_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM pantry
        WHERE id = ?
    """, (ingredient_id,))

    conn.commit()
    conn.close()

# ==================================================
# RECIPE FUNCTIONS
# ==================================================


def create_recipe_tables():
    conn = connect_db()
    cursor = conn.cursor()

    # Stores basic recipe information
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS recipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            servings INTEGER NOT NULL,
            instructions TEXT
        )
    """)

    # Stores ingredients belonging to each recipe
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS recipe_ingredients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            recipe_id INTEGER NOT NULL,
            ingredient_name TEXT NOT NULL,
            quantity REAL NOT NULL,
            unit TEXT NOT NULL,
            FOREIGN KEY (recipe_id)
                REFERENCES recipes(id)
                ON DELETE CASCADE
        )
    """)

    conn.commit()
    conn.close()


def add_recipe(name, servings, instructions, ingredients):
    conn = connect_db()
    cursor = conn.cursor()

    # First create the recipe
    cursor.execute("""
        INSERT INTO recipes (
            name,
            servings,
            instructions
        )
        VALUES (?, ?, ?)
    """, (
        name,
        servings,
        instructions
    ))

    # Get ID of the recipe we just created
    recipe_id = cursor.lastrowid

    # Add every ingredient belonging to that recipe
    for ingredient in ingredients:

        cursor.execute("""
            INSERT INTO recipe_ingredients (
                recipe_id,
                ingredient_name,
                quantity,
                unit
            )
            VALUES (?, ?, ?, ?)
        """, (
            recipe_id,
            ingredient["name"],
            ingredient["quantity"],
            ingredient["unit"]
        ))

    conn.commit()
    conn.close()


def get_recipes():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM recipes
        ORDER BY id DESC
    """)

    recipes = cursor.fetchall()

    conn.close()

    return recipes


def get_recipe_ingredients(recipe_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM recipe_ingredients
        WHERE recipe_id = ?
    """, (recipe_id,))

    ingredients = cursor.fetchall()

    conn.close()

    return ingredients


def delete_recipe(recipe_id):
    conn = connect_db()
    cursor = conn.cursor()

    # Delete recipe ingredients first
    cursor.execute("""
        DELETE FROM recipe_ingredients
        WHERE recipe_id = ?
    """, (recipe_id,))

    # Then delete recipe
    cursor.execute("""
        DELETE FROM recipes
        WHERE id = ?
    """, (recipe_id,))

    conn.commit()
    conn.close()

def reduce_ingredient_quantity(
    ingredient_name,
    quantity_used,
    used_unit
):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM pantry
        WHERE LOWER(name) = LOWER(?)
    """, (ingredient_name,))

    pantry_items = cursor.fetchall()

    for ingredient in pantry_items:

        ingredient_id = ingredient[0]
        pantry_quantity = ingredient[2]
        pantry_unit = ingredient[3]

        converted_quantity = convert_quantity(
            quantity_used,
            used_unit,
            pantry_unit
        )

        if converted_quantity is not None:

            new_quantity = (
                pantry_quantity
                - converted_quantity
            )

            if new_quantity < 0:
                new_quantity = 0

            cursor.execute("""
                UPDATE pantry
                SET quantity = ?
                WHERE id = ?
            """, (
                new_quantity,
                ingredient_id
            ))

            break

    conn.commit()
    conn.close()


# ==================================================
# UNIT CONVERSION HELPERS
# ==================================================


def get_unit_type(unit):

    if unit in ["kg", "g"]:
        return "weight"

    elif unit in ["L", "ml"]:
        return "volume"

    else:
        return unit


def convert_quantity(quantity, from_unit, to_unit):

    # Same unit - no conversion needed
    if from_unit == to_unit:
        return quantity

    # Weight conversions
    if from_unit == "kg" and to_unit == "g":
        return quantity * 1000

    if from_unit == "g" and to_unit == "kg":
        return quantity / 1000

    # Volume conversions
    if from_unit == "L" and to_unit == "ml":
        return quantity * 1000

    if from_unit == "ml" and to_unit == "L":
        return quantity / 1000

    # Units cannot be converted
    return None


# ==================================================
# GROCERY FUNCTIONS
# ==================================================


def create_grocery_table():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS groceries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            quantity REAL NOT NULL,
            unit TEXT NOT NULL,
            purchased INTEGER DEFAULT 0
        )
    """)

    conn.commit()
    conn.close()


def add_grocery_item(
    name,
    quantity,
    unit
):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM groceries
        WHERE LOWER(name) = LOWER(?)
        AND unit = ?
        AND purchased = 0
    """, (
        name,
        unit
    ))

    existing = cursor.fetchone()

    if existing:

        new_quantity = (
            existing[2] + quantity
        )

        cursor.execute("""
            UPDATE groceries
            SET quantity = ?
            WHERE id = ?
        """, (
            new_quantity,
            existing[0]
        ))

    else:

        cursor.execute("""
            INSERT INTO groceries (
                name,
                quantity,
                unit,
                purchased
            )
            VALUES (?, ?, ?, 0)
        """, (
            name,
            quantity,
            unit
        ))

    conn.commit()
    conn.close()


def get_grocery_items():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM groceries
        WHERE purchased = 0
        ORDER BY id DESC
    """)

    groceries = cursor.fetchall()

    conn.close()

    return groceries


def delete_grocery_item(grocery_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM groceries
        WHERE id = ?
    """, (grocery_id,))

    conn.commit()
    conn.close()

def purchase_grocery_item(grocery_id):
    conn = connect_db()
    cursor = conn.cursor()

    # Get grocery item
    cursor.execute("""
        SELECT *
        FROM groceries
        WHERE id = ?
    """, (grocery_id,))

    grocery = cursor.fetchone()

    if grocery is None:
        conn.close()
        return

    name = grocery[1]
    quantity = grocery[2]
    unit = grocery[3]

    # Look for same ingredient in pantry
    cursor.execute("""
        SELECT *
        FROM pantry
        WHERE LOWER(name) = LOWER(?)
    """, (name,))

    pantry_items = cursor.fetchall()

    ingredient_found = False

    for pantry_item in pantry_items:

        pantry_id = pantry_item[0]
        pantry_quantity = pantry_item[2]
        pantry_unit = pantry_item[3]

        converted_quantity = convert_quantity(
            quantity,
            unit,
            pantry_unit
        )

        if converted_quantity is not None:

            new_quantity = (
                pantry_quantity
                + converted_quantity
            )

            cursor.execute("""
                UPDATE pantry
                SET quantity = ?
                WHERE id = ?
            """, (
                new_quantity,
                pantry_id
            ))

            ingredient_found = True
            break

    # Ingredient does not exist in pantry yet
    if not ingredient_found:

        cursor.execute("""
            INSERT INTO pantry (
                name,
                quantity,
                unit,
                category,
                low_stock,
                expiry_date
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            name,
            quantity,
            unit,
            "Other",
            0,
            None
        ))

    # Remove purchased item from grocery list
    cursor.execute("""
        DELETE FROM groceries
        WHERE id = ?
    """, (grocery_id,))

    conn.commit()
    conn.close()