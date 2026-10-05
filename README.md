Free Tools Website (Ad-ready)
A fast, static "free online tools" website. It ships with 5 working tools, SEO meta tags, a sitemap, the policy pages ad networks require, and empty ad slots ready for Adsterra (or any other network).
Built with the Python standard library only — no pip install needed.
Build
python3 generator.py
This writes the whole site into site/. Open it locally:
cd site && python3 -m http.server 12000
What's included
24 interactive tools plus 17 dedicated unit-conversion pages (45 pages total). Every page has an SEO guide and FAQ section, with FAQPage structured data for rich results.
Category
Tools
Text
Word Counter, Case Converter, Lorem Ipsum, Text to PDF
Calculators
Age, Percentage, BMI, Tip, Loan EMI, Date Difference
Converters
Unit, Color, Roman Numeral, Unix Timestamp
Generators
QR Code, Password, Random Number
Developer
JSON Formatter, Base64 Encoder, Hash Generator, URL Encoder
Media
Image Compressor, Image Resizer
Productivity
Pomodoro Timer
Dedicated conversion pages (targeting single search queries such as "cm to inches"): CM/Inches, Inches/CM, Meters/Feet, Feet/Meters, KM/Miles, Miles/KM, MM/Inches, KG/Pounds, Pounds/KG, Grams/Ounces, Ounces/Grams, Celsius/Fahrenheit, Fahrenheit/Celsius, Celsius/Kelvin, MB/GB, GB/MB. Hub page at /convert/.
Plus the pages ad networks require: /about/, /privacy/, /contact/, and a sitemap.xml and robots.txt for search engines.
Putting Adsterra ads in
See ADS-AND-ANALYTICS.md for the full walkthrough, including which Adsterra format goes in which slot and the placement rules that protect your account.
Quick version:
Sign up at adsterra.com and add your site.
Create ad units (Social Bar, Popunder, Native Banner, 300x250 / 728x90).
Paste each snippet into the matching block near the top of generator.py:
AD_HEADER = ""     # social bar / header banner
AD_INARTICLE = ""  # banner shown mid-page
AD_SIDEBAR = ""    # 300x250 on the home page
AD_FOOTER = ""     # native banner
Re-run python3 generator.py and redeploy.
For Google Analytics, set GA_MEASUREMENT_ID = "G-XXXXXXXXXX" in the same file.
Ad networks pay per impression/click from real visitors. Never buy bot traffic or click your own ads — that is click fraud, gets accounts banned, and is not a legitimate income method.
Before you publish (important)
In generator.py, set SITE_URL to your real domain and SITE_NAME to your brand.
Edit site/about/index.html and site/contact/index.html (or the LEGAL dict in generator.py) with your real details and email.
Replace the placeholder privacy text with one that matches the ad network you use.
Deploy (free)
The build output is plain static files, so it works on any host. Build configs are already included for all four options below. All of them read SITE_URL, CONTACT_EMAIL, SITE_NAME and GA_MEASUREMENT_ID from environment variables, so you set your real address once in the host's dashboard.
Recommended: Cloudflare Pages (Code -> GitHub -> Cloudflare -> live)
Full walkthrough in CLOUDFLARE-PAGES.md. In short:
Setting
Value
Build command
bash build.sh
Build output directory
site
Environment variables
SITE_URL, CONTACT_EMAIL, SITE_NAME, GA_MEASUREMENT_ID
Every push to main rebuilds and republishes the site automatically.
Option 1: GitHub Pages (auto-deploy on every push)
git remote add origin https://github.com/<your-username>/<repo>.git
git push -u origin main
Then in the repository: Settings > Pages > Build and deployment > Source = GitHub Actions. The included workflow (.github/workflows/deploy.yml) builds the site and publishes it on every push to main.
Option 2: Netlify
See NETLIFY-DEPLOY.md for the drag-and-drop route.
New site from Git, pick the repo. netlify.toml sets the build command to python3 generator.py and the publish directory to site.
Or drag the site/ folder straight into the Netlify dashboard for a manual deploy.
Option 3: Vercel
Import the repo. vercel.json sets the build command and output directory.
Or run vercel --prod from the project root.
A custom domain (around $10 per year) is optional at the start. It helps ad-network approval, so buy one once the site earns, not before.
Getting traffic (the part that actually earns)
Ads only pay when people visit. Free tools rank well because people search for them daily. The site already has 24 of them, so focus on the steps that bring visitors:
Submit sitemap.xml in Google Search Console and Bing Webmaster.
Share each tool on Reddit, Quora and niche Facebook groups where it genuinely helps.
Make short demo videos (YouTube Shorts / Reels) showing the tool.
Improve the tools that already get traffic, and add related ones around them.
Realistic timeline: first clicks and impressions within weeks, meaningful payouts after a few months of steady work. It is not instant money, but it compounds and needs no ongoing ad spend.