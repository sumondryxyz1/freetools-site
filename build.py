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

AD_HEADER = ""
AD_INARTICLE = ""
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

TOOLS = [
    {
        "slug": "word-counter",
        "name": "Word Counter",
        "title": "Free Word Counter - Count Words, Characters & Reading Time",
        "desc": "Paste your text to instantly count words, characters, sentences and estimated reading time. Free, private and works offline in your browser.",
        "keywords": "word counter, character counter, count words online, reading time calculator",
        "body": """
      <div class="card">
        <label for="wc-input">Your text</label>
        <textarea id="wc-input" rows="10" placeholder="Paste or type your text here..."></textarea>
        <div class="stats" id="wc-stats">
          <div><span id="wc-words">0</span><small>Words</small></div>
          <div><span id="wc-chars">0</span><small>Characters</small></div>
          <div><span id="wc-sentences">0</span><small>Sentences</small></div>
          <div><span id="wc-minutes">0</span><small>Min read</small></div>
        </div>
      </div>
      <div class="card">
        <button class="btn" onclick="wcClear()">Clear</button>
      </div>
""",
        "script": """
  const input = document.getElementById('wc-input');
  function wcUpdate() {
    const text = input.value;
    const words = text.trim() ? text.trim().split(/\\s+/).length : 0;
    document.getElementById('wc-words').textContent = words;
    document.getElementById('wc-chars').textContent = text.length;
    document.getElementById('wc-sentences').textContent = text.trim() ? (text.match(/[.!?]+/g) || []).length : 0;
    document.getElementById('wc-minutes').textContent = Math.max(1, Math.round(words / 200));
  }
  function wcClear() { input.value = ''; wcUpdate(); }
  input.addEventListener('input', wcUpdate);
  wcUpdate();
""",
    },
    {
        "slug": "case-converter",
        "name": "Case Converter",
        "title": "Free Case Converter - Uppercase, Lowercase & Title Case",
        "desc": "Convert text to UPPERCASE, lowercase, Title Case or Sentence case instantly. A simple, free online text case changer.",
        "keywords": "case converter, uppercase converter, lowercase converter, title case generator",
        "body": """
      <div class="card">
        <textarea id="cc-input" rows="8" placeholder="Type or paste text..."></textarea>
        <div class="row">
          <button class="btn" onclick="ccApply('upper')">UPPERCASE</button>
          <button class="btn" onclick="ccApply('lower')">lowercase</button>
          <button class="btn" onclick="ccApply('title')">Title Case</button>
          <button class="btn" onclick="ccApply('sentence')">Sentence case</button>
          <button class="btn ghost" onclick="ccCopy()">Copy</button>
        </div>
      </div>
""",
        "script": """
  const cc = document.getElementById('cc-input');
  function ccApply(mode) {
    const t = cc.value;
    if (mode === 'upper') cc.value = t.toUpperCase();
    else if (mode === 'lower') cc.value = t.toLowerCase();
    else if (mode === 'title') cc.value = t.replace(/\\w\\S*/g, w => w[0].toUpperCase() + w.slice(1).toLowerCase());
    else cc.value = t.toLowerCase().replace(/(^\\s*\\w|\\.\\s*\\w)/g, m => m.toUpperCase());
  }
  function ccCopy() { cc.select(); document.execCommand('copy'); }
""",
    },
    {
        "slug": "qr-generator",
        "name": "QR Code Generator",
        "title": "Free QR Code Generator - Create QR Codes Instantly",
        "desc": "Generate a QR code for any link or text and download it as an image. Free, no sign-up, works in your browser.",
        "keywords": "qr code generator, free qr code, create qr code online, qr code for link",
        "body": """
      <div class="card">
        <input id="qr-input" type="text" placeholder="https://your-link.com" value="https://example.com">
        <button class="btn" onclick="qrMake()">Generate</button>
        <div id="qr-box" class="qr-box"></div>
      </div>
""",
        "script": """
  function qrMake() {
    const val = document.getElementById('qr-input').value.trim() || 'https://example.com';
    const url = 'https://api.qrserver.com/v1/create-qr-code/?size=240x240&data=' + encodeURIComponent(val);
    document.getElementById('qr-box').innerHTML =
      '<img alt="QR code" src="' + url + '"><p><a href="' + url + '" download="qr.png">Download image</a></p>';
  }
  qrMake();
""",
    },
    {
        "slug": "password-generator",
        "name": "Password Generator",
        "title": "Free Strong Password Generator - Secure Random Passwords",
        "desc": "Create strong, random passwords with custom length and character sets. Generated locally in your browser, nothing is sent to a server.",
        "keywords": "password generator, strong password, random password generator, secure password",
        "body": """
      <div class="card">
        <label for="pg-len">Length: <span id="pg-lenval">16</span></label>
        <input id="pg-len" type="range" min="6" max="48" value="16">
        <div class="row">
          <label><input type="checkbox" id="pg-upper" checked> A-Z</label>
          <label><input type="checkbox" id="pg-lower" checked> a-z</label>
          <label><input type="checkbox" id="pg-num" checked> 0-9</label>
          <label><input type="checkbox" id="pg-sym" checked> !@#</label>
        </div>
        <div class="output" id="pg-out"></div>
        <div class="row">
          <button class="btn" onclick="pgMake()">Generate</button>
          <button class="btn ghost" onclick="pgCopy()">Copy</button>
        </div>
      </div>
""",
        "script": """
  const pgLen = document.getElementById('pg-len');
  pgLen.addEventListener('input', () => { document.getElementById('pg-lenval').textContent = pgLen.value; pgMake(); });
  function pgMake() {
    let chars = '';
    if (document.getElementById('pg-upper').checked) chars += 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
    if (document.getElementById('pg-lower').checked) chars += 'abcdefghijklmnopqrstuvwxyz';
    if (document.getElementById('pg-num').checked) chars += '0123456789';
    if (document.getElementById('pg-sym').checked) chars += '!@#$%^&*()-_=+[]{}';
    if (!chars) chars = 'abcdefghijklmnopqrstuvwxyz';
    const len = +pgLen.value;
    const arr = new Uint32Array(len);
    crypto.getRandomValues(arr);
    let out = '';
    for (let i = 0; i < len; i++) out += chars[arr[i] % chars.length];
    document.getElementById('pg-out').textContent = out;
  }
  function pgCopy() {
    const el = document.getElementById('pg-out');
    navigator.clipboard && navigator.clipboard.writeText(el.textContent);
  }
  pgMake();
""",
    },
    {
        "slug": "lorem-ipsum",
        "name": "Lorem Ipsum Generator",
        "title": "Free Lorem Ipsum Generator - Dummy Placeholder Text",
        "desc": "Generate Lorem Ipsum placeholder text by paragraph, sentence or word count. Ideal for designers and developers.",
        "keywords": "lorem ipsum generator, dummy text, placeholder text generator, filler text",
        "body": """
      <div class="card">
        <div class="row">
          <label>Paragraphs <input id="li-count" type="number" min="1" max="20" value="3"></label>
          <button class="btn" onclick="liMake()">Generate</button>
          <button class="btn ghost" onclick="liCopy()">Copy</button>
        </div>
        <div class="output" id="li-out"></div>
      </div>
""",
        "script": """
  const LI_WORDS = 'lorem ipsum dolor sit amet consectetur adipiscing elit sed do eiusmod tempor incididunt ut labore et dolore magna aliqua enim ad minim veniam quis nostrud exercitation ullamco laboris nisi aliquip ex ea commodo consequat'.split(' ');
  function liMake() {
    const n = Math.min(20, Math.max(1, +document.getElementById('li-count').value || 1));
    let out = '';
    for (let p = 0; p < n; p++) {
      const len = 30 + Math.floor(Math.random() * 30);
      let s = '';
      for (let i = 0; i < len; i++) s += LI_WORDS[Math.floor(Math.random() * LI_WORDS.length)] + ' ';
      out += '<p>' + s.trim().replace(/^./, c => c.toUpperCase()) + '.</p>';
    }
    document.getElementById('li-out').innerHTML = out;
  }
  function liCopy() { navigator.clipboard && navigator.clipboard.writeText(document.getElementById('li-out').innerText); }
  liMake();
""",
    },
    {
        "slug": "age-calculator",
        "name": "Age Calculator",
        "title": "Free Age Calculator - Calculate Your Exact Age in Years, Months & Days",
        "desc": "Find your exact age in years, months and days from your date of birth. Free online age calculator.",
        "keywords": "age calculator, calculate age, how old am i, date of birth calculator",
        "body": """
      <div class="card">
        <label for="age-dob">Date of birth</label>
        <input id="age-dob" type="date">
        <button class="btn" onclick="ageCalc()">Calculate age</button>
        <div class="output" id="age-out"></div>
      </div>
""",
        "script": """
  function ageCalc() {
    const v = document.getElementById('age-dob').value;
    const out = document.getElementById('age-out');
    if (!v) { out.textContent = 'Please choose your date of birth.'; return; }
    const dob = new Date(v + 'T00:00:00');
    const now = new Date();
    if (dob > now) { out.textContent = 'Date of birth cannot be in the future.'; return; }
    let years = now.getFullYear() - dob.getFullYear();
    let months = now.getMonth() - dob.getMonth();
    let days = now.getDate() - dob.getDate();
    if (days < 0) { months--; days += new Date(now.getFullYear(), now.getMonth(), 0).getDate(); }
    if (months < 0) { years--; months += 12; }
    const totalDays = Math.floor((now - dob) / 86400000);
    out.innerHTML = '<strong>' + years + ' years, ' + months + ' months, ' + days + ' days</strong><br>' +
      'About ' + totalDays.toLocaleString() + ' days, or ' + Math.floor(totalDays/7).toLocaleString() + ' weeks.';
  }
""",
    },
    {
        "slug": "percentage-calculator",
        "name": "Percentage Calculator",
        "title": "Free Percentage Calculator - Percent Of, Increase & Decrease",
        "desc": "Calculate percentages online: what is X% of Y, X is what percent of Y, and percentage increase or decrease.",
        "keywords": "percentage calculator, percent of, percentage increase calculator, percentage decrease",
        "body": """
      <div class="card">
        <h3>What is X% of Y?</h3>
        <div class="row">
          <input id="p1a" type="number" placeholder="X" style="max-width:120px">
          <span>% of</span>
          <input id="p1b" type="number" placeholder="Y" style="max-width:120px">
          <button class="btn" onclick="pct1()">=</button>
          <strong id="p1r"></strong>
        </div>
      </div>
      <div class="card">
        <h3>X is what percent of Y?</h3>
        <div class="row">
          <input id="p2a" type="number" placeholder="X" style="max-width:120px">
          <span>is what % of</span>
          <input id="p2b" type="number" placeholder="Y" style="max-width:120px">
          <button class="btn" onclick="pct2()">=</button>
          <strong id="p2r"></strong>
        </div>
      </div>
      <div class="card">
        <h3>Percentage change (from &rarr; to)</h3>
        <div class="row">
          <input id="p3a" type="number" placeholder="from" style="max-width:120px">
          <input id="p3b" type="number" placeholder="to" style="max-width:120px">
          <button class="btn" onclick="pct3()">=</button>
          <strong id="p3r"></strong>
        </div>
      </div>
""",
        "script": """
  const pv = id => parseFloat(document.getElementById(id).value);
  function pct1() { document.getElementById('p1r').textContent = isNaN(pv('p1a'))||isNaN(pv('p1b')) ? '—' : (pv('p1a')/100*pv('p1b')).toLocaleString(); }
  function pct2() { document.getElementById('p2r').textContent = isNaN(pv('p2a'))||!pv('p2b') ? '—' : (pv('p2a')/pv('p2b')*100).toFixed(2) + '%'; }
  function pct3() { const a=pv('p3a'), b=pv('p3b'); document.getElementById('p3r').textContent = isNaN(a)||!a ? '—' : (((b-a)/Math.abs(a))*100).toFixed(2) + '%'; }
""",
    },
    {
        "slug": "bmi-calculator",
        "name": "BMI Calculator",
        "title": "Free BMI Calculator - Body Mass Index for Adults",
        "desc": "Calculate your Body Mass Index from height and weight and see your category. Free online BMI calculator.",
        "keywords": "bmi calculator, body mass index, bmi chart, healthy weight calculator",
        "body": """
      <div class="card">
        <div class="row">
          <label>Height (cm) <input id="bmi-h" type="number" value="170" style="max-width:120px"></label>
          <label>Weight (kg) <input id="bmi-w" type="number" value="70" style="max-width:120px"></label>
        </div>
        <button class="btn" onclick="bmiCalc()">Calculate BMI</button>
        <div class="output" id="bmi-out"></div>
      </div>
""",
        "script": """
  function bmiCalc() {
    const h = parseFloat(document.getElementById('bmi-h').value) / 100;
    const w = parseFloat(document.getElementById('bmi-w').value);
    const out = document.getElementById('bmi-out');
    if (!h || !w || h <= 0 || w <= 0) { out.textContent = 'Enter a valid height and weight.'; return; }
    const bmi = w / (h * h);
    let cat = 'Normal weight';
    if (bmi < 18.5) cat = 'Underweight';
    else if (bmi >= 25 && bmi < 30) cat = 'Overweight';
    else if (bmi >= 30) cat = 'Obese';
    out.innerHTML = '<strong>BMI: ' + bmi.toFixed(1) + '</strong> — ' + cat;
  }
""",
    },
    {
        "slug": "unit-converter",
        "name": "Unit Converter",
        "title": "Free Unit Converter - Length, Weight & Temperature",
        "desc": "Convert between common units of length, weight and temperature instantly. Free online unit converter.",
        "keywords": "unit converter, length converter, weight converter, temperature converter, cm to inches",
        "body": """
      <div class="card">
        <div class="row">
          <select id="uc-cat" onchange="ucFill()">
            <option value="length">Length</option>
            <option value="weight">Weight</option>
            <option value="temp">Temperature</option>
          </select>
          <input id="uc-val" type="number" value="1" style="max-width:120px">
          <select id="uc-from"></select>
          <span>to</span>
          <select id="uc-to"></select>
          <button class="btn" onclick="ucConvert()">Convert</button>
        </div>
        <div class="output" id="uc-out"></div>
      </div>
""",
        "script": """
  const UC = {
    length: { m:1, km:1000, cm:0.01, mm:0.001, inch:0.0254, ft:0.3048, yd:0.9144, mile:1609.344 },
    weight: { kg:1, g:0.001, mg:0.000001, lb:0.45359237, oz:0.028349523125, ton:1000 }
  };
  function ucFill() {
    const cat = document.getElementById('uc-cat').value;
    const from = document.getElementById('uc-from'), to = document.getElementById('uc-to');
    from.innerHTML = ''; to.innerHTML = '';
    const units = cat === 'temp' ? ['C','F','K'] : Object.keys(UC[cat]);
    units.forEach(u => { from.add(new Option(u,u)); to.add(new Option(u,u)); });
    if (units.length > 1) to.value = units[1];
    ucConvert();
  }
  function ucConvert() {
    const cat = document.getElementById('uc-cat').value;
    const v = parseFloat(document.getElementById('uc-val').value);
    const f = document.getElementById('uc-from').value, t = document.getElementById('uc-to').value;
    const out = document.getElementById('uc-out');
    if (isNaN(v)) { out.textContent = 'Enter a number.'; return; }
    let res;
    if (cat === 'temp') {
      const c = f === 'C' ? v : f === 'F' ? (v - 32) * 5/9 : v - 273.15;
      res = t === 'C' ? c : t === 'F' ? c * 9/5 + 32 : c + 273.15;
    } else {
      res = v * UC[cat][f] / UC[cat][t];
    }
    out.innerHTML = '<strong>' + v + ' ' + f + ' = ' + (+res.toFixed(6)) + ' ' + t + '</strong>';
  }
  ucFill();
""",
    },
    {
        "slug": "image-compressor",
        "name": "Image Compressor",
        "title": "Free Image Compressor - Compress JPG & PNG Online",
        "desc": "Compress JPG and PNG images in your browser without uploading them. Adjust quality and download the smaller file.",
        "keywords": "image compressor, compress jpg, compress png, reduce image size online",
        "body": """
      <div class="card">
        <input id="ic-file" type="file" accept="image/*">
        <label for="ic-q">Quality: <span id="ic-qv">70</span>%</label>
        <input id="ic-q" type="range" min="10" max="100" value="70">
        <button class="btn" onclick="icCompress()">Compress</button>
        <div class="output" id="ic-out"></div>
      </div>
""",
        "script": """
  const icQ = document.getElementById('ic-q');
  icQ.addEventListener('input', () => document.getElementById('ic-qv').textContent = icQ.value);
  function icCompress() {
    const file = document.getElementById('ic-file').files[0];
    const out = document.getElementById('ic-out');
    if (!file) { out.textContent = 'Choose an image first.'; return; }
    const img = new Image();
    img.onload = () => {
      const c = document.createElement('canvas');
      c.width = img.width; c.height = img.height;
      c.getContext('2d').drawImage(img, 0, 0);
      c.toBlob(blob => {
        const url = URL.createObjectURL(blob);
        const saved = Math.max(0, Math.round((1 - blob.size / file.size) * 100));
        out.innerHTML = 'Original: ' + Math.round(file.size/1024) + ' KB → Compressed: ' +
          Math.round(blob.size/1024) + ' KB (' + saved + '% smaller)<br>' +
          '<a href="' + url + '" download="compressed.jpg">Download compressed image</a>';
      }, 'image/jpeg', icQ.value / 100);
    };
    img.onerror = () => out.textContent = 'Could not read that image.';
    img.src = URL.createObjectURL(file);
  }
""",
    },
    {
        "slug": "json-formatter",
        "name": "JSON Formatter",
        "title": "Free JSON Formatter & Validator - Beautify JSON Online",
        "desc": "Format, beautify and validate JSON instantly in your browser. Spot syntax errors with a clear message.",
        "keywords": "json formatter, json validator, beautify json, json beautifier online",
        "body": """
      <div class="card">
        <label for="jf-in">JSON input</label>
        <textarea id="jf-in" rows="8" placeholder='{"hello":"world"}'></textarea>
        <div class="row">
          <button class="btn" onclick="jfFormat(2)">Format</button>
          <button class="btn" onclick="jfFormat(0)">Minify</button>
          <button class="btn ghost" onclick="jfClear()">Clear</button>
        </div>
        <div class="output" id="jf-out"></div>
      </div>
""",
        "script": """
  function jfFormat(space) {
    const out = document.getElementById('jf-out');
    try {
      const obj = JSON.parse(document.getElementById('jf-in').value);
      out.textContent = JSON.stringify(obj, null, space);
      out.style.color = '';
    } catch (e) { out.textContent = 'Invalid JSON: ' + e.message; out.style.color = '#f87171'; }
  }
  function jfClear() { document.getElementById('jf-in').value = ''; document.getElementById('jf-out').textContent = ''; }
""",
    },
    {
        "slug": "base64-encoder",
        "name": "Base64 Encoder",
        "title": "Free Base64 Encoder & Decoder - Encode Text Online",
        "desc": "Encode text to Base64 or decode Base64 back to text. Handles Unicode safely, all in your browser.",
        "keywords": "base64 encoder, base64 decoder, encode base64, decode base64 online",
        "body": """
      <div class="card">
        <label for="b64-in">Text or Base64</label>
        <textarea id="b64-in" rows="6"></textarea>
        <div class="row">
          <button class="btn" onclick="b64Do('enc')">Encode to Base64</button>
          <button class="btn" onclick="b64Do('dec')">Decode from Base64</button>
        </div>
        <div class="output" id="b64-out"></div>
      </div>
""",
        "script": """
  function b64Do(mode) {
    const out = document.getElementById('b64-out');
    const v = document.getElementById('b64-in').value;
    try {
      if (mode === 'enc') out.textContent = btoa(unescape(encodeURIComponent(v)));
      else out.textContent = decodeURIComponent(escape(atob(v.trim())));
    } catch (e) { out.textContent = 'Error: input is not valid for this operation.'; }
  }
""",
    },
    {
        "slug": "random-number-generator",
        "name": "Random Number Generator",
        "title": "Free Random Number Generator - Pick Numbers in a Range",
        "desc": "Generate random numbers within a range, with or without duplicates. Great for draws and giveaways.",
        "keywords": "random number generator, random number picker, rng, lottery number generator",
        "body": """
      <div class="card">
        <div class="row">
          <label>Min <input id="rn-min" type="number" value="1" style="max-width:100px"></label>
          <label>Max <input id="rn-max" type="number" value="100" style="max-width:100px"></label>
          <label>How many <input id="rn-count" type="number" value="1" style="max-width:100px"></label>
          <label><input type="checkbox" id="rn-uniq" checked> Unique</label>
        </div>
        <button class="btn" onclick="rnGen()">Generate</button>
        <div class="output" id="rn-out"></div>
      </div>
""",
        "script": """
  function rnGen() {
    const min = Math.ceil(+document.getElementById('rn-min').value);
    const max = Math.floor(+document.getElementById('rn-max').value);
    const count = Math.max(1, Math.min(1000, +document.getElementById('rn-count').value || 1));
    const uniq = document.getElementById('rn-uniq').checked;
    const out = document.getElementById('rn-out');
    if (max < min) { out.textContent = 'Max must be greater than min.'; return; }
    const range = max - min + 1;
    if (uniq && count > range) { out.textContent = 'Cannot pick ' + count + ' unique numbers from a range of ' + range + '.'; return; }
    const res = [];
    if (uniq) {
      const pool = Array.from({length: range}, (_, i) => min + i);
      for (let i = 0; i < count; i++) res.push(pool.splice(Math.floor(Math.random()*pool.length), 1)[0]);
    } else {
      for (let i = 0; i < count; i++) res.push(min + Math.floor(Math.random()*range));
    }
    out.textContent = res.join(', ');
  }
  rnGen();
""",
    },
    {
        "slug": "unix-timestamp",
        "name": "Unix Timestamp Converter",
        "title": "Unix Timestamp Converter - Epoch to Date and Back",
        "desc": "Convert a Unix timestamp to a human-readable date, or a date to a Unix timestamp. Shows the live current epoch time.",
        "keywords": "unix timestamp converter, epoch converter, timestamp to date, epoch time now",
        "body": """
      <div class="card">
        <h3>Current Unix time</h3>
        <div class="output"><strong id="ts-now"></strong></div>
      </div>
      <div class="card">
        <h3>Timestamp &rarr; Date</h3>
        <div class="row">
          <input id="ts-in" type="number" placeholder="e.g. 1700000000" style="max-width:220px">
          <button class="btn" onclick="tsToDate()">Convert</button>
          <strong id="ts-dater"></strong>
        </div>
      </div>
      <div class="card">
        <h3>Date &rarr; Timestamp</h3>
        <div class="row">
          <input id="ts-date" type="datetime-local">
          <button class="btn" onclick="dateToTs()">Convert</button>
          <strong id="ts-tsr"></strong>
        </div>
      </div>
""",
        "script": """
  function tsTick() { document.getElementById('ts-now').textContent = Math.floor(Date.now()/1000); }
  setInterval(tsTick, 1000); tsTick();
  function tsToDate() {
    const v = +document.getElementById('ts-in').value;
    document.getElementById('ts-dater').textContent = v ? new Date(v*1000).toString() : '—';
  }
  function dateToTs() {
    const v = document.getElementById('ts-date').value;
    document.getElementById('ts-tsr').textContent = v ? Math.floor(new Date(v).getTime()/1000) : '—';
  }
""",
    },
    {
        "slug": "color-converter",
        "name": "Color Converter",
        "title": "Free Color Converter - HEX, RGB and HSL",
        "desc": "Convert colors between HEX, RGB and HSL and preview the colour. Free online colour converter for designers and developers.",
        "keywords": "hex to rgb, rgb to hex, color converter, hsl converter, color picker",
        "body": """
      <div class="card">
        <div class="row">
          <input id="col-in" type="text" value="#38bdf8" style="max-width:160px">
          <input id="col-pick" type="color" value="#38bdf8">
          <button class="btn" onclick="colConvert()">Convert</button>
        </div>
        <div class="row"><div id="col-swatch" style="width:100%;height:60px;border-radius:8px;background:#38bdf8"></div></div>
        <div class="output" id="col-out"></div>
      </div>
""",
        "script": """
  const colIn = document.getElementById('col-in'), colPick = document.getElementById('col-pick');
  colPick.addEventListener('input', () => { colIn.value = colPick.value; colConvert(); });
  function colConvert() {
    let hex = colIn.value.trim().replace('#','');
    if (hex.length === 3) hex = hex.split('').map(c => c+c).join('');
    if (!/^[0-9a-fA-F]{6}$/.test(hex)) { document.getElementById('col-out').textContent = 'Enter a valid HEX colour, e.g. #38bdf8.'; return; }
    const r = parseInt(hex.slice(0,2),16), g = parseInt(hex.slice(2,4),16), b = parseInt(hex.slice(4,6),16);
    const rr = r/255, gg = g/255, bb = b/255;
    const max = Math.max(rr,gg,bb), min = Math.min(rr,gg,bb);
    let h = 0, s = 0;
    const l = (max+min)/2;
    if (max !== min) {
      const d = max-min;
      s = l > 0.5 ? d/(2-max-min) : d/(max+min);
      h = max === rr ? (gg-bb)/d + (gg<bb?6:0) : max === gg ? (bb-rr)/d + 2 : (rr-gg)/d + 4;
      h *= 60;
    }
    document.getElementById('col-swatch').style.background = '#'+hex;
    colPick.value = '#'+hex;
    document.getElementById('col-out').innerHTML =
      '<strong>HEX</strong> #' + hex.toLowerCase() + '<br>' +
      '<strong>RGB</strong> rgb(' + r + ', ' + g + ', ' + b + ')<br>' +
      '<strong>HSL</strong> hsl(' + Math.round(h) + ', ' + Math.round(s*100) + '%, ' + Math.round(l*100) + '%)';
  }
  colConvert();
""",
    },
    {
        "slug": "image-resizer",
        "name": "Image Resizer",
        "title": "Free Image Resizer - Resize Photos Online in Your Browser",
        "desc": "Resize images to any width and height online. Keep the aspect ratio and download instantly, without uploading your photos.",
        "keywords": "image resizer, resize image online, resize photo, change image size",
        "body": """
      <div class="card">
        <input id="ir-file" type="file" accept="image/*">
        <div class="row">
          <label>Width <input id="ir-w" type="number" placeholder="px" style="max-width:120px"></label>
          <label>Height <input id="ir-h" type="number" placeholder="px" style="max-width:120px"></label>
          <label><input type="checkbox" id="ir-ratio" checked> Keep ratio</label>
        </div>
        <button class="btn" onclick="irResize()">Resize</button>
        <div class="output" id="ir-out"></div>
      </div>
""",
        "script": """
  const irFile = document.getElementById('ir-file');
  let irImg = null;
  irFile.addEventListener('change', () => {
    const f = irFile.files[0]; if (!f) return;
    irImg = new Image();
    irImg.onload = () => {
      document.getElementById('ir-w').value = irImg.width;
      document.getElementById('ir-h').value = irImg.height;
      document.getElementById('ir-out').textContent = 'Loaded ' + irImg.width + 'x' + irImg.height + ' image.';
    };
    irImg.src = URL.createObjectURL(f);
  });
  document.getElementById('ir-w').addEventListener('input', () => {
    if (irImg && document.getElementById('ir-ratio').checked) {
      document.getElementById('ir-h').value = Math.round(document.getElementById('ir-w').value * irImg.height / irImg.width);
    }
  });
  function irResize() {
    const out = document.getElementById('ir-out');
    if (!irImg) { out.textContent = 'Choose an image first.'; return; }
    const w = Math.max(1, +document.getElementById('ir-w').value || irImg.width);
    const h = Math.max(1, +document.getElementById('ir-h').value || irImg.height);
    const c = document.createElement('canvas'); c.width = w; c.height = h;
    c.getContext('2d').drawImage(irImg, 0, 0, w, h);
    c.toBlob(blob => {
      out.innerHTML = 'Resized to ' + w + 'x' + h + ' (' + Math.round(blob.size/1024) + ' KB)<br>' +
        '<a href="' + URL.createObjectURL(blob) + '" download="resized.png">Download resized image</a>';
    }, 'image/png');
  }
""",
    },
    {
        "slug": "pomodoro-timer",
        "name": "Pomodoro Timer",
        "title": "Free Pomodoro Timer - 25 Minute Focus Timer Online",
        "desc": "A simple Pomodoro timer with 25 minute work and 5 minute break sessions. Stay focused and track your productivity.",
        "keywords": "pomodoro timer, focus timer, 25 minute timer, study timer online",
        "body": """
      <div class="card" style="text-align:center">
        <div class="output" id="pomo-display" style="font-size:3rem;font-weight:700">25:00</div>
        <div class="row" style="justify-content:center">
          <button class="btn" id="pomo-start" onclick="pomoToggle()">Start</button>
          <button class="btn ghost" onclick="pomoReset()">Reset</button>
          <button class="btn ghost" onclick="pomoMode('work')">Work 25m</button>
          <button class="btn ghost" onclick="pomoMode('break')">Break 5m</button>
        </div>
        <p id="pomo-label" style="color:var(--muted)">Focus session</p>
      </div>
""",
        "script": """
  let pomoLeft = 25 * 60, pomoRunning = false, pomoTimer = null, pomoName = 'Focus session';
  function pomoRender() {
    const m = Math.floor(pomoLeft/60), s = pomoLeft % 60;
    document.getElementById('pomo-display').textContent = (m<10?'0':'')+m+':'+(s<10?'0':'')+s;
  }
  function pomoToggle() {
    pomoRunning = !pomoRunning;
    document.getElementById('pomo-start').textContent = pomoRunning ? 'Pause' : 'Start';
    if (pomoRunning) {
      pomoTimer = setInterval(() => {
        if (pomoLeft > 0) { pomoLeft--; pomoRender(); }
        else { clearInterval(pomoTimer); pomoRunning = false;
          document.getElementById('pomo-start').textContent = 'Start';
          try { new AudioContext(); } catch(e) {}
        }
      }, 1000);
    } else { clearInterval(pomoTimer); }
  }
  function pomoReset() { clearInterval(pomoTimer); pomoRunning = false; document.getElementById('pomo-start').textContent='Start'; pomoMode(pomoName==='Break time'?'break':'work'); }
  function pomoMode(mode) {
    clearInterval(pomoTimer); pomoRunning = false; document.getElementById('pomo-start').textContent='Start';
    pomoName = mode === 'work' ? 'Focus session' : 'Break time';
    pomoLeft = (mode === 'work' ? 25 : 5) * 60;
    document.getElementById('pomo-label').textContent = pomoName;
    pomoRender();
  }
  pomoRender();
""",
    },
    {
        "slug": "hash-generator",
        "name": "Hash Generator",
        "title": "Free SHA-256 & MD5 Hash Generator Online",
        "desc": "Generate SHA-256, SHA-1 and SHA-512 hashes of any text, plus a non-cryptographic MD5-style checksum. Runs in your browser.",
        "keywords": "sha256 generator, md5 generator, hash generator, sha512 online",
        "body": """
      <div class="card">
        <label for="hash-in">Text to hash</label>
        <textarea id="hash-in" rows="4" placeholder="Type text..."></textarea>
        <button class="btn" onclick="hashRun()">Generate hashes</button>
        <div class="output" id="hash-out"></div>
      </div>
""",
        "script": """
  async function hashRun() {
    const out = document.getElementById('hash-out');
    const data = new TextEncoder().encode(document.getElementById('hash-in').value);
    const algs = ['SHA-1','SHA-256','SHA-512'];
    let res = '';
    for (const alg of algs) {
      const buf = await crypto.subtle.digest(alg, data);
      res += '<strong>' + alg + '</strong>: ' + Array.from(new Uint8Array(buf)).map(b=>b.toString(16).padStart(2,'0')).join('') + '<br>';
    }
    out.innerHTML = res;
  }
""",
    },
    {
        "slug": "url-encoder",
        "name": "URL Encoder / Decoder",
        "title": "Free URL Encoder & Decoder - Percent-Encoding Online",
        "desc": "Encode text for use in URLs (percent-encoding) or decode an encoded URL back to readable text. Free and instant.",
        "keywords": "url encoder, url decoder, percent encoding, encode url online",
        "body": """
      <div class="card">
        <label for="url-in">Text or encoded URL</label>
        <textarea id="url-in" rows="5"></textarea>
        <div class="row">
          <button class="btn" onclick="urlDo('enc')">Encode</button>
          <button class="btn" onclick="urlDo('dec')">Decode</button>
        </div>
        <div class="output" id="url-out"></div>
      </div>
""",
        "script": """
  function urlDo(mode) {
    const out = document.getElementById('url-out');
    try {
      out.textContent = mode === 'enc'
        ? encodeURIComponent(document.getElementById('url-in').value)
        : decodeURIComponent(document.getElementById('url-in').value);
    } catch (e) { out.textContent = 'Error: input is not valid for decoding.'; }
  }
""",
    },
    {
        "slug": "roman-numeral-converter",
        "name": "Roman Numeral Converter",
        "title": "Free Roman Numeral Converter - Numbers to Roman Numerals",
        "desc": "Convert numbers to Roman numerals and Roman numerals back to numbers. Supports 1 to 3999.",
        "keywords": "roman numeral converter, numbers to roman numerals, roman numerals to numbers",
        "body": """
      <div class="card">
        <div class="row">
          <input id="rn2-input" type="text" placeholder="e.g. 1987 or MCMLXXXVII" style="max-width:260px">
          <button class="btn" onclick="romanConvert()">Convert</button>
        </div>
        <div class="output" id="rn2-out"></div>
      </div>
""",
        "script": """
  const ROMAN = [[1000,'M'],[900,'CM'],[500,'D'],[400,'CD'],[100,'C'],[90,'XC'],[50,'L'],[40,'XL'],[10,'X'],[9,'IX'],[5,'V'],[4,'IV'],[1,'I']];
  function romanConvert() {
    const v = document.getElementById('rn2-input').value.trim().toUpperCase();
    const out = document.getElementById('rn2-out');
    if (/^[0-9]+$/.test(v)) {
      let n = +v;
      if (n < 1 || n > 3999) { out.textContent = 'Please enter a number from 1 to 3999.'; return; }
      let r = '';
      for (const [val, sym] of ROMAN) while (n >= val) { r += sym; n -= val; }
      out.innerHTML = '<strong>' + v + ' = ' + r + '</strong>';
    } else if (/^[MDCLXVI]+$/.test(v)) {
      let n = 0;
      for (let i = 0; i < v.length; i++) {
        const cur = ROMAN.find(x => x[1] === v[i])[0];
        const nxt = ROMAN.find(x => x[1] === v[i+1]);
        n += (nxt && cur < nxt[0]) ? -cur : cur;
      }
      out.innerHTML = '<strong>' + v + ' = ' + n + '</strong>';
    } else { out.textContent = 'Enter a number (1-3999) or a Roman numeral.'; }
  }
""",
    },
    {
        "slug": "tip-calculator",
        "name": "Tip Calculator",
        "title": "Free Tip Calculator - Split a Bill and Calculate Tips",
        "desc": "Calculate the tip and split a restaurant bill between any number of people. Free online tip calculator.",
        "keywords": "tip calculator, bill splitter, calculate tip, restaurant tip calculator",
        "body": """
      <div class="card">
        <div class="row">
          <label>Bill <input id="tip-bill" type="number" value="50" style="max-width:120px"></label>
          <label>Tip % <input id="tip-pct" type="number" value="15" style="max-width:100px"></label>
          <label>People <input id="tip-people" type="number" value="2" min="1" style="max-width:100px"></label>
          <button class="btn" onclick="tipCalc()">Calculate</button>
        </div>
        <div class="output" id="tip-out"></div>
      </div>
""",
        "script": """
  function tipCalc() {
    const bill = +document.getElementById('tip-bill').value || 0;
    const pct = +document.getElementById('tip-pct').value || 0;
    const people = Math.max(1, +document.getElementById('tip-people').value || 1);
    const tip = bill * pct / 100;
    const total = bill + tip;
    document.getElementById('tip-out').innerHTML =
      '<strong>Tip: ' + tip.toFixed(2) + '</strong><br>' +
      'Total: ' + total.toFixed(2) + '<br>' +
      'Each person pays: ' + (total / people).toFixed(2);
  }
  tipCalc();
""",
    },
    {
        "slug": "date-difference",
        "name": "Date Difference Calculator",
        "title": "Free Date Difference Calculator - Days Between Two Dates",
        "desc": "Calculate the number of days, weeks and months between two dates. Free online date difference calculator.",
        "keywords": "date difference calculator, days between dates, date calculator, how many days until",
        "body": """
      <div class="card">
        <div class="row">
          <label>From <input id="dd-from" type="date"></label>
          <label>To <input id="dd-to" type="date"></label>
          <button class="btn" onclick="ddCalc()">Calculate</button>
        </div>
        <div class="output" id="dd-out"></div>
      </div>
""",
        "script": """
  function ddCalc() {
    const f = document.getElementById('dd-from').value, t = document.getElementById('dd-to').value;
    const out = document.getElementById('dd-out');
    if (!f || !t) { out.textContent = 'Pick both dates.'; return; }
    const a = new Date(f+'T00:00:00'), b = new Date(t+'T00:00:00');
    const days = Math.round((b - a) / 86400000);
    out.innerHTML = '<strong>' + Math.abs(days) + ' days</strong><br>' +
      Math.abs(days/7).toFixed(1) + ' weeks, about ' + Math.abs(days/30.44).toFixed(1) + ' months.<br>' +
      (days < 0 ? '(the second date is earlier)' : '');
  }
""",
    },
    {
        "slug": "loan-emi-calculator",
        "name": "Loan EMI Calculator",
        "title": "Free Loan EMI Calculator - Monthly Payment & Total Interest",
        "desc": "Calculate the monthly EMI, total interest and total payment for a loan. Free online EMI calculator.",
        "keywords": "emi calculator, loan calculator, monthly payment calculator, mortgage calculator",
        "body": """
      <div class="card">
        <div class="row">
          <label>Loan amount <input id="emi-p" type="number" value="100000" style="max-width:150px"></label>
          <label>Annual interest % <input id="emi-r" type="number" value="10" style="max-width:120px"></label>
          <label>Years <input id="emi-y" type="number" value="5" style="max-width:100px"></label>
          <button class="btn" onclick="emiCalc()">Calculate</button>
        </div>
        <div class="output" id="emi-out"></div>
      </div>
""",
        "script": """
  function emiCalc() {
    const P = +document.getElementById('emi-p').value || 0;
    const annual = +document.getElementById('emi-r').value || 0;
    const years = +document.getElementById('emi-y').value || 1;
    const r = annual / 12 / 100, n = years * 12;
    const emi = r === 0 ? P / n : P * r * Math.pow(1 + r, n) / (Math.pow(1 + r, n) - 1);
    const total = emi * n;
    document.getElementById('emi-out').innerHTML =
      '<strong>Monthly EMI: ' + emi.toFixed(2) + '</strong><br>' +
      'Total interest: ' + (total - P).toFixed(2) + '<br>' +
      'Total payment: ' + total.toFixed(2);
  }
  emiCalc();
""",
    },
    {
        "slug": "word-to-pdf-notes",
        "name": "Text to PDF",
        "title": "Free Text to PDF Converter - Turn Notes into a PDF",
        "desc": "Paste or type text and download it as a clean PDF file. Free online text to PDF converter, works in your browser.",
        "keywords": "text to pdf, notes to pdf, convert text to pdf online, plain text to pdf",
        "body": """
      <div class="card">
        <label for="t2p-in">Your text</label>
        <textarea id="t2p-in" rows="10" placeholder="Type or paste your notes here..."></textarea>
        <button class="btn" onclick="t2pMake()">Create PDF</button>
        <div class="output" id="t2p-out"></div>
      </div>
""",
        "script": """
  function t2pEscape(s) { return s.replace(/\\\\/g,'\\\\\\\\').replace(/\\(/g,'\\\\(').replace(/\\)/g,'\\\\)'); }
  function t2pMake() {
    const text = document.getElementById('t2p-in').value;
    const out = document.getElementById('t2p-out');
    if (!text.trim()) { out.textContent = 'Enter some text first.'; return; }
    const lines = text.replace(/\\r/g,'').split('\\n').slice(0, 48);
    let content = 'BT /F1 12 Tf 50 760 Td 16 TL\\n';
    for (const line of lines) content += '(' + t2pEscape(line.slice(0, 90)) + ') Tj T*\\n';
    content += 'ET';
    const objects = [
      '<< /Type /Catalog /Pages 2 0 R >>',
      '<< /Type /Pages /Kids [3 0 R] /Count 1 >>',
      '<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>',
      '<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>',
      '<< /Length ' + content.length + ' >>\\nstream\\n' + content + '\\nendstream'
    ];
    let pdf = '%PDF-1.4\\n';
    const offsets = [0];
    objects.forEach((obj, i) => { offsets.push(pdf.length); pdf += (i+1) + ' 0 obj\\n' + obj + '\\nendobj\\n'; });
    const xref = pdf.length;
    pdf += 'xref\\n0 ' + (objects.length+1) + '\\n0000000000 65535 f \\n';
    for (let i = 1; i <= objects.length; i++) pdf += String(offsets[i]).padStart(10,'0') + ' 00000 n \\n';
    pdf += 'trailer\\n<< /Size ' + (objects.length+1) + ' /Root 1 0 R >>\\nstartxref\\n' + xref + '\\n%%EOF';
    const blob = new Blob([pdf], {type:'application/pdf'});
    out.innerHTML = 'PDF created (' + Math.round(blob.size/1024) + ' KB)<br><a href="' + URL.createObjectURL(blob) + '" download="notes.pdf">Download PDF</a>';
  }
""",
    },
]

