# Advertising Dashboard MVP - Project Structure

```
advertising_dashboard/
│
├── .gitignore
├── README.md
├── run.sh                     # Main entry point
│
├── dashboard/                 # Main package containing all application code
│   ├── __init__.py
│   ├── settings.py                # Project settings
│   │
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py            # Main Streamlit app with page routing
│   │   │
│   │   ├── pages/             # Streamlit multipage app structure
│   │   │   ├── __init__.py
│   │   │   ├── login.py     # Login/registration page
│   │   │   ├── dashboard.py # Main dashboard overview
│   │   │   ├── create_campaign.py # Campaign creation page
│   │   │   └── campaign_list.py # List of campaigns page
│   │   │
│   │   ├── components/        # Reusable UI components
│   │   │   ├── __init__.py
│   │   │   ├── auth_forms.py  # Login and registration forms
│   │   │   ├── campaign_card.py # Campaign display component
│   │   │   ├── targeting_selector.py # Audience targeting UI
│   │   │   └── image_uploader.py # Banner upload component
│   │   │
│   │   └── utils/            # Utility functions
│   │       ├── __init__.py
│   │       ├── auth.py       # Authentication functions
│   │       ├── session.py    # Session state management
│   │       └── image_processing.py # Image handling utilities
│   │
│   ├── data/                 # Data storage
│   │   ├── __init__.py
│   │   ├── store/            # In-memory data storage
│   │   │   ├── __init__.py
│   │   │   ├── memory_store.py # In-memory data management
│   │   │   ├── user_store.py # User data access
│   │   │   └── campaign_store.py # Campaign data access
│   │   │
│   │   └── models/           # Pydantic models
│   │       ├── __init__.py
│   │       ├── user.py       # User models
│   │       ├── campaign.py   # Campaign models
│   │       └── targeting.py  # Audience targeting models
│   │
│   ├── services/             # Business logic services
│   │   ├── __init__.py
│   │   ├── auth_service.py   # Authentication service
│   │   ├── campaign_service.py # Campaign management service
│   │   └── ai_service.py     # OpenRouter.ai powered features
│   │
│   └── assets/               # Static assets
│       ├── images/           # Default images and icons
│       └── mock_data/        # Mock data for interests, locations
│
└── pyproject.toml            # Project dependencies using UV
```

## Key Files and Their Contents

### Models (Pydantic Schemas)

**dashboard/data/models/user.py**

- `UserSchema`: User data validation model
- `UserLoginSchema`: Login form validation model
- `UserRegistrationSchema`: Registration form validation model

**dashboard/data/models/campaign.py**

- `CampaignSchema`: Campaign data validation model
- `CampaignStatusEnum`: Status enumeration (draft, active, paused, etc.)
- `AdBannerSchema`: Ad banner data validation model
- `CampaignListItemSchema`: Simplified campaign model for list display

**dashboard/data/models/targeting.py**

- `AgeRangeSchema`: Age range targeting model
- `LocationSchema`: Location targeting model
- `InterestSchema`: Interest targeting model
- `AudienceTargetingSchema`: Combined targeting model

### In-Memory Data Store

**dashboard/data/store/memory_store.py**

- Base in-memory storage mechanisms
- Data structure initialization
- Memory consumption management

**dashboard/data/store/user_store.py**

- In-memory storage for user data
- Authentication data access

**dashboard/data/store/campaign_store.py**

- In-memory storage for campaigns
- Query methods for campaign lists and filters

### Services

**dashboard/services/auth_service.py**

- User registration logic
- User authentication logic
- Password hashing and verification
- Session management

**dashboard/services/campaign_service.py**

- Campaign creation
- Campaign status management
- Campaign querying and filtering
- Image upload handling

**dashboard/services/ai_service.py**

- OpenRouter.ai API integration
- Ad copy generation
- Campaign performance suggestions

### Streamlit UI

**dashboard/app/main.py**

- Streamlit app initialization
- Authentication state management
- Page routing logic

**dashboard/app/pages/1_login.py**

- Login UI
- Registration UI
- Authentication forms

**dashboard/app/pages/2_dashboard.py**

- Main dashboard view
- Summary statistics
- Quick actions

**dashboard/app/pages/3_create_campaign.py**

- Campaign creation form
- Image upload interface
- Targeting selection UI
- Preview and submission

**dashboard/app/pages/4_campaign_list.py**

- Campaign listing with filters
- Status updates
- Detail view

### Root Files

**run.py**

- Application entry point
- Environment setup
- Command-line parameters

**pyproject.toml**

- Project dependencies managed with UV
- Development dependencies

This simplified structure provides a clean separation of concerns while focusing on MVP features with in-memory storage.
