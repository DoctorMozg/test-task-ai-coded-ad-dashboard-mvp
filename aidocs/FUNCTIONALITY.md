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

```python
# Example OpenRouter.ai integration
import requests
import json
import os

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

def generate_ad_copy(campaign_info):
    """Generate ad copy based on campaign information using OpenRouter.ai"""
    
    prompt = f"""
    Create a compelling ad description for a campaign with the following details:
    - Product: {campaign_info['product']}
    - Target audience: {campaign_info['audience']}
    - Campaign goal: {campaign_info['goal']}
    
    The ad copy should be concise, engaging, and persuasive.
    """
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENROUTER_API_KEY}"
    }
    
    payload = {
        "model": "anthropic/claude-3-haiku-20240307",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    
    try:
        response = requests.post(OPENROUTER_URL, headers=headers, json=payload)
        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["message"]["content"]
        else:
            return f"Error generating ad copy: {response.status_code}"
    except Exception as e:
        return f"Error connecting to OpenRouter.ai: {str(e)}"
```

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
