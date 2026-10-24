
from decimal import Decimal, InvalidOperation


class ProductValidation:

    @staticmethod
    def validate_product(data):
        if not isinstance(data, dict):
            return None, "JSON object is required"

        name = data.get("name")
        description = data.get("description", "")
        price = data.get("price")
        stock_quantity = data.get("stock_quantity", 0)

        if not isinstance(name, str) or not name.strip() or len(name.strip()) > 120:
            return None, "A valid product name is required"

        if not isinstance(description, str):
            return None, "Description must be text"

        if len(description) > 5000:
            return None, "Description is too long"

        if isinstance(price, bool) or not isinstance(price, (str, int, float)):
            return None, "A valid price is required"

        try:
            price = Decimal(str(price))
        except (InvalidOperation, ValueError):
            return None, "A valid price is required"

        if not price.is_finite() or price <= 0 or price > Decimal("99999999.99"):
            return None, "Price must be positive and within the allowed range"

        if isinstance(stock_quantity, bool) or not isinstance(stock_quantity, int):
            return None, "Stock quantity must be a whole number"

        if stock_quantity < 0 or stock_quantity > 1000000000:
            return None, "Stock quantity is out of range"

        return {
            "name": name.strip(),
            "description": description.strip(),
            "price": price,
            "stock_quantity": stock_quantity
        }, None


    @staticmethod
    def validate_product_update(data):
        """Validate editable product fields without allowing stock edits here."""
        if not isinstance(data, dict):
            return None, "JSON object is required"

        allowed_fields = {"name", "description", "price"}
        if not data:
            return None, "At least one editable field is required"
        unknown_fields = set(data) - allowed_fields
        if unknown_fields:
            return None, "Only name, description and price can be updated here"

        validated = {}
        if "name" in data:
            name = data["name"]
            if not isinstance(name, str) or not name.strip() or len(name.strip()) > 120:
                return None, "A valid product name is required"
            validated["name"] = name.strip()

        if "description" in data:
            description = data["description"]
            if not isinstance(description, str):
                return None, "Description must be text"
            if len(description) > 5000:
                return None, "Description is too long"
            validated["description"] = description.strip()

        if "price" in data:
            price = data["price"]
            if isinstance(price, bool) or not isinstance(price, (str, int, float)):
                return None, "A valid price is required"
            try:
                price = Decimal(str(price))
            except (InvalidOperation, ValueError):
                return None, "A valid price is required"
            if not price.is_finite() or price <= 0 or price > Decimal("99999999.99"):
                return None, "Price must be positive and within the allowed range"
            validated["price"] = price

        return validated, None
