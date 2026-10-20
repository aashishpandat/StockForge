# StockForge

A RESTful inventory and order management backend API built with Flask and MySQL.

StockForge provides product management, inventory adjustments, order processing, JWT authentication, and role-based access control. The project uses a layered architecture to separate request handling, business logic, database operations, and input validation.

## 🚀 Live Demo

**Live API:**  
https://stockforge-production-e334.up.railway.app/api/products

This endpoint demonstrates the deployed StockForge API and returns the available products.

## Features

- Retrieve available products
- Create products with administrator access
- Adjust inventory quantities with validation and adjustment reasons
- Place customer orders
- Retrieve orders based on user permissions
- Cancel eligible pending orders with ownership checks
- JWT-based authentication and role-based authorization
- Validate request data and handle invalid operations
- Maintain inventory consistency during order cancellation
- Automated tests for services, controllers, and validation logic
- Postman collection for API testing

## Tech Stack

- **Language:** Python
- **Framework:** Flask
- **Database:** MySQL
- **ORM:** Flask-SQLAlchemy
- **Database Driver:** PyMySQL
- **Authentication:** Flask-JWT-Extended
- **Configuration:** python-dotenv
- **Testing:** pytest
- **API Testing:** Postman

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/auth/register` | Register a customer account |
| POST | `/api/auth/login` | Authenticate a user and obtain a JWT |
| GET | `/api/products` | Retrieve products |
| POST | `/api/products` | Create a product (Admin) |
| PATCH | `/api/inventory/<product_id>/adjust` | Adjust inventory (Admin) |
| POST | `/api/orders` | Place an order |
| GET | `/api/orders` | Retrieve orders allowed for the authenticated user |
| PATCH | `/api/orders/<order_id>/cancel` | Cancel an eligible order |

Protected endpoints require a valid JWT access token. Administrative operations require the appropriate role, and order access is subject to authorization and ownership rules.

## Project Architecture

The application separates HTTP handling, business logic, database access, and validation into dedicated layers.

```text
StockForge/
├── app/
│   ├── controllers/
│   │   ├── inventory_controller.py
│   │   ├── order_controller.py
│   │   └── product_controller.py
│   ├── models/
│   │   ├── inventory_movement.py
│   │   ├── order.py
│   │   ├── order_item.py
│   │   ├── product.py
│   │   ├── user.py
│   │   └── __init__.py
│   ├── repositories/
│   │   ├── inventory_repository.py
│   │   ├── order_repository.py
│   │   └── product_repository.py
│   ├── routes/
│   │   ├── auth_routes.py
│   │   ├── inventory_routes.py
│   │   ├── order_routes.py
│   │   └── product_routes.py
│   ├── services/
│   │   ├── inventory_service.py
│   │   ├── order_service.py
│   │   ├── product_service.py
│   │   └── __init__.py
│   ├── validations/
│   │   ├── inventory_validation.py
│   │   ├── order_validation.py
│   │   ├── product_validation.py
│   │   └── __init__.py
│   ├── extensions.py
│   └── __init__.py
├── tests/
│   ├── test_inventory_service.py
│   ├── test_inventory_validation.py
│   ├── test_order_controller.py
│   ├── test_order_service.py
│   ├── test_order_validation.py
│   ├── test_product_service.py
│   ├── test_product_validation.py
│   └── __init__.py
├── .gitignore
├── create_tables.py
├── requirements.txt
├── run.py
├── StockForge_API.postman_collection.json
└── README.md
```

### Layer Responsibilities

- **Routes:** Define API endpoints and handle HTTP requests.
- **Controllers:** Coordinate request handling and responses.
- **Services:** Implement business logic for products, inventory, and orders.
- **Repositories:** Handle database queries and persistence.
- **Models:** Define database entities and relationships.
- **Validations:** Validate incoming data before processing.
- **Tests:** Verify service behavior, controller operations, and validation rules.

## Getting Started

### Prerequisites

- Python
- MySQL Server
- Git
- Postman for API testing

### 1. Clone the Repository

```bash
git clone https://github.com/aashishpandat/StockForge.git
cd StockForge
```

### 2. Create and Activate a Virtual Environment

**Windows CMD:**

```cmd
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root with the following settings:

```env
SECRET_KEY=your_secret_key
JWT_SECRET_KEY=your_jwt_secret_key

DB_USER=your_mysql_username
DB_PASSWORD=your_mysql_password
DB_HOST=localhost
DB_PORT=3306
DB_NAME=your_database_name
```

Replace the example values with your actual configuration. Keep your secret keys and database credentials private, and do not commit `.env` to a public repository.

### 5. Create the Database Tables

Create the database in MySQL first, then run:

```bash
python create_tables.py
```

This script initializes the Flask application and creates the database tables using SQLAlchemy.

### 6. Run the Application

```bash
python run.py
```

Use the local address and port configured by the application to access the API.

## Authentication

StockForge uses JWT access tokens for authenticated requests.

Register a customer account using `POST /api/auth/register`, then log in using `POST /api/auth/login` to obtain an access token.

Include the token in the `Authorization` header for protected endpoints:

```text
Authorization: Bearer <your_access_token>
```

Administrative endpoints require an account with the appropriate role.

## Example Request

An inventory adjustment request uses `PATCH /api/inventory/<product_id>/adjust`.

```json
{
  "change_quantity": 5,
  "reason": "Restocking inventory"
}
```

The adjustment quantity must be a non-zero whole number, and a reason is required. The operation is subject to authorization and inventory validation.

## Running Tests

The project includes tests for inventory services and validation, order controllers and services, and product services and validation.

Install pytest if it is not already available:

```bash
python -m pip install pytest
```

Run the tests from the project root:

```bash
python -m pytest -v
```

## API Testing with Postman

Import `StockForge_API.postman_collection.json` into Postman to test the API requests.

Test successful operations as well as invalid authentication, insufficient inventory, invalid request data, unauthorized access, order ownership restrictions, and attempts to cancel orders that are no longer pending.

## 🧪 API Testing

The API was tested using Postman for:

- User registration and login
- JWT authentication
- Product management
- Inventory adjustment
- Order placement
- Order cancellation
- Stock validation
- Role-based access control
- Error handling and validation

## Author

**Aashish Jha**

- GitHub: https://github.com/aashishpandat
- LinkedIn: https://www.linkedin.com/in/aashish-jha-62a77843b