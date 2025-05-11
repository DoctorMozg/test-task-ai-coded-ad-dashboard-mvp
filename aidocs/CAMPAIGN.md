# Campaign Management Implementation for MVP

## Overview

This document outlines the campaign management implementation for the Advertising Dashboard MVP using Streamlit and in-memory storage. It describes the simplified data model, core functionality, and user workflows for creating and managing advertising campaigns.

## Campaign Structure

### Simplified Organization

1. **Campaign Level**
   - Overall budget allocation
   - Date range constraints
   - Target audience (demographic, geographic)
   - Creative assets (single banner image)
   - Performance metrics

## Core Functionality

### Campaign Creation

- Simple step-by-step interface
- Campaign naming and description
- Date range selection (start/end dates)
- Budget allocation
- Audience targeting:
  - Age range selection
  - Geographic targeting
  - Interest category selection
- Banner image upload
- Preview and submission

### Campaign Management

- Campaign listing with basic filtering
- Status indicators (active, paused, completed)
- Edit functionality
- Pause/resume campaigns

### Creative Management

- Single image upload per campaign
- Image preview
- Basic format validation

## Technical Implementation

### In-Memory Data Storage

- Campaign data stored in Python dictionaries
- Nested dictionaries for related data
- In-memory filtering for queries
- Custom sorting for listing views

### File Storage

- Local image storage for MVP
- Basic file management
- File naming based on campaign ID
- Memory-efficient image handling

### Business Logic

- Budget allocation validation
- Date range validation
- Targeting parameter validation
- Status management based on dates

## Workflows

### Campaign Creation Flow

1. User initiates new campaign
2. Basic campaign details entered (name, dates, budget)
3. Target audience defined
4. Banner image uploaded
5. Review and submission
6. Confirmation

### Campaign Editing Flow

1. Select campaign from list
2. Modify relevant parameters
3. Save changes
4. View updated campaign

### Campaign Monitoring Flow

1. View campaign dashboard
2. Check key performance indicators
3. Make status changes as needed

## Mock Data Generation

- Sample campaign templates
- Randomized performance metrics
- Example targeting configurations

## OpenRouter.ai Integration

The MVP includes basic AI-powered features using OpenRouter.ai:

- Suggest campaign names based on targeting
- Generate simple ad descriptions
- Provide basic performance insights

```python
# Example OpenRouter.ai integration for campaign suggestions
import requests
import json

def get_campaign_suggestions(product_type, target_audience):
    """Generate campaign name suggestions using OpenRouter.ai"""

    prompt = f"""
    Generate 3 creative campaign name ideas for a {product_type} advertisement
    targeting {target_audience}. Response should be a JSON array of strings.
    """

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENROUTER_API_KEY}"
    }

    payload = {
        "model": "anthropic/claude-3-haiku-20240307",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "response_format": {"type": "json_object"}
    }

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=payload
    )

    if response.status_code == 200:
        result = response.json()
        return json.loads(result["choices"][0]["message"]["content"])["campaign_names"]
    else:
        return ["Campaign Idea 1", "Campaign Idea 2", "Campaign Idea 3"]
```

This simplified campaign management implementation provides essential functionality for creating and managing advertising campaigns in the MVP, focusing on ease of use and quick implementation while setting the foundation for future enhancements.
