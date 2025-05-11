# UI Implementation for Advertising Dashboard MVP

## Overview

This document outlines the simplified user interface implementation for the Advertising Dashboard MVP using Streamlit. It describes the essential layout, components, and user experience design focused on core MVP functionality.

## UI Structure

### Minimalist Application Layout

1. **Sidebar**
   - User authentication status
   - Main navigation links
   - Basic filtering options

2. **Main Content Area**
   - Dashboard view
   - Campaign creation form
   - Campaign list view

3. **Header**
   - Application title/logo
   - Help button

## Key UI Components

### Authentication Screens

- Simple login form
- Basic registration form
- Password reset functionality

### Dashboard Elements

- Performance metric cards
- Campaign status counters
- Simple bar chart for clicks
- Line chart for daily performance

### Campaign Management

- Step-by-step campaign creation form
- Image upload with preview
- Basic audience targeting selectors
- Budget input
- Date range picker

### Campaign List

- Sortable campaign table
- Status indicators
- Edit and delete buttons
- Basic filter options

## Technical Implementation

### Streamlit Components

- Using st.sidebar for navigation
- st.form for data input
- st.columns for layout organization
- Session state for maintaining UI state
- st.file_uploader for image uploads

### UI State Management

- Session state for authentication
- Form validation state
- View switching logic
- Selected campaign tracking

### Performance Considerations

- Limit visible data in tables
- Use pagination for longer lists
- Optimize image handling
- Cache frequently accessed data

## OpenRouter.ai UI Integration

- AI suggestion buttons in campaign creation
- Generated ad copy display
- Performance insight cards
- Simple feedback mechanism for AI suggestions

```python
# Example of OpenRouter.ai UI integration in Streamlit
def display_ai_suggestions(campaign_info):
    if st.button("Get AI Campaign Name Suggestions"):
        with st.spinner("Generating campaign name ideas..."):
            suggestions = get_campaign_suggestions(
                campaign_info["product"],
                campaign_info["audience"]
            )

        st.success("AI suggestions generated!")

        # Display suggestions in a clean UI
        for i, suggestion in enumerate(suggestions, 1):
            col1, col2 = st.columns([4, 1])
            with col1:
                st.write(f"**Suggestion {i}:** {suggestion}")
            with col2:
                if st.button("Use this", key=f"use_suggestion_{i}"):
                    st.session_state.campaign_name = suggestion
                    st.experimental_rerun()
```

## Mockups and Examples

For the MVP, simple mockups include:

1. **Login Screen**
   - Username/password inputs
   - Login button
   - Registration link

2. **Dashboard**
   - 3-4 metric cards (Campaigns, Impressions, Clicks, CTR)
   - Campaign status summary
   - Quick action buttons

3. **Campaign Form**
   - Name input
   - Date range selector
   - Budget input
   - Basic targeting options
   - Banner upload

4. **Campaign List**
   - Tabular view with key information
   - Status badges
   - Action buttons

## Responsive Considerations

- Mobile-friendly layout using Streamlit's responsive design
- Simplified views on smaller screens
- Touch-friendly inputs

This UI implementation provides a clean, focused interface for the Advertising Dashboard MVP while leveraging Streamlit's capabilities for rapid development. The simplified approach prioritizes core functionality while maintaining a good user experience.
