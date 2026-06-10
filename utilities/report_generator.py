
import os
import time
import re
from datetime import datetime

class ExecutionReportGenerator:
    @staticmethod
    def generate_report(log_file=None, output_dir="docs/executions"):
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_name = f"Execution_Summary_{file_timestamp}.html"
        report_path = os.path.join(output_dir, report_name)
        
        # Read latest log if not provided
        if not log_file:
            log_files = [os.path.join("logs", f) for f in os.listdir("logs") if f.endswith(".log") and "reversed" not in f]
            if log_files:
                log_file = max(log_files, key=os.path.getmtime)
            else:
                return "No log file found."

        log_content = ""
        if os.path.exists(log_file):
            with open(log_file, 'r') as f:
                log_content = f.read()

        # Simple log parsing for stats
        passed = len(re.findall(r"PASSED", log_content))
        failed = len(re.findall(r"FAILED", log_content))
        errors = len(re.findall(r"ERROR", log_content))
        total = passed + failed + errors

        html_template = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Execution Summary - {{timestamp}}</title>
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
                
                :root {{
                    --primary: #2563eb;
                    --secondary: #1e40af;
                    --success: #10b981;
                    --danger: #ef4444;
                    --warning: #f59e0b;
                    --bg: #f8fafc;
                    --card: #ffffff;
                    --text: #1e293b;
                }}

                body {{
                    font-family: 'Inter', sans-serif;
                    margin: 0;
                    padding: 0;
                    background: var(--bg);
                    color: var(--text);
                    line-height: 1.6;
                }}

                .container {{
                    max-width: 1000px;
                    margin: 40px auto;
                    padding: 0 20px;
                }}

                .header {{
                    background: white;
                    padding: 30px;
                    border-radius: 16px;
                    box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
                    text-align: center;
                    margin-bottom: 30px;
                    border-top: 6px solid var(--primary);
                }}

                .header img {{
                    height: 80px;
                    margin-bottom: 15px;
                }}

                .header h1 {{
                    margin: 0;
                    font-size: 28px;
                    color: var(--text);
                }}

                .header p {{
                    color: #64748b;
                    margin: 5px 0 0 0;
                }}

                .stats-grid {{
                    display: grid;
                    grid-template-columns: repeat(4, 1fr);
                    gap: 20px;
                    margin-bottom: 30px;
                }}

                .stat-card {{
                    background: white;
                    padding: 20px;
                    border-radius: 12px;
                    box-shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1);
                    text-align: center;
                }}

                .stat-card .label {{
                    font-size: 14px;
                    color: #64748b;
                    font-weight: 600;
                    text-transform: uppercase;
                }}

                .stat-card .value {{
                    font-size: 32px;
                    font-weight: 700;
                    margin-top: 5px;
                }}

                .stat-total {{ border-bottom: 4px solid var(--primary); }}
                .stat-passed {{ border-bottom: 4px solid var(--success); color: var(--success); }}
                .stat-failed {{ border-bottom: 4px solid var(--danger); color: var(--danger); }}
                .stat-errors {{ border-bottom: 4px solid var(--warning); color: var(--warning); }}

                .log-section {{
                    background: white;
                    padding: 30px;
                    border-radius: 16px;
                    box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
                }}

                .log-section h2 {{
                    margin-top: 0;
                    font-size: 20px;
                    display: flex;
                    align-items: center;
                    gap: 10px;
                }}

                pre {{
                    background: #1e293b;
                    color: #e2e8f0;
                    padding: 20px;
                    border-radius: 8px;
                    overflow-x: auto;
                    font-family: 'Fira Code', monospace;
                    font-size: 13px;
                    max-height: 600px;
                    border-left: 4px solid var(--primary);
                }}

                .footer {{
                    text-align: center;
                    margin-top: 40px;
                    padding-bottom: 40px;
                    color: #94a3b8;
                    font-size: 14px;
                }}

                @media print {{
                    .container {{ margin: 0; max-width: 100%; }}
                    .header, .stat-card, .log-section {{ box-shadow: none; border: 1px solid #e2e8f0; }}
                    body {{ background: white; }}
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <img src="https://upload.wikimedia.org/wikipedia/en/2/23/NIOS_Logo.png" alt="NIOS Logo">
                    <h1>Automation Execution Summary</h1>
                    <p>Bridge Automation Framework | Test Run Report</p>
                    <p><strong>Generated on:</strong> {timestamp}</p>
                </div>

                <div class="stats-grid">
                    <div class="stat-card stat-total">
                        <div class="label">Total Scenarios</div>
                        <div class="value">{total}</div>
                    </div>
                    <div class="stat-card stat-passed">
                        <div class="label">Passed</div>
                        <div class="value">{passed}</div>
                    </div>
                    <div class="stat-card stat-failed">
                        <div class="label">Failed</div>
                        <div class="value">{failed}</div>
                    </div>
                    <div class="stat-card stat-errors">
                        <div class="label">Errors</div>
                        <div class="value">{errors}</div>
                    </div>
                </div>

                <div class="log-section">
                    <h2>Detailed Execution Logs</h2>
                    <pre>{log_content.replace("<", "&lt;").replace(">", "&gt;")}</pre>
                </div>

                <div class="footer">
                    &copy; 2026 Bridge Automation Framework | Private & Confidential
                </div>
            </div>
        </body>
        </html>
        """
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(html_template)
            
        print(f"Execution report generated: {report_path}")
        return report_path

if __name__ == "__main__":
    ExecutionReportGenerator.generate_report()
