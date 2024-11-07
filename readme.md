# Supermarket Checkout System using Django Rest Framework

This project is a REST API for a Supermarket Checkout System built with Django and Django REST Framework. The API allows users to scan items, calculate totals, and apply special pricing rules.

## Features
- **Item Scanning**: Add items to the checkout cart by SKU.
- **Total Calculation**: Calculate the total price based on scanned items, including special pricing rules (e.g., "buy n items for a discounted price").
- **Flexible Pricing Rules**: Allows dynamic changes to pricing rules without modifying code.
- **Clean Code & SOLID Principles**: The code follows Clean Code and SOLID principles, ensuring maintainability and testability.
- **Unit Tests**: High test coverage using `pytest`.

## Requirements(should be installed in local):

- Python 3.8+
- pip
- virtualenv

## Getting Started

Follow these steps to set up and run the project.

## Setup

1. Clone the repository:
   ```
    git clone https://github.com/anirbanchakraborty123/Supermarket-checkout-system.git
    cd checkout_management
   ```

2. Create a virtual environment:
   ```
   - virtualenv venv
   ```

3. Activate the virtual environment:
   - On Windows:
      ```
       venv\Scripts\activate
      ```
  
   - On macOS and Linux:
     ```
       source venv/bin/activate
     ```
  
4. Install dependencies:
```
   - pip install -r requirements.txt
```

5. Apply migrations:
```
   - python manage.py makemigrations
   - python manage.py migrate
```

6. Create Superuser (for accessing Django Admin):
```
   - python manage.py createsuperuser
```

7. Start the development server:
```
   - python manage.py runserver
```

8. Running Tests- To run the tests, use PyTest:
    ```bash
    pytest --cov=. --ds=checkout_management.settings

    The --cov flag generates a coverage report, and --ds specifies the Django settings module for pytest.
    ```
---

## Available API Endpoints

### Checkout API

The following endpoints are available for the checkout process:

1. **Scan Item**

   - **URL**: `supermarket/checkout/scan/`
   - **Method**: `POST`
   - **Description**: Adds an item to the checkout cart based on SKU.
   - **Payload**:
     ```json
     {
       "sku": "A"
     }
     ```
   - **Responses**:
     - **200 OK**: Item scanned successfully.
       ```json
       {
         "message": "Item A scanned"
       }
       ```
     - **400 Bad Request**: Item with SKU does not exist.
       ```json
       {
         "sku": ["Item with this SKU does not exist."]
       }
       ```

2. **Get Total Price**

   - **URL**: `supermarket/checkout/total/`
   - **Method**: `GET`
   - **Description**: Returns the total price of all scanned items, including any special discounts or pricing rules.
   - **Response**:
     ```json
     {
       "total": 130.00
     }
     ```
---

## Notes
- Currently, state is managed in-memory for each checkout session. For production, we can consider persisting session data in a database or we can use Django’s session framework for scalability.
- The project uses SQLite by default. For production, we can configure a more robust database like PostgreSQL.