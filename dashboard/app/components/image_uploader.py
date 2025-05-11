from io import BytesIO
from pathlib import Path
from typing import Any, TypedDict, cast
from uuid import uuid4

import streamlit as st
from PIL import Image

# Constants for image validation
MAX_IMAGE_SIZE_KB = 250

# Valid image formats
VALID_FORMATS = ["JPEG", "PNG", "GIF"]

# Standard banner sizes and names
BANNER_SIZE_LEADERBOARD = (728, 90)
BANNER_SIZE_LEADERBOARD_X2 = (800, 288)
BANNER_SIZE_MEDIUM_RECTANGLE = (300, 250)
BANNER_SIZE_WIDE_SKYSCRAPER = (160, 600)
BANNER_SIZE_MOBILE_LEADERBOARD = (320, 50)
BANNER_SIZE_LARGE_RECTANGLE = (336, 280)

STANDARD_BANNER_SIZES = [
    BANNER_SIZE_LEADERBOARD,
    BANNER_SIZE_LEADERBOARD_X2,
    BANNER_SIZE_MEDIUM_RECTANGLE,
    BANNER_SIZE_WIDE_SKYSCRAPER,
    BANNER_SIZE_MOBILE_LEADERBOARD,
    BANNER_SIZE_LARGE_RECTANGLE,
]

BANNER_SIZE_NAMES = {
    BANNER_SIZE_LEADERBOARD: "Leaderboard",
    BANNER_SIZE_LEADERBOARD_X2: "Leaderboard (x2)",
    BANNER_SIZE_MEDIUM_RECTANGLE: "Medium Rectangle",
    BANNER_SIZE_WIDE_SKYSCRAPER: "Wide Skyscraper",
    BANNER_SIZE_MOBILE_LEADERBOARD: "Mobile Leaderboard",
    BANNER_SIZE_LARGE_RECTANGLE: "Large Rectangle",
}

# File paths
UPLOADS_DIR = Path("dashboard/assets/uploads")
DEFAULT_BANNER_NAME_PREFIX = "Banner"
CUSTOM_BANNER_NAME_PREFIX = "Custom Banner"


class ImageValidationResult(TypedDict, total=False):
    valid: bool
    width: int
    height: int
    format: str
    size_kb: float
    errors: list[str]


class BannerData(TypedDict, total=False):
    name: str
    image_url: str
    width_px: int
    height_px: int
    created_by: str


def validate_image(image_file: Any) -> ImageValidationResult:
    try:
        img = Image.open(image_file)
        width, height = img.size

        exact_match = False
        for size in STANDARD_BANNER_SIZES:
            if (width, height) == size:
                exact_match = True
                break

        # Check file format
        valid_format = img.format in VALID_FORMATS

        # Check file size
        img_byte_arr = BytesIO()
        img.save(img_byte_arr, format=img.format)
        file_size = len(img_byte_arr.getvalue()) / 1024  # KB
        valid_size = file_size <= MAX_IMAGE_SIZE_KB

        result: ImageValidationResult = {
            "valid": exact_match and valid_format and valid_size,
            "width": width,
            "height": height,
            "format": cast(str, img.format),
            "size_kb": file_size,
            "errors": [],
        }

        if not exact_match:
            closest_size = min(
                STANDARD_BANNER_SIZES,
                key=lambda s: abs(s[0] - width) + abs(s[1] - height),
            )
            error_msg = (
                f"Image dimensions ({width}x{height}) don't match standard "
                f"banner sizes. Closest standard size: "
                f"{closest_size[0]}x{closest_size[1]} "
                f"({BANNER_SIZE_NAMES.get(closest_size, 'Custom')})."
            )
            result["errors"].append(error_msg)

        if not valid_format:
            formats_str = ", ".join(VALID_FORMATS)
            error_msg = (
                f"Invalid format: {img.format}. Please use one of: {formats_str}."
            )
            result["errors"].append(error_msg)

        if not valid_size:
            error_msg = (
                f"File too large: {file_size:.1f}KB. "
                f"Maximum allowed: {MAX_IMAGE_SIZE_KB}KB."
            )
            result["errors"].append(error_msg)
    except OSError as e:
        # Specific exceptions for file handling errors
        return {
            "valid": False,
            "errors": [f"Error processing image: {e!s}"],
        }
    else:
        return result


def save_uploaded_image(uploaded_file: Any, user_id: str) -> str:
    # Ensure upload directory exists
    UPLOADS_DIR.mkdir(parents=True, exist_ok=True)

    # Create a unique filename
    file_ext = Path(uploaded_file.name).suffix
    unique_name = f"{user_id}_{uuid4()}{file_ext}"
    file_path = UPLOADS_DIR / unique_name

    # Save the file
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Return the relative path
    return f"/assets/uploads/{unique_name}"


def image_uploader(user_id: str) -> BannerData | None:
    st.subheader("Ad Banner")

    help_text = (
        "Upload a banner image. Standard sizes are recommended (728x90, 300x250, etc.)."
    )

    uploaded_file = st.file_uploader(
        "Upload banner image",
        type=["png", "jpg", "jpeg", "gif"],
        help=help_text,
    )

    banner_data: BannerData | None = None

    if uploaded_file is not None:
        # Display the image
        st.image(uploaded_file, caption="Uploaded Banner", use_container_width=True)

        # Validate the image
        validation = validate_image(uploaded_file)

        if validation.get("valid", False):
            st.success("Image is valid for ad use.")

            # Save the image and create banner data
            image_url = save_uploaded_image(uploaded_file, user_id)

            name_value = (
                f"{DEFAULT_BANNER_NAME_PREFIX} "
                f"{validation.get('width')}x{validation.get('height')}"
            )

            banner_name = st.text_input("Banner Name", value=name_value)

            banner_data = {
                "name": banner_name,
                "image_url": image_url,
                "width_px": validation.get("width", 0),
                "height_px": validation.get("height", 0),
                "created_by": user_id,
            }
        else:
            for error in validation.get("errors", []):
                st.warning(error)

            # If dimensions are the only issue, still allow with a warning
            dimension_only_issue = (
                len(validation.get("errors", [])) == 1
                and "dimensions" in validation.get("errors", [])[0]
            )

            if dimension_only_issue:
                st.warning("Non-standard dimensions may affect ad performance.")

                # Save the image and create banner data
                image_url = save_uploaded_image(uploaded_file, user_id)

                name_value = (
                    f"{CUSTOM_BANNER_NAME_PREFIX} "
                    f"{validation.get('width')}x{validation.get('height')}"
                )

                banner_name = st.text_input("Banner Name", value=name_value)

                banner_data = {
                    "name": banner_name,
                    "image_url": image_url,
                    "width_px": validation.get("width", 0),
                    "height_px": validation.get("height", 0),
                    "created_by": user_id,
                }

    return banner_data
