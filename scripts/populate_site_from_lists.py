from pathlib import Path
import textwrap

ROOT = Path(__file__).resolve().parent.parent
LISTS_DIR = ROOT / "lists"
BRANDS_DIR = ROOT / "_brands"
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
    "walmart_grocery": "Walmart Grocery",
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


def default_brand_name(slug: str) -> str:
    return slug.replace("-", " ").replace("_", " ").title()


def ensure_logo(brand_slug: str) -> str:
    if brand_slug in LOGO_PATHS:
        return LOGO_PATHS[brand_slug]
    return f"/media/brand_logos/{brand_slug}.jpg"


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


def main() -> None:
    BRANDS_DIR.mkdir(exist_ok=True)
    LOGOS_DIR.mkdir(parents=True, exist_ok=True)

    list_slugs = sorted(path.stem.lower() for path in LISTS_DIR.glob("*.csv"))

    for existing_brand in BRANDS_DIR.glob("*.md"):
        if existing_brand.stem.lower() not in list_slugs:
            existing_brand.unlink()

    for brand_slug in list_slugs:
        brand_name = BRAND_NAMES.get(brand_slug, default_brand_name(brand_slug))
        logo_path = ensure_logo(brand_slug)
        brand_file = BRANDS_DIR / f"{brand_slug}.md"
        brand_file.write_text(build_brand_page(brand_slug, brand_name, logo_path))


if __name__ == "__main__":
    main()