CSS = """
:root { --bg:#0f172a; --card:#1e293b; --accent:#38bdf8; --text:#e2e8f0; --muted:#94a3b8; }
* { box-sizing:border-box; }
body { margin:0; font-family:system-ui,-apple-system,Segoe UI,Roboto,sans-serif; background:var(--bg); color:var(--text); line-height:1.6; }
a { color:var(--accent); text-decoration:none; }
header { background:#111c33; padding:14px 20px; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; }
header .brand { font-weight:700; font-size:1.2rem; }
nav a { margin-left:14px; color:var(--muted); }
main { max-width:900px; margin:0 auto; padding:24px 20px; }
h1 { font-size:1.7rem; }
.grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(220px,1fr)); gap:16px; }
.card { background:var(--card); border-radius:12px; padding:18px; margin:16px 0; }
.tool-card { display:block; }
.tool-card h3 { margin:0 0 6px; }
.tool-card p { color:var(--muted); margin:0; font-size:.9rem; }
textarea, input[type=text], input[type=number] { width:100%; padding:12px; border-radius:8px; border:1px solid #334155; background:#0b1220; color:var(--text); font-family:inherit; font-size:1rem; }
label { display:block; margin:8px 0; color:var(--muted); }
.row { display:flex; flex-wrap:wrap; gap:10px; align-items:center; margin-top:10px; }
.btn { background:var(--accent); color:#04121f; border:0; padding:10px 16px; border-radius:8px; font-weight:600; cursor:pointer; }
.btn.ghost { background:transparent; color:var(--accent); border:1px solid var(--accent); }
.stats { display:grid; grid-template-columns:repeat(auto-fit,minmax(100px,1fr)); gap:10px; margin-top:16px; text-align:center; }
.stats span { font-size:1.6rem; font-weight:700; color:var(--accent); display:block; }
.stats small { color:var(--muted); }
.output { background:#0b1220; border-radius:8px; padding:14px; margin-top:12px; white-space:pre-wrap; word-break:break-word; }
.qr-box { text-align:center; margin-top:16px; }
.qr-box img { background:#fff; padding:8px; border-radius:8px; }
.ad { background:#0b1220; border:1px dashed #334155; color:var(--muted); text-align:center; padding:18px; border-radius:10px; margin:18px 0; font-size:.85rem; }
footer { border-top:1px solid #1e293b; color:var(--muted); padding:24px 20px; text-align:center; font-size:.85rem; }
footer a { color:var(--muted); margin:0 8px; }
.prose { line-height:1.75; }
.prose h2 { margin-top:1.4em; font-size:1.25rem; }
.prose h3 { font-size:1.05rem; color:var(--accent); }
.prose p, .prose li { color:#cbd5e1; }
.prose details { border-top:1px solid #334155; padding:10px 0; }
.prose summary { cursor:pointer; font-weight:600; color:var(--text); }
.prose details p { margin:8px 0 0; }
.cookie-bar { position:fixed; left:0; right:0; bottom:0; background:#111c33; color:var(--text);
  padding:12px 18px; display:flex; gap:12px; align-items:center; justify-content:center;
  flex-wrap:wrap; font-size:.85rem; border-top:1px solid #334155; z-index:50; }
select { padding:8px; border-radius:8px; border:1px solid #334155; background:#0b1220; color:var(--text); }
.conv-table { width:100%; border-collapse:collapse; margin-top:8px; }
.conv-table th, .conv-table td { text-align:left; padding:8px 12px; border-bottom:1px solid #334155; color:#cbd5e1; }
.conv-table th { color:var(--text); }
"""

