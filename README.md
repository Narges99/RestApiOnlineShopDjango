
# RestAPI django online shop

Project Description: Online Shop REST API

This project is a RESTful API designed for an online shopping platform, providing a seamless and efficient way for users to manage products, categories, carts, orders, and payments. The API facilitates essential e-commerce functionalities, allowing users to register, log in, browse products, add items to their cart, place orders, and manage their payments.

Target Audience:

Customers: Individuals looking to purchase products online, who will benefit from user-friendly account management and shopping functionalities.
Administrators: Users responsible for managing product listings, categories, and monitoring orders and payments, ensuring a smooth operation of the online store.
This API is built using Django and Django Rest Framework, ensuring robust performance and scalability to accommodate growing user needs.

## API Reference


After running the project locally (localhost), you can access your APIs through the following links:

- **Swagger UI Documentation:** [http://localhost:8000/swagger/](http://localhost:8000/swagger/)
- **Redoc Documentation:** [http://localhost:8000/redoc/](http://localhost:8000/redoc/)
## Roadmap

If you log in as an admin, you can add or delete products, manage categories, and have full access to the CRUD operations for products. At the same time, you can still make purchases.

However, if you log in as a user, you will only have access to purchasing operations.

The purchasing process works as follows: 
first, you must log in and authenticate. An access token must be included in the header.

```http
  POST /accounts/login/
```
After that, you can view the list of products
```http
  GET  /products/products/
```

and add them to your cart.

```http
  POST  /carts/cart/add/
```
At any given time, you can have only one active cart.

You may also remove any unwanted items from your cart.
```http
  POST  /carts/cart/remove/
```
Once your cart is complete, you must create an order.

```http
  POST  /orders/order/create/
```

At this point, the cart will be closed, and you can open another active cart.

If you wish to proceed with payment, you can input your order number through the payment API,

```http
  POST  /payment/process/
```
and that order will be marked as paid.


Finally, you can log out.

```http
  POST  /accounts/logout/
```


## Installation

Install my-project with npm

```bash
git clone https://github.com/username/repo.git
cd repo
pip install -r requirements.txt
