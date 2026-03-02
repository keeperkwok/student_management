# Agent Guidelines for Student Management System

This document provides coding standards and development guidelines for AI agents working on this codebase.

## Project Overview

This is a student management system with:
- **Backend**: Python-based API (backend/)
- **Frontend**: Web application (frontend/)

## Build, Lint, and Test Commands

### Backend (Python)

```bash
# Setup
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Run application
python main.py
# or
python -m uvicorn main:app --reload  # For FastAPI
# or
python manage.py runserver  # For Django

# Testing
pytest                           # Run all tests
pytest tests/test_students.py    # Run single test file
pytest tests/test_students.py::test_create_student  # Run single test
pytest -v                        # Verbose output
pytest -k "student"              # Run tests matching pattern
pytest --cov                     # With coverage

# Linting and formatting
ruff check .                     # Lint with Ruff
ruff check --fix .               # Auto-fix issues
ruff format .                    # Format code
black .                          # Format with Black (alternative)
mypy .                           # Type checking
isort .                          # Sort imports

# Database migrations (if using Django)
python manage.py makemigrations
python manage.py migrate

# Database migrations (if using Alembic)
alembic revision --autogenerate -m "description"
alembic upgrade head
```

### Frontend

```bash
# Setup
cd frontend
npm install  # or: yarn install, pnpm install

# Development
npm run dev                      # Start dev server
npm run build                    # Production build
npm run preview                  # Preview build

# Testing
npm test                         # Run all tests
npm test -- StudentForm          # Run single test file/suite
npm test -- --watch              # Watch mode
npm run test:coverage            # With coverage

# Linting and formatting
npm run lint                     # Lint code
npm run lint:fix                 # Auto-fix issues
npm run format                   # Format with Prettier
npm run type-check               # TypeScript type checking
```

## Code Style Guidelines

### Python Backend

#### File Organization
```
backend/
├── main.py              # Application entry point
├── models/              # Database models
├── routes/              # API routes/endpoints
├── services/            # Business logic
├── schemas/             # Pydantic schemas/DTOs
├── utils/               # Helper functions
├── tests/               # Test files
└── requirements.txt     # Dependencies
```

#### Imports
```python
# Standard library
import os
from datetime import datetime

# Third-party packages
from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import Session

# Local application
from models.student import Student
from schemas.student import StudentCreate, StudentResponse
from services.student_service import StudentService
```

- Use absolute imports for local modules
- Group imports: standard library, third-party, local
- Sort alphabetically within groups
- Use `from x import y` for specific items

#### Naming Conventions
- **Files/Modules**: `snake_case.py` (e.g., `student_service.py`)
- **Classes**: `PascalCase` (e.g., `StudentService`, `UserModel`)
- **Functions/Methods**: `snake_case` (e.g., `get_student_by_id()`)
- **Variables**: `snake_case` (e.g., `student_name`, `total_count`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `MAX_PAGE_SIZE`, `DATABASE_URL`)
- **Private members**: `_leading_underscore` (e.g., `_internal_method()`)

#### Type Hints
Always use type hints for function parameters and return values:
```python
def get_student(student_id: int) -> Student | None:
    """Retrieve student by ID."""
    pass

def create_student(data: StudentCreate) -> Student:
    """Create new student record."""
    pass
```

#### Error Handling
```python
# Use specific exceptions
try:
    student = get_student(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
except ValueError as e:
    raise HTTPException(status_code=400, detail=str(e))
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    raise HTTPException(status_code=500, detail="Internal server error")
```

- Catch specific exceptions, not bare `except`
- Log errors with context
- Return appropriate HTTP status codes
- Provide meaningful error messages

#### Documentation
```python
def calculate_gpa(grades: list[float]) -> float:
    """Calculate GPA from list of grades.
    
    Args:
        grades: List of numerical grades (0-100)
        
    Returns:
        GPA on 4.0 scale
        
    Raises:
        ValueError: If grades are out of valid range
    """
    pass
```

### Frontend

#### File Organization
```
frontend/
├── src/
│   ├── components/      # Reusable components
│   ├── pages/           # Page components
│   ├── services/        # API services
│   ├── hooks/           # Custom React hooks
│   ├── utils/           # Helper functions
│   ├── types/           # TypeScript types
│   ├── styles/          # CSS/styling files
│   └── App.tsx          # Root component
```

#### Naming Conventions
- **Components**: `PascalCase.tsx` (e.g., `StudentForm.tsx`)
- **Hooks**: `camelCase.ts` starting with `use` (e.g., `useStudentData.ts`)
- **Utils**: `camelCase.ts` (e.g., `formatDate.ts`)
- **Constants**: `UPPER_SNAKE_CASE` or `camelCase` for configs

#### TypeScript
Always use TypeScript with strict mode:
```typescript
interface Student {
  id: number;
  name: string;
  email: string;
  enrollmentDate: Date;
}

const getStudent = async (id: number): Promise<Student> => {
  const response = await fetch(`/api/students/${id}`);
  if (!response.ok) throw new Error('Failed to fetch student');
  return response.json();
};
```

#### Error Handling
```typescript
try {
  const student = await getStudent(id);
  setStudent(student);
} catch (error) {
  console.error('Error fetching student:', error);
  setError(error instanceof Error ? error.message : 'Unknown error');
}
```

## Git Commit Guidelines

- Use imperative mood: "Add feature" not "Added feature"
- Format: `type: brief description`
- Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`
- Examples:
  - `feat: add student enrollment endpoint`
  - `fix: resolve pagination bug in student list`
  - `test: add tests for grade calculation`

## Testing Guidelines

- Write tests for all new features
- Maintain minimum 80% code coverage
- Test file naming: `test_<module>.py` or `<Component>.test.tsx`
- Use descriptive test names: `test_create_student_with_valid_data()`
- Mock external dependencies (database, APIs)
- Test edge cases and error conditions

## Database Guidelines

- Use migrations for all schema changes
- Never commit database files (SQLite, etc.)
- Use environment variables for connection strings
- Add indexes for frequently queried fields
- Use transactions for multi-step operations

## Security Best Practices

- Never commit secrets, API keys, or passwords
- Use environment variables for configuration
- Validate and sanitize all user inputs
- Use parameterized queries to prevent SQL injection
- Implement proper authentication and authorization
- Use HTTPS in production
- Set appropriate CORS policies

## Performance Guidelines

- Use pagination for large datasets
- Implement caching where appropriate
- Optimize database queries (use `select_related`, `prefetch_related`)
- Lazy load components and data
- Minimize API calls
- Use connection pooling for databases

## Code Review Checklist

Before committing:
- [ ] Code follows style guidelines
- [ ] Tests are written and passing
- [ ] No commented-out code
- [ ] No console.log or print debugging statements
- [ ] Error handling is implemented
- [ ] Documentation is updated
- [ ] No security vulnerabilities introduced
