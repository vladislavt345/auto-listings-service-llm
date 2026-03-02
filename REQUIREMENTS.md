**Technical Specification: Car Listings Service**

Develop a system for collecting car listings with an API, admin panel, and Telegram bot.

---

## 1. Backend & Scraper

A worker periodically collects listings from **carsensor.net**. Required fields: make, model, year, price, color, link.

Upsert logic:

* Update existing records if data changes
* Insert new records if they do not exist

Basic retry logic for network errors is required.

Database: **PostgreSQL** or **MySQL**
Migrations via **Alembic**, seeding with a default administrator account.

Endpoints:

* `POST /api/login` — authentication, returns JWT
* `GET /api/cars` — protected endpoint returning the list of cars

---

## 2. Frontend (SPA)

React or Next.js, any UI library.

Routes:

* `/login` — login form, store JWT
* `/` — protected route displaying a table of cars from the API

---

## 3. Telegram Bot

Accepts free-form queries (e.g., “Find a red BMW under 2 million”).

Using Function Calling from any LLM API, extract filtering parameters, query the database, and return a readable response.

If you don’t have access to an LLM API, implement the logic — an API key will be provided.

---

## 4. Submission Requirements

* Run with a single command:
  `docker-compose up --build`
* Public repository with a `.env.example` file
* README including:

  * Setup instructions
  * Admin login/password
  * Description of architectural decisions
