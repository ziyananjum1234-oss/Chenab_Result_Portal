import os
import base64
import json
import pandas as pd

desktop = r"C:\Users\IT_OFFICE02\Desktop"
portal_folder = os.path.join(desktop, "Chenab_Result_Portal")
os.makedirs(portal_folder, exist_ok=True)

logo_path = os.path.join(desktop, "chenab_logo.jpg")
logo_b64 = ""
if os.path.exists(logo_path):
    with open(logo_path, "rb") as f:
        logo_b64 = "data:image/jpeg;base64," + base64.b64encode(f.read()).decode("utf-8")

excel_path = os.path.join(desktop, "rptConsolidatedResultSheet.xls")
if not os.path.exists(excel_path):
    excel_path = os.path.join(portal_folder, "rptConsolidatedResultSheet.xls")

df = pd.read_excel(excel_path)

institute = str(df.iloc[0, 2]).strip()
test_name = str(df.iloc[0, 7]).strip()
session = str(df.iloc[1, 7]).strip()
class_name = str(df.iloc[3, 3]).strip()
exam_date = str(df.iloc[4, 7]).strip()

def get_grade(pct):
    if pct >= 90: return "A+"
    if pct >= 80: return "A"
    if pct >= 70: return "B"
    if pct >= 60: return "C"
    if pct >= 50: return "D"
    return "F"

def get_remarks(pct):
    if pct >= 90: return "Outstanding performance! Keep maintaining this exemplary standard."
    if pct >= 80: return "Excellent achievement! High academic dedication demonstrated."
    if pct >= 70: return "Very good result. With focused effort, can achieve top grades."
    if pct >= 60: return "Good effort. Consistent revision recommended for improvement."
    if pct >= 50: return "Satisfactory progress. Needs to devote more time to studies."
    return "Needs immediate academic attention and remedial guidance."

students = []
subject_defs = [
    ("English", "ENG", 7),
    ("Urdu", "URD", 8),
    ("Mathematics", "MTH", 9),
    ("Science", "SCI", 10),
    ("Social Studies", "SST", 11),
    ("Islamiat", "ISL", 12),
    ("Quranic Education", "Q.E", 13),
    ("Computer Science", "CSC", 14),
]

for idx in range(9, 33):
    sid = str(df.iloc[idx, 1]).strip()
    if not sid or sid == "nan":
        continue
    name = str(df.iloc[idx, 3]).strip()
    class_pos = str(df.iloc[idx, 4]).strip() if pd.notna(df.iloc[idx, 4]) else "-"
    sec_pos = str(df.iloc[idx, 6]).strip() if pd.notna(df.iloc[idx, 6]) else "-"
    
    subjects = []
    for s_name, s_code, col_idx in subject_defs:
        raw_val = str(df.iloc[idx, col_idx]).strip()
        max_m = 25.0
        pass_m = 10.0
        
        is_leave = raw_val in ["(L)", "L", "Leave", "LEAVE"]
        if is_leave:
            sub_pct = "-"
            sub_grade = "Leave"
            sub_status = "Leave"
            sub_obt = "Leave"
        else:
            try:
                obt_f = float(raw_val)
                pct_calc = round((obt_f / max_m) * 100, 1)
                sub_pct = f"{pct_calc:.1f}%"
                sub_grade = get_grade(pct_calc)
                sub_status = "Pass" if obt_f >= pass_m else "Fail"
                sub_obt = f"{obt_f:g}"
            except:
                sub_pct = "-"
                sub_grade = "-"
                sub_status = "N/A"
                sub_obt = raw_val

        subjects.append({
            "name": s_name,
            "code": s_code,
            "max": 25,
            "pass": 10,
            "obtained": sub_obt,
            "percentage": sub_pct,
            "grade": sub_grade,
            "status": sub_status
        })

    ttl_mark = str(df.iloc[idx, 15]).strip()
    obt_mark = str(df.iloc[idx, 16]).strip()
    pct_raw = str(df.iloc[idx, 17]).strip()
    
    try:
        pct_float = float(pct_raw)
        calc_grade = get_grade(pct_float)
        calc_remarks = get_remarks(pct_float)
    except:
        pct_float = 0
        calc_grade = "-"
        calc_remarks = "-"

    grade = str(df.iloc[idx, 18]).strip() if pd.notna(df.iloc[idx, 18]) and str(df.iloc[idx, 18]).strip() != "nan" else calc_grade
    status = str(df.iloc[idx, 19]).strip()
    
    students.append({
        "id": sid,
        "name": name,
        "class_pos": class_pos,
        "sec_pos": sec_pos,
        "subjects": subjects,
        "total_marks": ttl_mark,
        "obtained_marks": obt_mark,
        "percentage": pct_raw,
        "grade": grade,
        "remarks": calc_remarks,
        "status": status
    })

