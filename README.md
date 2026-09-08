# Elmir Garage Equipment - Online Automotive & Workshop Catalog

Modern, responsive, bilingual (English & Arabic) online catalog for **Elmir Garage Equipment**, showcasing 299+ professional automotive tools, garage machinery, hydraulic vehicle lifts, diagnostic scanners, and workshop equipment.

Designed and optimized for static hosting on **Cloudflare Pages** and deployment via **Git**.

---

## 🚀 Live Demo & Repository
- **Production Website**: [https://elmir-tools-co.pages.dev/](https://elmir-tools-co.pages.dev/)
- **GitHub Repository**: [https://github.com/peterchehab1-hub/Elmir-Tools-CO](https://github.com/peterchehab1-hub/Elmir-Tools-CO)

## ✨ Key Features
- **299 Catalog Products**: Fully digitized data from official garage equipment catalogs, batch additions, and equipment sheets.
- **Strict Price Filtering**: 100% compliant with zero pricing data exposed.
- **Bilingual Interface**: Seamless English (LTR) and Arabic (RTL) switching with tailored typography (`Inter` & `Cairo`).
- **Live Search & Filters**: Instant client-side search across English & Arabic names, Reference Numbers, Part Numbers (`ET-001` to `ET-299`), and specifications.
- **Category Navigation**: 9 core categories with real-time product counts.
- **Quote Request Cart**: Users can select multiple tools and generate an instant formatted inquiry message sent directly to WhatsApp (`+961 76 339 423`).
- **Zero Pricing Exposed**: Adheres strictly to the quote-request workflow with no raw pricing displayed.
- **High Performance & Zero Dependencies**: Built with pure vanilla HTML5, CSS3, and JavaScript for instantaneous load times and 100/100 Lighthouse performance.

---

## 📁 Repository Structure

```text
├── index.html            # Main web application entry point
├── catalog.json          # Complete 240-item database (EN/AR, Specs, Categories)
├── _headers              # Cloudflare Pages cache & security headers
├── build_catalog.py      # Data extraction & image normalization pipeline
├── css/
│   └── style.css         # Modern automotive dark/carbon theme & RTL styles
├── js/
│   └── app.js            # Reactive catalog engine, search, cart & WhatsApp API
└── images/
    ├── products/         # Standardized product images (1.jpg to 240.jpg)
    └── ...               # Source scans and reference grid sheets
```

---

## 🚀 Deployment Instructions

### Option 1: Deploy to Cloudflare Pages via GitHub (Recommended)

1. **Initialize Git Repository**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Elmir Tools & Co catalog"
   ```

2. **Push to GitHub**:
   - Create a new repository on [GitHub](https://github.com/new) named `elmir-tools-catalog`.
   - Run the following commands (replace `<username>` with your GitHub username):
     ```bash
     git remote add origin https://github.com/<username>/elmir-tools-catalog.git
     git branch -M main
     git push -u origin main
     ```

3. **Connect to Cloudflare Pages**:
   - Log in to your [Cloudflare Dashboard](https://dash.cloudflare.com/).
   - Go to **Workers & Pages** > **Create application** > **Pages** > **Connect to Git**.
   - Select your GitHub repository `elmir-tools-catalog`.
   - Set the build settings:
     - **Framework preset**: `None`
     - **Build command**: *(leave blank)*
     - **Build output directory**: `/` (or root)
   - Click **Save and Deploy**. Your site will be live on a custom `.pages.dev` domain in under 30 seconds!

---

### Option 2: Direct Upload via Wrangler CLI

If you prefer deploying directly from your terminal without linking GitHub:

```bash
# Install Wrangler (if not already installed)
npm install -g wrangler

# Deploy current directory to Cloudflare Pages
wrangler pages deploy . --project-name=elmir-tools-catalog
```

---

## 🔧 Local Development & Testing

To preview the website locally on your computer:

```bash
# Using Python's built-in HTTP server:
python -m http.server 8080
```
Open your browser at `http://localhost:8080`.

---

## 📞 Business Contact Information

- **Owner**: Elmir Antoine Chehab
- **Phone / WhatsApp**: [+961 76 339 423](https://wa.me/96176339423)
- **Email**: [elmirb21@gmail.com](mailto:elmirb21@gmail.com)
- **Location**: Lebanon
