import openpyxl
import os
import html

reports = [
    ('1-Load-Test-Report-100VUs-Passed', '⚡ Load & Baseline Test (100 VUs - 1 min)'),
    ('2-Security-Vulnerability-Report', '🛡️ Security Assessment & Vulnerability Audit'),
    ('3-Selenium-Web-E2E-300-Tests-Passed', '🌐 Selenium Web E2E (330 Tests Passed)'),
    ('4-Appium-Mobile-330-Tests-Passed', '📱 Appium Mobile E2E (330 Tests Passed)')
]

for filename, title in reports:
    xlsx_path = os.path.join('Test-Reports-Passed-Excel', f'{filename}.xlsx')
    if not os.path.exists(xlsx_path):
        continue
    wb = openpyxl.load_workbook(xlsx_path, data_only=True)
    
    html_parts = [
        '<!DOCTYPE html>',
        '<html lang="en">',
        '<head>',
        '  <meta charset="UTF-8">',
        f'  <title>{title} - AGRO AI</title>',
        '  <style>',
        "    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background: #f8fafc; color: #1e293b; margin: 0; padding: 24px; }",
        '    .header { background: #166534; color: white; padding: 20px 24px; border-radius: 12px; margin-bottom: 24px; box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1); }',
        '    .header h1 { margin: 0 0 6px 0; font-size: 22px; }',
        '    .header p { margin: 0; opacity: 0.9; font-size: 14px; }',
        '    .tabs { display: flex; gap: 8px; margin-bottom: 16px; border-bottom: 2px solid #e2e8f0; padding-bottom: 8px; flex-wrap: wrap; }',
        '    .tab-btn { background: #e2e8f0; border: none; padding: 8px 16px; border-radius: 6px; font-weight: 600; cursor: pointer; font-size: 13px; color: #475569; }',
        '    .tab-btn.active { background: #166534; color: white; }',
        '    .tab-content { display: none; background: white; border-radius: 12px; padding: 20px; box-shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1); overflow-x: auto; }',
        '    .tab-content.active { display: block; }',
        '    table { width: 100%; border-collapse: collapse; font-size: 13px; margin-top: 8px; }',
        '    th, td { border: 1px solid #e2e8f0; padding: 8px 12px; text-align: left; }',
        '    th { background: #f1f5f9; font-weight: 600; color: #0f172a; position: sticky; top: 0; }',
        '    tr:nth-child(even) { background: #f8fafc; }',
        '    tr:hover { background: #f0fdf4; }',
        '    .badge-pass { background: #dcfce7; color: #166534; padding: 2px 8px; border-radius: 9999px; font-weight: 600; font-size: 11px; }',
        '    .badge-fail { background: #fee2e2; color: #991b1b; padding: 2px 8px; border-radius: 9999px; font-weight: 600; font-size: 11px; }',
        '    .badge-high { background: #fef08a; color: #854d0e; padding: 2px 8px; border-radius: 9999px; font-weight: 600; font-size: 11px; }',
        '  </style>',
        '</head>',
        '<body>',
        '  <div class="header">',
        f'    <h1>{title}</h1>',
        '    <p>AGRO AI Automated Test Report • Interactive Microsoft Edge / Browser View</p>',
        '  </div>',
        '  <div class="tabs">'
    ]

    for i, sname in enumerate(wb.sheetnames):
        active_cls = 'active' if i == 0 else ''
        html_parts.append(f'    <button class="tab-btn {active_cls}" onclick="switchTab(event, \'tab_{i}\')">{html.escape(sname)}</button>')
    html_parts.append('  </div>')

    for i, sname in enumerate(wb.sheetnames):
        ws = wb[sname]
        active_cls = 'active' if i == 0 else ''
        html_parts.append(f'  <div id="tab_{i}" class="tab-content {active_cls}">')
        html_parts.append('    <table>')
        
        rows = list(ws.iter_rows(values_only=True))
        if rows:
            for r_idx, row in enumerate(rows):
                if not any(row):
                    continue
                tag = 'th' if r_idx == 0 or (r_idx < 4 and len([c for c in row if c]) > 2) else 'td'
                html_parts.append('      <tr>')
                for cell in row:
                    val = str(cell) if cell is not None else ''
                    val_str = html.escape(val)
                    if val in ['PASS', 'Passed', 'PASSED', '100%']:
                        val_str = f'<span class="badge-pass">{val_str}</span>'
                    elif val in ['FAIL', 'Failed', 'FAILED']:
                        val_str = f'<span class="badge-fail">{val_str}</span>'
                    elif val in ['HIGH', 'CRITICAL']:
                        val_str = f'<span class="badge-high">{val_str}</span>'
                    html_parts.append(f'        <{tag}>{val_str}</{tag}>')
                html_parts.append('      </tr>')
        html_parts.append('    </table>')
        html_parts.append('  </div>')

    html_parts.extend([
        '  <script>',
        '    function switchTab(evt, tabId) {',
        "      document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));",
        "      document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));",
        "      evt.currentTarget.classList.add('active');",
        "      document.getElementById(tabId).classList.add('active');",
        '    }',
        '  </script>',
        '</body>',
        '</html>'
    ])

    out_html = os.path.join('Test-Reports-Passed-Excel', f'{filename}.html')
    with open(out_html, 'w', encoding='utf-8') as f:
        f.write('\n'.join(html_parts))
    print(f'Generated: {out_html}')
