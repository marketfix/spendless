import csv
import re
import shutil
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
    "chewy": "Chewy",
    "expedia": "Expedia",
    "hotelscom": "Hotels.com",
    "lulus": "Lulus",
    "lumens": "Lumens",
    "meta": "Meta",
    "nike": "Nike",
    "petco": "Petco",
    "playstation": "PlayStation",
    "shein": "SHEIN",
    "saily": "Saily",
    "walmart": "Walmart",
    "kiwi_com": "Kiwi.com",
    "nordvpn": "NordVPN",
    "protonvpn": "ProtonVPN",
    "trip_com": "Trip.com",
    "qatar_airways": "Qatar Airways",
    "etihad_airways": "Etihad Airways",
    "ebay": "eBay",
    "skullcandy": "Skullcandy",
    "spelab": "SPELAB",
    "surfshark": "Surfshark",
    "temu": "Temu",
    "vevor": "VEVOR",
    "vrbo": "Vrbo",
}

LOGO_PATHS = {
    "etihad_airways": "/media/brand_logos/etihad.jpg",
    "kiwi_com": "/media/brand_logos/kiwic.jpg",
    "qatar_airways": "/media/brand_logos/qatar.jpg",
    "trip_com": "/media/brand_logos/tripcom.jpg",
}

MERGED_BRAND_SLUGS = {
    "booking_com": "booking",
    "hotels_com": "hotelscom",
    "walmart_grocery": "walmart",
}


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", text).strip("-").lower()
    return slug or "offer"


def default_brand_name(slug: str) -> str:
    return slug.replace("-", " ").replace("_", " ").title()


def ensure_logo(brand_slug: str) -> str:
    if brand_slug in LOGO_PATHS:
        return LOGO_PATHS[brand_slug]
    return f"/media/brand_logos/{brand_slug}.jpg"


def country_prefix(text: str) -> str:
    value = text.lower()
    checks = [
        ("US", r"\bus\b|\busa\b|united states|\$|usnew|wethrift30|admitad30|sapnew10"),
        ("UK", r"\buk\b|united kingdom|britain|£"),
        ("Canada", r"canada|canadian|\bcad\b"),
        ("Australia", r"australia|australian|admitadau30"),
        ("Germany", r"germany|german|admitadde30"),
        ("Ireland", r"ireland|irish"),
        ("Italy", r"italy|italian|itnew30"),
        ("Poland", r"poland|polish|zł|zl"),
        ("Europe", r"europe|european|€|\beu\b"),
        ("UAE", r"\buae\b|emirates|aed"),
        ("Morocco", r"morocco|moroccan"),
        ("Middle East", r"middle east"),
        ("Global", r"global|worldwide|sitewide|all users|full order|full cart|no minimum"),
    ]
    for label, pattern in checks:
        if re.search(pattern, value):
            return label
    return ""


def specific_scope(text: str) -> str:
    value = text.lower()
    amount_match = re.search(r"(?:over|minimum|spend)\s*([$€£]?\s?\d+|[0-9]+\s?(?:aed|cad|zł|zl))", value)
    if re.search(r"contact|lens|acuvue|biofinity|aquasoft", value):
        return "contact lens orders"
    if "kids" in value:
        return "kids category orders"
    if re.search(r"free gift|free gifts|gift bundle|0€|£0|\$0", value):
        return "free gift app offers"
    if re.search(r"coupon bundle|voucher|vouchers|coupon pack|pack of coupons|bundle", value):
        return "coupon bundle orders"
    if re.search(r"free shipping|free delivery", value):
        return "orders with free shipping"
    if amount_match:
        return f"orders over {amount_match.group(1).replace(' ', '')}"
    if re.search(r"first order|new user|new customer|first time", value):
        return "new customer orders"
    if re.search(r"app|mobile", value):
        return "mobile app orders"
    if re.search(r"sitewide|storewide|full order|full cart|all users|no minimum|any order", value):
        return "sitewide online orders"
    if "fashion" in value:
        return "fashion category orders"
    if "electronics" in value:
        return "electronics category orders"
    return "online checkout orders"