# --- SEO articles + FAQs -------------------------------------------------
# Each tool page gets a short guide and a FAQ section. The FAQs are also
# emitted as FAQPage structured data, which can earn rich results in Google.
ARTICLES = {
    "word-counter": {
        "h2": "How to use the word counter",
        "body": """<p>Paste your text into the box and the counts update as you type. The tool shows
<strong>words</strong>, <strong>characters</strong>, <strong>sentences</strong> and an
estimated <strong>reading time</strong> based on 200 words per minute.</p>
<p>Writers use it to hit word limits for essays, articles and social posts. Students use it
for assignments with a strict word count. Marketers use it to keep meta descriptions under
the recommended length.</p>
<h3>Why reading time matters</h3>
<p>Knowing how long a piece takes to read helps you match the format to the audience. Blog
posts that take 3 to 7 minutes to read tend to perform well in search, while short posts suit
social media.</p>""",
        "faqs": [
            ("How are words counted?", "A word is any run of characters separated by spaces or line breaks. Punctuation alone is not counted as a word."),
            ("Does it count characters with spaces?", "Yes. The character total includes spaces, which is what most word processors and forms expect."),
            ("Is my text uploaded anywhere?", "No. Counting happens in your browser, so your text never leaves your device."),
        ],
    },
    "case-converter": {
        "h2": "When to use each text case",
        "body": """<p>Different situations call for different capitalisation. This converter changes your
text instantly so you do not have to retype it.</p>
<ul>
<li><strong>UPPERCASE</strong> for headings, labels and acronyms.</li>
<li><strong>lowercase</strong> for tags, usernames and hashtags.</li>
<li><strong>Title Case</strong> for article titles and book names.</li>
<li><strong>Sentence case</strong> for normal prose and captions.</li>
</ul>
<h3>Consistency beats preference</h3>
<p>Whatever style you pick, apply it consistently. Mixed capitalisation is one of the most
common reasons a document looks unprofessional.</p>""",
        "faqs": [
            ("What is the difference between Title Case and Sentence case?", "Title Case capitalises the first letter of each significant word. Sentence case only capitalises the first letter of the sentence and proper nouns."),
            ("Can I convert a whole paragraph at once?", "Yes, paste as much text as you like and choose a case."),
            ("Will it change my spelling?", "No, it only changes capitalisation."),
        ],
    },
    "qr-generator": {
        "h2": "What you can put in a QR code",
        "body": """<p>A QR code stores text that a phone camera can read. The most common use is a link,
but you can encode almost anything:</p>
<ul>
<li>A website or landing page URL</li>
<li>Wi-Fi login details</li>
<li>Contact details (vCard)</li>
<li>Plain text notes or coupon codes</li>
</ul>
<h3>Tips for scannable codes</h3>
<p>Keep the encoded text short. The more characters you add, the denser the pattern becomes
and the harder it is for a camera to read at a distance. Print codes at least 2 cm square and
leave a clear margin around them.</p>""",
        "faqs": [
            ("Do QR codes expire?", "The code itself does not expire. It keeps working as long as the destination link is online."),
            ("Can I download the QR code?", "Yes, use the download link under the generated image."),
            ("Are QR codes free to use?", "Yes, creating and using QR codes is free. No licence is required."),
        ],
    },
    "password-generator": {
        "h2": "How to create a strong password",
        "body": """<p>A strong password is long, random and unique to one account. This generator uses
your browser's secure random number generator, so the passwords are not predictable.</p>
<h3>What makes a password strong</h3>
<ul>
<li><strong>Length</strong> matters most. Aim for at least 12 characters, ideally 16 or more.</li>
<li><strong>Variety</strong> of upper case, lower case, digits and symbols increases the number of possible combinations.</li>
<li><strong>Uniqueness</strong> means never reusing a password across sites.</li>
</ul>
<h3>Store them safely</h3>
<p>Nobody can memorise dozens of random passwords. Use a reputable password manager to store
them, and protect the manager itself with a long passphrase and two-factor authentication.</p>""",
        "faqs": [
            ("Are the passwords sent to a server?", "No. They are generated locally in your browser and never transmitted."),
            ("How long should my password be?", "At least 12 characters for most accounts, and 16 or more for email and banking."),
            ("Should I reuse passwords?", "No. If one site is breached, reused passwords let attackers access your other accounts."),
        ],
    },
    "lorem-ipsum": {
        "h2": "What Lorem Ipsum is used for",
        "body": """<p>Lorem Ipsum is placeholder text used by designers and developers while building a
layout. It fills space so you can judge typography, spacing and structure before the real
content is ready.</p>
<h3>Why not use real text?</h3>
<p>Real words distract reviewers, who start reading instead of checking the design. Neutral
placeholder text keeps attention on the layout.</p>
<h3>Remember to replace it</h3>
<p>Never ship a page with placeholder text still in place. Before publishing, swap every block
for real content and proofread it.</p>""",
        "faqs": [
            ("Is Lorem Ipsum real Latin?", "It is derived from a Latin text by Cicero, but it has been altered and is not a coherent passage."),
            ("How many paragraphs can I generate?", "Up to 20 at a time."),
            ("Can I use it commercially?", "Yes, placeholder text is free to use in any project."),
        ],
    },
    "age-calculator": {
        "h2": "How age is calculated",
        "body": """<p>The calculator compares your date of birth with today's date and returns your age
in years, months and days. It also shows the total number of days and weeks you have lived.</p>
<h3>Why the result can differ by a day</h3>
<p>Age depends on the time zone and the exact time of birth. Most official forms only ask for
the date, so a one-day difference between tools is normal and rarely matters.</p>
<h3>Common uses</h3>
<ul>
<li>Checking eligibility for exams, jobs or benefits with an age limit</li>
<li>Filling forms that ask for exact age</li>
<li>Curiosity about milestones such as your 10,000th day</li>
</ul>""",
        "faqs": [
            ("How do I calculate my exact age?", "Enter your date of birth and the tool subtracts it from today's date, giving years, months and days."),
            ("Does it handle leap years?", "Yes, the calculation uses the real calendar, including leap years."),
            ("Can I calculate age on a future date?", "This version compares against today. For a future date, use the date difference calculator."),
        ],
    },
    "percentage-calculator": {
        "h2": "The three percentage problems",
        "body": """<p>Almost every percentage question is one of three types, and this page solves all of
them.</p>
<ol>
<li><strong>What is X% of Y?</strong> Multiply Y by X and divide by 100. For example, 15% of 200 is 30.</li>
<li><strong>X is what percent of Y?</strong> Divide X by Y and multiply by 100. For example, 30 is 15% of 200.</li>
<li><strong>Percentage change.</strong> Subtract the old value from the new one, divide by the old value, then multiply by 100.</li>
</ol>
<h3>Where percentages are used</h3>
<p>Discounts, tax, tips, interest rates, exam scores and statistics all rely on percentages.
Getting the direction of a change right, increase versus decrease, is the most common mistake.</p>""",
        "faqs": [
            ("How do I calculate a discount?", "Use the first calculator: enter the discount percent as X and the original price as Y to get the amount off."),
            ("How do I work out percentage increase?", "Use the change calculator with the original value as 'from' and the new value as 'to'."),
            ("Why is my percentage negative?", "A negative result means the value decreased rather than increased."),
        ],
    },
    "bmi-calculator": {
        "h2": "Understanding your BMI",
        "body": """<p>Body Mass Index (BMI) is a simple ratio of weight to height. It is a rough screening
tool, not a diagnosis.</p>
<h3>Adult BMI ranges</h3>
<ul>
<li>Below 18.5: underweight</li>
<li>18.5 to 24.9: normal weight</li>
<li>25 to 29.9: overweight</li>
<li>30 and above: obese</li>
</ul>
<h3>What BMI does not tell you</h3>
<p>BMI does not distinguish muscle from fat, so athletes can score as overweight. It also does
not reflect where fat is stored. Always discuss health concerns with a qualified professional
rather than relying on a single number.</p>""",
        "faqs": [
            ("Is BMI accurate for everyone?", "No. It is less reliable for athletes, pregnant women, children and older adults."),
            ("What is a healthy BMI?", "For most adults, a BMI between 18.5 and 24.9 is considered healthy."),
            ("Does BMI measure body fat?", "No, it is only a ratio of weight to height and does not measure body fat directly."),
        ],
    },
    "unit-converter": {
        "h2": "Common unit conversions",
        "body": """<p>Unit conversion is one of the most frequent everyday calculations. This tool handles
length, weight and temperature.</p>
<h3>Handy reference values</h3>
<ul>
<li>1 inch = 2.54 centimetres</li>
<li>1 foot = 30.48 centimetres</li>
<li>1 mile = 1.609 kilometres</li>
<li>1 kilogram = 2.205 pounds</li>
<li>1 ounce = 28.35 grams</li>
</ul>
<h3>Temperature is different</h3>
<p>Temperature scales do not simply multiply. Water freezes at 0&deg;C or 32&deg;F and boils at
100&deg;C or 212&deg;F, so the conversion includes an offset. Use the temperature option to get
the right answer.</p>""",
        "faqs": [
            ("How many cm is an inch?", "One inch equals exactly 2.54 centimetres."),
            ("How do I convert kg to pounds?", "Multiply kilograms by 2.2046, or use the weight option above."),
            ("Can I convert Celsius to Fahrenheit?", "Yes, choose the temperature category and pick C and F."),
        ],
    },
    "image-compressor": {
        "h2": "How image compression works",
        "body": """<p>This tool redraws your image on a canvas and re-encodes it as a JPEG at the quality
level you choose. Lower quality means a smaller file, at the cost of some detail.</p>
<h3>Choosing a quality level</h3>
<ul>
<li><strong>80 to 100%</strong> for photos where detail matters</li>
<li><strong>60 to 80%</strong> for web images, a good balance</li>
<li><strong>Below 60%</strong> for thumbnails and previews</li>
</ul>
<h3>Why smaller images matter</h3>
<p>Large images are the main reason pages load slowly. Faster pages rank better in search and
keep visitors on the page, which also improves ad performance.</p>
<h3>Your files stay private</h3>
<p>Compression runs entirely in your browser. Your images are never uploaded to a server.</p>""",
        "faqs": [
            ("Are my images uploaded?", "No. Everything happens locally in your browser, so your photos stay private."),
            ("What quality should I use for the web?", "Around 70 to 80% usually gives a big size saving with little visible loss."),
            ("Does it change the dimensions?", "No, this tool only reduces file size. Use the image resizer to change dimensions."),
        ],
    },
    "json-formatter": {
        "h2": "Why format JSON",
        "body": """<p>Minified JSON is compact but hard to read. Formatting adds indentation so you can
inspect the structure, and validation tells you exactly where a syntax error is.</p>
<h3>Common JSON mistakes</h3>
<ul>
<li>Trailing commas after the last item</li>
<li>Using single quotes instead of double quotes</li>
<li>Unquoted keys</li>
<li>Comments, which JSON does not allow</li>
</ul>
<h3>Minify for production</h3>
<p>When sending JSON over a network, minified output saves bandwidth. Format it while debugging,
then minify it before deploying.</p>""",
        "faqs": [
            ("Is my data sent anywhere?", "No, formatting and validation happen in your browser."),
            ("Why is my JSON invalid?", "The error message points to the problem. Common causes are trailing commas and single quotes."),
            ("What is the difference between format and minify?", "Format adds indentation for readability. Minify removes all unnecessary whitespace."),
        ],
    },
    "base64-encoder": {
        "h2": "What Base64 is used for",
        "body": """<p>Base64 turns binary data into plain text using 64 safe characters. It is not
encryption, it just makes data safe to move through systems that only handle text.</p>
<h3>Everyday uses</h3>
<ul>
<li>Embedding small images directly in HTML or CSS</li>
<li>Sending binary data in JSON or email</li>
<li>Storing tokens in URLs where special characters are not allowed</li>
</ul>
<h3>Base64 is not secure</h3>
<p>Anyone can decode Base64 instantly. Never use it to hide passwords, keys or personal data.
Use proper encryption for anything sensitive.</p>""",
        "faqs": [
            ("Is Base64 encryption?", "No. It is an encoding, not encryption, and can be reversed by anyone."),
            ("Does Base64 make data smaller?", "No, it makes data about 33% larger because it uses four characters to represent three bytes."),
            ("Does it handle emoji and accents?", "Yes, the tool encodes Unicode safely."),
        ],
    },
    "random-number-generator": {
        "h2": "Random numbers you can trust",
        "body": """<p>This generator uses JavaScript's built-in random function. It is fine for draws,
giveaways, games and picking a winner, but it is not suitable for cryptography.</p>
<h3>Unique versus repeatable</h3>
<p>With the unique option on, no number is picked twice, which is what you want for lottery
style draws. Turn it off if repeats are acceptable, such as simulating dice rolls.</p>
<h3>Fair draws</h3>
<p>For a public giveaway, announce the range and the number of winners before you draw, then
run the generator live so everyone can see the result.</p>""",
        "faqs": [
            ("Are the numbers truly random?", "They are pseudo-random, which is more than enough for games and draws but not for security."),
            ("Can I pick multiple unique numbers?", "Yes, set how many you need and keep the unique option checked."),
            ("What happens if I ask for more unique numbers than the range?", "The tool warns you, because it is impossible to pick more unique values than exist in the range."),
        ],
    },
    "unix-timestamp": {
        "h2": "What a Unix timestamp is",
        "body": """<p>A Unix timestamp is the number of seconds that have passed since 1 January 1970 at
00:00 UTC, a moment known as the epoch. Servers and databases store time this way because a
single number is easy to sort and compare.</p>
<h3>Reading a timestamp</h3>
<p>Ten digits usually means seconds. Thirteen digits usually means milliseconds, which is what
JavaScript uses. If a converted date looks far in the future, you probably entered
milliseconds.</p>
<h3>Time zones</h3>
<p>The timestamp itself is always UTC. The readable date depends on the time zone of the
computer displaying it.</p>""",
        "faqs": [
            ("Why does my timestamp convert to 1970?", "A very small number is only a few seconds after the epoch, so it shows as January 1970."),
            ("Is the timestamp in seconds or milliseconds?", "Unix timestamps are in seconds. JavaScript uses milliseconds, which is 1000 times larger."),
            ("What is the current Unix time?", "The live value at the top of the page updates every second."),
        ],
    },
    "color-converter": {
        "h2": "HEX, RGB and HSL explained",
        "body": """<p>Colours can be written in several ways, and different tools expect different
formats. This converter moves between the three most common ones.</p>
<h3>The formats</h3>
<ul>
<li><strong>HEX</strong> like #38bdf8, a compact code used in HTML and CSS.</li>
<li><strong>RGB</strong> like rgb(56, 189, 248), three values from 0 to 255.</li>
<li><strong>HSL</strong> like hsl(198, 93%, 60%), hue, saturation and lightness.</li>
</ul>
<h3>Why HSL is useful</h3>
<p>HSL is easier to reason about by hand. To make a colour lighter, raise the lightness. To make
it more muted, lower the saturation. That is harder to do with HEX or RGB values.</p>""",
        "faqs": [
            ("How do I convert hex to RGB?", "Enter the hex code and the RGB values appear instantly."),
            ("What is HSL used for?", "HSL describes a colour by hue, saturation and lightness, which makes it easy to create lighter or darker shades."),
            ("Can I preview the colour?", "Yes, the swatch shows the colour and the picker lets you choose a new one."),
        ],
    },
    "image-resizer": {
        "h2": "Resizing images without losing quality",
        "body": """<p>Resizing changes the pixel dimensions of an image, which is different from
compressing it. Use resize when a site or form demands exact dimensions, such as a profile
photo of 400 by 400 pixels.</p>
<h3>Keep the aspect ratio</h3>
<p>If you change the width without the height in proportion, the image stretches. Leave the
keep ratio option on unless you specifically want to crop or distort the picture.</p>
<h3>Resize before you compress</h3>
<p>Shrinking a large photo first, then compressing it, gives the smallest file with the best
appearance. Doing it the other way around can leave visible artefacts.</p>
<p>Like the other tools here, resizing happens in your browser and your images are never
uploaded.</p>""",
        "faqs": [
            ("Are my images uploaded?", "No, resizing happens in your browser."),
            ("Will resizing reduce quality?", "Enlarging an image always softens it. Shrinking keeps it sharp."),
            ("How do I keep the aspect ratio?", "Leave the keep ratio box checked and type only the width."),
        ],
    },
    "pomodoro-timer": {
        "h2": "How the Pomodoro technique works",
        "body": """<p>The Pomodoro technique breaks work into focused intervals separated by short
breaks. The classic pattern is 25 minutes of work followed by a 5 minute break, with a longer
break after four rounds.</p>
<h3>Why it helps</h3>
<ul>
<li>A fixed interval makes a large task feel manageable.</li>
<li>Breaks prevent fatigue and keep concentration high.</li>
<li>Counting finished intervals shows real progress.</li>
</ul>
<h3>Getting the most from it</h3>
<p>During a work interval, close distractions and write down anything unrelated that comes to
mind, then return to it in the break. Keep this page open in a tab as your timer.</p>""",
        "faqs": [
            ("What is the standard Pomodoro length?", "25 minutes of work and a 5 minute break is the classic version."),
            ("Can I change the interval?", "Yes, use the Work 25m and Break 5m buttons, or keep the timer running for custom lengths."),
            ("Does the timer keep running if I switch tabs?", "Yes, it keeps counting while the tab is open in the background."),
        ],
    },
    "hash-generator": {
        "h2": "What hashing is used for",
        "body": """<p>A hash function turns any input into a fixed length string called a digest. The
same input always produces the same digest, but you cannot work backwards from the digest to
the original text.</p>
<h3>Where hashes are used</h3>
<ul>
<li>Verifying that a download was not corrupted</li>
<li>Storing passwords in a hashed form</li>
<li>Checking whether two files are identical</li>
</ul>
<h3>SHA versus MD5</h3>
<p>SHA-256 and SHA-512 are modern and considered secure. MD5 and SHA-1 are outdated for
security purposes because collisions have been found, but they are still useful as quick
checksums.</p>""",
        "faqs": [
            ("Is hashing the same as encryption?", "No. Encryption is reversible with a key. Hashing is one way."),
            ("Which hash should I use?", "Use SHA-256 for most purposes. Avoid MD5 and SHA-1 for anything security related."),
            ("Is my text sent to a server?", "No, hashing runs in your browser using the Web Crypto API."),
        ],
    },
    "url-encoder": {
        "h2": "Why URLs need encoding",
        "body": """<p>URLs can only contain a limited set of characters. Spaces, ampersands and non
English letters must be converted into a percent sign followed by two hexadecimal digits, a
process called percent-encoding.</p>
<h3>When you need it</h3>
<ul>
<li>Building a link that contains spaces or special characters</li>
<li>Passing a value as a query parameter</li>
<li>Debugging a link that broke after being copied</li>
</ul>
<h3>A space becomes %20</h3>
<p>For example, the text "hello world" encodes to "hello%20world". Decoding reverses the
process, turning the escapes back into readable characters.</p>""",
        "faqs": [
            ("What does %20 mean in a URL?", "It is the encoded form of a space character."),
            ("Should I encode a whole URL or just part of it?", "Encode the values you add to a URL, not the scheme and domain, which are already valid."),
            ("Is encoding the same as encryption?", "No, it is reversible by anyone and hides nothing."),
        ],
    },
    "roman-numeral-converter": {
        "h2": "Reading Roman numerals",
        "body": """<p>Roman numerals use seven letters: I, V, X, L, C, D and M, standing for 1, 5, 10,
50, 100, 500 and 1000.</p>
<h3>The subtraction rule</h3>
<p>When a smaller symbol comes before a larger one, you subtract. IV is 4, IX is 9, XL is 40
and CM is 900. In every other case you add the values.</p>
<h3>Where you still see them</h3>
<ul>
<li>Copyright years, such as MMXXVI</li>
<li>Chapter numbers in books</li>
<li>Clock faces and film sequels</li>
<li>Names of monarchs and popes</li>
</ul>
<p>Standard Roman numerals cover 1 to 3999, which is the range this tool supports.</p>""",
        "faqs": [
            ("What is 2026 in Roman numerals?", "MMXXVI."),
            ("Why is there no zero in Roman numerals?", "The system was designed for counting and did not have a symbol for zero."),
            ("What is the largest number I can convert?", "3999, written as MMMCMXCIX, using standard notation."),
        ],
    },
    "tip-calculator": {
        "h2": "How much should you tip",
        "body": """<p>Tipping customs vary by country and service. This calculator works out the tip
amount, the total bill and the split per person.</p>
<h3>Typical ranges</h3>
<ul>
<li>Restaurants in the United States: 15 to 20 percent</li>
<li>Delivery: a few dollars or around 10 percent</li>
<li>Many countries in Europe and Asia: service is included, tipping is optional</li>
</ul>
<h3>Splitting fairly</h3>
<p>Enter the number of people and the tool divides the total, including tip, equally. If some
people ordered more than others, agree on the split before you calculate.</p>""",
        "faqs": [
            ("How do I calculate a 15 percent tip?", "Enter the bill, set the tip to 15 percent, and the amount appears instantly."),
            ("How do I split the bill?", "Set the number of people and the tool shows what each person pays, tip included."),
            ("Should I tip on the pre-tax amount?", "Either is acceptable. Tipping on the total is simpler and slightly more generous."),
        ],
    },
    "date-difference": {
        "h2": "Counting days between dates",
        "body": """<p>This calculator finds the gap between two dates in days, weeks and months. It
handles leap years and different month lengths correctly.</p>
<h3>Common uses</h3>
<ul>
<li>Counting down to a deadline, exam or event</li>
<li>Working out the length of a project or trip</li>
<li>Checking notice periods and contract terms</li>
</ul>
<h3>Inclusive versus exclusive counting</h3>
<p>Some people count the start day, some do not. This tool reports the difference, so a
Monday to Friday gap is 4 days. Add one if you need to count both end days inclusively.</p>""",
        "faqs": [
            ("Does it include the end date?", "It reports the difference between the two dates, so the end day is not counted separately."),
            ("Does it handle leap years?", "Yes, the calculation uses the real calendar."),
            ("Can the result be negative?", "Yes, if the second date is earlier, and the tool tells you so."),
        ],
    },
    "loan-emi-calculator": {
        "h2": "How loan EMI is calculated",
        "body": """<p>EMI stands for Equated Monthly Instalment, the fixed amount you pay each month
until a loan is repaid. Each payment covers part interest and part principal.</p>
<h3>The idea behind it</h3>
<p>Early payments are mostly interest because the balance is still large. Over time the interest
portion shrinks and more of each payment goes to the principal. The monthly amount stays the
same, which makes budgeting easier.</p>
<h3>What affects your EMI</h3>
<ul>
<li><strong>Loan amount</strong>: a bigger loan means a bigger payment.</li>
<li><strong>Interest rate</strong>: even a small increase adds up over many years.</li>
<li><strong>Term</strong>: a longer term lowers the monthly payment but raises total interest.</li>
</ul>
<p>Use the calculator to compare terms before you commit, and always confirm final figures with
your lender.</p>""",
        "faqs": [
            ("What does EMI mean?", "Equated Monthly Instalment, the fixed monthly payment on a loan."),
            ("Is a longer loan term better?", "It lowers the monthly payment but increases the total interest you pay."),
            ("Does this include fees?", "No, it covers principal and interest only. Lenders may charge additional fees."),
        ],
    },
    "word-to-pdf-notes": {
        "h2": "Turning text into a PDF",
        "body": """<p>PDF is the safest format for sharing a document because it looks the same on every
device. This tool takes plain text and builds a PDF in your browser, with no upload and no
account.</p>
<h3>Good uses</h3>
<ul>
<li>Turning quick notes into a clean document to send</li>
<li>Saving a plain text draft as a fixed file</li>
<li>Creating a simple printable page</li>
</ul>
<h3>Limits to know</h3>
<p>This is a lightweight converter. It handles plain text on a single page with a standard font.
For rich formatting, images, tables or multiple pages, use a full word processor and export
from there.</p>""",
        "faqs": [
            ("Is my text uploaded?", "No, the PDF is generated in your browser."),
            ("Does it support images or tables?", "No, it converts plain text only."),
            ("How many lines fit?", "Up to 48 lines on one page. Longer text is trimmed, so split it into separate files."),
        ],
    },
}


