import streamlit as st
from datetime import date, datetime

from database import (
    create_table,
    add_ingredient,
    get_ingredients,
    find_ingredient,
    update_quantity,
    delete_ingredient,
    create_recipe_tables,
    add_recipe,
    get_recipes,
    get_recipe_ingredients,
    delete_recipe,
    reduce_ingredient_quantity,
    get_unit_type,
    convert_quantity,
    create_grocery_table,
    add_grocery_item,
    get_grocery_items,
    delete_grocery_item,
    purchase_grocery_item
)


# ---------------- PAGE SETUP ----------------

st.set_page_config(
    page_title="PantryPal",
    page_icon="🥘",
    layout="wide"
)

create_table()
create_recipe_tables()
create_grocery_table()

# ---------------- SIDEBAR ----------------

st.sidebar.title("🥘 PantryPal")

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Home",
        "📦 My Pantry",
        "🍳 Cook",
        "📖 My Recipes",
        "🛒 Groceries"
    ]
)

st.sidebar.divider()

st.sidebar.write("💬 **Pal Assistant**")
st.sidebar.caption("Your kitchen buddy is coming soon 👀")


# ==================================================
# HOME
# ==================================================

if page == "🏠 Home":

    ingredients = get_ingredients()

    total_ingredients = len(ingredients)

    low_stock_items = []

    use_soon_items = []

    for ingredient in ingredients:

        quantity = ingredient[2]
        low_stock = ingredient[5]
        expiry_date = ingredient[6]

        # Check low stock
        if low_stock > 0 and quantity <= low_stock:
            low_stock_items.append(ingredient)

        # Check expiry
        if expiry_date:

            expiry = datetime.strptime(
                expiry_date,
                "%Y-%m-%d"
            ).date()

            days_left = (expiry - date.today()).days

            if 0 <= days_left <= 3:
                use_soon_items.append(
                    (ingredient, days_left)
                )


    st.title("🥘 PantryPal")
    st.caption("Your kitchen remembers, so you don't have to.")

    st.header("Good evening 👋")
    st.write("What's cooking today?")

    # Dashboard numbers
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
        "📦 Ingredients",
        total_ingredients
    )

    with col2:
        st.metric(
        "⚠️ Running Low",
        len(low_stock_items)
    )

    with col3:
        st.metric(
        "🥬 Use Soon",
        len(use_soon_items)
    )

    st.divider()

    if st.button(
        "✨ What can I cook?",
        use_container_width=True
    ):
        st.info(
            "Pal will soon help you decide what to cook 👨‍🍳"
        )

    st.subheader("Quick Actions")

    col1, col2 = st.columns(2)

    with col1:
        if st.button(
            "➕ Add Groceries",
            use_container_width=True
        ):
            st.write("Pantry feature is ready! 📦")

    with col2:
        if st.button(
            "🍽️ I Cooked Something",
            use_container_width=True
        ):
            st.write("Cooking tracker coming soon!")

    st.subheader("⚠️ Running Low")

    if len(low_stock_items) == 0:

        st.write("Everything looks well stocked! 🎉")

    else:

        for ingredient in low_stock_items:

            name = ingredient[1]
            quantity = ingredient[2]
            unit = ingredient[3]

            st.warning(
                f"{name} — only {quantity:g} {unit} left"
            )

    st.subheader("🥬 Use Soon")

    if len(use_soon_items) == 0:

        st.write(
            "Nothing needs to be used urgently."
        )

    else:

        for ingredient, days_left in use_soon_items:

            name = ingredient[1]

            if days_left == 0:
                message = f"{name} expires today! 😭"

            elif days_left == 1:
                message = f"{name} expires tomorrow."

            else:
                message = (
                    f"{name} expires in {days_left} days."
                )

            st.warning(message)


# ==================================================
# MY PANTRY
# ==================================================

