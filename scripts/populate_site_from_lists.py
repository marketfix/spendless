import csv
import re
from pathlib import Path
import textwrap

ROOT = Path(__file__).resolve().parent.parent
LISTS_DIR = ROOT / "lists"
BRANDS_DIR = ROOT / "_brands"
COUPONS_DIR = ROOT / "_coupons"
LOGOS_DIR = ROOT / "media" / "brand_logos"

BRAND_NAMES = {
    "1800contacts": "1-800 Contacts",
    "aliexpress": "AliExpress",
    "autonationparts": "AutoNationParts",
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
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", text).strip("-").lower()
    return slug or "offer"


def default_brand_name(slug: str) -> str:
    return slug.replace("-", " ").title()


def initials_for_brand(brand_name: str) -> str:
    chunks = re.findall(r"[A-Za-z0-9]+", brand_name)
    if not chunks:
        return "SL"
    if len(chunks) == 1:
        return chunks[0][:2].upper()
    return (chunks[0][0] + chunks[1][0]).upper()


def ensure_logo(brand_slug: str, brand_name: str) -> str:
    jpg = LOGOS_DIR / f"{brand_slug}.jpg"
    if jpg.exists():
        return f"/media/brand_logos/{brand_slug}.jpg"

    svg = LOGOS_DIR / f"{brand_slug}.svg"
    if not svg.exists():
        initial = initials_for_brand(brand_name)
        svg.write_text(
            textwrap.dedent(
                f"""
                <svg xmlns="http://www.w3.org/2000/svg" width="120" height="120" viewBox="0 0 120 120" role="img" aria-label="{brand_name} logo placeholder">
                  <defs>
                    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
                      <stop offset="0%" stop-color="#e2e8f0" />
                      <stop offset="100%" stop-color="#cbd5e1" />
                    </linearGradient>
                  </defs>
                  <rect width="120" height="120" fill="url(#bg)" rx="16" />
                  <text x="60" y="68" text-anchor="middle" font-family="Inter, Arial, sans-serif" font-size="34" font-weight="700" fill="#334155">{initial}</text>
                </svg>
                """
            ).strip()
            + "\n"
        )

    return f"/media/brand_logos/{brand_slug}.svg"


def build_brand_page(brand_slug: str, brand_name: str, logo_path: str) -> str:
    description_short = (
        f"Latest {brand_name} discount codes and promo codes from /r/SpendLess."
    )
    body = textwrap.dedent(
        f"""
        This is the official {brand_name} brand page for SpendLess.

        We publish every currently available {brand_name} discount code shared in /r/SpendLess, then keep expired ones listed for reference.
        """
    ).strip()

    front_matter = textwrap.dedent(
        f"""
        ---
        layout: brand
        title: "{brand_name} discount codes"
        brand_slug: "{brand_slug}"
        logo_path: "{logo_path}"
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

        This code is included from the latest /r/SpendLess list for {brand_name}. Availability can change quickly.
        """
    ).strip()

    return f"{front_matter}\n\n{body}\n"


def main() -> None:
    BRANDS_DIR.mkdir(exist_ok=True)
    COUPONS_DIR.mkdir(exist_ok=True)
    LOGOS_DIR.mkdir(parents=True, exist_ok=True)

    list_slugs = sorted(path.stem.lower() for path in LISTS_DIR.glob("*.csv"))

    # Brand pages should be limited to known subreddit brand lists.
    for existing_brand in BRANDS_DIR.glob("*.md"):
        if existing_brand.stem.lower() not in list_slugs:
            existing_brand.unlink()

    # Coupon dirs should only exist for active subreddit brand lists.
    for existing_coupon_dir in COUPONS_DIR.iterdir():
        if existing_coupon_dir.is_dir() and existing_coupon_dir.name.lower() not in list_slugs:
            for existing in existing_coupon_dir.glob("*.md"):
                existing.unlink()
            existing_coupon_dir.rmdir()

    for csv_path in LISTS_DIR.glob("*.csv"):
        brand_slug = csv_path.stem.lower()
        brand_name = BRAND_NAMES.get(brand_slug, default_brand_name(brand_slug))
        logo_path = ensure_logo(brand_slug, brand_name)

        brand_output = build_brand_page(brand_slug, brand_name, logo_path)
        brand_file = BRANDS_DIR / f"{brand_slug}.md"
        brand_file.write_text(brand_output)

        coupon_dir = COUPONS_DIR / brand_slug
        coupon_dir.mkdir(parents=True, exist_ok=True)

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
