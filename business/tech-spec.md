# Tech Spec: ERP Order Sync
=====================================

## Stack
---------------

*   **Language**: Node.js (14.x)
*   **Framework**: Express.js (4.x)
*   **Runtime**: Docker (20.x) with Alpine Linux (3.x)
*   **Database**: PostgreSQL (13.x) with TimescaleDB (2.x) for time-series data
*   **Message Queue**: RabbitMQ (3.x) for asynchronous processing

## Hosting
------------

*   **Free-tier-first**: AWS Free Tier (12 months) for development and testing
*   **Specific platforms**:
    *   Production: AWS Elastic Beanstalk (1.x) with Auto Scaling and Load Balancing
    *   Staging: DigitalOcean App Platform (1.x) with Auto Scaling and Load Balancing
    *   Development: Local Docker Compose (1.x) with Docker Desktop (4.x)

## Data Model
----------------

*   **Tables/Collections**:
    *   `orders`: stores order data from various sources and formats
        *   `id` (primary key): UUID
        `source`: string (e.g., "ERP System A")
        `format`: string (e.g., "CSV")
        `data`: JSONB (order data)
    *   `order_syncs`: stores order sync history
        *   `id` (primary key): UUID
        `order_id`: foreign key referencing `orders.id`
        `sync_status`: string (e.g., "success", "failure")
        `sync_time`: timestamp
*   **Key fields**:
    *   `id`: UUID
    *   `source`: string
    *   `format`: string

## API Surface
----------------

*   **Endpoints**:
    1.  **GET /orders**: retrieve all orders
        *   Method: GET
        *   Path: `/orders`
        *   Purpose: retrieve a list of all orders
    2.  **POST /orders**: create a new order
        *   Method: POST
        *   Path: `/orders`
        *   Purpose: create a new order from a given source and format
    3.  **GET /orders/{id}**: retrieve an order by ID
        *   Method: GET
        *   Path: `/orders/{id}`
        *   Purpose: retrieve an order by its unique ID
    4.  **PUT /orders/{id}**: update an order
        *   Method: PUT
        *   Path: `/orders/{id}`
        *   Purpose: update an existing order
    5.  **DELETE /orders/{id}**: delete an order
        *   Method: DELETE
        *   Path: `/orders/{id}`
        *   Purpose: delete an existing order
    6.  **GET /order-syncs**: retrieve all order sync history
        *   Method: GET
        *   Path: `/order-syncs`
        *   Purpose: retrieve a list of all order sync history
    7.  **POST /order-syncs**: create a new order sync
        *   Method: POST
        *   Path: `/order-syncs`
        *   Purpose: create a new order sync
    8.  **GET /order-syncs/{id}**: retrieve an order sync by ID
        *   Method: GET
        *   Path: `/order-syncs/{id}`
        *   Purpose: retrieve an order sync by its unique ID
    9.  **PUT /order-syncs/{id}**: update an order sync
        *   Method: PUT
        *   Path: `/order-syncs/{id}`
        *   Purpose: update an existing order sync
    10. **DELETE /order-syncs/{id}**: delete an order sync
        *   Method: DELETE
        *   Path: `/order-syncs/{id}`
        *   Purpose: delete an existing order sync

## Security Model
-----------------

*   **Auth**: OAuth 2.0 with JWT tokens
*   **Secrets**: stored in AWS Secrets Manager (1.x) for production and DigitalOcean App Platform (1.x) for staging
*   **IAM**: AWS IAM (1.x) for production and DigitalOcean IAM (1.x) for staging

## Observability
----------------

*   **Logs**: sent to AWS CloudWatch Logs (1.x) for production and DigitalOcean Loggly (1.x) for staging
*   **Metrics**: sent to AWS CloudWatch Metrics (1.x) for production and DigitalOcean Metrics (1.x) for staging
*   **Traces**: sent to AWS X-Ray (1.x) for production and DigitalOcean Tracing (1.x) for staging

## Build/CI
------------

*   **Build**: Docker Compose (1.x) with Docker Desktop (4.x) for development
*   **CI**: GitHub Actions (1.x) with Node.js (14.x) and Docker (20.x) for production and staging

Note: This is a high-level technical specification and may require adjustments based on specific requirements and constraints.