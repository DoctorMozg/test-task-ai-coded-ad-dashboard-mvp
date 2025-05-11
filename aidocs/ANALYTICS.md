# Simplified Analytics for Advertising Dashboard MVP

## Overview

This document outlines the simplified analytics approach for the Advertising Dashboard MVP using Streamlit and in-memory data storage. It focuses on essential metrics and basic visualizations that provide value without overcomplicating the initial implementation.

## Key Performance Metrics

### Basic Campaign Metrics

- **Impressions**: Total number of ad views
- **Clicks**: Total number of ad clicks
- **Click-Through Rate (CTR)**: Clicks/Impressions
- **Cost**: Total campaign spend

### Simplified Reporting

- Basic campaign performance overview
- Daily trend visualization
- Campaign comparison view

## Data Visualization

### Simple Dashboard Elements

- **Time Series Chart**: Basic performance over time
- **Bar Charts**: Simple comparison between campaigns
- **Metrics Cards**: Key performance indicators
- **Progress Bars**: Budget utilization visualization

### Minimalist Interactive Elements

- Date range selector
- Campaign selector for comparisons
- Simple filtering options

## Technical Implementation

### Data Representation

- In-memory data structures for metrics
- Simple aggregation functions
- Basic time-based grouping
- Mock data generation for testing

### Visualization Implementation

- Streamlit native charts
- Built-in Streamlit components
- Simple CSS customizations

## Mock Data Approach

### Simplified Simulation

- Basic random data generation
- Reasonable value ranges
- Time-based patterns
- Seed data for demonstrations

### Implementation

```python
# Example mock data generation
import random
from datetime import datetime, timedelta

def generate_mock_metrics(campaign_id, days=7):
    """Generate simple mock metrics for a campaign"""
    start_date = datetime.now() - timedelta(days=days)
    metrics = []

    # Base metrics that look somewhat realistic
    base_impressions = random.randint(500, 2000)
    base_ctr = random.uniform(1.0, 3.0)

    for i in range(days):
        day = start_date + timedelta(days=i)

        # Add some randomness and a slight trend
        daily_impressions = base_impressions + random.randint(-200, 200)
        daily_impressions += i * 50  # Slight upward trend

        # Calculate clicks based on a realistic CTR
        daily_ctr = base_ctr + random.uniform(-0.5, 0.5)
        daily_clicks = int(daily_impressions * daily_ctr / 100)

        metrics.append({
            "campaign_id": campaign_id,
            "date": day.date(),
            "impressions": daily_impressions,
            "clicks": daily_clicks,
            "ctr": daily_clicks / daily_impressions * 100 if daily_impressions > 0 else 0,
            "cost": daily_clicks * random.uniform(0.5, 1.5)  # Simple cost calculation
        })

    return metrics
```

## User Experience

### Simple Insights

- Basic performance summaries
- Trend indicators (up/down arrows)
- Comparison to previous periods
- Highlighting of significant changes

### Export Options

- CSV download of basic metrics
- Screenshot capability via browser

## OpenRouter.ai Integration for Advanced Insights (Optional)

For campaigns that have accumulated some data, integrate with OpenRouter.ai to:

- Generate simple performance insights
- Suggest basic optimization tips
- Provide natural language summaries of campaign performance

This simplified analytics approach provides essential insights for the MVP while keeping implementation straightforward and avoiding unnecessary complexity. As the product evolves, more sophisticated analytics features can be added based on user feedback and needs.
