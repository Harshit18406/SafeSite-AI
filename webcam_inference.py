import cv2
from ultralytics import YOLO
import csv
from datetime import datetime
import os
import time

# 1. Load the Custom Model and Bind Webcam Node
model = YOLO('best_ppe.pt')
cap = cv2.VideoCapture(0)

log_file = 'safety_logs.csv'
html_file = 'dashboard.html'

# Setup/Reset CSV Log File (Wipes previous run data for a clean interview demo)
with open(log_file, mode='w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Timestamp', 'Violation_Type', 'Status'])

# Anti-spam Logging Cooldown Parameters
last_log_time = 0
log_cooldown = 5  # Seconds before recording a consecutive violation

def generate_html_dashboard():
    """Reads the CSV log registry and builds a high-end, clean single-page dashboard."""
    if not os.path.exists(log_file):
        return

    # Ingest historical records from local CSV
    rows = []
    with open(log_file, mode='r') as f:
        reader = csv.reader(f)
        headers = next(reader)  # Skip table header row
        for row in reader:
            rows.append(row)

    total_violations = len(rows)
    hat_missed = sum(1 for r in rows if 'NO-Hardhat' in r[1])
    vest_missed = sum(1 for r in rows if 'NO-Safety Vest' in r[1])

    # Build incident table rows dynamically using modern dark utility styling
    table_rows_html = ""
    for r in reversed(rows):
        table_rows_html += f"""
        <tr>
            <td style="font-family: monospace; color: #94a3b8;">{r[0]}</td>
            <td><span class="badge badge-danger">{r[1]}</span></td>
            <td><span class="status">CRITICAL</span></td>
        </tr>
        """

    # Modern Enterprise Executive Dashboard Layout (Clean & Focused)
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>SafeSite AI Engine | Analytics Console</title>
        <meta http-equiv="refresh" content="5">
        <style>
            :root {{
                --bg-primary: #0f172a;
                --bg-surface: #1e293b;
                --text-main: #f8fafc;
                --text-muted: #94a3b8;
                --accent-danger: #ef4444;
                --accent-warning: #f59e0b;
                --accent-safe: #10b981;
            }}
            * {{ box-sizing: border-box; margin: 0; padding: 0; }}
            body {{ 
                font-family: 'Segoe UI', system-ui, -apple-system, sans-serif; 
                background-color: var(--bg-primary); 
                color: var(--text-main);
                background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
                min-height: 100vh;
                padding: 40px;
            }}
            
            .container {{
                max-width: 1200px;
                margin: 0 auto;
            }}

            /* Top Navigation Bar Component */
            .navbar {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding-bottom: 20px;
                border-bottom: 1px solid #1e293b;
                margin-bottom: 35px;
            }}
            .navbar .logo {{ font-size: 22px; font-weight: 800; color: var(--accent-safe); letter-spacing: 1px; }}
            .navbar .live-indicator {{
                display: flex;
                align-items: center;
                gap: 8px;
                background: rgba(16, 185, 129, 0.1);
                padding: 6px 14px;
                border-radius: 20px;
                font-size: 12px;
                font-weight: 700;
                color: var(--accent-safe);
                border: 1px solid rgba(16, 185, 129, 0.2);
            }}
            .live-dot {{ width: 8px; height: 8px; background: var(--accent-safe); border-radius: 50%; animation: pulse 1.5s infinite; }}
            @keyframes pulse {{ 0% {{ opacity: 0.4; }} 50% {{ opacity: 1; }} 100% {{ opacity: 0.4; }} }}

            .header h1 {{ font-size: 28px; font-weight: 700; margin-bottom: 8px; }}
            .header p {{ color: var(--text-muted); font-size: 14px; margin-bottom: 35px; }}
            
            /* Grid Data Layouts */
            .metrics-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px; margin-bottom: 40px; }}
            .card {{ background: var(--bg-surface); border: 1px solid #334155; padding: 24px; border-radius: 12px; position: relative; overflow: hidden; }}
            .card h3 {{ font-size: 12px; font-weight: 600; text-transform: uppercase; color: var(--text-muted); letter-spacing: 0.5px; }}
            .card p {{ font-size: 36px; font-weight: 800; margin-top: 12px; }}
            .card::after {{ content: ''; position: absolute; bottom: 0; left: 0; width: 100%; height: 4px; }}
            .card.violations::after {{ background: var(--accent-danger); }}
            .card.hardhats::after {{ background: var(--accent-warning); }}
            .card.vests::after {{ background: var(--accent-safe); }}
            
            /* Clean Matrix Table styling */
            .table-container {{ background: var(--bg-surface); border: 1px solid #334155; border-radius: 12px; overflow: hidden; }}
            .table-title {{ padding: 20px 24px; font-size: 16px; font-weight: 600; border-bottom: 1px solid #334155; background: #162238; }}
            table {{ width: 100%; border-collapse: collapse; text-align: left; }}
            th, td {{ padding: 16px 24px; font-size: 14px; }}
            th {{ background: #162238; color: var(--text-muted); font-weight: 600; text-transform: uppercase; font-size: 11px; letter-spacing: 0.5px; border-bottom: 1px solid #334155; }}
            td {{ border-bottom: 1px solid #334155; color: #cbd5e1; }}
            tr:last-child td {{ border-bottom: none; }}
            
            /* Badges & Status Indicators */
            .badge {{ display: inline-block; padding: 4px 10px; border-radius: 20px; font-size: 11px; font-weight: 600; }}
            .badge-danger {{ background: rgba(239, 68, 68, 0.15); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.3); }}
            .status {{ display: inline-flex; align-items: center; gap: 6px; font-weight: 600; font-size: 12px; color: var(--accent-danger); }}
            .status::before {{ content: ''; display: inline-block; width: 8px; height: 8px; background: var(--accent-danger); border-radius: 50%; box-shadow: 0 0 8px var(--accent-danger); }}
        </style>
    </head>
    <body>

        <div class="container">
            <div class="navbar">
                <div class="logo">SAFESITE AI</div>
                <div class="live-indicator">
                    <div class="live-dot"></div>
                    <span>LIVE COMPLIANCE FEED ACTIVE</span>
                </div>
            </div>

            <div class="header">
                <h1>AI Edge Safety Control Console</h1>
                <p>Real-time edge telemetry monitoring site environments for active PPE violations and structural compliance rates.</p>
            </div>
            
            <div class="metrics-grid">
                <div class="card violations"><h3>🚨 Active Violations Logged</h3><p>{total_violations}</p></div>
                <div class="card hardhats"><h3>🪖 Missing Hardhat Alerts</h3><p>{hat_missed}</p></div>
                <div class="card vests"><h3>🦺 Missing Safety Vests</h3><p>{vest_missed}</p></div>
            </div>
            
            <div class="table-container">
                <div class="table-title">Live Incident Stream Registry</div>
                <table>
                    <thead>
                        <tr><th>Timestamp</th><th>Identified Violation Scope</th><th>Risk Assessment Level</th></tr>
                    </thead>
                    <tbody>
                        {table_rows_html}
                    </tbody>
                </table>
            </div>
        </div>

    </body>
    </html>
    """

    # Forces file creation using explicit UTF-8 rules to prevent Windows Emoji errors
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

# Compiles initial dashboard configuration file layout on start-up
generate_html_dashboard()

print("Safety System Engine Online... Press 'q' key in video preview window to terminate execution loop.")

# 2. Main High-Performance Processing Real-time Stream Loop
while True:
    ret, frame = cap.read()
    if not ret: 
        break

    # Execute downsampled high-speed inference sweep via local computing layers
    results = model(frame, conf=0.50, imgsz=320)[0]
    violation_detected = False
    current_violations = []
    
    # Evaluate parsed vector array outputs matching target domains
    for box in results.boxes:
        cls_id = int(box.cls[0])
        class_name = model.names[cls_id]
        if class_name in ["NO-Hardhat", "NO-Safety Vest"]:
            violation_detected = True
            if class_name not in current_violations:
                current_violations.append(class_name)

    # Draw native bounding layer tags over matrix layer copy
    annotated_frame = results.plot()
    h, w, _ = annotated_frame.shape
    current_time = time.time()

    if violation_detected:
        # Overlay Warning Bar notification blocks inside video stream matrix
        cv2.rectangle(annotated_frame, (0, 0), (w, 60), (0, 0, 255), -1)
        cv2.putText(annotated_frame, "WARNING: PPE VIOLATION", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
        # Verify if anti-flood lock timer parameters are cleared
        if current_time - last_log_time > log_cooldown:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            violation_str = " & ".join(current_violations)
            
            # Commit unique incident row parameters to persistent CSV
            with open(log_file, mode='a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([timestamp, violation_str, 'UNSAFE'])
            
            print(f"🚨 Logged Violation: {violation_str} at {timestamp}")
            
            # Recompile and generate updated structural view sheets dynamically
            generate_html_dashboard()
            last_log_time = current_time
            
    else:
        # Overlay Safe Status Bar notification blocks inside video stream matrix
        cv2.rectangle(annotated_frame, (0, 0), (w, 60), (0, 255, 0), -1)
        cv2.putText(annotated_frame, "SYSTEM SAFE: COMPLIANT", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

    # Output dynamic window graphics elements onto screen layout layer
    cv2.imshow("Worker Safety Detection System", annotated_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'): 
        break

# Safely close pipeline stream processes and return compute pools
cap.release()
cv2.destroyAllWindows()