def ga_snippet() -> str:
    if not GA_MEASUREMENT_ID:
        return ""
    return f"""<script async src="https://www.googletagmanager.com/gtag/js?id={GA_MEASUREMENT_ID}"></script>
<script>
window.dataLayer = window.dataLayer || [];
function gtag(){{dataLayer.push(arguments);}}
gtag('js', new Date());
gtag('config', '{GA_MEASUREMENT_ID}');
</script>"""


def cookie_banner() -> str:
    """Consent notice shown until the visitor dismisses it.

    Third-party ad networks may set cookies, so most networks and privacy laws
    (for example GDPR in the EU) expect a notice. The choice is stored in
    localStorage and is per browser.
    """
    return """<div id="cookie-bar" class="cookie-bar" hidden>
  <span>This site uses cookies for analytics and advertising. By continuing you agree to the
  <a href="/privacy/">privacy policy</a>.</span>
  <button class="btn" onclick="cookieOk()">Got it</button>
</div>
<script>
(function(){
  try {
    if (!localStorage.getItem('cookie-ok')) document.getElementById('cookie-bar').hidden = false;
  } catch (e) { document.getElementById('cookie-bar').hidden = false; }
})();
function cookieOk() {
  try { localStorage.setItem('cookie-ok','1'); } catch (e) {}
  document.getElementById('cookie-bar').hidden = true;
}
</script>"""


