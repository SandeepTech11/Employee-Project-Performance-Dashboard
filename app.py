"""
Employee & Project Performance Dashboard - Python + SQL Analytics
Uses Flask + SQLite3 (SQL query engine) + HTML5 + CSS.
"""

from flask import Flask, render_template, request, jsonify, Response
import sqlite3
import pandas as pd
import os
import re
import csv
import io

app = Flask(__name__, template_folder="templates", static_folder="static")

DB_PATH = os.path.join(os.path.dirname(__file__), "dashboard.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def sanitize_table_name(name):
    clean = re.sub(r'[^a-zA-Z0-9_]', '_', name).lower()
    return f"data_custom_{clean}"

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, subtitle, category_label, metric_label, metric_prefix, score_label, table_name FROM dataset_registry;")
    datasets = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return render_template('dashboard.html', datasets=datasets)

@app.route('/api/query', methods=['GET'])
def query_dashboard():
    dataset_id = request.args.get('dataset', 'employee_projects')
    search_q = request.args.get('search', '').strip()
    category = request.args.get('category', 'ALL')
    status = request.args.get('status', 'ALL')
    priority = request.args.get('priority', 'ALL')
    start_date = request.args.get('start_date', '').strip()
    end_date = request.args.get('end_date', '').strip()

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM dataset_registry WHERE id = ?;", (dataset_id,))
    ds_row = cursor.fetchone()

    if not ds_row:
        conn.close()
        return jsonify({'error': 'Dataset not found'}), 404

    ds_meta = dict(ds_row)
    table_name = ds_meta['table_name']

    where_clauses = []
    params = []

    if search_q:
        where_clauses.append("(title LIKE ? OR description LIKE ? OR category LIKE ? OR status LIKE ?)")
        search_pattern = f"%{search_q}%"
        params.extend([search_pattern, search_pattern, search_pattern, search_pattern])

    if category != 'ALL':
        where_clauses.append("category = ?")
        params.append(category)

    if status != 'ALL':
        where_clauses.append("status = ?")
        params.append(status)

    if priority != 'ALL':
        where_clauses.append("priority = ?")
        params.append(priority)

    if start_date:
        where_clauses.append("start_date >= ?")
        params.append(start_date)

    if end_date:
        where_clauses.append("start_date <= ?")
        params.append(end_date)

    where_sql = (" WHERE " + " AND ".join(where_clauses)) if where_clauses else ""

    records_sql = f"SELECT id, title, description, category, status, priority, start_date, deadline, completion_date, budget, score, hours_logged, team_members FROM {table_name}{where_sql} ORDER BY id ASC;"
    cursor.execute(records_sql, params)
    records = [dict(row) for row in cursor.fetchall()]

    kpi_sql = f"SELECT COUNT(*) as total_count, COALESCE(SUM(budget), 0) as total_budget, COALESCE(AVG(score), 0) as avg_score, COALESCE(SUM(hours_logged), 0) as total_hours FROM {table_name}{where_sql};"
    cursor.execute(kpi_sql, params)
    kpi_row = dict(cursor.fetchone())

    pie_sql = f"SELECT status, COUNT(*) as cnt FROM {table_name}{where_sql} GROUP BY status ORDER BY cnt DESC;"
    cursor.execute(pie_sql, params)
    status_distribution = [dict(row) for row in cursor.fetchall()]

    bar_sql = f"SELECT category, SUM(budget) as total_budget, COUNT(*) as cnt FROM {table_name}{where_sql} GROUP BY category ORDER BY total_budget DESC;"
    cursor.execute(bar_sql, params)
    category_distribution = [dict(row) for row in cursor.fetchall()]

    priority_sql = f"SELECT priority, COUNT(*) as cnt FROM {table_name}{where_sql} GROUP BY priority ORDER BY cnt DESC;"
    cursor.execute(priority_sql, params)
    priority_distribution = [dict(row) for row in cursor.fetchall()]

    cursor.execute(f"SELECT DISTINCT category FROM {table_name} WHERE category IS NOT NULL ORDER BY category ASC;")
    all_categories = [row['category'] for row in cursor.fetchall()]

    cursor.execute(f"SELECT DISTINCT status FROM {table_name} WHERE status IS NOT NULL ORDER BY status ASC;")
    all_statuses = [row['status'] for row in cursor.fetchall()]

    conn.close()

    return jsonify({
        'meta': ds_meta,
        'slicers': {
            'categories': all_categories,
            'statuses': all_statuses
        },
        'kpis': {
            'total_count': kpi_row['total_count'],
            'total_budget': round(kpi_row['total_budget'], 2),
            'avg_score': round(kpi_row['avg_score'], 1),
            'total_hours': kpi_row['total_hours']
        },
        'charts': {
            'status_pie': status_distribution,
            'category_bar': category_distribution,
            'priority_bar': priority_distribution
        },
        'records': records
    })

@app.route('/upload_dataset', methods=['POST'])
def upload_dataset():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    dataset_name = request.form.get('name', '').strip() or file.filename.rsplit('.', 1)[0]
    category_label = request.form.get('category_label', 'Category').strip()
    metric_label = request.form.get('metric_label', 'Metric Value').strip()

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    filename = file.filename
    ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''

    try:
        if ext == 'csv':
            df = pd.read_csv(file)
        elif ext == 'json':
            df = pd.read_json(file)
        else:
            return jsonify({'error': 'Only .CSV and .JSON files are supported'}), 400

        if df.empty:
            return jsonify({'error': 'Uploaded file is empty'}), 400

        title_col = next((c for c in df.columns if any(k in c.lower() for k in ['title', 'name', 'project', 'item', 'subject'])), df.columns[0])
        category_col = next((c for c in df.columns if any(k in c.lower() for k in ['dept', 'department', 'category', 'group', 'type'])), df.columns[1] if len(df.columns) > 1 else df.columns[0])
        status_col = next((c for c in df.columns if any(k in c.lower() for k in ['status', 'state', 'phase'])), df.columns[2] if len(df.columns) > 2 else df.columns[0])
        priority_col = next((c for c in df.columns if any(k in c.lower() for k in ['priority', 'level', 'urgency'])), None)
        numeric_col = next((c for c in df.columns if any(k in c.lower() for k in ['budget', 'revenue', 'cost', 'price', 'amount', 'val', 'value'])), None)
        date_col = next((c for c in df.columns if any(k in c.lower() for k in ['date', 'start', 'created', 'time'])), None)
        score_col = next((c for c in df.columns if any(k in c.lower() for k in ['score', 'rating', 'nps', 'percent', 'pct'])), None)

        safe_id = sanitize_table_name(dataset_name)
        sql_table_name = safe_id

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(f"DROP TABLE IF EXISTS {sql_table_name};")

        cursor.execute(f"""
        CREATE TABLE {sql_table_name} (
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

        records_to_insert = []
        for idx, row in df.iterrows():
            title_val = str(row[title_col]) if pd.notna(row[title_col]) else f"Item #{idx+1}"
            category_val = str(row[category_col]) if pd.notna(row[category_col]) else "General"
            status_val = str(row[status_col]) if pd.notna(row[status_col]) else "Active"
            priority_val = str(row[priority_col]) if priority_col and pd.notna(row[priority_col]) else ("High" if idx % 3 == 0 else "Medium")
            
            budget_val = 0.0
            if numeric_col and pd.notna(row[numeric_col]):
                try:
                    budget_val = float(re.sub(r'[^0-9.-]+', '', str(row[numeric_col])))
                except:
                    budget_val = 0.0

            score_val = 85.0
            if score_col and pd.notna(row[score_col]):
                try:
                    score_val = float(re.sub(r'[^0-9.-]+', '', str(row[score_col])))
                except:
                    score_val = 85.0

            date_val = str(row[date_col])[:10] if date_col and pd.notna(row[date_col]) else "2026-01-15"

            records_to_insert.append((
                title_val,
                f"Custom record from {filename}",
                category_val,
                status_val,
                priority_val,
                date_val,
                "2026-12-31",
                "2026-06-30" if "complete" in status_val.lower() else None,
                budget_val,
                score_val,
                int(budget_val / 500) if budget_val > 0 else (idx + 1) * 20,
                "Custom Lead"
            ))

        cursor.executemany(f"""
        INSERT INTO {sql_table_name} (title, description, category, status, priority, start_date, deadline, completion_date, budget, score, hours_logged, team_members)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, records_to_insert)

        ds_id = f"custom_{safe_id}"
        cursor.execute("DELETE FROM dataset_registry WHERE id = ?;", (ds_id,))
        cursor.execute("""
        INSERT INTO dataset_registry (id, name, subtitle, category_label, metric_label, metric_prefix, score_label, table_name)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?);
        """, (
            ds_id,
            dataset_name,
            f"Custom dataset uploaded from '{filename}' ({len(records_to_insert)} records).",
            category_label,
            metric_label,
            "$",
            "Score Rating",
            sql_table_name
        ))

        conn.commit()
        conn.close()

        return jsonify({
            'success': True,
            'dataset_id': ds_id,
            'name': dataset_name,
            'record_count': len(records_to_insert)
        })

    except Exception as e:
        return jsonify({'error': f'Failed to process file: {str(e)}'}), 500

@app.route('/export_csv', methods=['GET'])
def export_csv():
    dataset_id = request.args.get('dataset', 'employee_projects')
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT table_name, name FROM dataset_registry WHERE id = ?;", (dataset_id,))
    ds_row = cursor.fetchone()
    if not ds_row:
        conn.close()
        return "Dataset not found", 404

    table_name = ds_row['table_name']

    cursor.execute(f"SELECT id, title, description, category, status, priority, start_date, deadline, budget, score, hours_logged FROM {table_name};")
    rows = cursor.fetchall()
    conn.close()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['ID', 'Title', 'Description', 'Category', 'Status', 'Priority', 'Start Date', 'Deadline', 'Budget', 'Score', 'Hours Logged'])

    for row in rows:
        writer.writerow(list(row))

    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-disposition": f"attachment; filename={dataset_id}_export.csv"}
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
