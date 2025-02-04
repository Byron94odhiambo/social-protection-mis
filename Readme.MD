# Social Protection Program MIS API

A Management Information System (MIS) API for tracking social protection program beneficiaries. This system manages program information, beneficiary households, and geographic locations with secure data handling features.

## System Architecture

### Overview
The system follows a layered architecture pattern with the following components:

```
┌─────────────────┐
│    API Layer    │
│  (FastAPI App)  │
├─────────────────┤
│  Service Layer  │
│(Business Logic) │
├─────────────────┤
│    Data Layer   │
│   (SQLAlchemy)  │
├─────────────────┤
│    Database     │
│   (PostgreSQL)  │
└─────────────────┘
```

### Key Components

1. **API Layer**
   - FastAPI framework for RESTful endpoints
   - Pydantic models for request/response validation
   - Swagger UI for API documentation and testing

2. **Service Layer**
   - Business logic implementation
   - Data encryption/decryption services
   - Input validation and error handling

3. **Data Layer**
   - SQLAlchemy ORM for database operations
   - Async database operations support
   - Model relationships and constraints

4. **Database**
   - PostgreSQL for data persistence
   - Encrypted storage for sensitive data
   - Proper indexing and constraints

## Database Schema

### Entity Relationship Diagram
```
Program ─┐
         ├── Household ──── HouseholdMember
SubLocation ┘
     ▲
Location
     ▲
SubCounty
     ▲
County
```

### Tables
1. **programs**
   - id (PK)
   - name
   - description
   - created_at

2. **counties**
   - id (PK)
   - name

3. **sub_counties**
   - id (PK)
   - name
   - county_id (FK)

4. **locations**
   - id (PK)
   - name
   - sub_county_id (FK)

5. **sub_locations**
   - id (PK)
   - name
   - location_id (FK)

6. **households**
   - id (PK)
   - program_id (FK)
   - sub_location_id (FK)
   - head_name
   - encrypted_phone
   - national_id (Unique)
   - created_at

7. **household_members**
   - id (PK)
   - household_id (FK)
   - name
   - age
   - gender
   - relationship

## API Endpoints

### Programs
```
GET /api/v1/programs/
- List all programs
- Response: List[ProgramResponse]

POST /api/v1/programs/
- Create new program
- Request: ProgramCreate
- Response: ProgramResponse
```

### Households
```
POST /api/v1/households/
- Create new household
- Request: HouseholdCreate
- Response: HouseholdResponse

GET /api/v1/households/{household_id}
- Get household details with members
- Response: HouseholdResponse

POST /api/v1/households/{household_id}/members/
- Add member to household
- Request: HouseholdMemberCreate
- Response: HouseholdMemberResponse
```

## Security Features

1. **Phone Number Encryption**
   - Uses Fernet symmetric encryption
   - Encrypted storage in database
   - Automatic decryption in API responses

2. **Data Validation**
   - Input validation using Pydantic models
   - Proper error handling and messages
   - SQL injection prevention through ORM

## Setup and Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/social-protection-mis.git
cd social-protection-mis
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up PostgreSQL database:
```bash
sudo -u postgres psql -c "CREATE DATABASE social_protection_db;"
sudo -u postgres psql -c "CREATE USER social_protection WITH PASSWORD 'social_protection_password';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE social_protection_db TO social_protection;"
```

5. Configure environment variables:
```bash
echo "DATABASE_URL=postgresql+asyncpg://social_protection:social_protection_password@localhost/social_protection_db" > .env
```

6. Initialize database with sample data:
```bash
PYTHONPATH=$PYTHONPATH:. python app/db/sample_data.py
```

7. Run the application:
```bash
uvicorn main:app --reload
```

8. Access the API documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Structure
```
social_protection_mis/
├── alembic/                  # Database migrations
├── app/
│   ├── api/                  # API endpoints
│   │   ├── v1/
│   │   │   ├── endpoints/    # Route handlers
│   │   │   └── router.py     # API router
│   │   └── deps.py          # Dependencies
│   ├── core/                 # Core functionality
│   │   ├── config.py        # Configuration
│   │   └── security.py      # Security utilities
│   ├── models/              # SQLAlchemy models
│   └── schemas/             # Pydantic schemas
├── tests/                    # Test cases
├── .env                      # Environment variables
├── .gitignore
├── requirements.txt          # Dependencies
└── main.py                   # Application entry point
```

## Testing

To run the tests:
```bash
pytest
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.