elif page == "📦 My Pantry":

    st.title("📦 My Pantry")
    st.write("Everything in your kitchen lives here.")

    # ---------------- ADD INGREDIENT ----------------

    with st.expander("➕ Add Ingredient"):

        name = st.text_input("Ingredient name")

        quantity = st.number_input(
            "Quantity",
            min_value=0.0,
            step=0.5
        )

        unit = st.selectbox(
            "Unit",
            [
                "kg",
                "g",
                "L",
                "ml",
                "pieces",
                "packets"
            ]
        )

        category = st.selectbox(
            "Category",
            [
                "Grains",
                "Vegetables",
                "Fruits",
                "Dairy",
                "Spices",
                "Pulses",
                "Other"
            ]
        )

        low_stock = st.number_input(
            "Warn me when quantity goes below",
            min_value=0.0,
            step=0.5
        )

        expiry_date = st.date_input(
            "Expiry / Use-by date",
            value=None
        )

        if st.button("Add to Pantry"):

            if name.strip() == "":

                st.warning(
                    "Please enter an ingredient name."
                )

            elif quantity <= 0:

                st.warning(
                    "Quantity must be greater than 0."
                )

            else:

                # Convert the date into text for SQLite
                expiry = (
                    expiry_date.isoformat()
                    if expiry_date
                    else None
                )

                # Check whether ingredient already exists
                existing = find_ingredient(
                    name.strip(),
                    unit
                )

                if existing:

                    old_quantity = existing[2]

                    new_quantity = (
                        old_quantity + quantity
                    )

                    update_quantity(
                        existing[0],
                        new_quantity
                    )

                    st.success(
                        f"{name} updated: "
                        f"{old_quantity:g} → "
                        f"{new_quantity:g} {unit} 🥘"
                    )

                else:

                    add_ingredient(
                        name.strip(),
                        quantity,
                        unit,
                        category,
                        low_stock,
                        expiry
                    )

                    st.success(
                        f"{name} added to your pantry! 🥘"
                    )

                st.rerun()

    st.divider()

    # ---------------- DISPLAY PANTRY ----------------

    st.subheader("Your Ingredients")

    ingredients = get_ingredients()

    if len(ingredients) == 0:

        st.info(
            "Your pantry is empty. "
            "Add your first ingredient 👆"
        )

    else:

        for ingredient in ingredients:

            ingredient_id = ingredient[0]
            name = ingredient[1]
            quantity = ingredient[2]
            unit = ingredient[3]
            category = ingredient[4]
            low_stock = ingredient[5]

            col1, col2, col3 = st.columns(
                [5, 2, 1]
            )

            # Ingredient information
            with col1:

                st.write(f"**{name}**")

                st.caption(
                    f"{quantity:g} {unit} · {category}"
                )

                if (
                    low_stock > 0
                    and quantity <= low_stock
                ):
                    st.warning(
                        "⚠️ Running low!"
                    )

            # Update quantity
            with col2:

                new_quantity = st.number_input(
                    "Quantity",
                    min_value=0.0,
                    value=float(quantity),
                    step=0.5,
                    key=f"quantity_{ingredient_id}"
                )

                if st.button(
                    "Update",
                    key=f"update_{ingredient_id}"
                ):

                    update_quantity(
                        ingredient_id,
                        new_quantity
                    )

                    st.success(
                        f"{name} updated!"
                    )

                    st.rerun()

            # Delete ingredient
            with col3:

                if st.button(
                    "🗑️",
                    key=f"delete_{ingredient_id}"
                ):

                    delete_ingredient(
                        ingredient_id
                    )

                    st.rerun()

            st.divider()


# ==================================================
# COOK
# ==================================================

elif page == "🍳 Cook":

    st.title("🍳 Cook")

    st.write(
        "Choose how you want to cook."
    )

    st.button(
        "✨ What Can I Cook?",
        use_container_width=True
    )

    st.button(
        "📖 Cook From My Recipes",
        use_container_width=True
    )

    st.button(
        "🍽️ I Made Something",
        use_container_width=True
    )


# ==================================================
# MY RECIPES
# ==================================================

