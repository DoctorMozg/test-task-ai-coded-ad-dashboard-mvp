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
   # Edit .env with your configuration including OPENROUTER_API_KEY
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

## OpenRouter.ai Integration

The application integrates with OpenRouter.ai to provide AI-powered features:

### Setting Up OpenRouter.ai

1. Create an account at [OpenRouter.ai](https://openrouter.ai/)
2. Generate an API key
3. Add the API key to your `.env` file as `OPENROUTER_API_KEY`

### AI Features

- **Campaign Name Generation**: Automatically suggests creative campaign names based on product type and target audience
- **Ad Copy Generation**: Creates compelling ad copy including headlines, descriptions, and calls-to-action

The AI uses GPT models for generation and all requests are cached to minimize API usage and costs.

## Analytics Features

The dashboard provides comprehensive analytics for campaign performance:

- **Time Range Selection**: Select specific date ranges for analysis
- **Performance Metrics**: View key metrics including impressions, clicks, CTR, and cost
- **Campaign Comparison**: Compare performance across multiple campaigns
- **Interactive Charts**: Visualize performance trends over time
- **Metric Drill-Down**: Analyze specific metrics for deeper insights

Mock analytics data is automatically generated for demonstration purposes.

## Authentication

For demo purposes, use the following credentials:

- Username: `demo`
- Password: `demo123`

## Testing

Run the test suite using pytest:

```bash
uv run pytest
```

The tests cover key functionality including:
- AI integration services with proper mocking
- Analytics data generation and processing
- Input validation and error handling

## Tech Stack

- **Frontend**: Streamlit
- **Data Visualization**: Altair
- **AI Integration**: OpenRouter.ai API (GPT models)
- **Data Storage**: In-memory with proper indexing
- **Authentication**: Streamlit session state with PBKDF2 hashing

## Development Timeline

Estimated time: 5-6 hours

## Process

1. Preparation
    1. Configure Cursor AI with project-specific development guidelines
    2. Set up linters and code quality tools to ensure consistent code standards
2. Planning
    1. Develop comprehensive implementation architecture in `aidocs`
    2. Conduct documentation review and refinement
    3. Generate project-specific Cursor rules based on architecture decisions
