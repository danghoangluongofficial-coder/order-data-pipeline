Inventory Order API (Work in Progress)
Overview

This is a FastAPI project that simulates a warehouse order system.

Users can:

view products
create orders
update stock automatically
Current Features
FastAPI endpoints (GET /products, POST /create-orders)
MySQL database integration
Order creation with stock validation
Known Limitation

Currently, each SKU creates a separate order_id.

This does not reflect real-world systems where:

one order contains multiple items
Next Improvement

Refactor database design into:

orders (order header)
order_items (order lines)
Tech Stack
Python
FastAPI
MySQL
