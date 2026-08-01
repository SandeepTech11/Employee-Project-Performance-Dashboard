"""
SQLite Database Initialization Script for Employee & Project Performance Dashboard
Creates 'dashboard.db' SQLite database with pre-populated datasets using SQL schema & INSERT statements.
"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "dashboard.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("PRAGMA foreign_keys = ON;")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS dataset_registry (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        subtitle TEXT,
        category_label TEXT NOT NULL,
        metric_label TEXT NOT NULL,
        metric_prefix TEXT DEFAULT '$',
        score_label TEXT DEFAULT 'Score Rating',
        table_name TEXT NOT NULL
    );
    """)

    cursor.execute("DELETE FROM dataset_registry;")
    cursor.execute("""
    INSERT INTO dataset_registry (id, name, subtitle, category_label, metric_label, metric_prefix, score_label, table_name)
    VALUES 
    ('employee_projects', 'Employee & Project Performance', 'Analyzing project timelines, department budget allocation, performance scores, and team effort.', 'Department', 'Budget', '$', 'Avg Performance Score', 'data_employee_projects'),
    ('ecommerce_sales', 'E-Commerce & Global Revenue', 'Omnichannel sales performance, regional customer orders, fulfillment status, and transaction margins.', 'Product Category', 'Revenue', '$', 'Customer Satisfaction %', 'data_ecommerce_sales'),
    ('saas_metrics', 'SaaS Product Growth & ARR Tracker', 'Monitoring monthly recurring revenue, customer acquisition cost, conversion funnels, and feature adoption.', 'Product Module', 'ARR Impact', '$', 'NPS Score', 'data_saas_metrics');
    """)

    cursor.execute("DROP TABLE IF EXISTS data_employee_projects;")
    cursor.execute("""
    CREATE TABLE data_employee_projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        category TEXT NOT NULL,
        status TEXT NOT NULL,
        priority TEXT NOT NULL,
        start_date TEXT,
        deadline TEXT,
        completion_date TEXT,
        budget REAL DEFAULT 0,
        score REAL DEFAULT 0,
        hours_logged INTEGER DEFAULT 0,
        team_members TEXT
    );
    """)

    employee_projects_data = [
        (1, "Cloud Infrastructure Migration", "Migrate legacy core services to GCP Kubernetes Cluster", "Engineering", "Completed", "High", "2025-08-04", "2025-12-02", "2025-11-27", 85000, 93.8, 219, "Alex Rivera, Michael Brown"),
        (2, "Customer Portal Redesign", "Complete UX revamp for customer self-service web app", "Design & UX", "Completed", "High", "2025-09-03", "2025-12-12", "2025-12-17", 62000, 94.0, 115, "Lucas Dubois"),
        (3, "Real-time Analytics Pipeline", "Implement Kafka + BigQuery pipeline for streaming events", "Data & Analytics", "Completed", "High", "2025-08-14", "2025-11-22", "2025-11-17", 95000, 91.8, 263, "Maya Lin, Rohan Gupta, Sophia Martinez"),
        (4, "Q2 Global Marketing Campaign", "Multi-channel advertising for product expansion", "Marketing & Growth", "Completed", "Medium", "2025-09-23", "2025-12-22", "2025-12-27", 45000, 85.7, 138, "Carlos Mendoza"),
        (5, "AI Code Assistant Integration", "Deploy LLM-powered autocomplete for internal tools", "Engineering", "Completed", "High", "2025-10-03", "2025-12-17", "2025-12-12", 75000, 87.4, 168, "Alex Rivera, Liam Chen"),
        (6, "Mobile App V2.0", "Major version release with biometrics and instant search", "Product Management", "Completed", "High", "2025-09-13", "2025-12-22", "2025-12-30", 110000, 82.8, 205, "Samantha Wu, Jordan Taylor"),
        (7, "Automated Churn Prediction Model", "Scikit-Learn & XGBoost pipeline targeting high risk accounts", "Data & Analytics", "Completed", "Medium", "2025-10-13", "2025-12-12", "2025-12-14", 40000, 90.5, 320, "Rohan Gupta, Sophia Martinez"),
        (8, "Brand Refresh & Style Guide", "Unified design system and asset library across platforms", "Design & UX", "Completed", "Low", "2025-10-23", "2025-12-22", "2025-12-20", 30000, 97.6, 42, "Lucas Dubois"),
        (9, "SEO Engine Optimization", "Core Web Vitals enhancement and structured data schema", "Marketing & Growth", "Completed", "Medium", "2025-11-02", "2025-12-17", "2025-12-22", 25000, 90.7, 143, "Ethan Hunt"),
        (10, "PCI-DSS Security Compliance Audit", "Remediation and compliance readiness for payment gateways", "Engineering", "Completed", "High", "2025-08-24", "2025-11-12", "2025-11-14", 50000, 88.9, 408, "Alex Rivera, Liam Chen, Michael Brown"),
        (11, "Enterprise API Gateway", "Unified GraphQL API layer for client microservices", "Engineering", "In Progress", "High", "2025-11-22", "2026-01-31", None, 90000, 82.8, 143, "Alex Rivera"),
        (12, "Customer Data Platform (CDP)", "Single customer view consolidating web, mobile, and CRM", "Data & Analytics", "In Progress", "High", "2025-12-02", "2026-02-15", None, 120000, 76.9, 238, "Sophia Martinez, Maya Lin, Rohan Gupta"),
        (13, "Next-Gen Onboarding Workflow", "Streamlined signup funnel reducing drop-off by 25%", "Product Management", "In Progress", "Medium", "2025-12-07", "2026-01-21", None, 35000, 79.8, 106, "Jordan Taylor"),
        (14, "Social Media Automation Tooling", "Content scheduling and automated engagement tracking", "Marketing & Growth", "Delayed", "Medium", "2025-11-02", "2025-12-27", None, 28000, 71.4, 245, "Carlos Mendoza, Emma Watson"),
        (15, "Dark Mode & Accessibility Audit", "WCAG 2.1 AA compliance across web and mobile web", "Design & UX", "In Progress", "Low", "2025-12-12", "2026-01-26", None, 22000, 78.8, 131, "Lucas Dubois, Chloe Kim"),
        (16, "Billing & Subscription Revamp", "Stripe integration for multi-currency tiered plans", "Engineering", "Delayed", "High", "2025-10-23", "2025-12-22", None, 80000, 73.8, 41, "Michael Brown"),
        (17, "Sales Funnel Attribution Engine", "Multi-touch attribution reporting in Looker", "Data & Analytics", "In Progress", "Medium", "2025-11-27", "2026-01-16", None, 48000, 88.0, 57, "Maya Lin"),
        (18, "Q3 Partner Ecosystem Launch", "Co-marketing and referral portal launch", "Marketing & Growth", "Planning", "Low", "2026-01-11", "2026-03-02", None, 32000, 80.0, 0, "Emma Watson"),
        (19, "Design System Tokenization", "Figma to CSS variable automated pipeline", "Design & UX", "In Progress", "Medium", "2025-12-17", "2026-01-31", None, 18000, 82.0, 218, "Lucas Dubois, Chloe Kim"),
        (20, "Data Warehouse Cost Optimization", "BigQuery query tuning and partition cleanup", "Data & Analytics", "Completed", "High", "2025-11-12", "2025-12-22", "2025-12-20", 15000, 92.5, 248, "Maya Lin, Sophia Martinez")
    ]

    cursor.executemany("""
    INSERT INTO data_employee_projects (id, title, description, category, status, priority, start_date, deadline, completion_date, budget, score, hours_logged, team_members)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, employee_projects_data)

    cursor.execute("DROP TABLE IF EXISTS data_ecommerce_sales;")
    cursor.execute("""
    CREATE TABLE data_ecommerce_sales (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        category TEXT NOT NULL,
        status TEXT NOT NULL,
        priority TEXT NOT NULL,
        start_date TEXT,
        deadline TEXT,
        completion_date TEXT,
        budget REAL DEFAULT 0,
        score REAL DEFAULT 0,
        hours_logged INTEGER DEFAULT 0,
        team_members TEXT
    );
    """)

    ecommerce_data = [
        (101, "UltraWireless Noise-Canceling Headphones", "Batch #402 Order fulfillment across North America", "Consumer Electronics", "Delivered", "High", "2025-11-01", "2025-11-05", "2025-11-04", 145000, 96.2, 120, "Logistics Alpha"),
        (102, "Ergonomic Mesh Office Chair", "Corporate bulk order for tech hub office upgrade", "Home & Furniture", "Delivered", "High", "2025-11-03", "2025-11-10", "2025-11-09", 88000, 92.0, 85, "Supply Chain Direct"),
        (103, "Winter Down Jacket Collection", "Flash sale campaign for EU retail stockists", "Apparel & Fashion", "Delivered", "Medium", "2025-11-10", "2025-11-20", "2025-11-18", 210000, 94.5, 140, "Global Fashion Dist"),
        (104, "Smart OLED Fitness Watch", "Holiday promo bundle shipment", "Sports & Fitness", "In Transit", "High", "2025-11-15", "2025-11-30", None, 175000, 89.1, 95, "APAC Logistics Hub"),
        (105, "Organic Hydrating Serum Set", "Direct-to-Consumer subscription deliveries", "Beauty & Personal Care", "Delivered", "Medium", "2025-11-05", "2025-11-12", "2025-11-11", 64000, 98.0, 60, "Beauty Ops"),
        (106, "4K Portable Gaming Monitor", "Black Friday pre-stock distribution", "Consumer Electronics", "In Transit", "High", "2025-11-18", "2025-12-05", None, 320000, 87.5, 210, "Electronics Express"),
        (107, "Minimalist Ceramic Dining Set", "Boutique store seasonal restocking", "Home & Furniture", "Processing", "Low", "2025-11-22", "2025-12-10", None, 42000, 85.0, 35, "Home Decor Warehouse"),
        (108, "Pro Trail Running Shoes", "E-Commerce fulfillment for marathon sponsors", "Sports & Fitness", "Delivered", "High", "2025-10-25", "2025-11-08", "2025-11-07", 115000, 95.3, 110, "Footwear Logistics"),
        (109, "Cashmere Knit Sweater Series", "Luxury retail inventory shipment", "Apparel & Fashion", "Returned", "Medium", "2025-11-02", "2025-11-15", "2025-11-16", 53000, 72.4, 45, "Apparel Returns Unit"),
        (110, "Anti-Aging Night Cream Duo", "Omnichannel replenishment order", "Beauty & Personal Care", "Delivered", "Low", "2025-11-12", "2025-11-22", "2025-11-21", 49000, 93.6, 50, "Skincare Logistics")
    ]

    cursor.executemany("""
    INSERT INTO data_ecommerce_sales (id, title, description, category, status, priority, start_date, deadline, completion_date, budget, score, hours_logged, team_members)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, ecommerce_data)

    cursor.execute("DROP TABLE IF EXISTS data_saas_metrics;")
    cursor.execute("""
    CREATE TABLE data_saas_metrics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        category TEXT NOT NULL,
        status TEXT NOT NULL,
        priority TEXT NOT NULL,
        start_date TEXT,
        deadline TEXT,
        completion_date TEXT,
        budget REAL DEFAULT 0,
        score REAL DEFAULT 0,
        hours_logged INTEGER DEFAULT 0,
        team_members TEXT
    );
    """)

    saas_data = [
        (201, "SSO & SAML 2.0 Enterprise Gate", "Multi-tenant auth support for Fortune 500 deals", "Security & IAM", "General Availability", "High", "2025-07-01", "2025-09-30", "2025-09-25", 180000, 91.0, 340, "Security Squad"),
        (202, "Salesforce & Hubspot Sync V3", "Two-way real-time data sync pipeline", "Integrations API", "General Availability", "High", "2025-08-15", "2025-10-31", "2025-10-28", 125000, 88.4, 290, "Ecosystem Team"),
        (203, "AI Document Summarizer Copilot", "LLM contextual summary inside task workspace", "AI Copilot", "Beta Testing", "High", "2025-09-01", "2025-12-15", None, 250000, 94.2, 420, "Applied AI Lab"),
        (204, "Usage-Based Metered Billing Engine", "Stripe Metering integration for API calls", "Billing & Analytics", "General Availability", "High", "2025-06-10", "2025-08-30", "2025-08-28", 95000, 86.0, 210, "Fintech Squad"),
        (205, "Realtime Collaborative Editor", "Operational Transform (OT) multi-user canvas", "Core Workspace", "Beta Testing", "High", "2025-09-15", "2026-01-31", None, 310000, 89.5, 510, "Core Platform Team"),
        (206, "Audit Logs Export to Datadog / Splunk", "Security compliance event streaming", "Security & IAM", "General Availability", "Medium", "2025-10-01", "2025-11-15", "2025-11-12", 60000, 92.5, 130, "SecOps"),
        (207, "Custom Webhook Builder Console", "Developer portal for custom API event triggers", "Integrations API", "In Development", "Medium", "2025-10-20", "2026-01-15", None, 78000, 82.0, 180, "DevRel & API Squad"),
        (208, "Predictive Churn Risk Widget", "Customer success dashboard alert for low usage", "Billing & Analytics", "In Development", "Low", "2025-11-01", "2026-02-01", None, 45000, 84.0, 95, "Data Analytics Team")
    ]

    cursor.executemany("""
    INSERT INTO data_saas_metrics (id, title, description, category, status, priority, start_date, deadline, completion_date, budget, score, hours_logged, team_members)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, saas_data)

    conn.commit()
    conn.close()
    print("Database 'dashboard.db' initialized successfully.")

if __name__ == "__main__":
    init_db()
