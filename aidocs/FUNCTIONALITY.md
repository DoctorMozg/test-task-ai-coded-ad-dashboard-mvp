# Core Functionalities for Advertising Dashboard MVP

## Data Management

### Simplified Data Structure

- Campaigns with basic targeting
- Simple image banner per campaign
- Basic performance metrics
- In-memory storage with reasonable limits

### Data Export

- CSV export of campaign data
- Basic metrics export
- Local backup functionality

## Dashboard Components

### Simple Overview Dashboard

- Key performance metrics
- Campaign spend visualization
- Basic click-through rate display
- Active campaign count

### Campaign Management

- Create/edit/delete campaigns
- Set campaign budgets and date ranges
- Basic targeting parameters
- Preview campaigns before activation
- Duplicate existing campaigns

### Creative Management

- Upload and store banner images
- Preview ads before publishing
- Basic image validation

## Analytics

### Basic Performance Metrics

- Impressions and clicks tracking
- CTR calculation
- Basic budget utilization metrics
- Simple performance visualization

### Visualization Tools

- Basic charts for key metrics
- Time-series for daily performance
- Campaign comparison charts
- Custom date range selection

## User Experience

### UI Components

- Responsive Streamlit layout
- Simple dashboard widgets
- Campaign creation workflow
- Campaign list with filtering

### Simple Notification System

- Basic error messages
- Success confirmations
- Session-based notifications

## AI-Powered Features with OpenRouter.ai

### Campaign Enhancement

- Campaign name suggestions based on products and audience
- Ad copy generation for campaigns
- Simple performance insights
- Audience targeting suggestions

### Implementation Approach

OpenRouter.ai integration will be implemented with the following principles:

- OpenRouter API key and settings should be stored in a dedicated settings file
- API endpoint URLs and model selections should be configurable in the settings
- Different AI models should be selectable for different tasks (copy generation vs. insights)
- Implementation should include error handling and graceful fallbacks
- Requests should be rate-limited to prevent excessive API usage
- Results should be cached when appropriate to minimize costs
- User feedback mechanism for AI-generated content should be included
- Default prompt templates should be defined in the settings file
- Logging of API usage for monitoring purposes

This approach ensures a flexible, maintainable integration with OpenRouter.ai that can be easily configured and extended without changing code.

## Technical Architecture

### In-Memory Data Storage

- Python dictionaries and lists for data storage
- Memory limit management
- Session-based data persistence

### Simple Performance Optimization

- Basic data caching
- Efficient in-memory queries
- Streamlit's built-in caching

### Security Measures

- Password hashing for user authentication
- Input validation with Pydantic
- Session management
- Basic error handling

## Deployment Configuration

### Environment Setup

- Python 3.13 environment
- Dependencies managed with UV
- Environment variable configuration
- Simple command-line parameters

This functionality outline focuses on the essential features for an MVP, prioritizing simplicity and rapid implementation while providing a clear foundation for future enhancements.