def favicon_data_uri() -> str:
    """A small square favicon generated as a PNG data URI, no binary asset needed."""
    size, bg, fg = 32, (15, 23, 42), (56, 189, 248)
    rows = b""
    for y in range(size):
        rows += b"\x00"
        for x in range(size):
            edge = 3 <= x <= 28 and 3 <= y <= 28
            inner = 9 <= x <= 22 and 9 <= y <= 22
            color = fg if inner else bg if edge else None
            rows += bytes(color + (255,)) if color else b"\x00\x00\x00\x00"
    def chunk(tag, data):
        body = tag + data
        return struct.pack(">I", len(data)) + body + struct.pack(">I", zlib.crc32(body) & 0xFFFFFFFF)
    ihdr = struct.pack(">IIBBBBB", size, size, 8, 6, 0, 0, 0)
    png = (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr)
           + chunk(b"IDAT", zlib.compress(rows)) + chunk(b"IEND", b""))
    import base64
    return "data:image/png;base64," + base64.b64encode(png).decode()


def page(title: str, desc: str, keywords: str, body: str, canonical: str,
         extra_script: str = "", extra_head: str = "") -> str:
    """Render a full HTML page. Ad slot markup lives here."""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<meta name="keywords" content="{html.escape(keywords)}">
<link rel="canonical" href="{canonical}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:type" content="website">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{favicon_data_uri()}">
<meta name="twitter:card" content="summary">
<link rel="icon" href="{favicon_data_uri()}">
<link rel="stylesheet" href="/style.css">
{AD_HEADER}
{ga_snippet()}
{extra_head}
</head>
<body>
<header>
  <div class="brand"><a href="/">{SITE_NAME}</a></div>
  <nav>
    <a href="/">Tools</a>
    <a href="/convert/">Converters</a>
    <a href="/about/">About</a>
    <a href="/privacy/">Privacy</a>
    <a href="/contact/">Contact</a>
  </nav>