portal_data = {
    "institute": institute,
    "test_name": test_name,
    "session": session,
    "class_name": class_name,
    "exam_date": exam_date,
    "total_students": len(students),
    "students": students
}

with open(os.path.join(portal_folder, "data.json"), "w", encoding="utf-8") as f:
    json.dump(portal_data, f, ensure_ascii=False, indent=2)

json_str = json.dumps(portal_data)

html_code = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Online Result Portal &bull; Chenab College Shorkot</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;800;900&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Playfair+Display:ital,wght@0,600;1,600&display=swap" rel="stylesheet">
    <style>
        :root {{
            --navy-deep: #081d38;
            --navy-card: #0c274a;
            --navy-light: #163660;
            --gold: #c69222;
            --gold-light: #dfb249;
            --gold-subtle: #fcf8ee;
            --gold-border: #e6cb85;
            --slate-bg: #f3f6fa;
            --text-dark: #0f172a;
            --text-muted: #52637a;
            --border-soft: #e2e8f0;
            --success-green: #0d824d;
            --success-bg: #eafaf1;
            --danger-red: #c02626;
            --danger-bg: #fdf2f2;
            --leave-orange: #b45309;
            --leave-bg: #fffbeb;
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        body {{
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: var(--slate-bg);
            color: var(--text-dark);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            line-height: 1.5;
            background-image: 
                radial-gradient(at 0% 0%, rgba(12, 39, 74, 0.03) 0px, transparent 50%),
                radial-gradient(at 100% 100%, rgba(198, 146, 34, 0.04) 0px, transparent 50%);
        }}

        .wrapper {{
            width: 100%;
            max-width: 900px;
            padding: 40px 16px 60px;
            display: flex;
            flex-direction: column;
            gap: 28px;
        }}

        /* Clean Executive Header */
        .executive-header {{
            background: #ffffff;
            border-radius: 20px;
            padding: 36px 24px;
            text-align: center;
            border: 1px solid rgba(226, 232, 240, 0.9);
            box-shadow: 0 10px 30px -8px rgba(8, 29, 56, 0.07);
            position: relative;
            overflow: hidden;
        }}
        .executive-header::before {{
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 5px;
            background: linear-gradient(90deg, var(--navy-deep), var(--gold), var(--navy-deep));
        }}

        .college-logo {{
            width: 95px;
            height: 95px;
            object-fit: contain;
            margin: 0 auto 14px;
            display: block;
            border-radius: 50%;
            border: 3px solid var(--gold);
            padding: 4px;
            background: #ffffff;
            box-shadow: 0 4px 16px rgba(198, 146, 34, 0.2);
        }}

        .college-title {{
            font-family: 'Cinzel', Georgia, serif;
            font-size: 2.15rem;
            color: var(--navy-deep);
            font-weight: 800;
            letter-spacing: 0.8px;
            text-transform: uppercase;
            line-height: 1.2;
            margin-bottom: 6px;
        }}

        .controller-tag {{
            font-size: 0.95rem;
            font-weight: 700;
            color: var(--gold);
            text-transform: uppercase;
            letter-spacing: 2px;
            margin-bottom: 14px;
            display: inline-block;
        }}

        .exam-info-badges {{
            display: inline-flex;
            gap: 10px;
            background: #f8fafc;
            border: 1px solid var(--border-soft);
            padding: 8px 22px;
            border-radius: 40px;
            font-size: 0.85rem;
            color: var(--text-muted);
            font-weight: 600;
            flex-wrap: wrap;
            justify-content: center;
        }}
        .exam-info-badges strong {{
            color: var(--navy-deep);
        }}

        /* Clean Search Box ONLY */
        .search-container {{
            background: #ffffff;
            border-radius: 20px;
            padding: 32px 28px;
            border: 1px solid var(--border-soft);
            box-shadow: 0 10px 30px -8px rgba(8, 29, 56, 0.07);
            text-align: center;
        }}

        .search-title {{
            font-size: 1.3rem;
            font-weight: 700;
            color: var(--navy-deep);
            margin-bottom: 6px;
        }}

        .search-hint {{
            color: var(--text-muted);
            font-size: 0.9rem;
            margin-bottom: 24px;
        }}

        .search-form {{
            display: flex;
            gap: 12px;
            max-width: 620px;
            margin: 0 auto;
            flex-direction: column;
        }}
        @media (min-width: 580px) {{
            .search-form {{
                flex-direction: row;
            }}
        }}

        .input-group {{
            position: relative;
            flex: 1;
        }}

        .search-input {{
            width: 100%;
            height: 54px;
            padding: 0 20px 0 48px;
            font-size: 1.05rem;
            font-weight: 500;
            color: var(--navy-deep);
            background: #f8fafc;
            border: 2px solid #cbd5e1;
            border-radius: 12px;
            outline: none;
            transition: all 0.2s ease;
            font-family: inherit;
        }}
        .search-input:focus {{
            background: #ffffff;
            border-color: var(--gold);
            box-shadow: 0 0 0 4px rgba(198, 146, 34, 0.15);
        }}
        .search-input::placeholder {{
            color: #94a3b8;
            font-size: 0.95rem;
        }}

        .search-icon {{
            position: absolute;
            left: 16px;
            top: 50%;
            transform: translateY(-50%);
            color: #94a3b8;
            font-size: 1.25rem;
        }}

        .btn-check {{
            height: 54px;
            padding: 0 32px;
            background: linear-gradient(135deg, var(--navy-deep), var(--navy-card));
            color: #ffffff;
            font-size: 1rem;
            font-weight: 700;
            border: none;
            border-radius: 12px;
            cursor: pointer;
            transition: all 0.2s ease;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
            box-shadow: 0 4px 14px rgba(8, 29, 56, 0.25);
            white-space: nowrap;
        }}
        .btn-check:hover {{
            background: linear-gradient(135deg, var(--navy-card), var(--navy-light));
            transform: translateY(-1px);
            box-shadow: 0 6px 20px rgba(8, 29, 56, 0.35);
        }}

        /* Error Notification */
        .error-box {{
            display: none;
            max-width: 620px;
            margin: 18px auto 0;
            padding: 14px 18px;
            background: var(--danger-bg);
            border: 1px solid #fecaca;
            color: var(--danger-red);
            border-radius: 10px;
            font-size: 0.92rem;
            font-weight: 600;
            align-items: center;
            gap: 10px;
            text-align: left;
        }}

        /* ========================================================
           WORLD-CLASS RESULT TRANSCRIPT / DMC
        ======================================================== */
        #resultView {{
            display: none;
            animation: slideUp 0.35s cubic-bezier(0.16, 1, 0.3, 1);
        }}
        @keyframes slideUp {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        .transcript-card {{
            background: #ffffff;
            border-radius: 20px;
            border: 2px solid var(--gold-border);
            box-shadow: 0 20px 50px -10px rgba(8, 29, 56, 0.18);
            position: relative;
            overflow: hidden;
        }}

        .transcript-inner {{
            padding: 44px 38px 36px;
            position: relative;
            background: #ffffff;
        }}
        .transcript-inner::before {{
            content: "CCS";
            position: absolute;
            top: 52%;
            left: 50%;
            transform: translate(-50%, -50%) rotate(-25deg);
            font-family: 'Cinzel', serif;
            font-size: 16rem;
            font-weight: 900;
            color: rgba(8, 29, 56, 0.025);
            pointer-events: none;
            user-select: none;
            z-index: 0;
        }}

        /* Certificate Title Header with QR Code Corner */
        .cert-header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            border-bottom: 2px solid var(--navy-deep);
            padding-bottom: 22px;
            margin-bottom: 26px;
            position: relative;
            z-index: 1;
            gap: 16px;
        }}
        .cert-header-main {{
            flex: 1;
            text-align: center;
        }}
        .cert-logo-center {{
            width: 76px;
            height: 76px;
            object-fit: contain;
            margin: 0 auto 10px;
            display: block;
        }}
        .cert-college {{
            font-family: 'Cinzel', Georgia, serif;
            font-size: 1.85rem;
            font-weight: 800;
            color: var(--navy-deep);
            letter-spacing: 1px;
            text-transform: uppercase;
        }}
        .cert-doc-type {{
            font-family: 'Playfair Display', Georgia, serif;
            font-size: 1.35rem;
            color: var(--gold);
            font-style: italic;
            font-weight: 600;
            letter-spacing: 0.5px;
            margin-top: 2px;
        }}
        .cert-session-line {{
            font-size: 0.88rem;
            font-weight: 600;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 1.2px;
            margin-top: 4px;
        }}

        .cert-qr-box {{
            width: 82px;
            text-align: center;
            flex-shrink: 0;
            display: none;
        }}
        @media (min-width: 620px) {{
            .cert-qr-box {{
                display: block;
            }}
        }}
        .qr-img {{
            width: 76px;
            height: 76px;
            border: 1px solid #cbd5e1;
            border-radius: 6px;
            padding: 2px;
            background: #ffffff;
        }}
        .qr-caption {{
            font-size: 0.65rem;
            font-weight: 700;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-top: 3px;
        }}

        /* Student Metadata Grid */
        .student-bio-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 16px;
            background: #f8fafc;
            border: 1px solid var(--border-soft);
            border-radius: 14px;
            padding: 20px 24px;
            margin-bottom: 28px;
            position: relative;
            z-index: 1;
        }}
        .bio-field {{
            display: flex;
            flex-direction: column;
        }}
        .bio-label {{
            font-size: 0.72rem;
            text-transform: uppercase;
            font-weight: 700;
            color: var(--text-muted);
            letter-spacing: 0.8px;
            margin-bottom: 3px;
        }}
        .bio-val {{
            font-size: 1.05rem;
            font-weight: 700;
            color: var(--navy-deep);
        }}
        .bio-val.highlight {{
            color: var(--gold);
        }}

        /* Master Marks Table */
        .table-wrap {{
            overflow-x: auto;
            margin-bottom: 24px;
            position: relative;
            z-index: 1;
            border-radius: 12px;
            border: 1px solid var(--border-soft);
        }}
        .cert-table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 0.94rem;
        }}
        .cert-table thead th {{
            background: var(--navy-deep);
            color: #ffffff;
            font-weight: 700;
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            padding: 14px 16px;
            text-align: left;
        }}
        .cert-table thead th.center {{
            text-align: center;
        }}
        .cert-table tbody td {{
            padding: 13px 16px;
            border-bottom: 1px solid var(--border-soft);
            color: var(--text-dark);
            vertical-align: middle;
        }}
        .cert-table tbody td.center {{
            text-align: center;
        }}
        .cert-table tbody tr:nth-child(even) {{
            background: #fafbfc;
        }}
        .cert-table tbody tr:hover {{
            background: #f1f5f9;
        }}

        .pct-cell {{
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            font-weight: 700;
            color: var(--navy-deep);
        }}
        .mini-bar {{
            width: 50px;
            height: 6px;
            background: #e2e8f0;
            border-radius: 10px;
            overflow: hidden;
            display: inline-block;
        }}
        .mini-bar-fill {{
            height: 100%;
            background: linear-gradient(90deg, var(--gold), var(--success-green));
            border-radius: 10px;
        }}

        .badge {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.78rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        .badge-pass {{
            background: var(--success-bg);
            color: var(--success-green);
            border: 1px solid #bbf7d0;
        }}
        .badge-fail {{
            background: var(--danger-bg);
            color: var(--danger-red);
            border: 1px solid #fecaca;
        }}
        .badge-leave {{
            background: var(--leave-bg);
            color: var(--leave-orange);
            border: 1px solid #fde68a;
        }}

        /* Executive Summary Panel */
        .summary-dashboard {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
            gap: 12px;
            margin-bottom: 24px;
            position: relative;
            z-index: 1;
        }}
        .dash-tile {{
            background: #f8fafc;
            border: 1px solid var(--border-soft);
            border-radius: 14px;
            padding: 16px 14px;
            text-align: center;
        }}
        .dash-tile.grand-status {{
            background: linear-gradient(135deg, var(--navy-deep), var(--navy-card));
            color: #ffffff;
            border-color: var(--navy-deep);
        }}
        .dash-tile.grand-status .tile-lbl {{
            color: rgba(255, 255, 255, 0.75);
        }}
        .dash-tile.grand-status .tile-val {{
            color: #ffffff;
        }}
        .tile-lbl {{
            font-size: 0.72rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            color: var(--text-muted);
            margin-bottom: 5px;
        }}
        .tile-val {{
            font-size: 1.55rem;
            font-weight: 800;
            color: var(--navy-deep);
        }}
        .tile-val.gold {{
            color: var(--gold);
        }}

        /* Teacher Remarks Box */
        .remarks-box {{
            background: var(--gold-subtle);
            border: 1px solid var(--gold-border);
            border-radius: 12px;
            padding: 14px 18px;
            margin-bottom: 30px;
            display: flex;
            align-items: center;
            gap: 12px;
            font-size: 0.92rem;
            position: relative;
            z-index: 1;
        }}
        .remarks-tag {{
            font-weight: 800;
            color: var(--gold);
            text-transform: uppercase;
            font-size: 0.78rem;
            letter-spacing: 0.8px;
            white-space: nowrap;
        }}
        .remarks-text {{
            color: var(--navy-deep);
            font-weight: 600;
            font-style: italic;
        }}

        /* Official Verification & Signatures with Stamp */
        .cert-footer-grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 16px;
            margin-top: 36px;
            padding-top: 32px;
            border-top: 1px dashed #cbd5e1;
            text-align: center;
            position: relative;
            z-index: 1;
            align-items: flex-end;
        }}
        @media (max-width: 600px) {{
            .cert-footer-grid {{
                grid-template-columns: repeat(2, 1fr);
                gap: 24px;
            }}
        }}

        .official-seal {{
            width: 80px;
            height: 80px;
            margin: 0 auto 6px;
            border: 2px dashed #b91c1c;
            border-radius: 50%;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            color: #b91c1c;
            transform: rotate(-10deg);
            padding: 4px;
            user-select: none;
        }}
        .seal-txt-top {{ font-size: 0.55rem; font-weight: 800; letter-spacing: 0.5px; text-transform: uppercase; }}
        .seal-txt-mid {{ font-size: 0.75rem; font-weight: 900; letter-spacing: 1px; text-transform: uppercase; }}
        .seal-txt-bot {{ font-size: 0.52rem; font-weight: 700; text-transform: uppercase; }}

        .sig-rule {{
            width: 75%;
            margin: 0 auto 6px;
            border-top: 1px solid #94a3b8;
        }}
        .sig-name {{
            font-size: 0.82rem;
            font-weight: 700;
            color: var(--text-muted);
            text-transform: uppercase;
        }}

        /* Security Bar */
        .security-audit-bar {{
            margin-top: 26px;
            padding-top: 14px;
            border-top: 1px solid #f1f5f9;
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 0.75rem;
            color: #94a3b8;
            flex-wrap: wrap;
            gap: 8px;
        }}

        /* Action Tray */
        .action-tray {{
            background: #f8fafc;
            border-top: 1px solid var(--border-soft);
            padding: 16px 28px;
            display: flex;
            justify-content: flex-end;
            gap: 12px;
            flex-wrap: wrap;
        }}
        .btn-ui {{
            padding: 11px 20px;
            border-radius: 10px;
            font-size: 0.92rem;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.2s;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            border: none;
            font-family: inherit;
        }}
        .btn-print-doc {{
            background: linear-gradient(135deg, var(--gold), #a77717);
            color: #ffffff;
            box-shadow: 0 4px 12px rgba(198, 146, 34, 0.25);
        }}
        .btn-print-doc:hover {{
            background: linear-gradient(135deg, var(--gold-light), var(--gold));
            transform: translateY(-1px);
        }}
        .btn-whatsapp {{
            background: #25d366;
            color: #ffffff;
            box-shadow: 0 4px 12px rgba(37, 211, 102, 0.25);
        }}
        .btn-whatsapp:hover {{
            background: #1eb857;
            transform: translateY(-1px);
        }}
        .btn-new-search {{
            background: #ffffff;
            color: var(--navy-deep);
            border: 1px solid #cbd5e1;
        }}
        .btn-new-search:hover {{
            background: #e2e8f0;
        }}

        /* Bottom Footer */
        .footer-note {{
            text-align: center;
            font-size: 0.82rem;
            color: var(--text-muted);
            margin-top: auto;
        }}

        /* Clean Print Style */
        @media print {{
            body {{
                background: #ffffff !important;
                padding: 0 !important;
            }}
            .executive-header, .search-container, .action-tray, .footer-note {{
                display: none !important;
            }}
            .wrapper {{
                max-width: 100% !important;
                padding: 0 !important;
                margin: 0 !important;
            }}
            #resultView {{
                display: block !important;
            }}
            .transcript-card {{
                box-shadow: none !important;
                border: 2px solid #000000 !important;
                border-radius: 0 !important;
            }}
            .transcript-inner {{
                padding: 24px !important;
            }}
            .cert-table thead th {{
                background: #e2e8f0 !important;
                color: #000000 !important;
                border: 1px solid #000000 !important;
            }}
            .cert-table tbody td {{
                border: 1px solid #cccccc !important;
            }}
            .dash-tile.grand-status {{
                background: #f1f5f9 !important;
                color: #000 !important;
                border: 1px solid #000 !important;
            }}
            .dash-tile.grand-status .tile-lbl, .dash-tile.grand-status .tile-val {{
                color: #000 !important;
            }}
            .cert-footer-grid {{
                margin-top: 50px !important;
            }}
        }}
    </style>