def clean_sentence(text: str, discount: str = "", code: str = "") -> str:
    combined = f"{text} {discount} {code}"
    prefix = country_prefix(combined)
    scope = specific_scope(combined)
    words = []
    if prefix and not scope.lower().startswith(prefix.lower()):
        words.extend(prefix.split())
    words.extend(scope.split())

    if code and len(words) <= 7:
        words.extend(["with", "code", code])

    words = [word for word in words if word.lower() not in {"eligible", "select", "selected", "qualifying"}]
    if len(words) > 10:
        words = words[:10]
    while len(words) < 4 and code:
        words.extend(["with", "code", code])
        if len(words) > 10:
            words = words[:10]
            break

    cleaned = " ".join(words).strip(" .")
    if not cleaned:
        cleaned = f"Online checkout orders with code {code}".strip()
    return f"{cleaned[0].upper()}{cleaned[1:]}."


def build_brand_page(brand_slug: str, brand_name: str, logo_path: str) -> str:
    description_short = f"Current {brand_name} discount codes from /r/SpendLess."
    body = textwrap.dedent(
        f"""
        Current {brand_name} codes shared in /r/SpendLess.
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
    description_short = clean_sentence(description, discount, code)
    title = f"{discount} {description_short}".strip()

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
        Use code **{code}** at checkout for {discount.lower()}.

        This code is included from the latest /r/SpendLess list for {brand_name}. Availability can change quickly.
        """
    ).strip()

    return f"{front_matter}\n\n{body}\n"


def main() -> None:
    BRANDS_DIR.mkdir(exist_ok=True)
    COUPONS_DIR.mkdir(exist_ok=True)
    LOGOS_DIR.mkdir(parents=True, exist_ok=True)

    list_slugs = sorted(path.stem.lower() for path in LISTS_DIR.glob("*.csv"))
    canonical_slugs = {MERGED_BRAND_SLUGS.get(slug, slug) for slug in list_slugs}

    for existing_brand in BRANDS_DIR.glob("*.md"):
        if existing_brand.stem.lower() not in canonical_slugs:
            existing_brand.unlink()

    for existing_coupon_dir in COUPONS_DIR.iterdir():
        if existing_coupon_dir.is_dir() and existing_coupon_dir.name.lower() not in canonical_slugs:
            for existing in existing_coupon_dir.glob("*.md"):
                if existing.is_dir():
                    shutil.rmtree(existing)
                else:
                    existing.unlink()
            existing_coupon_dir.rmdir()

    cleared_coupon_dirs = set()
    seen_coupon_codes_by_brand = {}

    for csv_path in sorted(LISTS_DIR.glob("*.csv")):
        raw_brand_slug = csv_path.stem.lower()
        brand_slug = MERGED_BRAND_SLUGS.get(raw_brand_slug, raw_brand_slug)
        brand_name = BRAND_NAMES.get(raw_brand_slug, BRAND_NAMES.get(brand_slug, default_brand_name(brand_slug)))
        logo_path = ensure_logo(brand_slug)

        brand_output = build_brand_page(brand_slug, brand_name, logo_path)
        brand_file = BRANDS_DIR / f"{brand_slug}.md"
        brand_file.write_text(brand_output)

        coupon_dir = COUPONS_DIR / brand_slug
        coupon_dir.mkdir(parents=True, exist_ok=True)
        seen_coupon_codes = seen_coupon_codes_by_brand.setdefault(brand_slug, set())

        if brand_slug not in cleared_coupon_dirs:
            for existing in coupon_dir.glob("*.md"):
                if existing.is_dir():
                    shutil.rmtree(existing)
                else:
                    existing.unlink()
            cleared_coupon_dirs.add(brand_slug)

        with csv_path.open(newline="") as handle:
            reader = csv.DictReader(handle)
            for row in reader:
                code = row.get("code", "").strip()
                discount = row.get("discount_amount", "").strip()
                description = row.get("description", "").strip()
                code_key = code.upper()
                if not code_key or code_key in seen_coupon_codes:
                    continue
                seen_coupon_codes.add(code_key)

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
