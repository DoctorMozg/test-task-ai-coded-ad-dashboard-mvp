# Advertising Dashboard MVP

## Author's Note

This project was developed as a technical assessment with the following considerations:

- Streamlit was selected as the framework of choice for rapid MVP prototyping, despite having no prior experience with it. This decision allowed for leveraging AI assistance to bridge knowledge gaps while maintaining development velocity.
- An in-memory storage solution was implemented to optimize development time while still demonstrating proper data management patterns.
- Integration with OpenRouter.ai provides AI capabilities (requires a valid API key).
- Development time totaled approximately 4 hours.
- While my typical development approach involves incremental, step-by-step processes with targeted AI assistance, the scope of this task led to approximately 95% of the codebase being AI-generated.
- Campaign data is randomly generated for demonstration purposes.

## Process

1. Preparation
    1. Configure Cursor AI with project-specific development guidelines
    2. Set up linters and code quality tools to ensure consistent code standards
2. Planning
    1. Develop comprehensive implementation architecture in `aidocs`
    2. Conduct documentation review and refinement
    3. Generate project-specific Cursor rules based on architecture decisions
3. Implementation
    1. Set up project structure and dependencies
    2. Implement authentication system
    3. Create core data models using Pydantic
    4. Build campaign management interfaces
    5. Integrate OpenRouter.ai for AI-powered features
    6. Develop analytics visualization components
    7. Implement in-memory storage patterns
4. Testing
    1. Write unit tests for core functionality
    2. Perform manual testing of UI workflows
    3. Test AI integration with various inputs
    4. Validate analytics calculations
5. Refinement
    1. Improve error handling and user feedback
    2. Enhance UI/UX based on testing results
    3. Update README

## Features

- User authentication
- Campaign creation and management
- Performance analytics with visualizations
- AI assistance for campaign naming and ad copy generation
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