elif page == "📖 My Recipes":

    st.title("📖 My Recipes")
    st.write("Save the recipes you already know and love.")

    # ==================================================
    # ADD NEW RECIPE
    # ==================================================

    with st.expander("➕ Add My Recipe"):

        recipe_name = st.text_input("Recipe name")

        servings = st.number_input(
            "Servings",
            min_value=1,
            value=2,
            step=1
        )

        st.write("### Ingredients")

        ingredient_count = st.number_input(
            "How many ingredients?",
            min_value=1,
            max_value=20,
            value=3,
            step=1
        )

        recipe_ingredients = []

        for i in range(int(ingredient_count)):

            st.write(f"**Ingredient {i + 1}**")

            col1, col2, col3 = st.columns([3, 2, 2])

            with col1:
                ingredient_name = st.text_input(
                    "Name",
                    key=f"recipe_ingredient_name_{i}"
                )

            with col2:
                ingredient_quantity = st.number_input(
                    "Quantity",
                    min_value=0.0,
                    step=0.5,
                    key=f"recipe_ingredient_quantity_{i}"
                )

            with col3:
                ingredient_unit = st.selectbox(
                    "Unit",
                    [
                        "kg",
                        "g",
                        "L",
                        "ml",
                        "pieces",
                        "packets",
                        "tbsp",
                        "tsp"
                    ],
                    key=f"recipe_ingredient_unit_{i}"
                )

            recipe_ingredients.append({
                "name": ingredient_name.strip(),
                "quantity": ingredient_quantity,
                "unit": ingredient_unit
            })

        instructions = st.text_area(
            "Instructions",
            placeholder=(
                "1. Boil the eggs...\n"
                "2. Heat the oil...\n"
                "3. Add onions..."
            )
        )

        if st.button("💾 Save Recipe"):

            valid_ingredients = []

            for ingredient in recipe_ingredients:

                if (
                    ingredient["name"] != ""
                    and ingredient["quantity"] > 0
                ):
                    valid_ingredients.append(ingredient)

            if recipe_name.strip() == "":

                st.warning(
                    "Please give your recipe a name."
                )

            elif len(valid_ingredients) == 0:

                st.warning(
                    "Please add at least one valid ingredient."
                )

            else:

                add_recipe(
                    recipe_name.strip(),
                    servings,
                    instructions.strip(),
                    valid_ingredients
                )

                st.success(
                    f"{recipe_name} saved! 📖"
                )

                st.rerun()

    st.divider()

    # ==================================================
    # DISPLAY SAVED RECIPES
    # ==================================================

    st.subheader("Your Saved Recipes")

    recipes = get_recipes()

    if len(recipes) == 0:

        st.info(
            "You haven't saved any recipes yet."
        )

    else:

        for recipe in recipes:

            recipe_id = recipe[0]
            recipe_name = recipe[1]
            servings = recipe[2]
            instructions = recipe[3]

            with st.expander(
                f"🍽️ {recipe_name} · {servings} servings"
            ):

                # ==========================================
                # GET RECIPE INGREDIENTS
                # ==========================================

                ingredients = get_recipe_ingredients(
                    recipe_id
                )

                # ==========================================
                # CHECK PANTRY
                # ==========================================

                pantry_items = get_ingredients()

                missing_ingredients = []

                for recipe_ingredient in ingredients:

                    needed_name = recipe_ingredient[2]
                    needed_quantity = recipe_ingredient[3]
                    needed_unit = recipe_ingredient[4]

                    found = False

                    for pantry_item in pantry_items:

                        pantry_name = pantry_item[1]
                        pantry_quantity = pantry_item[2]
                        pantry_unit = pantry_item[3]

                        if (
                            pantry_name.lower()
                            == needed_name.lower()
                        ):

                            converted_needed = convert_quantity(
                                needed_quantity,
                                needed_unit,
                                pantry_unit
                            )

                            if converted_needed is not None:

                                found = True

                                if (
                                    pantry_quantity
                                    < converted_needed
                                ):

                                    missing_in_pantry_unit = (
                                        converted_needed
                                        - pantry_quantity
                                    )

                                    missing_ingredients.append(
                                        f"{needed_name} "
                                        f"({missing_in_pantry_unit:g} "
                                        f"{pantry_unit} more needed)"
                                    )

                                break

                    if not found:

                        missing_ingredients.append(
                            f"{needed_name} "
                            f"({needed_quantity:g} "
                            f"{needed_unit} needed)"
                        )
                # ==========================================
                # SHOW INGREDIENTS
                # ==========================================

                st.write("### Ingredients")

                for ingredient in ingredients:

                    ingredient_name = ingredient[2]
                    quantity = ingredient[3]
                    unit = ingredient[4]

                    st.write(
                        f"• {ingredient_name} — "
                        f"{quantity:g} {unit}"
                    )

                # ==========================================
                # SHOW INSTRUCTIONS
                # ==========================================

                st.write("### Instructions")

                if instructions:

                    st.write(instructions)

                else:

                    st.caption(
                        "No instructions saved."
                    )

                st.divider()

                # ==========================================
                # COOK THIS RECIPE
                # ==========================================

                st.write("### Cook this recipe")

                if len(missing_ingredients) == 0:

                    if st.button(
                        "🍳 I Cooked This",
                        key=f"cook_recipe_{recipe_id}"
                    ):

                        st.session_state[
                            "recipe_to_cook"
                        ] = recipe_id

                else:

                    st.info(
                        "You need the missing ingredients "
                        "before cooking this recipe."
                    )

                # ==========================================
                # COOKING CONFIRMATION
                # ==========================================

                if (
                    st.session_state.get(
                        "recipe_to_cook"
                    )
                    == recipe_id
                ):

                    st.warning(
                        "This will update your pantry."
                    )

                    st.write(
                        "The following ingredients "
                        "will be used:"
                    )

                    for ingredient in ingredients:

                        ingredient_name = ingredient[2]
                        quantity = ingredient[3]
                        unit = ingredient[4]

                        st.write(
                            f"• {ingredient_name}: "
                            f"-{quantity:g} {unit}"
                        )

                    confirm_col, cancel_col = st.columns(2)

                    with confirm_col:

                        if st.button(
                            "✅ Confirm",
                            key=f"confirm_cook_{recipe_id}"
                        ):

                            for ingredient in ingredients:

                                reduce_ingredient_quantity(
                                    ingredient[2],
                                    ingredient[3],
                                    ingredient[4]
                                )

                            st.session_state[
                                "recipe_to_cook"
                            ] = None

                            st.success(
                                "Pantry updated! 🎉"
                            )

                            st.rerun()

                    with cancel_col:

                        if st.button(
                            "❌ Cancel",
                            key=f"cancel_cook_{recipe_id}"
                        ):

                            st.session_state[
                                "recipe_to_cook"
                            ] = None

                            st.rerun()

                st.divider()

                # ==========================================
                # DELETE RECIPE
                # ==========================================

                if st.button(
                    "🗑️ Delete Recipe",
                    key=f"delete_recipe_{recipe_id}"
                ):

                    delete_recipe(recipe_id)

                    st.rerun()


