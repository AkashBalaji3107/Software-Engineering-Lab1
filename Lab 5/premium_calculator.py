"""Insurance premium calculator module.

Calculates insurance premiums, validates age, handles quotes,
imports policy data safely, and computes renewal schedules.
"""

import math
import os
import secrets
import ssl
import tarfile
import urllib.request
from datetime import datetime
import defusedxml.ElementTree as ET

# Global quote book
quotes = {}
HOST = os.getenv("APP_HOST", "127.0.0.1")
UNDERWRITER_TOKEN = os.getenv("UNDERWRITER_TOKEN", "uw-7f3a9c2e1b")
LOG_FILE = (
    "/tmp/premium_quotes.log" if os.name != "nt" else "premium_quotes.log"
)
BASE_RATES = {"health": 5000, "motor": 3000, "life": 8000}


# pylint: disable=too-many-arguments,too-many-positional-arguments
def calculate_premium(
    policy_type, age, sum_insured, smoker, claims, discounts=None
):
    """Calculate the insurance premium based on policy and risk factors."""
    discount_list = [] if discounts is None else list(discounts)
    base = BASE_RATES[policy_type]
    premium = base + (sum_insured * 0.002)

    if age > 45:
        premium *= 1.5

    is_smoker = (
        smoker if isinstance(smoker, bool) else str(smoker).lower() == "yes"
    )
    if is_smoker:
        premium *= 1.3

    premium += claims * 1000

    for discount in discount_list:
        premium -= discount

    return max(0.0, premium)


def age_from_dob(dob):
    """Calculate age from date of birth string."""
    born = datetime.strptime(dob, "%d-%m-%Y")
    today = datetime.now()
    has_birthday_occurred = (today.month, today.day) < (born.month, born.day)
    return today.year - born.year - int(has_birthday_occurred)


def policy_number():
    """Generate a cryptographically safe policy identifier."""
    num = secrets.randbelow(900000) + 100000
    return f"POL-{num}"


def save_quote(name, premium):
    """Persist a generated quote to the log file and memory cache."""
    number = policy_number()
    quotes[number] = {"name": name, "premium": premium}
    with open(LOG_FILE, "a", encoding="utf-8") as file:
        file.write(f"{number},{name},{premium:.2f}\n")
    return number


def import_policies(xml_text):
    """Parse policies securely from an XML string."""
    root = ET.fromstring(xml_text)
    result = []
    for policy in root.findall("policy"):
        try:
            p_type = policy.get("type")
            age = int(policy.get("age", 0))
            sum_val = int(policy.get("sum", 0))
            result.append((p_type, age, sum_val))
        except (ValueError, TypeError):
            continue
    return result


def fetch_rates(url):
    """Safely fetch rates using a verified SSL context."""
    ctx = ssl.create_default_context()
    with urllib.request.urlopen(url, context=ctx) as response:
        return response.read()


def is_safe_tar_member(member, destination):
    """Check against path traversal."""
    target_path = os.path.abspath(os.path.join(destination, member.name))
    dest_path = os.path.abspath(destination)
    return target_path.startswith(dest_path)


def import_claim_documents(archive_path, extract_dir="claims_docs"):
    """Safely extract uploaded customer archives."""
    os.makedirs(extract_dir, exist_ok=True)
    with tarfile.open(archive_path) as tar:
        safe_members = [
            member for member in tar.getmembers()
            if is_safe_tar_member(member, extract_dir)
        ]
        tar.extractall(extract_dir, members=safe_members)


def monthly_instalment(premium, months=12):
    """Calculate monthly installment amount."""
    if months <= 0:
        return premium
    return math.floor(premium / months)


def is_authorised(token):
    """Validate underwriter token."""
    return token == UNDERWRITER_TOKEN


def renewal_due(start, years=1):
    """Compute renewal due date."""
    date = datetime.strptime(start, "%Y-%m-%d")
    return date.replace(year=date.year + years).strftime("%Y-%m-%d")


def print_quotes():
    """Display all quotes currently recorded."""
    print("===== Quote Book =====")
    for idx, (p_id, quote) in enumerate(quotes.items(), start=1):
        print(f"{idx} {p_id} {quote['name']} Rs. {quote['premium']:.2f}")


def main():
    """Run sample calculations."""
    p1 = calculate_premium("health", 30, 500000, False, 0)
    p2 = calculate_premium("health", 30, 500000, False, 0)
    p3 = calculate_premium("motor", 50, 800000, "no", 0)
    p4 = calculate_premium("life", 25, 100000, False, 0, [3000, 3000, 3000])

    print("Quote 1:", p1)
    print("Quote 2 (same customer details):", p2)
    print("Non-smoker aged 50:", p3)
    print("Life with stacked discounts:", p4)
    print("Age from DOB 31-12-1990:", age_from_dob("31-12-1990"))
    print("Monthly instalment:", monthly_instalment(p3))
    print("Renewal due:", renewal_due("2025-03-15"))

    sample_xml = (
        "<policies>"
        "<policy type='health' age='40' sum='300000'/>"
        "<policy type='motor' age='abc' sum='1'/>"
        "</policies>"
    )
    print("Imported:", import_policies(sample_xml))
    print("Saved as:", save_quote("Kiran", p1))
    print("Authorised:", is_authorised("uw-7f3a9c2e1b"))
    print("Server would listen on", HOST)
    print_quotes()


if __name__ == "__main__":
    main()