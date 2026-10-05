#!/usr/bin/env python3
"""Static generator for a small, SEO-friendly "free tools" website.

The site is intentionally dependency-free (stdlib only) so it can be built
anywhere with Python 3 and deployed as plain static files.

Ad slot markup is centralised in TEMPLATE so a real ad-network snippet can be
dropped in once an account is approved.
"""
from __future__ import annotations

import html
import json
import os
import shutil
import struct
import zlib
from pathlib import Path

AD_HEADER = """
<script src="https://pl31650611.profitableratecpmnetwork.com/26/98/69/26986910ba4ccafa9fa155977134a3ca.js"></script>
<script src="https://pl31650613.profitableratecpmnetwork.com/33/c0/f9/33c0f9632f1aa63372172b2f925276a7.js"></script>
"""
AD_INARTICLE = """
<script async="async" data-cfasync="false" src="https://pl31650614.profitableratecpmnetwork.com/4371774b26da680de16b6540d646292a/invoke.js"></script>
<div id="container-4371774b26da680de16b6540d646292a"></div>
"""
AD_SIDEBAR = ""
AD_FOOTER = ""

CONVERSIONS = [
    # --- Length ---
    {
        "slug": "cm-to-inches", "category": "Length",
        "from": "cm", "to": "in", "factor": 0.393700787,
        "name": "CM to Inches",
        "title": "CM to Inches Converter - Convert Centimeters to Inches",
        "desc": "Convert centimetres to inches instantly. Enter a value to see the result, plus a quick reference table and the formula.",
        "keywords": "cm to inches, centimeters to inches, convert cm to inches, cm in inches",
        "formula": "inches = centimetres × 0.393701",
        "table": [1, 2, 5, 10, 20, 50, 100],
        "faqs": [
            ("How many inches is 1 cm?", "1 centimetre equals 0.393701 inches."),
            ("How many cm in an inch?", "1 inch equals exactly 2.54 centimetres."),
            ("What is 100 cm in inches?", "100 centimetres is 39.37 inches, just under 40 inches."),
        ],
    },
    {
        "slug": "inches-to-cm", "category": "Length",
        "from": "in", "to": "cm", "factor": 2.54,
        "name": "Inches to CM",
        "title": "Inches to CM Converter - Convert Inches to Centimeters",
        "desc": "Convert inches to centimetres instantly. Includes a reference table and the exact conversion formula.",
        "keywords": "inches to cm, convert inches to centimeters, inch to cm",
        "formula": "centimetres = inches × 2.54",
        "table": [1, 2, 5, 10, 12, 20, 36],
        "faqs": [
            ("How many cm is 1 inch?", "1 inch equals exactly 2.54 centimetres."),
            ("How many cm is 12 inches?", "12 inches equals 30.48 centimetres."),
            ("Is 1 inch 2.5 cm?", "It is 2.54 cm. Rounding to 2.5 is fine for rough estimates."),
        ],
    },
    {
        "slug": "m-to-feet", "category": "Length",
        "from": "m", "to": "ft", "factor": 3.280839895,
        "name": "Meters to Feet",
        "title": "Meters to Feet Converter - Convert m to ft",
        "desc": "Convert metres to feet instantly, with a conversion table and the formula for doing it yourself.",
        "keywords": "meters to feet, convert m to ft, metre to feet",
        "formula": "feet = metres × 3.28084",
        "table": [1, 2, 5, 10, 20, 50, 100],
        "faqs": [
            ("How many feet is 1 metre?", "1 metre equals about 3.28084 feet."),
            ("How many feet is 10 metres?", "10 metres equals about 32.81 feet."),
            ("What is 1.8 m in feet?", "1.8 metres equals about 5.91 feet, roughly 5 feet 11 inches."),
        ],
    },
    {
        "slug": "feet-to-m", "category": "Length",
        "from": "ft", "to": "m", "factor": 0.3048,
        "name": "Feet to Meters",
        "title": "Feet to Meters Converter - Convert ft to m",
        "desc": "Convert feet to metres instantly. Includes a quick reference table and the formula.",
        "keywords": "feet to meters, convert ft to m, foot to metre",
        "formula": "metres = feet × 0.3048",
        "table": [1, 3, 5, 6, 10, 20, 50],
        "faqs": [
            ("How many metres is 1 foot?", "1 foot equals exactly 0.3048 metres."),
            ("How many metres is 6 feet?", "6 feet equals 1.8288 metres."),
            ("How many metres is 10 feet?", "10 feet equals 3.048 metres."),
        ],
    },
    {
        "slug": "km-to-miles", "category": "Length",
        "from": "km", "to": "mi", "factor": 0.621371192,
        "name": "KM to Miles",
        "title": "KM to Miles Converter - Convert Kilometres to Miles",
        "desc": "Convert kilometres to miles instantly. Useful for running distances, road trips and travel.",
        "keywords": "km to miles, kilometers to miles, convert km to miles",
        "formula": "miles = kilometres × 0.621371",
        "table": [1, 5, 10, 21, 42, 100],
        "faqs": [
            ("How many miles is 1 km?", "1 kilometre equals about 0.621371 miles."),
            ("How many miles is a 5K?", "A 5 kilometre run is about 3.11 miles."),
            ("How many miles is a marathon?", "A marathon is 42.195 km, which is 26.2 miles."),
        ],
    },
    {
        "slug": "miles-to-km", "category": "Length",
        "from": "mi", "to": "km", "factor": 1.609344,
        "name": "Miles to KM",
        "title": "Miles to KM Converter - Convert Miles to Kilometres",
        "desc": "Convert miles to kilometres instantly, with a reference table and the exact formula.",
        "keywords": "miles to km, convert miles to kilometers, mile to km",
        "formula": "kilometres = miles × 1.609344",
        "table": [1, 3, 5, 10, 26.2, 100],
        "faqs": [
            ("How many km is 1 mile?", "1 mile equals exactly 1.609344 kilometres."),
            ("How many km is 10 miles?", "10 miles equals 16.09 kilometres."),
            ("How many km is a marathon?", "26.2 miles equals 42.195 kilometres."),
        ],
    },
    {
        "slug": "mm-to-inches", "category": "Length",
        "from": "mm", "to": "in", "factor": 0.0393700787,
        "name": "MM to Inches",
        "title": "MM to Inches Converter - Convert Millimetres to Inches",
        "desc": "Convert millimetres to inches instantly. Handy for engineering, woodworking and DIY measurements.",
        "keywords": "mm to inches, millimeters to inches, convert mm to inches",
        "formula": "inches = millimetres × 0.0393701",
        "table": [1, 5, 10, 25, 50, 100],
        "faqs": [
            ("How many inches is 1 mm?", "1 millimetre equals about 0.03937 inches."),
            ("How many inches is 25 mm?", "25 millimetres equals about 0.984 inches, close to 1 inch."),
            ("How many mm in an inch?", "1 inch equals exactly 25.4 millimetres."),
        ],
    },
    # --- Weight ---
    {
        "slug": "kg-to-pounds", "category": "Weight",
        "from": "kg", "to": "lb", "factor": 2.204622622,
        "name": "KG to Pounds",
        "title": "KG to Pounds Converter - Convert Kilograms to Pounds",
        "desc": "Convert kilograms to pounds instantly. Useful for body weight, luggage limits and shipping.",
        "keywords": "kg to pounds, kilograms to pounds, convert kg to lbs",
        "formula": "pounds = kilograms × 2.20462",
        "table": [1, 5, 10, 20, 50, 70, 100],
        "faqs": [
            ("How many pounds is 1 kg?", "1 kilogram equals about 2.20462 pounds."),
            ("How many pounds is 70 kg?", "70 kilograms equals about 154.32 pounds."),
            ("How many pounds is 50 kg?", "50 kilograms equals about 110.23 pounds."),
        ],
    },
    {
        "slug": "pounds-to-kg", "category": "Weight",
        "from": "lb", "to": "kg", "factor": 0.45359237,
        "name": "Pounds to KG",
        "title": "Pounds to KG Converter - Convert Pounds to Kilograms",
        "desc": "Convert pounds to kilograms instantly, with a reference table and the formula.",
        "keywords": "pounds to kg, lbs to kg, convert pounds to kilograms",
        "formula": "kilograms = pounds × 0.453592",
        "table": [1, 10, 50, 100, 150, 200],
        "faqs": [
            ("How many kg is 1 pound?", "1 pound equals about 0.453592 kilograms."),
            ("How many kg is 150 pounds?", "150 pounds equals about 68.04 kilograms."),
            ("How many kg is 200 pounds?", "200 pounds equals about 90.72 kilograms."),
        ],
    },
    {
        "slug": "grams-to-ounces", "category": "Weight",
        "from": "g", "to": "oz", "factor": 0.0352739619,
        "name": "Grams to Ounces",
        "title": "Grams to Ounces Converter - Convert g to oz",
        "desc": "Convert grams to ounces instantly, with a quick reference table and the formula.",
        "keywords": "grams to ounces, g to oz, convert grams to ounces",
        "formula": "ounces = grams × 0.035274",
        "table": [1, 10, 50, 100, 250, 500],
        "faqs": [
            ("How many ounces is 1 gram?", "1 gram equals about 0.035274 ounces."),
            ("How many ounces is 100 grams?", "100 grams equals about 3.527 ounces."),
            ("How many grams in an ounce?", "1 ounce equals exactly 28.3495 grams."),
        ],
    },
    {
        "slug": "ounces-to-grams", "category": "Weight",
        "from": "oz", "to": "g", "factor": 28.349523125,
        "name": "Ounces to Grams",
        "title": "Ounces to Grams Converter - Convert oz to g",
        "desc": "Convert ounces to grams instantly, with a reference table and the exact formula.",
        "keywords": "ounces to grams, oz to g, convert ounces to grams",
        "formula": "grams = ounces × 28.3495",
        "table": [1, 2, 4, 8, 12, 16],
        "faqs": [
            ("How many grams is 1 ounce?", "1 ounce equals exactly 28.3495 grams."),
            ("How many grams is 8 ounces?", "8 ounces equals about 226.8 grams."),
            ("How many grams is 16 ounces?", "16 ounces equals about 453.6 grams, close to half a kilogram."),
        ],
    },
    # --- Temperature (special formulas) ---
    {
        "slug": "celsius-to-fahrenheit", "category": "Temperature",
        "from": "C", "to": "F", "kind": "temp",
        "name": "Celsius to Fahrenheit",
        "title": "Celsius to Fahrenheit Converter - Convert °C to °F",
        "desc": "Convert Celsius to Fahrenheit instantly, with a reference table of common temperatures and the formula.",
        "keywords": "celsius to fahrenheit, c to f, convert celsius to fahrenheit",
        "formula": "°F = (°C × 9/5) + 32",
        "table": [0, 10, 20, 25, 30, 37, 100],
        "faqs": [
            ("How do I convert Celsius to Fahrenheit?", "Multiply by 9, divide by 5, then add 32. So 20°C becomes 68°F."),
            ("What is 100°C in Fahrenheit?", "100°C equals 212°F, the boiling point of water."),
            ("What is 37°C in Fahrenheit?", "37°C equals 98.6°F, normal body temperature."),
        ],
    },
    {
        "slug": "fahrenheit-to-celsius", "category": "Temperature",
        "from": "F", "to": "C", "kind": "temp",
        "name": "Fahrenheit to Celsius",
        "title": "Fahrenheit to Celsius Converter - Convert °F to °C",
        "desc": "Convert Fahrenheit to Celsius instantly, with a reference table and the formula.",
        "keywords": "fahrenheit to celsius, f to c, convert fahrenheit to celsius",
        "formula": "°C = (°F − 32) × 5/9",
        "table": [32, 50, 68, 77, 86, 98.6, 212],
        "faqs": [
            ("How do I convert Fahrenheit to Celsius?", "Subtract 32, multiply by 5, then divide by 9. So 68°F becomes 20°C."),
            ("What is 98.6°F in Celsius?", "98.6°F equals 37°C, normal body temperature."),
            ("What is 32°F in Celsius?", "32°F equals 0°C, the freezing point of water."),
        ],
    },
    {
        "slug": "celsius-to-kelvin", "category": "Temperature",
        "from": "C", "to": "K", "kind": "temp",
        "name": "Celsius to Kelvin",
        "title": "Celsius to Kelvin Converter - Convert °C to K",
        "desc": "Convert Celsius to Kelvin instantly. Kelvin is the SI base unit of temperature.",
        "keywords": "celsius to kelvin, c to k, convert celsius to kelvin",
        "formula": "K = °C + 273.15",
        "table": [0, 25, 37, 100, -273.15],
        "faqs": [
            ("How do I convert Celsius to Kelvin?", "Add 273.15. So 0°C is 273.15 K."),
            ("What is absolute zero in Celsius?", "Absolute zero is −273.15°C, which is 0 K."),
            ("Why is there no degree symbol for Kelvin?", "Kelvin is an absolute scale, so it uses the unit K without a degree symbol."),
        ],
    },
    # --- Data ---
    {
        "slug": "mb-to-gb", "category": "Data",
        "from": "MB", "to": "GB", "factor": 1 / 1024,
        "name": "MB to GB",
        "title": "MB to GB Converter - Convert Megabytes to Gigabytes",
        "desc": "Convert megabytes to gigabytes instantly, with a reference table and the formula used for storage.",
        "keywords": "mb to gb, megabytes to gigabytes, convert mb to gb",
        "formula": "gigabytes = megabytes ÷ 1024",
        "table": [512, 1024, 2048, 4096, 8192, 10240],
        "faqs": [
            ("How many GB is 1024 MB?", "1024 megabytes equals 1 gigabyte."),
            ("How many MB is 1 GB?", "1 gigabyte equals 1024 megabytes."),
            ("Why 1024 and not 1000?", "Computers count in powers of two, so storage is often measured in steps of 1024."),
        ],
    },
    {
        "slug": "gb-to-mb", "category": "Data",
        "from": "GB", "to": "MB", "factor": 1024,
        "name": "GB to MB",
        "title": "GB to MB Converter - Convert Gigabytes to Megabytes",
        "desc": "Convert gigabytes to megabytes instantly, with a reference table and the formula.",
        "keywords": "gb to mb, gigabytes to megabytes, convert gb to mb",
        "formula": "megabytes = gigabytes × 1024",
        "table": [0.5, 1, 2, 4, 8, 16],
        "faqs": [
            ("How many MB is 1 GB?", "1 gigabyte equals 1024 megabytes."),
            ("How many MB is 2 GB?", "2 gigabytes equals 2048 megabytes."),
            ("Is 1000 MB the same as 1 GB?", "Close. Storage is often sold as 1000 MB per GB, while software reports 1024 MB."),
        ],
    },
]


