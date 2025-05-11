import random
from datetime import UTC, datetime, timedelta
from pathlib import Path

from dashboard.data.models import (
    AdBannerSchema,
    AgeRangeSchema,
    AudienceTargetingSchema,
    CampaignSchema,
    CampaignStatusEnum,
    InterestSchema,
    LocationSchema,
)
from dashboard.data.store import (
    banner_store,
    campaign_store,
    interest_store,
    targeting_store,
)

# Interest categories
CATEGORY_TECH = "Tech"
CATEGORY_LIFESTYLE = "Lifestyle"
CATEGORY_SPORTS = "Sports"
CATEGORY_TRAVEL = "Travel"

# Sample interest names
INTEREST_TECHNOLOGY = "Technology"
INTEREST_SOFTWARE = "Software Development"
INTEREST_MOBILE = "Mobile Devices"
INTEREST_CLOUD = "Cloud Computing"
INTEREST_FASHION = "Fashion"
INTEREST_HOME = "Home Decor"
INTEREST_BEAUTY = "Beauty"
INTEREST_CUISINE = "Cuisine"
INTEREST_SOCCER = "Soccer"
INTEREST_BASKETBALL = "Basketball"
INTEREST_TENNIS = "Tennis"
INTEREST_CYCLING = "Cycling"
INTEREST_EUROPE = "European Travel"
INTEREST_BEACH = "Beach Destinations"
INTEREST_ADVENTURE = "Adventure Tourism"
INTEREST_CITY = "City Breaks"

# Location data
COUNTRY_US = "US"
REGION_CALIFORNIA = "California"
REGION_NEW_YORK = "New York"
CITY_SAN_FRANCISCO = "San Francisco"
CITY_NEW_YORK = "New York City"

# Age range defaults
DEFAULT_MIN_AGE = 18
DEFAULT_MAX_AGE = 35

# Banner defaults
DEFAULT_BANNER_WIDTH = 728
DEFAULT_BANNER_HEIGHT = 90
SAMPLE_BANNER_NAME = "Sample Ad Banner"

# Path constants
SAMPLES_DIR = Path("dashboard/assets/samples")
SAMPLE_BANNER_FILE = "sample_banner.txt"
SAMPLE_BANNER_CONTENT = "This is a placeholder for a sample banner image."
SAMPLE_BANNER_URL_PREFIX = "/assets/samples/"

# Campaign defaults
SAMPLE_CAMPAIGN_NAME = "Sample Marketing Campaign"
DEFAULT_CAMPAIGN_BUDGETS = [100, 250, 500, 1000, 2000]
MIN_RANDOM_DAYS = 1
MAX_RANDOM_DAYS = 30
CAMPAIGN_DURATION_DAYS = 30


def create_sample_interests() -> list[InterestSchema]:
    if interest_store.count() > 0:
        return interest_store.list()

    sample_interests: list[dict[str, str]] = [
        {"name": INTEREST_TECHNOLOGY, "category": CATEGORY_TECH},
        {"name": INTEREST_SOFTWARE, "category": CATEGORY_TECH},
        {"name": INTEREST_MOBILE, "category": CATEGORY_TECH},
        {"name": INTEREST_CLOUD, "category": CATEGORY_TECH},
        {"name": INTEREST_FASHION, "category": CATEGORY_LIFESTYLE},
        {"name": INTEREST_HOME, "category": CATEGORY_LIFESTYLE},
        {"name": INTEREST_BEAUTY, "category": CATEGORY_LIFESTYLE},
        {"name": INTEREST_CUISINE, "category": CATEGORY_LIFESTYLE},
        {"name": INTEREST_SOCCER, "category": CATEGORY_SPORTS},
        {"name": INTEREST_BASKETBALL, "category": CATEGORY_SPORTS},
        {"name": INTEREST_TENNIS, "category": CATEGORY_SPORTS},
        {"name": INTEREST_CYCLING, "category": CATEGORY_SPORTS},
        {"name": INTEREST_EUROPE, "category": CATEGORY_TRAVEL},
        {"name": INTEREST_BEACH, "category": CATEGORY_TRAVEL},
        {"name": INTEREST_ADVENTURE, "category": CATEGORY_TRAVEL},
        {"name": INTEREST_CITY, "category": CATEGORY_TRAVEL},
    ]

    for interest_data in sample_interests:
        interest = InterestSchema(  # type: ignore
            name=interest_data["name"],
            category=interest_data["category"],
        )
        interest_store.add(interest)

    return interest_store.list()


def ensure_sample_banner_exists() -> str:
    # Create a simple text file as a placeholder for a sample banner
    SAMPLES_DIR.mkdir(parents=True, exist_ok=True)

    sample_banner_path = SAMPLES_DIR / SAMPLE_BANNER_FILE

    if not sample_banner_path.exists():
        with open(sample_banner_path, "w") as f:
            f.write(SAMPLE_BANNER_CONTENT)

    return f"{SAMPLE_BANNER_URL_PREFIX}{SAMPLE_BANNER_FILE}"


def create_sample_campaign(user_id: str) -> CampaignSchema:
    # Ensure we have sample interests
    create_sample_interests()

    # Ensure we have a sample banner image/placeholder
    sample_banner_url = ensure_sample_banner_exists()

    # Create sample banner
    sample_banner = AdBannerSchema(  # type: ignore
        name=SAMPLE_BANNER_NAME,
        image_url=sample_banner_url,
        width_px=DEFAULT_BANNER_WIDTH,
        height_px=DEFAULT_BANNER_HEIGHT,
        created_by=user_id,
    )

    added_banner = banner_store.add(sample_banner)

    # Get some random interests
    all_interests = interest_store.list()
    random_interests = random.sample(
        [i.id for i in all_interests],
        min(3, len(all_interests)),
    )

    # Create sample targeting
    sample_targeting = AudienceTargetingSchema(  # type: ignore
        age_range=AgeRangeSchema(min_age=DEFAULT_MIN_AGE, max_age=DEFAULT_MAX_AGE),
        locations=[
            LocationSchema(
                country=COUNTRY_US,
                region=REGION_CALIFORNIA,
                city=CITY_SAN_FRANCISCO,
            ),
            LocationSchema(
                country=COUNTRY_US,
                region=REGION_NEW_YORK,
                city=CITY_NEW_YORK,
            ),
        ],
        interests=random_interests,
    )

    added_targeting = targeting_store.add(sample_targeting)

    # Create sample campaign with random start date
    start_date = datetime.now(UTC) + timedelta(
        days=random.randint(MIN_RANDOM_DAYS, MAX_RANDOM_DAYS),
    )

    sample_campaign = CampaignSchema(  # type: ignore
        name=SAMPLE_CAMPAIGN_NAME,
        banner_id=added_banner.id,
        targeting_id=added_targeting.id,
        budget_usd=random.choice(DEFAULT_CAMPAIGN_BUDGETS),
        status=CampaignStatusEnum.DRAFT,
        start_date=start_date,
        end_date=start_date + timedelta(days=CAMPAIGN_DURATION_DAYS)
        if random.choice([True, False])
        else None,
        created_by=user_id,
    )

    return campaign_store.add(sample_campaign)
