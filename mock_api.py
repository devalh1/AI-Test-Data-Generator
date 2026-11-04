
from fastapi import FastAPI, HTTPException
import re

app = FastAPI(title="Test Data Generator Demo API")


@app.get("/")
def home():
    return {"message": "Demo API is running"}


@app.post("/products", status_code=201)
def create_product(data: dict):
    # Required fields
    if "name" not in data or "price" not in data:
        raise HTTPException(422, "Missing required field")

    # Validate name
    if not isinstance(data["name"], str):
        raise HTTPException(422, "Name must be a string")

    # Validate price (booleans are not accepted as numbers)
    price = data["price"]
    if isinstance(price, bool) or not isinstance(price, (int, float)):
        raise HTTPException(422, "Price must be a number")

    return {
        "message": "Product created",
        "product": data
    }


@app.post("/users", status_code=201)
def create_user(data: dict):
    # Required fields
    if "username" not in data or "email" not in data:
        raise HTTPException(422, "Missing required field")

    username = data["username"]
    email = data["email"]

    # Validate username
    if not isinstance(username, str) or not 3 <= len(username) <= 20:
        raise HTTPException(422, "Username must contain 3-20 characters")

    # Validate optional age
    if "age" in data:
        age = data["age"]

        if (
            isinstance(age, bool)
            or not isinstance(age, int)
            or not 18 <= age <= 100
        ):
            raise HTTPException(422, "Age must be an integer from 18 to 100")

    # Simple email format check for this demo
    if not isinstance(email, str) or not re.fullmatch(
        r"[^@\s]+@[^@\s]+\.[^@\s]+", email
    ):
        raise HTTPException(422, "Invalid email format")
    
    # Validate tags array
    if "tags" in data:
        tags = data["tags"]

        if not isinstance(tags, list):
            raise HTTPException(
                status_code=422,
                detail="Tags must be an array"
            )

        if not 1 <= len(tags) <= 3:
            raise HTTPException(
                status_code=422,
                detail="Tags must contain between 1 and 3 items"
            )

        if not all(isinstance(tag, str) for tag in tags):
            raise HTTPException(
                status_code=422,
                detail="Every tag must be a string"
            )

    # Validate role enum
    if "role" in data:
        allowed_roles = ["admin", "user", "guest"]

        if data["role"] not in allowed_roles:
            raise HTTPException(
                status_code=422,
                detail="Role must be admin, user, or guest"
            )
    
    # Validate full_name when provided
    if "full_name" in data:
        full_name = data["full_name"]

        if not isinstance(full_name, str):
            raise HTTPException(
                status_code=422,
                detail="Full name must be a string"
            )

        if not 3 <= len(full_name) <= 60:
            raise HTTPException(
                status_code=422,
                detail="Full name must contain 3-60 characters"
            )

    return {
        "message": "User created",
        "user": data
    }