</head>
<body>

    <div class="wrapper">
        <!-- 1. Executive College Header (Clean & Official) -->
        <header class="executive-header">
            <img src="{logo_b64}" alt="Chenab College Logo" class="college-logo">
            <h1 class="college-title">Chenab College Shorkot</h1>
            <div class="controller-tag">Office of the Controller of Examinations</div>
            <div>
                <div class="exam-info-badges">
                    <span><strong>Assessment:</strong> Monthly Test Oct, 2026</span>
                    <span>&bull;</span>
                    <span><strong>Session:</strong> 2026-2027</span>
                    <span>&bull;</span>
                    <span><strong>Class:</strong> 7 - (G) Jades</span>
                    <span>&bull;</span>
                    <span><strong>Date:</strong> 10/16/2026</span>
                </div>
            </div>
        </header>

        <!-- 2. Clean Search Box ONLY (No other data shown before search) -->
        <section class="search-container" id="searchSection">
            <h2 class="search-title">Online Student Result Portal</h2>
            <p class="search-hint">Enter your Student ID / B-Form Number or Student Name to view your Detailed Marksheet.</p>

            <form class="search-form" id="searchForm" onsubmit="executeSearch(event)">
                <div class="input-group">
                    <span class="search-icon">🔍</span>
                    <input 
                        type="text" 
                        id="studentInput" 
                        class="search-input" 
                        placeholder="Enter Student ID (e.g. 3320354393768) or Name"
                        autocomplete="off"
                        required
                        autofocus
                    >
                </div>
                <button type="submit" class="btn-check">
                    <span>View Result</span> &rarr;
                </button>
            </form>

            <div id="errorAlert" class="error-box">
                <span>⚠️</span>
                <span id="errorMsg">Record not found. Please verify the ID or Name.</span>
            </div>
        </section>

        <!-- 3. World-Class Result Transcript (Revealed on Search) -->
        <section id="resultView">
            <div class="transcript-card">
                <div class="transcript-inner">
                    <!-- Certificate Header -->
                    <div class="cert-header">
                        <div style="width: 82px;" class="cert-qr-box"></div>
                        <div class="cert-header-main">
                            <img src="{logo_b64}" alt="Chenab College" class="cert-logo-center">
                            <div class="cert-college">Chenab College Shorkot</div>
                            <div class="cert-doc-type">Detailed Marks Certificate (DMC)</div>
                            <div class="cert-session-line">Monthly Examination &bull; Academic Session 2026-2027</div>
                        </div>
                        <div class="cert-qr-box">
                            <img id="dynamicQr" src="" alt="Verification QR" class="qr-img">
                            <div class="qr-caption">Scan to Verify</div>
                        </div>
                    </div>

                    <!-- Student Information Grid -->
                    <div class="student-bio-grid">
                        <div class="bio-field">
                            <span class="bio-label">Student Name</span>
                            <span class="bio-val" id="dispName">-</span>
                        </div>
                        <div class="bio-field">
                            <span class="bio-label">Registration / B-Form ID</span>
                            <span class="bio-val" id="dispId" style="font-family: monospace; letter-spacing: 0.5px;">-</span>
                        </div>
                        <div class="bio-field">
                            <span class="bio-label">Class & Section</span>
                            <span class="bio-val">Class : 7 - (G) Jades</span>
                        </div>
                        <div class="bio-field">
                            <span class="bio-label">Exam Date</span>
                            <span class="bio-val">10/16/2026</span>
                        </div>
                        <div class="bio-field">
                            <span class="bio-label">Class Position</span>
                            <span class="bio-val highlight" id="dispClassPos">-</span>
                        </div>
                        <div class="bio-field">
                            <span class="bio-label">Section Position</span>
                            <span class="bio-val" id="dispSecPos" style="color: var(--success-green);">-</span>
                        </div>
                    </div>

                    <!-- Detailed Subject-Wise Marks & Percentages -->
                    <div class="table-wrap">
                        <table class="cert-table">
                            <thead>
                                <tr>
                                    <th style="width: 45px;" class="center">Sr.</th>
                                    <th>Subject Description</th>
                                    <th class="center" style="width: 95px;">Max Marks</th>
                                    <th class="center" style="width: 95px;">Pass Marks</th>
                                    <th class="center" style="width: 120px;">Marks Obtained</th>
                                    <th class="center" style="width: 130px;">Percentage</th>
                                    <th class="center" style="width: 80px;">Grade</th>
                                    <th class="center" style="width: 100px;">Status</th>
                                </tr>
                            </thead>
                            <tbody id="subjectTableBody">
                                <!-- Populated dynamically -->
                            </tbody>
                        </table>
                    </div>

                    <!-- Executive Summary Tiles -->
                    <div class="summary-dashboard">
                        <div class="dash-tile">
                            <div class="tile-lbl">Total Marks</div>
                            <div class="tile-val" id="dispTotalMarks">200</div>
                        </div>
                        <div class="dash-tile">
                            <div class="tile-lbl">Marks Obtained</div>
                            <div class="tile-val" id="dispObtainedMarks">-</div>
                        </div>
                        <div class="dash-tile">
                            <div class="tile-lbl">Aggregate %</div>
                            <div class="tile-val" id="dispPercentage">-%</div>
                        </div>
                        <div class="dash-tile">
                            <div class="tile-lbl">Overall Grade</div>
                            <div class="tile-val gold" id="dispGrade">-</div>
                        </div>
                        <div class="dash-tile grand-status" id="dispStatusTile">
                            <div class="tile-lbl">Result Status</div>
                            <div class="tile-val" id="dispStatus">PASS</div>
                        </div>
                    </div>

                    <!-- Teacher Remarks -->
                    <div class="remarks-box">
                        <span class="remarks-tag">Academic Remarks:</span>
                        <span class="remarks-text" id="dispRemarks">Outstanding performance! Keep it up.</span>
                    </div>

                    <!-- Signatures Block with Red Official Seal -->
                    <div class="cert-footer-grid">
                        <div class="sig-col">
                            <div class="sig-rule"></div>
                            <div class="sig-name">Class Incharge</div>
                        </div>
                        <div class="sig-col">
                            <div class="sig-rule"></div>
                            <div class="sig-name">Coordinator</div>
                        </div>
                        <div class="sig-col">
                            <div class="official-seal">
                                <span class="seal-txt-top">Chenab College</span>
                                <span class="seal-txt-mid">VERIFIED</span>
                                <span class="seal-txt-bot">Exam Branch</span>
                            </div>
                            <div class="sig-rule"></div>
                            <div class="sig-name">Controller Exam</div>
                        </div>
                        <div class="sig-col">
                            <div class="sig-rule"></div>
                            <div class="sig-name">Principal</div>
                        </div>
                    </div>

                    <!-- Security Audit Line -->
                    <div class="security-audit-bar">
                        <span>🔒 Computer Generated Official DMC &bull; Chenab College Shorkot</span>
                        <span id="auditTimestamp">System Date: October 2026</span>
                    </div>
                </div>

                <!-- Action Tray -->
                <div class="action-tray">
                    <button type="button" class="btn-ui btn-new-search" onclick="backToSearch()">
                        🔍 Search Another Student
                    </button>
                    <button type="button" class="btn-ui btn-whatsapp" onclick="shareOnWhatsApp()">
                        💬 Share on WhatsApp
                    </button>
                    <button type="button" class="btn-ui btn-print-doc" onclick="window.print()">
                        🖨️ Print / Save as PDF (DMC)
                    </button>
                </div>
            </div>
        </section>

        <!-- Footer -->
        <footer class="footer-note">
            &copy; 2026-2027 Chenab College Shorkot. All Rights Reserved. &bull; Official Examination Portal
        </footer>
    </div>

    <!-- Student Data and Logic -->
    <script>
        const DB = {json_str};
        let currentStudent = null;

        function executeSearch(e) {{
            e.preventDefault();
            const raw = document.getElementById('studentInput').value.trim().toLowerCase();
            const errorAlert = document.getElementById('errorAlert');
            const errorMsg = document.getElementById('errorMsg');

            if (!raw) return;

            const record = DB.students.find(st => {{
                return st.id.toLowerCase() === raw || 
                       st.name.toLowerCase().includes(raw) ||
                       st.id.endsWith(raw);
            }});

            if (record) {{
                errorAlert.style.display = 'none';
                renderResult(record);
            }} else {{
                errorMsg.textContent = `No record found for "${{raw}}". Please enter a valid Student ID or Name.`;
                errorAlert.style.display = 'flex';
                document.getElementById('resultView').style.display = 'none';
            }}
        }}

        function renderResult(st) {{
            currentStudent = st;
            document.getElementById('dispName').textContent = st.name;
            document.getElementById('dispId').textContent = st.id;
            document.getElementById('dispClassPos').textContent = st.class_pos;
            document.getElementById('dispSecPos').textContent = st.sec_pos;
            document.getElementById('dispTotalMarks').textContent = st.total_marks;
            document.getElementById('dispObtainedMarks').textContent = st.obtained_marks;
            document.getElementById('dispPercentage').textContent = st.percentage + '%';
            document.getElementById('dispGrade').textContent = st.grade || '-';
            document.getElementById('dispRemarks').textContent = st.remarks || 'Keep up the good work.';
            
            // Dynamic Verification QR code
            const qrUrl = 'https://api.qrserver.com/v1/create-qr-code/?size=100x100&data=' + encodeURIComponent('CHENAB COLLEGE VERIFIED: ' + st.name + ' (' + st.id + ') Marks: ' + st.obtained_marks + '/200 (' + st.percentage + '%)');
            document.getElementById('dynamicQr').src = qrUrl;

            const statusVal = document.getElementById('dispStatus');
            const statusTile = document.getElementById('dispStatusTile');
            statusVal.textContent = st.status.toUpperCase();
            
            if (st.status.toLowerCase() === 'pass') {{
                statusTile.style.background = 'linear-gradient(135deg, #0d824d, #085a34)';
            }} else {{
                statusTile.style.background = 'linear-gradient(135deg, #c02626, #8e1818)';
            }}

            // Render Subjects with Individual Percentages & Mini-Bars
            const tbody = document.getElementById('subjectTableBody');
            tbody.innerHTML = '';

            st.subjects.forEach((sub, idx) => {{
                const tr = document.createElement('tr');

                let badgeClass = 'badge-pass';
                let statusText = 'Pass';
                let pctNum = 0;

                if (sub.status === 'Leave') {{
                    badgeClass = 'badge-leave';
                    statusText = 'Leave';
                }} else if (sub.status === 'Fail') {{
                    badgeClass = 'badge-fail';
                    statusText = 'Fail';
                }}

                if (sub.percentage && sub.percentage.includes('%')) {{
                    pctNum = parseFloat(sub.percentage) || 0;
                }}

                const miniBarHtml = sub.status === 'Leave' 
                    ? '<span style="color: #94a3b8;">-</span>'
                    : `
                        <div class="pct-cell">
                            <span>${{sub.percentage}}</span>
                            <div class="mini-bar">
                                <div class="mini-bar-fill" style="width: ${{pctNum}}%;"></div>
                            </div>
                        </div>
                    `;

                tr.innerHTML = `
                    <td class="center" style="color: var(--text-muted); font-size: 0.85rem;">${{idx + 1}}</td>
                    <td style="font-weight: 700; color: var(--navy-deep);">${{sub.name}} <span style="font-size: 0.8rem; color: #94a3b8; font-weight: 500;">(${{sub.code}})</span></td>
                    <td class="center" style="font-weight: 600;">${{sub.max}}</td>
                    <td class="center" style="color: var(--text-muted);">${{sub.pass}}</td>
                    <td class="center" style="font-weight: 800; font-size: 1.05rem; color: var(--navy-deep);">${{sub.obtained}}</td>
                    <td class="center">${{miniBarHtml}}</td>
                    <td class="center" style="font-weight: 800; color: var(--gold);">${{sub.grade}}</td>
                    <td class="center"><span class="badge ${{badgeClass}}">${{statusText}}</span></td>
                `;
                tbody.appendChild(tr);
            }});

            const resultView = document.getElementById('resultView');
            resultView.style.display = 'block';
            resultView.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
        }}

        function backToSearch() {{
            document.getElementById('studentInput').value = '';
            document.getElementById('studentInput').focus();
            document.getElementById('resultView').style.display = 'none';
            document.getElementById('errorAlert').style.display = 'none';
            window.scrollTo({{ top: 0, behavior: 'smooth' }});
        }}

        function shareOnWhatsApp() {{
            if (!currentStudent) return;
            const text = `🎓 *Chenab College Shorkot - Result Card*%0A` +
                         `*Exam:* Monthly Test Oct, 2026%0A` +
                         `*Student:* ${{currentStudent.name}}%0A` +
                         `*Roll No/ID:* ${{currentStudent.id}}%0A` +
                         `*Marks:* ${{currentStudent.obtained_marks}} / ${{currentStudent.total_marks}} (${{currentStudent.percentage}}%)%0A` +
                         `*Grade:* ${{currentStudent.grade}}%0A` +
                         `*Class Position:* ${{currentStudent.class_pos}}%0A` +
                         `*Status:* ${{currentStudent.status}}`;
            window.open('https://api.whatsapp.com/send?text=' + text, '_blank');
        }}
    </script>
</body>
</html>
"""

portal_index_path = os.path.join(portal_folder, "index.html")
with open(portal_index_path, "w", encoding="utf-8") as f:
    f.write(html_code)

direct_desktop_file = os.path.join(desktop, "ResultPortal_ChenabCollege.html")
with open(direct_desktop_file, "w", encoding="utf-8") as f:
    f.write(html_code)

print("Updated with QR Code, Stamp, Remarks, and WhatsApp Share!")
