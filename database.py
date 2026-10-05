import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)


# Get business information
def get_business():
    return supabase.table("business").select("*").execute().data


# Get all products
def get_products():
    return supabase.table("products").select("*").execute().data


# Add a product
def add_product(data):
    return supabase.table("products").insert(data).execute().data


# Update a product
def update_product(product_id, data):
    return (
        supabase
        .table("products")
        .update(data)
        .eq("id", product_id)
        .execute()
        .data
    )


# Convert database data into text for the AI
def llm_context():

    business = get_business()
    products = get_products()

    text = "BUSINESS:\n"

    for row in business:
        text += str(row) + "\n"

    text += "\nPRODUCTS:\n"

    for row in products:
        text += str(row) + "\n"

    return text