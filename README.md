# 📊 Employee & Project Performance Dashboard

An interactive, full-stack analytics application built with **Python (Flask)**, **SQLite3 (SQL)**, **HTML5**, **CSS3**.

Designed to deliver multi-dataset enterprise insights including **Employee & Project Performance**, **E-Commerce & Global Revenue**, and **SaaS Product Growth & ARR**.

---

## ✨ Features

- **⚡ Multi-Dataset SQL Analytics Engine**: Seamlessly switch between HR/Employee Performance, E-Commerce Sales, and SaaS Growth metrics.
- **📊 High-Impact Visual Telemetry**: Dynamic KPI cards, interactive data breakdown, and real-time category filtering.
- **🔍 Advanced SQL Filter & Search**: Perform multi-parameter search across employees, departments, budget ranges, and performance scores.
- **📤 Dataset Ingestion & Upload**: Built-in CSV dataset uploader with automated SQLite table creation and dynamic column mapping.
- **💾 Data Export**: One-click CSV export of filtered dataset results.

---

## 🛠️ Tech Stack

- **Backend**: Python 3, Flask, SQLite3, Pandas
- **Frontend**: HTML5, Vanilla CSS3 (Custom Design System with Glassmorphism), Vanilla JS
- **Database**: SQLite3 (relational database with `dataset_registry` and normalized fact/dimension tables)

---

## 📁 Project Structure

```
dashboard/
├── app.py               # Flask application server & API routes
├── init_db.py           # SQLite database initialization script
├── dashboard.db         # SQLite database file
├── requirements.txt     # Python dependencies
├── static/
│   └── styles.css       # Custom CSS design system
└── templates/
    └── dashboard.html   # Main dashboard frontend template
```

---

## 🚀 Quick Start & Installation

### 1. Clone the repository
```bash
git clone https://github.com/SandeepTech11/Employee-Project-Performance-Dashboard.git
cd Employee-Project-Performance-Dashboard
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Initialize the database
```bash
python init_db.py
```

### 4. Run the application
```bash
python app.py
```

Navigate to `http://localhost:8080` in your web browser.

---

## 👤 Author

**Sandeep Kumar Reddy Kambham**
* GitHub: [@SandeepTech11](https://github.com/SandeepTech11)
* LinkedIn: [Sandeep Kumar Reddy Kambham](https://www.linkedin.com/in/kambham-sandeep-kumar-reddy-2b81822a7)