# ==================================================
# GROCERIES
# ==================================================

elif page == "🛒 Groceries":

    st.title("🛒 Groceries")

    st.write(
        "Keep track of what you need to buy."
    )

    # ==================================================
    # LOW-STOCK SUGGESTIONS
    # ==================================================

    st.subheader("⚠️ Suggested from Your Pantry")

    pantry_items = get_ingredients()

    low_stock_items = []

    for ingredient in pantry_items:

        quantity = ingredient[2]
        low_stock = ingredient[5]

        if (
            low_stock > 0
            and quantity <= low_stock
        ):
            low_stock_items.append(ingredient)

    if len(low_stock_items) == 0:

        st.success(
            "Your pantry looks well stocked! 🎉"
        )

    else:

        for ingredient in low_stock_items:

            ingredient_id = ingredient[0]
            name = ingredient[1]
            quantity = ingredient[2]
            unit = ingredient[3]
            low_stock = ingredient[5]

            col1, col2 = st.columns([4, 1])

            with col1:

                st.write(f"**{name}**")

                st.caption(
                    f"Only {quantity:g} {unit} left · "
                    f"Low-stock level: {low_stock:g} {unit}"
                )

            with col2:

                if st.button(
                    "➕ Add",
                    key=f"add_low_stock_{ingredient_id}"
                ):

                    amount_to_buy = (
                        low_stock - quantity
                    )

                    if amount_to_buy <= 0:
                        amount_to_buy = low_stock

                    add_grocery_item(
                        name,
                        amount_to_buy,
                        unit
                    )

                    st.success(
                        f"{name} added!"
                    )

                    st.rerun()

            st.divider()

    # ==================================================
    # MANUALLY ADD GROCERIES
    # ==================================================

    st.subheader("➕ Add Something Else")

    with st.expander("Add Grocery Item"):

        grocery_name = st.text_input(
            "Item name",
            key="manual_grocery_name"
        )

        grocery_quantity = st.number_input(
            "Quantity",
            min_value=0.0,
            step=0.5,
            key="manual_grocery_quantity"
        )

        grocery_unit = st.selectbox(
            "Unit",
            [
                "kg",
                "g",
                "L",
                "ml",
                "pieces",
                "packets"
            ],
            key="manual_grocery_unit"
        )

        if st.button(
            "🛒 Add to Grocery List"
        ):

            if grocery_name.strip() == "":

                st.warning(
                    "Please enter an item name."
                )

            elif grocery_quantity <= 0:

                st.warning(
                    "Quantity must be greater than 0."
                )

            else:

                add_grocery_item(
                    grocery_name.strip(),
                    grocery_quantity,
                    grocery_unit
                )

                st.success(
                    f"{grocery_name} added "
                    f"to your grocery list!"
                )

                st.rerun()

    # ==================================================
    # CURRENT GROCERY LIST
    # ==================================================

    st.divider()

    st.subheader("📝 Your Grocery List")

    grocery_items = get_grocery_items()

    if len(grocery_items) == 0:

        st.info(
            "Your grocery list is empty."
        )

    else:

        for grocery in grocery_items:

            grocery_id = grocery[0]
            name = grocery[1]
            quantity = grocery[2]
            unit = grocery[3]

            col1, col2, col3 = st.columns([5, 2, 1])

            with col1:

                st.write(
                    f"🛒 **{name}**"
                )

                st.caption(
                    f"{quantity:g} {unit}"
                )

            with col2:

                if st.button(
                    "✅ Purchased",
                    key=f"purchase_grocery_{grocery_id}"
                ):

                    st.session_state[
                        "grocery_to_purchase"
                    ] = grocery_id

            with col3:

                if st.button(
                    "🗑️",
                    key=f"delete_grocery_{grocery_id}"
                ):

                    delete_grocery_item(
                        grocery_id
                    )

                    st.rerun()

            if (
                st.session_state.get(
                    "grocery_to_purchase"
                )
                == grocery_id
            ):

                st.info(
                    f"Add {quantity:g} {unit} "
                    f"of {name} to your pantry?"
                )

                confirm_col, cancel_col = st.columns(2)

                with confirm_col:

                    if st.button(
                        "✅ Yes, add to pantry",
                        key=f"confirm_purchase_{grocery_id}"
                    ):

                        purchase_grocery_item(
                            grocery_id
                        )

                        st.session_state[
                            "grocery_to_purchase"
                        ] = None

                        st.rerun()

                with cancel_col:

                    if st.button(
                        "❌ Cancel",
                        key=f"cancel_purchase_{grocery_id}"
                    ):

                        st.session_state[
                            "grocery_to_purchase"
                        ] = None

                        st.rerun()
            st.divider()