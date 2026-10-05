AskMyShop — Business AI Agent

AskMyShop is a business-focused AI assistant that helps customers get information about a business and its products.

This is the first version (V1) of the project, built as a web-based AI assistant using Streamlit.

🚀 Live Project

Live Demo: https://askmyshop.streamlit.app/

✨ Features

🤖 Customer AI Assistant

AskMyShop answers business-related queries about:
• Products
• Pricing
• Stock availability
• GST information
• Business details
• Shipping policy
• Return policy

The AI is designed to ignore queries unrelated to the business.

🏪 Owner Panel

The owner can:
• View business information
• View products
• Search for products
• Add new products
• Update product information

🗄️ Database

Business and product information is stored in Supabase PostgreSQL.

🛠️ Tech Stack

• Python
• Streamlit
• LangChain
• Google Gemini
• Supabase
• PostgreSQL
• python-dotenv

🏗️ V1 Architecture

Customer
↓
Streamlit Customer Chat
↓
LangChain
↓
Google Gemini
↓
Business & Product Data
↓
Supabase PostgreSQL

Owner Panel

Business Owner
↓
Owner Panel
↓
Supabase
↓
Business & Product Data

📂 Project Structure

AskMyShop/
│
├── main.py
├── 1User_ui.py
├── 2Owner_ui.py
├── llm.py
├── database.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md

⚙️ Installation

1. Clone the repository

git clone YOUR_GITHUB_LINK

2. Open the project

cd AskMyShop

3. Install dependencies

pip install -r requirements.txt

4. Create .env

Create a .env file in the project folder:

GOOGLE_API_KEY=your_google_api_key
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key

5. Run the application

streamlit run main.py

🔐 Environment Variables

The application requires:

GOOGLE_API_KEY — Connects the application to Google Gemini
SUPABASE_URL — Connects the application to Supabase
SUPABASE_KEY — Authenticates the application with Supabase

Never upload your .env file or API keys to GitHub.

Add the following to .gitignore:
.env
.venv/
__pycache__/

🔮 Future Development — V2

The next version of AskMyShop will focus on WhatsApp integration.

V2 Goals

• WhatsApp integration
• AI assistant directly inside WhatsApp
• Business-specific AI assistants
• Product and inventory management
• Automatic customer responses
• Business-specific responses
• Multi-business support
• API-based architecture
• Support for multiple businesses and their customers

V2 Vision

Business
↓
AskMyShop Platform
↓
├── Business Data
├── Products
└── AI Assistant
       ↓
    WhatsApp
       ↓
   Customers

The goal of V2 is to make AskMyShop a WhatsApp-based AI assistant for businesses and their customers.

📌 Project Status

V1 — Completed ✅

• Web-based AI assistant
• Customer chat
• Owner panel
• Product management
• Supabase database
• Google Gemini
• LangChain
• Streamlit deployment

V2 — Planned 🚀

• WhatsApp integration
• Multi-business support
• API backend
• Improved AI routing
• Production-ready architecture

🎯 Project Goal

The goal of AskMyShop is to build an AI assistant that can help businesses handle customer questions about their products, pricing, availability, and business information, while avoiding unrelated conversations.

👨‍💻 Developer

Built as an AI/ML project to explore the development of business-focused AI assistants using LLMs, LangChain, databases, and web deployment.