from typing import TypedDict

import streamlit as st

from dashboard.data.models import AgeRangeSchema, InterestSchema, LocationSchema
from dashboard.data.store import interest_store

# Constants
DEFAULT_MIN_AGE = 18
DEFAULT_MAX_AGE = 65
MIN_AGE_LIMIT = 13
MAX_AGE_LIMIT = 100

# Country codes
COUNTRY_OPTIONS = ["US", "CA", "UK", "AU", "DE", "FR", "JP", "IN"]

# Category names
CATEGORY_OTHER = "Other"

# Default number of locations
DEFAULT_NUM_LOCATIONS = 1

# Interest categories for sample data
CATEGORY_TECH = "Tech"
CATEGORY_LIFESTYLE = "Lifestyle"
CATEGORY_ACTIVITIES = "Activities"
CATEGORY_ENTERTAINMENT = "Entertainment"
CATEGORY_BUSINESS = "Business"
CATEGORY_WELLNESS = "Wellness"


class TargetingData(TypedDict):
    age_range: AgeRangeSchema
    locations: list[LocationSchema]
    interests: list[str]


def age_range_selector(key_prefix: str = "") -> AgeRangeSchema:
    st.subheader("Age Targeting")

    col1, col2 = st.columns(2)
    with col1:
        min_age = st.number_input(
            "Minimum Age",
            min_value=MIN_AGE_LIMIT,
            max_value=MAX_AGE_LIMIT,
            value=DEFAULT_MIN_AGE,
            step=1,
            key=f"{key_prefix}min_age",
        )

    with col2:
        max_age = st.number_input(
            "Maximum Age",
            min_value=MIN_AGE_LIMIT,
            max_value=MAX_AGE_LIMIT,
            value=DEFAULT_MAX_AGE,
            step=1,
            key=f"{key_prefix}max_age",
        )

    # Validate min_age <= max_age
    if min_age > max_age:
        st.warning(
            "Minimum age cannot be greater than maximum age. Adjusting maximum age.",
        )
        max_age = min_age

    return AgeRangeSchema(min_age=min_age, max_age=max_age)


def location_selector(key_prefix: str = "") -> list[LocationSchema]:
    st.subheader("Location Targeting")

    locations: list[LocationSchema] = []

    # Start with one location row
    num_locations: int = st.session_state.get(
        f"{key_prefix}num_locations",
        DEFAULT_NUM_LOCATIONS,
    )

    for i in range(num_locations):
        col1, col2, col3 = st.columns([2, 2, 1])

        with col1:
            country = st.selectbox(
                "Country",
                options=COUNTRY_OPTIONS,
                key=f"{key_prefix}country_{i}",
            )

        with col2:
            region = st.text_input(
                "Region/State (optional)",
                key=f"{key_prefix}region_{i}",
            )

        with col3:
            city = st.text_input(
                "City (optional)",
                key=f"{key_prefix}city_{i}",
            )

        locations.append(
            LocationSchema(
                country=country,
                region=region if region else None,
                city=city if city else None,
            ),
        )

    # Add button to add more locations
    if st.button("Add Another Location"):
        st.session_state[f"{key_prefix}num_locations"] = num_locations + 1
        st.rerun()

    return locations


def interest_selector(key_prefix: str = "") -> list[str]:
    st.subheader("Interest Targeting")

    # Get available interests from store
    available_interests = interest_store.list()

    # If no interests exist yet, create some sample ones
    if not available_interests:
        sample_interests: list[InterestSchema] = [
            InterestSchema(name="Technology", category=CATEGORY_TECH),  # type: ignore
            InterestSchema(name="Fashion", category=CATEGORY_LIFESTYLE),  # type: ignore
            InterestSchema(name="Sports", category=CATEGORY_ACTIVITIES),  # type: ignore
            InterestSchema(name="Travel", category=CATEGORY_LIFESTYLE),  # type: ignore
            InterestSchema(name="Gaming", category=CATEGORY_ENTERTAINMENT),  # type: ignore
            InterestSchema(name="Finance", category=CATEGORY_BUSINESS),  # type: ignore
            InterestSchema(name="Food", category=CATEGORY_LIFESTYLE),  # type: ignore
            InterestSchema(name="Health", category=CATEGORY_WELLNESS),  # type: ignore
        ]

        for interest in sample_interests:
            interest_store.add(interest)

        available_interests = interest_store.list()

    # Group interests by category
    interests_by_category: dict[str, list[InterestSchema]] = {}
    for interest in available_interests:
        category = interest.category or CATEGORY_OTHER
        if category not in interests_by_category:
            interests_by_category[category] = []
        interests_by_category[category].append(interest)

    selected_interests: list[str] = []

    # Display interests by category
    for category, interests in interests_by_category.items():
        st.markdown(f"**{category}**")

        # Create a multiselect for each category
        interest_names: list[str] = [interest.name for interest in interests]
        interest_ids: list[str] = [interest.id for interest in interests]

        selected_names = st.multiselect(
            "Select interests",
            options=interest_names,
            key=f"{key_prefix}interests_{category}",
            label_visibility="collapsed",
        )

        # Map selected names back to IDs
        for name in selected_names:
            idx = interest_names.index(name)
            selected_interests.append(interest_ids[idx])

    return selected_interests


def targeting_selector(key_prefix: str = "") -> TargetingData:
    with st.expander("Audience Targeting", expanded=True):
        age_range = age_range_selector(key_prefix)
        st.markdown("---")

        locations = location_selector(key_prefix)
        st.markdown("---")

        interests = interest_selector(key_prefix)

        return {
            "age_range": age_range,
            "locations": locations,
            "interests": interests,
        }
