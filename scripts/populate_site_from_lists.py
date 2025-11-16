import csv
import re
from pathlib import Path
import textwrap

ROOT = Path(__file__).resolve().parent.parent
LISTS_DIR = ROOT / "lists"
BRANDS_DIR = ROOT / "_brands"
COUPONS_DIR = ROOT / "_coupons"

BRAND_NAMES = {
    "1800contacts": "1-800 Contacts",
    "aliexpress": "AliExpress",
    "autonation": "AutoNation",
    "booking": "Booking.com",
    "expedia": "Expedia",
    "hotelscom": "Hotels.com",
    "lulus": "Lulus",
    "lumens": "Lumens",
    "nike": "Nike",
    "petco": "Petco",
    "shein": "SHEIN",
    "walmart": "Walmart",
}


def slugify(text: str) -> str:
    """Create a URL-friendly slug."""
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", text).strip("-").lower()
    return slug or "offer"


def default_brand_name(slug: str) -> str:
    return slug.replace("-", " ").title()


def build_brand_page(brand_slug: str, brand_name: str) -> str:
    description_short = (
        f"Latest {brand_name} discount codes, promo codes, and simple ways to save."
    )
    body = textwrap.dedent(
        f"""
        {brand_name} regularly promotes limited-time deals and coupon codes. This page keeps the newest options in one place so you can quickly check what still works.

        We list the current offers first, then expired ones as a reference for what has been available recently.
        """
    ).strip()

    front_matter = textwrap.dedent(
        f"""
        ---
        layout: brand
        title: "{brand_name} discount codes"
        brand_slug: "{brand_slug}"
        description_short: "{description_short}"
        ---
        """
    ).strip()

    return f"{front_matter}\n\n{body}\n"


def build_coupon_page(
    brand_slug: str, brand_name: str, code: str, discount: str, description: str
) -> str:
    title = f"{discount} {description}".strip()
    description_short = description

    front_matter = textwrap.dedent(
        f"""
        ---
        layout: coupon
        title: "{title}"
        brand_slug: "{brand_slug}"
        discount_value: "{discount}"
        code: "{code}"
        is_expired: false
        description_short: "{description_short}"
        ---
        """
    ).strip()

    body = textwrap.dedent(
        f"""
        Use code **{code}** at checkout to get {discount.lower()} on {description.lower()}.

        These offers come directly from the latest list we maintain for {brand_name}. Availability can change, so try the code soon if it fits your order.
        """
    ).strip()

    return f"{front_matter}\n\n{body}\n"


def main() -> None:
    BRANDS_DIR.mkdir(exist_ok=True)
    COUPONS_DIR.mkdir(exist_ok=True)

    for csv_path in LISTS_DIR.glob("*.csv"):
        brand_slug = csv_path.stem.lower()
        brand_name = BRAND_NAMES.get(brand_slug, default_brand_name(brand_slug))

        # Write brand page
        brand_output = build_brand_page(brand_slug, brand_name)
        brand_file = BRANDS_DIR / f"{brand_slug}.md"
        brand_file.write_text(brand_output)

        # Prepare coupon directory
        coupon_dir = COUPONS_DIR / brand_slug
        coupon_dir.mkdir(parents=True, exist_ok=True)

        # Clear existing coupons for a fresh sync
        for existing in coupon_dir.glob("*.md"):
            existing.unlink()

        with csv_path.open(newline="") as handle:
            reader = csv.DictReader(handle)
            for row in reader:
                code = row.get("code", "").strip()
                discount = row.get("discount_amount", "").strip()
                description = row.get("description", "").strip()

                file_slug = slugify(f"{code}-{discount}-{description}")
                coupon_file = coupon_dir / f"{file_slug}.md"
                coupon_output = build_coupon_page(
                    brand_slug=brand_slug,
                    brand_name=brand_name,
                    code=code,
                    discount=discount,
                    description=description,
                )
                coupon_file.write_text(coupon_output)


if __name__ == "__main__":
    main()
