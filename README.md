# Strelix Identity

**Strelix Identity** is a lightweight, open-source service for managing user and organization identities. It provides a simple API to create, update, and manage users and organizations, designed to integrate seamlessly with your existing projects.

This service is part of the **Strelix** ecosystem, designed for secure, scalable, and efficient identity management. 

---

## Features

- **User Management**: Create, read, update, and delete user profiles.
- **Organization Management**: Manage organizations and their members.
- **Secure**: PII-compliant, with security-first principles.
- **Flexible Integration**: Easily integrates with existing systems using RESTful API.
- **Caching Support**: Optimized for performance with caching capabilities.

---

## Installation

### Prerequisites
- Python 3.10+
- Django 4+
- PostgreSQL (or any django compatible database)
- Redis (for caching)

### Steps

1. **Clone the Repository**:
  ```bash
   git clone https://github.com/Strelix/Identity.git
   cd Identity
   ```
2. **Set up a Virtual Environment**:
  ```bash
  python3 -m venv venv
  source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
  ```
3. **Install Dependencies**:
  ```bash
  pip install poetry setuptools
  poetry install
  ```
4. **Configure Environment Variables**: Copy the sample environment file and update it with your settings:
  ```bash
  cp .env.example .env
  ```
  Set up your database and cache configurations in the .env file.
5. **Run Migrations**:
  ```bash
  python manage.py migrate
  ```
6. **Run the development server**
  ```bash
  python manage.py runserver
  ```
  The service should now be running at `http://localhost:8000`
