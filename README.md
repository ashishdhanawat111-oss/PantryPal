# 🥘 PantryPal AI

### Your kitchen remembers, so you don't have to.

PantryPal AI is a smart kitchen companion that helps users remember what is in their kitchen, discover what they can cook, manage recipes, reduce food waste, and keep their grocery list organized.

Instead of being just another recipe chatbot, PantryPal combines **AI suggestions with structured pantry data**.

> **AI suggests. User confirms. Database remembers.**

---

## 💡 The Problem

Keeping track of a kitchen sounds simple until you have to remember:

- What ingredients are available?
- How much is left?
- What is about to expire?
- What can I cook with what I already have?
- What do I need to buy?
- How much should be removed after cooking?

PantryPal brings all of this into one place.

---

## ✨ Features

### 📦 Smart Pantry

- Add, update, and delete pantry ingredients
- Track quantity and units
- Organize ingredients by category
- Set low-stock thresholds
- Track expiry dates
- Automatically identify ingredients that should be used soon

### 🤖 AI Meal Suggestions

PantryPal uses **Gemma AI** to suggest meal ideas based on:

- Ingredients currently available
- Meal type
- Number of servings
- Cooking preference
- Ingredients approaching expiry

AI recommendations are treated as suggestions rather than exact inventory operations, keeping pantry data reliable.

### 🍽️ I Made Something

Already cooked something without using a saved recipe?

Simply describe what you made.

PantryPal can:

1. Ask AI to estimate which pantry ingredients were used
2. Let you review and edit the estimate
3. Validate the ingredients against your pantry
4. Update inventory only after confirmation

This follows PantryPal's core principle:

**AI suggests → User confirms → Database remembers**

### 📖 My Recipes

Create and save your own recipes with exact ingredient quantities.

PantryPal checks whether the required ingredients are available and, after you confirm that you cooked the recipe, automatically deducts the correct quantities from your pantry.

### ⚖️ Unit Conversion

PantryPal supports automatic conversion between:

- kg ↔ g
- L ↔ ml

This allows recipes and pantry items to use different compatible units.

### 🛒 Smart Grocery List

- Add grocery items manually
- Get suggestions from low-stock pantry items
- Track items that need to be purchased
- Mark groceries as purchased
- Automatically add purchased items back into the pantry

### ⚠️ Expiry Awareness

PantryPal identifies ingredients approaching their expiry date and can prioritize them when generating meal ideas, helping reduce unnecessary food waste.

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
     │   Gemma AI      │       │ Python Logic    │
     │                 │       │                 │
     │ Meal ideas      │       │ Validation      │
     │ Estimation      │       │ Unit conversion │
     │ Suggestions     │       │ Pantry updates  │
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

AI handles flexible natural-language tasks, while Python and SQLite handle operations that require reliable quantities and persistent structured data.

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core application logic |
| Streamlit | Web interface |
| SQLite | Pantry, recipe, and grocery storage |
| Gemma 3 | AI meal suggestions and ingredient estimation |
| Hugging Face Inference API | AI model access |
| python-dotenv | Local environment variable management |

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

### 3. Activate it

Windows:

```bash
venv\Scripts\activate
```

macOS/Linux:

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

> Never commit your `.env` file or API token to GitHub.

### 6. Start PantryPal

```bash
streamlit run app.py
```

---

## 📸 Demo

Screenshots and live demo coming soon.

---

## 🔐 Security

Sensitive credentials such as the Hugging Face API token are stored using environment variables and excluded from version control.

The following files are intentionally ignored:

```text
.env
pantry.db
venv/
__pycache__/
```

---

## 🗺️ Future Roadmap

Possible future improvements include:

- 📱 Improved mobile experience
- 📷 Receipt and ingredient scanning
- 🏷️ Barcode scanning
- 🥗 Nutrition information
- 🎙️ Voice interaction
- 🔔 Expiry notifications
- 👥 Multi-user kitchens
- 🛍️ Grocery ordering integrations
- 🐾 PantryPal mascot interactions

---

## 🌱 Built for Hacktoberfest 2026

PantryPal AI was built as a Hacktoberfest 2026 project with a focus on combining AI with practical everyday software.

Rather than allowing an AI model to directly modify important user data, PantryPal separates responsibilities:

**AI handles suggestions and interpretation.  
Python handles validation and calculations.  
SQLite remembers the kitchen.**

---

## 📄 License

This project is licensed under the MIT License.

---

Made with Python, Streamlit, SQLite and Gemma. 🥘🤖