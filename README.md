# Campaign Management API (FastAPI)

A local **FastAPI REST API** for managing campaigns.  
Built using **FastAPI**, **SQLAlchemy**, **Pydantic v2**, **Supabase (PostgreSQL)**, and **Pytest**.

This project is structured for clarity, scalability, and testability.

---

## 🚀 Tech Stack

- **FastAPI** – API framework
- **SQLAlchemy** – ORM
- **Pydantic v2** – data validation & serialization
- **Supabase (PostgreSQL)** – production database
- **SQLite (in-memory)** – testing database
- **Pytest** – unit & integration testing
- **Uvicorn** – ASGI server

---

## 📦 Requirements

### System Requirements
- Python **3.10+**
- Internet access (for Supabase)
- pip or virtual environment tool

### Python Dependencies
- fastapi
- uvicorn
- sqlalchemy
- pydantic (v2)
- python-dotenv
- psycopg2-binary
- pytest
- httpx

---
## How to run the project
1. cd ..\test_dalmailer\
2. Activate the virtual environment by running this command in the bash terminal: `source .venv/Scripts/activate`
3. Then, install all the requirements by running this command: `pip install -r requirements.txt`
4. To finally run the project, execute this command: `uvicorn app.main:app --reload`
5. Go to http://127.0.0.1:8000/docs. You will see the following pages with its test-dev required endpoints (i.e. creation, retrieval, and deletion of a campaign, and retrieval of the campaigns).
![alt text](image.png)

## ASSUMPTIONS and DESIGN DECISIONS

### Data Storage
I used Supabase for Production and I used an sqlite database (i.e. dalmailer.db) for development phase. I chose Supabase as I saw that you were using Supabase. In the `..\app\database.py`, there is a variable called `PRODUCTION` which is a switch to turn off and on the development mode of the whole system. If set to `TRUE`, it will use the `Supabase`, while if set to `FALSE`, it will utilize the `dalmailer.db` database.

![alt text](image-1.png)

However, in the unittest, it is using an in-memory database.

### Project Structure
I created folders according to its purpose to ensure that each directory only serves one responsibility. For examples, the `schemas` folder should only deal with `schemas` and not the `models` or any `crud` operations.

It promotes easier navigation and testing especially when there are changes without breaking everything else. It also allows me to isolate issues easily and easier to debug.

### Virtual Environment
For every project that I build, I always have a virtual environment setup so that I could ensure that the versions of the libraries being used at the time of the creation of the project are preserved. Future versions may affect the current state of the system and may affect its efficiency in the background.

Updates must be done with full knowledge of what needs to be updated or changed, so that it can also be created with a unit test if applicable, otherwise, the system would crash and we will just blindly fix things without knowing the root cause.

## For improvement
With more time, I would focus on data validation and error handling, adding a CI/CD, and probably adding more parameters on endpoints, especially on the retrieval on data. In addition, I would be hosting the API online so that it does not have to go through runnign locally in the computer.

If I still have more time, I would also focus on the documentation of the project by adding more illustrations, screenshots, descriptions, flowcharts, and etc.