def convert_value(conv: dict, value: float) -> float:
    """Apply the conversion in Python, used to pre-render tables."""
    if conv.get("kind") == "temp":
        c = value if conv["from"] == "C" else (value - 32) * 5 / 9
        if conv["to"] == "C":
            return c
        if conv["to"] == "F":
            return c * 9 / 5 + 32
        return c + 273.15
    return value * conv["factor"]


def fmt(x: float) -> str:
    """Format a number without trailing zeros, keeping small values readable."""
    if x == int(x) and abs(x) < 1e15:
        return str(int(x))
    return f"{x:.6g}"

ROOT = Path(__file__).resolve().parent
SITE = ROOT / "site"
# These can also be set as environment variables so a host like Netlify can
# configure the site without editing this file.
SITE_URL = os.environ.get("SITE_URL", "https://example.com").rstrip("/")
CONTACT_EMAIL = os.environ.get("CONTACT_EMAIL", "you@example.com")
SITE_NAME = os.environ.get("SITE_NAME", "ToolBox")


# --- Google Analytics 4 -------------------------------------------------
# Paste your GA4 measurement ID (looks like "G-XXXXXXXXXX") to enable
# analytics on every page. Leave empty to keep analytics off.
GA_MEASUREMENT_ID = os.environ.get("GA_MEASUREMENT_ID", "")
# ------------------------------------------------------------------------

# --- Search Console verification ----------------------------------------
# Google Search Console gives you a meta tag with a content value. Set
# GOOGLE_SITE_VERIFICATION to that value (the part inside content="...") and
# every page will carry the tag. Bing uses the same idea: BING_SITE_VERIFICATION.
GOOGLE_SITE_VERIFICATION = os.environ.get("GOOGLE_SITE_VERIFICATION", "")
BING_SITE_VERIFICATION = os.environ.get("BING_SITE_VERIFICATION", "")
# Google also offers "HTML file" verification. Set this to the downloaded file
# name (for example "google3e2e52f02618f536.html") and the build creates it.
GOOGLE_SITE_VERIFICATION_FILE = os.environ.get("GOOGLE_SITE_VERIFICATION_FILE", "")
# ------------------------------------------------------------------------