</header>
<main>
{body}
  <div class="ad">{AD_INARTICLE or 'Ad space (paste your ad network code here)'}</div>
</main>
<footer>
  <div class="ad">{AD_FOOTER or 'Ad space'}</div>
  <p>&copy; {SITE_NAME}. <a href="/privacy/">Privacy</a> <a href="/about/">About</a> <a href="/contact/">Contact</a></p>
</footer>
{cookie_banner()}
{('<script>' + extra_script + '</script>') if extra_script else ''}
</body>
</html>
"""


def home_body() -> str:
    cards = "\n".join(
        f'      <a class="card tool-card" href="/{t["slug"]}/"><h3>{html.escape(t["name"])}</h3><p>{html.escape(t["desc"].split(".")[0])}.</p></a>'
        for t in TOOLS
    )
    return f"""  <h1>Free Online Tools</h1>
  <p>Handy browser tools that work instantly — no sign-up required.</p>
  <div class="ad">{AD_SIDEBAR or 'Ad space (top)'}</div>
  <div class="grid">
{cards}
  </div>
  <h2>Popular unit converters</h2>
  <p>Dedicated pages for the conversions people search most, each with a table and formula.</p>
  <div class="row">
    <a href="/cm-to-inches/">CM to Inches</a>
    <a href="/kg-to-pounds/">KG to Pounds</a>
    <a href="/celsius-to-fahrenheit/">Celsius to Fahrenheit</a>
    <a href="/km-to-miles/">KM to Miles</a>
    <a href="/convert/">All converters</a>
  </div>
