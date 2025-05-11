# Advertising Dashboard MVP

A streamlined Advertising Campaign management system built with Streamlit. This MVP allows for campaign creation, management, analytics visualization, and includes AI-powered features for campaign naming and ad copy generation.

## Features

- User authentication with secure password management
- Campaign creation and management
- Performance analytics with visualizations
- AI assistance for campaign naming and copy generation
- In-memory data storage with efficient patterns

## Development Setup

### Requirements

- Python 3.13
- UV package manager

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/advertising-dashboard.git
   cd advertising-dashboard
   ```

2. Create and activate a virtual environment:

   ```bash
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   uv pip install -e .
   ```

4. Setup environment variables:

   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

### Running the Application

```bash
python run.py
```

The application will be available at <http://localhost:8501>

## Project Structure

The project follows a clean architecture pattern with clear separation of concerns:

- `dashboard/app`: Streamlit UI and pages
- `dashboard/data`: Data models and storage
- `dashboard/services`: Business logic and external services
- `dashboard/assets`: Static assets and mock data

## Authentication

For demo purposes, use the following credentials:

- Username: `demo`
- Password: `demo123`

## Tech Stack

Using Streamlit for rapid development.

## Development Timeline

Estimated time: 3-4 hours

## Process

1. Preparation
    1. Configure Cursor AI with project-specific development guidelines
    2. Set up linters and code quality tools to ensure consistent code standards
2. Planning
    1. Develop comprehensive implementation architecture in `aidocs`
    2. Conduct documentation review and refinement
    3. Generate project-specific Cursor rules based on architecture decisions
