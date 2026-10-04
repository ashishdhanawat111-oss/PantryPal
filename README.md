# 🥘 PantryPal AI

### Your kitchen remembers, so you don't have to.

PantryPal AI is a smart kitchen companion that helps users track pantry ingredients, discover what they can cook, manage recipes, reduce food waste, and organize grocery shopping.

Instead of being just another recipe chatbot, PantryPal combines **AI suggestions with structured pantry data**.

> **AI suggests. User confirms. Database remembers.**

---

## 🚀 Live Demo

Try PantryPal AI here:

**https://pantrypal-drhiffdjnrxkrempz9bcak.streamlit.app/**

GitHub Repository:

**https://github.com/ashishdhanawat111-oss/PantryPal**

> PantryPal is currently an MVP deployed on Streamlit Community Cloud.  
> Its SQLite database is intended for demonstration purposes and may reset when the app restarts or redeploys.

---

## 💡 The Problem

Keeping track of a kitchen sounds simple until you have to remember:

- What ingredients are currently available?
- How much of each ingredient is left?
- What is about to expire?
- What can I cook using what I already have?
- What do I need to buy?
- How much should be removed from the pantry after cooking?

PantryPal brings all of this into one place.

---

## ✨ Features

### 📦 Smart Pantry

- Add, update, and delete pantry ingredients
- Track quantities and units
- Organize ingredients by category
- Set low-stock thresholds
- Track expiry dates
- Automatically identify ingredients that should be used soon

---

### 🤖 AI Meal Suggestions

PantryPal uses **Gemma 3** to suggest meal ideas based on:

- Ingredients currently available
- Meal type
- Number of servings
- Cooking preference
- Ingredients approaching expiry

AI recommendations are treated as suggestions rather than exact inventory operations, helping keep pantry data reliable.

---

### 🍽️ I Made Something

Already cooked something without using a saved recipe?

Simply describe what you made.

PantryPal can:

1. Ask AI to estimate which pantry ingredients were used
2. Let you review and edit the estimate
3. Validate the ingredients against your pantry
4. Update inventory only after your confirmation

This follows PantryPal's core principle:

**AI suggests → User confirms → Database remembers**

---

### 📖 My Recipes

Users can create and save their own recipes with exact ingredient quantities.

PantryPal checks whether the required ingredients are available and, after the user confirms that the recipe was cooked, automatically deducts the appropriate quantities from the pantry.

---

### ⚖️ Unit Conversion

PantryPal supports automatic conversion between:

- kg ↔ g
- L ↔ ml

This allows pantry items and recipes to use different compatible units.

For example:

```text
Pantry:
Rice — 2 kg

Recipe:
Rice — 300 g

After cooking:
Rice — 1.7 kg
```

---

### 🛒 Smart Grocery List

- Add grocery items manually
- Get suggestions from low-stock pantry items
- Track items that need to be purchased
- Mark groceries as purchased
- Automatically add purchased groceries back into the pantry

---

### ⚠️ Expiry Awareness

PantryPal identifies ingredients approaching their expiry date and can prioritize those ingredients when generating meal ideas.

This can help reduce unnecessary food waste.

---

## 🧠 How PantryPal Works

```text
                  ┌─────────────────┐
                  │      User       │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │ Streamlit UI    │
                  └────────┬────────┘
                           │
              ┌────────────┴────────────┐
              │                         │
              ▼                         ▼
     ┌─────────────────┐       ┌─────────────────┐
     │    Gemma AI     │       │  Python Logic   │
     │                 │       │                 │
     │ Meal ideas      │       │ Validation      │
     │ Interpretation  │       │ Unit conversion │
     │ Estimation      │       │ Pantry updates  │
     └─────────────────┘       └────────┬────────┘
                                       │
                                       ▼
                              ┌─────────────────┐
                              │     SQLite      │
                              │                 │
                              │ Pantry          │
                              │ Recipes         │
                              │ Groceries       │
                              └─────────────────┘
```

AI handles flexible natural-language tasks.

Python handles validation and calculations.

SQLite stores structured kitchen data.

---

## 🔄 Core Flow

```text
User adds pantry items
        ↓
PantryPal stores inventory
        ↓
AI analyzes available ingredients
        ↓
Meal ideas are suggested
        ↓
User decides what to cook
        ↓
User confirms ingredient usage
        ↓
Python validates quantities
        ↓
Pantry inventory is updated
        ↓
Low-stock and expiry status changes automatically
```

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core application logic |
| Streamlit | Web interface |
| SQLite | Pantry, recipe and grocery storage |
| Gemma 3 | Meal suggestions and ingredient estimation |
| Hugging Face Inference API | AI model access |
| python-dotenv | Local environment variable management |
| Git & GitHub | Version control and project hosting |

---

## 📁 Project Structure

```text
PantryPal/
│
├── app.py
├── ai_service.py
├── database.py
├── requirements.txt
├── README.md
├── LICENSE
└── .gitignore
```

### Main files

**app.py**  
Contains the Streamlit interface and user interaction flow.

**database.py**  
Handles SQLite operations including pantry, recipes, groceries and unit conversion.

**ai_service.py**  
Handles communication with Gemma through the Hugging Face Inference API.

---

## 🚀 Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/ashishdhanawat111-oss/PantryPal.git
cd PantryPal
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

#### Windows

```bash
venv\Scripts\activate
```

#### macOS / Linux

```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure the Hugging Face token

Create a `.env` file in the project root:

```env
HF_TOKEN=your_huggingface_token
```

You can create a Hugging Face token from your Hugging Face account settings.

> Never commit your `.env` file or API token to GitHub.

### 6. Start PantryPal

```bash
streamlit run app.py
```

The application should open in your browser.

---

## 🔐 Security

Sensitive credentials such as the Hugging Face API token are stored using environment variables and excluded from Git version control.

The following files are intentionally ignored:

```text
.env
pantry.db
venv/
__pycache__/
```

API tokens should never be committed to a public repository.

---

## 📸 Screenshots

Screenshots of PantryPal's main features can be added here.

Recommended screenshots:

- 🏠 Home Dashboard
- 📦 Pantry Inventory
- 🤖 AI Meal Suggestions
- 📖 My Recipes
- 🛒 Grocery List

---

## 🗺️ Future Roadmap

Possible future improvements include:

- 📱 Improved mobile-first experience
- 📷 Ingredient and receipt scanning
- 🏷️ Barcode scanning
- 🥗 Nutrition information
- 🎙️ Voice interaction
- 🔔 Expiry notifications
- 👥 Multi-user household support
- 🛍️ Grocery ordering integrations
- 📊 Pantry usage analytics
- 🐾 PantryPal mascot interactions

---

## 🌱 Built for Hacktoberfest 2026

PantryPal AI was built for **Hacktoberfest 2026** with a focus on combining AI with practical everyday software.

A key design decision was to avoid allowing an AI model to directly modify important inventory data.

Instead, PantryPal separates responsibilities:

**AI handles suggestions and interpretation.**

**Python handles validation and calculations.**

**SQLite remembers the kitchen.**

This creates a safer and more predictable AI-assisted workflow.

---

## 📄 License

This project is licensed under the **MIT License**.

---

## 🔗 Links

**Live App**  
https://pantrypal-drhiffdjnrxkrempz9bcak.streamlit.app/

**GitHub Repository**  
https://github.com/ashishdhanawat111-oss/PantryPal

---

Made with Python, Streamlit, SQLite and Gemma. 🥘🤖