"""


def faq_jsonld(faqs: list) -> str:
    data = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": a},
            }
            for q, a in faqs
        ],
    }
    return f'<script type="application/ld+json">{json.dumps(data)}</script>'


def article_block(slug: str) -> str:
    art = ARTICLES.get(slug)
    if not art:
        return ""
    faqs = "\n".join(
        f'    <details><summary>{html.escape(q)}</summary><p>{a}</p></details>'
        for q, a in art["faqs"]
    )
    return f"""  <article class="card prose">
    <h2>{html.escape(art["h2"])}</h2>
{art["body"]}
    <h2>Frequently asked questions</h2>
{faqs}
  </article>
"""


def conversion_page(c: dict) -> str:
    """A dedicated SEO page for one unit conversion query (e.g. cm to inches)."""
    rows = "\n".join(
        f"        <tr><td>{fmt(v)} {c['from']}</td><td>{fmt(convert_value(c, v))} {c['to']}</td></tr>"
        for v in c["table"]
    )
    faqs = "\n".join(
        f'    <details><summary>{html.escape(q)}</summary><p>{a}</p></details>'
        for q, a in c["faqs"]
    )
    related = [x for x in CONVERSIONS if x["category"] == c["category"] and x["slug"] != c["slug"]]
    rel_links = "\n".join(
        f'      <a href="/{r["slug"]}/">{html.escape(r["name"])}</a>' for r in related
    )
    body = f"""  <h1>{html.escape(c["name"])}</h1>
  <p>{html.escape(c["desc"])}</p>
  <div class="card">
    <div class="row">
      <input id="cv-val" type="number" value="1" style="max-width:160px">
      <span>{html.escape(c["from"])} =</span>
      <strong id="cv-out"></strong>
      <span>{html.escape(c["to"])}</span>
    </div>
  </div>
  <div class="card">
    <h3>Conversion table</h3>
    <table class="conv-table">
      <thead><tr><th>{html.escape(c["from"])}</th><th>{html.escape(c["to"])}</th></tr></thead>
      <tbody>
{rows}
      </tbody>
    </table>
  </div>
  <article class="card prose">
    <h2>How to convert {html.escape(c["from"])} to {html.escape(c["to"])}</h2>
    <p>Use the formula <strong>{html.escape(c["formula"])}</strong>. Type any value in the box
    above and the answer updates instantly.</p>
    <p>{html.escape(c["desc"])}</p>
    <h2>Frequently asked questions</h2>
{faqs}
  </article>
  <div class="card">
    <h3>Related conversions</h3>
    <div class="row">
{rel_links}
    </div>
  </div>
"""
    script = _cv_js(c)
    extra_head = faq_jsonld(c["faqs"])
    return page(
        c["title"], c["desc"], c["keywords"], body,
        f"{SITE_URL}/{c['slug']}/", script, extra_head,
    )


def _cv_js(c: dict) -> str:
    """Inline JS that converts the input value, handling temperature separately."""
    if c.get("kind") == "temp":
        f, t = c["from"], c["to"]
        if f == "C" and t == "F":
            expr = "v * 9 / 5 + 32"
        elif f == "F" and t == "C":
            expr = "(v - 32) * 5 / 9"
        elif f == "C" and t == "K":
            expr = "v + 273.15"
        else:
            expr = "v"
    else:
        expr = f"v * {c['factor']}"
    return (
        "  function cvRun() {\n"
        "    const v = parseFloat(document.getElementById('cv-val').value);\n"
        "    const el = document.getElementById('cv-out');\n"
        f"    el.textContent = isNaN(v) ? '—' : (+({expr}).toFixed(6));\n"
        "  }\n"
        "  document.getElementById('cv-val').addEventListener('input', cvRun);\n"
        "  cvRun();\n"
    )


def conversion_index() -> str:
    """A hub page listing every conversion page, grouped by category."""
    cats: dict = {}
    for c in CONVERSIONS:
        cats.setdefault(c["category"], []).append(c)
    sections = ""
    for cat, items in cats.items():
        links = "\n".join(
            f'      <a class="card tool-card" href="/{c["slug"]}/"><h3>{html.escape(c["name"])}</h3>'
            f'<p>{html.escape(c["desc"].split(".")[0])}.</p></a>'
            for c in items
        )
        sections += f'  <h2>{html.escape(cat)}</h2>\n  <div class="grid">\n{links}\n  </div>\n'
    body = f"""  <h1>Unit Converters</h1>
  <p>Free, instant conversion pages for the queries people search most. Each one has a
  calculator, a reference table and the formula.</p>
{sections}"""
    return page(
        f"Unit Converters - {SITE_NAME}",
        "Free unit conversion pages: cm to inches, kg to pounds, Celsius to Fahrenheit and more, each with a table and formula.",
        "unit converter, cm to inches, kg to pounds, celsius to fahrenheit",
        body, f"{SITE_URL}/convert/",
    )


def tool_page(tool: dict) -> str:
    others = "\n".join(
        f'      <a href="/{o["slug"]}/">{html.escape(o["name"])}</a>'
        for o in TOOLS if o["slug"] != tool["slug"]
    )
    body = f"""  <h1>{html.escape(tool["name"])}</h1>
  <p>{html.escape(tool["desc"])}</p>
{tool["body"]}
{article_block(tool["slug"])}
  <div class="card">
    <h3>Other tools</h3>
    <div class="row">
{others}
    </div>
  </div>
"""
    art = ARTICLES.get(tool["slug"])
    extra_head = faq_jsonld(art["faqs"]) if art else ""
    return page(
        tool["title"], tool["desc"], tool["keywords"], body,
        f"{SITE_URL}/{tool['slug']}/", tool["script"], extra_head,
    )


LEGAL = {
    "about": (
        "About",
        "About this site, who runs it and what it offers.",
        """<h1>About</h1>
<p>This site offers free browser-based tools to help with everyday tasks such as
counting words, converting text, generating QR codes and creating passwords.</p>
<p>All tools run entirely in your browser. We do not store the text you enter.</p>
<p>Replace this text with a short introduction about you and why you built the site.
A clear, honest About page improves trust and helps with ad-network approval.</p>""",
    ),
    "privacy": (
        "Privacy Policy",
        "How this site handles data, cookies and third-party advertising.",
        """<h1>Privacy Policy</h1>
<p>Last updated: 2026.</p>
<h2>Information we collect</h2>
<p>The tools on this site run in your browser. Text you type into a tool is not
uploaded to our servers.</p>
<h2>Cookies and advertising</h2>
<p>We may display advertising through third-party ad networks. These networks may
use cookies or similar technologies to show ads based on your prior visits to
this and other websites. You can opt out of personalised advertising through your
browser settings or the ad network's own opt-out page.</p>
<h2>Analytics</h2>
<p>We may use privacy-respecting analytics to understand aggregate traffic. This
data does not personally identify you.</p>
<h2>Your choices</h2>
<p>You can disable cookies in your browser at any time. Doing so may affect how
ads are shown but will not stop the tools from working.</p>
<h2>Contact</h2>
<p>Questions about this policy? Use the Contact page.</p>""",
    ),
    "contact": (
        "Contact",
        "Get in touch with the team behind this site.",
        f"""<h1>Contact</h1>
<p>Have a question, found a bug, or want a new tool? Email us at
<a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a>.</p>
<p>Replace this email with your real address before publishing.</p>""",
    ),
}


def build() -> None:
    if SITE.exists():
        shutil.rmtree(SITE)
    SITE.mkdir(parents=True)

    (SITE / "style.css").write_text(CSS.strip() + "\n", encoding="utf-8")
    (SITE / ".nojekyll").write_text("", encoding="utf-8")

    (SITE / "index.html").write_text(
        page(
            f"{SITE_NAME} - Free Online Tools",
            "A collection of free, fast, browser-based tools: word counter, case converter, QR code generator, password generator and more.",
            "free online tools, word counter, qr code generator, password generator",
            home_body(),
            f"{SITE_URL}/",
        ),
        encoding="utf-8",
    )

    for tool in TOOLS:
        d = SITE / tool["slug"]
        d.mkdir()
        (d / "index.html").write_text(tool_page(tool), encoding="utf-8")

    for c in CONVERSIONS:
        d = SITE / c["slug"]
        d.mkdir()
        (d / "index.html").write_text(conversion_page(c), encoding="utf-8")

    d = SITE / "convert"
    d.mkdir()
    (d / "index.html").write_text(conversion_index(), encoding="utf-8")

    for slug, (title, desc, body) in LEGAL.items():
        d = SITE / slug
        d.mkdir()
        (d / "index.html").write_text(
            page(f"{title} - {SITE_NAME}", desc, "", body, f"{SITE_URL}/{slug}/"),
            encoding="utf-8",
        )

    (SITE / "sitemap.xml").write_text(sitemap(), encoding="utf-8")
    (SITE / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n", encoding="utf-8"
    )
    print(f"Built {len(list(SITE.rglob('*.html')))} pages into {SITE}")


def sitemap() -> str:
    urls = [f"{SITE_URL}/"]
    urls += [f"{SITE_URL}/{t['slug']}/" for t in TOOLS]
    urls += [f"{SITE_URL}/{c['slug']}/" for c in CONVERSIONS]
    urls.append(f"{SITE_URL}/convert/")
    urls += [f"{SITE_URL}/{s}/" for s in LEGAL]
    items = "\n".join(
        f"  <url><loc>{u}</loc><changefreq>weekly</changefreq></url>" for u in urls
    )
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{items}\n</urlset>\n"
    )


if __name__ == "__main__":
    build()
