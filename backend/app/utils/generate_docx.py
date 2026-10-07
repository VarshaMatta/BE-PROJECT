import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls

def set_cell_background(cell, fill_color):
    """Sets background color for a table cell (RGB hex string without #)."""
    tcPr = cell._element.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_color}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Sets cell padding in dxa (1 pt = 20 dxa)."""
    tcPr = cell._element.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def add_heading_1(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(18)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = 'Arial'
    run.font.size = Pt(18)
    run.font.bold = True
    run.font.color.rgb = RGBColor(109, 40, 217) # Deep Violet
    return p

def add_heading_2(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = 'Arial'
    run.font.size = Pt(14)
    run.font.bold = True
    run.font.color.rgb = RGBColor(15, 20, 36) # Dark Navy
    return p

def add_heading_3(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = 'Arial'
    run.font.size = Pt(12)
    run.font.bold = True
    run.font.color.rgb = RGBColor(124, 58, 237) # Purple
    return p

def add_body_paragraph(doc, text="", bold_prefix=""):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = 'Calibri'
        r_pre.font.size = Pt(11)
        r_pre.font.bold = True
        r_pre.font.color.rgb = RGBColor(15, 20, 36)
    if text:
        r_text = p.add_run(text)
        r_text.font.name = 'Calibri'
        r_text.font.size = Pt(11)
        r_text.font.color.rgb = RGBColor(51, 65, 85)
    return p

def add_bullet_point(doc, bold_title="", text=""):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.15
    if bold_title:
        r_title = p.add_run(bold_title + " ")
        r_title.font.name = 'Calibri'
        r_title.font.size = Pt(11)
        r_title.font.bold = True
        r_title.font.color.rgb = RGBColor(15, 20, 36)
    if text:
        r_text = p.add_run(text)
        r_text.font.name = 'Calibri'
        r_text.font.size = Pt(11)
        r_text.font.color.rgb = RGBColor(51, 65, 85)
    return p

def add_callout(doc, text, title="IMPORTANT NOTICE"):
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = table.cell(0, 0)
    cell.width = Inches(6.5)
    set_cell_background(cell, "F3E8FF") # Light Purple
    set_cell_margins(cell, top=140, bottom=140, left=200, right=200)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_after = Pt(2)
    r_title = p.add_run(f"📌 {title}\n")
    r_title.font.name = 'Arial'
    r_title.font.size = Pt(11)
    r_title.font.bold = True
    r_title.font.color.rgb = RGBColor(109, 40, 217)
    
    r_text = p.add_run(text)
    r_text.font.name = 'Calibri'
    r_text.font.size = Pt(10.5)
    r_text.font.color.rgb = RGBColor(51, 65, 85)
    
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def add_code_block(doc, code_text):
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = table.cell(0, 0)
    cell.width = Inches(6.5)
    set_cell_background(cell, "0F1424") # Dark Navy
    set_cell_margins(cell, top=140, bottom=140, left=200, right=200)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.05
    run = p.add_run(code_text)
    run.font.name = 'Consolas'
    run.font.size = Pt(9.5)
    run.font.color.rgb = RGBColor(226, 232, 240)
    
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def create_styled_table(doc, headers, data):
    table = doc.add_table(rows=len(data) + 1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    
    # Format Header Row
    hdr_cells = table.rows[0].cells
    for i, title in enumerate(headers):
        hdr_cells[i].text = title
        set_cell_background(hdr_cells[i], "6D28D9") # Deep Violet
        set_cell_margins(hdr_cells[i], top=120, bottom=120, left=140, right=140)
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        for run in p.runs:
            run.font.name = 'Arial'
            run.font.size = Pt(10)
            run.font.bold = True
            run.font.color.rgb = RGBColor(255, 255, 255)
            
    # Format Data Rows
    for r_idx, row_data in enumerate(data):
        row_cells = table.rows[r_idx + 1].cells
        bg_color = "F8FAFC" if r_idx % 2 == 0 else "FFFFFF"
        for c_idx, val in enumerate(row_data):
            row_cells[c_idx].text = str(val)
            set_cell_background(row_cells[c_idx], bg_color)
            set_cell_margins(row_cells[c_idx], top=100, bottom=100, left=140, right=140)
            p = row_cells[c_idx].paragraphs[0]
            for run in p.runs:
                run.font.name = 'Calibri'
                run.font.size = Pt(10)
                run.font.color.rgb = RGBColor(30, 41, 59)
                
    doc.add_paragraph().paragraph_format.space_after = Pt(6)

def generate_documentation():
    os.makedirs("docs", exist_ok=True)
    doc = Document()

    # Page Margins
    sections = doc.sections
    for s in sections:
        s.top_margin = Inches(1)
        s.bottom_margin = Inches(1)
        s.left_margin = Inches(1)
        s.right_margin = Inches(1)

    # Document Header & Title Page
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(36)
    p_title.paragraph_format.space_after = Pt(8)
    run_t = p_title.add_run("PriceWise")
    run_t.font.name = 'Arial'
    run_t.font.size = Pt(32)
    run_t.font.bold = True
    run_t.font.color.rgb = RGBColor(109, 40, 217)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_after = Pt(24)
    run_sub = p_sub.add_run("An AI-Based Constraint-Aware Pricing and Promotion\nDecision Support System for Retailers")
    run_sub.font.name = 'Arial'
    run_sub.font.size = Pt(16)
    run_sub.font.bold = True
    run_sub.font.color.rgb = RGBColor(15, 20, 36)

    p_meta = doc.add_paragraph()
    p_meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_meta.paragraph_format.space_after = Pt(36)
    r_meta = p_meta.add_run("Final-Year Engineering Project Detailed System Documentation\nPrepared for Academic Review & Viva Defense")
    r_meta.font.name = 'Calibri'
    r_meta.font.size = Pt(12)
    r_meta.font.italic = True
    r_meta.font.color.rgb = RGBColor(100, 116, 139)

    doc.add_page_break()

    # ----------------------------------------------------
    # SECTION 1 — PROJECT OVERVIEW
    # ----------------------------------------------------
    add_heading_1(doc, "Section 1 — Project Overview")
    
    add_heading_2(doc, "1.1 What is PriceWise?")
    add_body_paragraph(doc, "PriceWise is an AI-based, constraint-aware decision-support web application tailored specifically for small and medium-sized retailers. It enables business owners to upload historical transaction datasets, inspect data cleanliness and data sufficiency, define business rules (cost price, maximum retail price, discount caps, minimum profit margins, and stock availability), and evaluate multiple feasible pricing/promotion scenarios ranked by estimated gross profit.")
    
    add_heading_2(doc, "1.2 Problem Statement & Motivation")
    add_body_paragraph(doc, "Small retailers currently rely heavily on gut instinct, manual spreadsheets, or simple percentage markups when setting product prices. Manual pricing decisions present significant operational challenges:")
    add_bullet_point(doc, "Lack of Elasticity Insights:", "Retailers fail to quantify how demand changes when prices increase or decrease.")
    add_bullet_point(doc, "Frequent Margin Breaches:", "Unplanned promotional discounts often erode profit margins below break-even thresholds.")
    add_bullet_point(doc, "Constraint Violations:", "Retailers inadvertently price products below unit cost or above the legally prescribed Maximum Retail Price (MRP).")
    add_bullet_point(doc, "Data Overload:", "Analyzing thousands of past transaction rows manually is time-consuming and error-prone.")

    add_heading_2(doc, "1.3 Decision Support vs. Automatic Price Changing")
    add_callout(doc, "PriceWise is strictly a DECISION SUPPORT SYSTEM. It DOES NOT automatically change prices on store cash registers or e-commerce sites. PriceWise analyzes data and recommends ranked, feasible pricing scenarios while preserving full authority for the retailer to accept, adjust, or reject recommended prices.", title="CORE SYSTEM PRINCIPLE")

    add_heading_2(doc, "1.4 Practical Numerical Example")
    add_body_paragraph(doc, "Consider a retailer selling Amul Milk 1L under the following parameters:")
    add_bullet_point(doc, "Unit Cost Price (C):", "₹52.00")
    add_bullet_point(doc, "Maximum Retail Price (MRP):", "₹68.00")
    add_bullet_point(doc, "Maximum Allowed Discount (D_max):", "15.0%")
    add_bullet_point(doc, "Minimum Required Profit Margin (M_min):", "10.0%")
    add_body_paragraph(doc, "PriceWise calculates lower bounds from cost (₹52.00), discount limit (₹57.80), and minimum margin requirement (₹57.78), establishing the valid feasible price range between ₹57.80 and ₹68.00. The system then predicts demand across candidate price points to recommend the price point yielding maximum gross profit (₹68.00 producing ₹467.52 expected profit).")

    # ----------------------------------------------------
    # SECTION 2 — PROJECT OBJECTIVES
    # ----------------------------------------------------
    add_heading_1(doc, "Section 2 — Project Objectives")
    add_body_paragraph(doc, "The major engineering objectives of PriceWise are detailed below, categorized by implementation status:")
    
    headers_obj = ["Objective", "Purpose & Necessity", "Implementation Status & Details"]
    data_obj = [
        ["User & Shop Management", "Isolate retailer data securely across multiple physical store outlets.", "IMPLEMENTED: JWT bearer authentication, bcrypt password hashing, ShopContext persistence."],
        ["Flexible CSV Ingestion", "Allow arbitrary retailer CSV uploads without rigid column names.", "IMPLEMENTED: Interactive column mapping UI and Pandas backend ingestion service."],
        ["CSV Validation & Cleaning", "Ensure transaction cleanliness, deduplication, and error reporting.", "IMPLEMENTED: Pandas checks for date formats, missing prices, invalid quantities, deduplication."],
        ["Data Sufficiency Audit", "Classify products by historical data quality before modeling.", "IMPLEMENTED: Rule-based classifier (ML READY, LIMITED DATA, COLD START)."],
        ["Constraint Engine", "Enforce business limits (cost, MRP, discount, margin, stock).", "IMPLEMENTED: Pure Python service (ConstraintEngine) with unit tests passing."],
        ["Demand Prediction", "Estimate sales quantity Q(P) based on historical price elasticity.", "IMPLEMENTED: Scikit-learn (Ridge/RandomForest) with XGBoost integration & elasticity fallback."],
        ["Scenario Ranking", "Generate, filter, and rank price/promotion options by profit.", "IMPLEMENTED: ScenarioOptimizer evaluating candidate price steps and ranking by gross profit."]
    ]
    create_styled_table(doc, headers_obj, data_obj)

    # ----------------------------------------------------
    # SECTION 3 — COMPLETE PROJECT FLOW
    # ----------------------------------------------------
    add_heading_1(doc, "Section 3 — Complete Project Flow")
    add_body_paragraph(doc, "The operational workflow executed by PriceWise follows a structured linear sequence from user onboarding to scenario optimization:")

    flow_diagram = (
        "User Registration / Login\n"
        "       ↓\n"
        "Shop Selection / Creation (Shops Page)\n"
        "       ↓\n"
        "Dashboard KPI & Sales Overview (Dashboard Page)\n"
        "       ↓\n"
        "Upload Historical Sales CSV (DataUpload Page)\n"
        "       ↓\n"
        "Interactive Column Mapping (ColumnMapping Page)\n"
        "       ↓\n"
        "Pandas CSV Validation & Data Cleaning (ValidationResult Page)\n"
        "       ↓\n"
        "Product Catalog & Data Sufficiency Classification (ProductsList Page)\n"
        "       ↓\n"
        "Product Historical Recharts Analysis (ProductAnalysis Page)\n"
        "       ↓\n"
        "Define Business Constraints (SetConstraints Page)\n"
        "       ↓\n"
        "Constraint Engine Bounds Evaluation (Backend ConstraintEngine)\n"
        "       ↓\n"
        "Demand Model Prediction & Scenario Ranking (Recommendations Page)"
    )
    add_code_block(doc, flow_diagram)

    # ----------------------------------------------------
    # SECTION 4 — SYSTEM ARCHITECTURE
    # ----------------------------------------------------
    add_heading_1(doc, "Section 4 — System Architecture")
    add_body_paragraph(doc, "PriceWise utilizes a decoupled client-server architecture. The frontend is a Single Page Application (SPA) built with React and Vite, communicating via REST API requests over HTTP/JSON with a FastAPI backend backed by a relational SQLite database.")

    arch_diagram = (
        "+-------------------------------------------------------------------+\n"
        "|                 REACT FRONTEND (Vite / Port 3000)                |\n"
        "|  AuthContext | ShopContext | React Router | Recharts | Axios Client|\n"
        "+-------------------------------------------------------------------+\n"
        "                                  │  REST API (JSON over HTTP)\n"
        "                                  ▼\n"
        "+-------------------------------------------------------------------+\n"
        "|                 FASTAPI BACKEND (Uvicorn / Port 8000)             |\n"
        "|  Routers (Auth, Shops, Uploads, Products, Constraints, Analytics) |\n"
        "|  Auth Middleware (JWT Bearer / Bcrypt Passwords)                 |\n"
        "|  Pandas Data Service | Constraint Engine | Scikit-Learn / XGBoost |\n"
        "+-------------------------------------------------------------------+\n"
        "                                  │  SQLAlchemy 2.0 ORM\n"
        "                                  ▼\n"
        "+-------------------------------------------------------------------+\n"
        "|                  SQLITE DATABASE (pricewise.db)                   |\n"
        "|  users | shops | csv_uploads | products | sales_records | ...    |\n"
        "+-------------------------------------------------------------------+"
    )
    add_code_block(doc, arch_diagram)

    # ----------------------------------------------------
    # SECTION 5 — TECHNOLOGY STACK
    # ----------------------------------------------------
    add_heading_1(doc, "Section 5 — Technology Stack")
    add_body_paragraph(doc, "The technology stack was selected to maximize maintainability, performance, security, and developer clarity:")

    headers_tech = ["Technology", "Category", "Purpose in PriceWise", "Selection Rationale"]
    data_tech = [
        ["React 18", "Frontend SPA Framework", "Renders component UI state, forms, and interactive views.", "Component-based architecture, virtual DOM performance."],
        ["Vite 6", "Frontend Build Tool", "Bundles React code and proxies API calls during dev.", "Ultra-fast HMR (Hot Module Replacement) and optimized build."],
        ["Tailwind CSS 3", "UI Styling", "Utility-class styling for dark navy modern SaaS design.", "Rapid styling, responsive design tokens, zero custom CSS bloat."],
        ["Recharts 2", "Data Visualization", "Renders Sales History area charts and Price History step charts.", "Native SVG rendering, highly responsive, smooth animations."],
        ["Python 3.13", "Backend Language", "Executes API routers, data processing, and ML algorithms.", "Rich ecosystem for pandas, scikit-learn, and FastAPI."],
        ["FastAPI 0.110", "Backend Web Framework", "Exposes asynchronous REST API endpoints with auto OpenAPI docs.", "High speed, automatic Pydantic request/response validation."],
        ["SQLite 3", "Relational Database", "Stores persistent users, shops, products, sales, and constraints.", "Zero configuration, file-based, lightweight for dev/viva."],
        ["SQLAlchemy 2.0", "Database ORM", "Maps Python classes to SQL tables with relationships.", "Decouples SQL dialect, facilitating easy migration to PostgreSQL."],
        ["Pandas 2.2", "Data Processing", "Ingests, validates, cleans, deduplicates, and parses CSVs.", "High-performance vector operations on tabular sales data."],
        ["Scikit-Learn 1.4", "Machine Learning", "Fits Ridge / RandomForest regression for demand prediction.", "Robust baseline algorithms for tabular elasticity estimation."],
        ["XGBoost 2.0", "Machine Learning", "Gradient boosted decision trees for non-linear demand fitting.", "State-of-the-art accuracy for retail transaction tabular data."],
        ["PyJWT / Jose", "Authentication", "Signs and verifies JWT access tokens for protected routes.", "Stateless, secure token authentication between React & FastAPI."],
        ["Passlib / Bcrypt", "Security", "Hashes and verifies user account passwords securely.", "Industry standard salted password hashing preventing plain-text storage."]
    ]
    create_styled_table(doc, headers_tech, data_tech)

    # ----------------------------------------------------
    # SECTION 6 — FRONTEND EXPLANATION
    # ----------------------------------------------------
    add_heading_1(doc, "Section 6 — Frontend Explanation")
    add_body_paragraph(doc, "The frontend source directory is organized cleanly into modular folders:")

    frontend_tree = (
        "frontend/src/\n"
        "├── assets/\n"
        "├── components/\n"
        "│   ├── common/          # Badge.jsx (Status pills)\n"
        "│   └── layout/          # Sidebar.jsx, Header.jsx, DashboardLayout.jsx\n"
        "├── context/\n"
        "│   ├── AuthContext.jsx  # User JWT token & login state\n"
        "│   └── ShopContext.jsx  # Active shop selection & list persistence\n"
        "├── pages/\n"
        "│   ├── Login.jsx, Register.jsx, Shops.jsx, Dashboard.jsx\n"
        "│   ├── DataUpload.jsx, ColumnMapping.jsx, ValidationResult.jsx\n"
        "│   ├── ProductsList.jsx, ProductAnalysis.jsx, SetConstraints.jsx\n"
        "│   └── Recommendations.jsx\n"
        "├── services/\n"
        "│   └── api.js           # Axios instance configured to http://127.0.0.1:8000/api\n"
        "├── App.jsx              # React Router protected/public routes\n"
        "├── index.css            # Tailwind directives & dark theme scrollbars\n"
        "└── main.jsx             # React entrypoint"
    )
    add_code_block(doc, frontend_tree)

    # ----------------------------------------------------
    # SECTION 7 — BACKEND EXPLANATION
    # ----------------------------------------------------
    add_heading_1(doc, "Section 7 — Backend Explanation")
    add_body_paragraph(doc, "The FastAPI backend follows a clean layered architecture separating routes, validation schemas, SQLAlchemy ORM models, and business logic:")

    backend_tree = (
        "backend/app/\n"
        "├── auth/                # jwt.py, password.py, dependencies.py (get_current_user)\n"
        "├── constraint_engine/   # evaluator.py (Pure Python lower/upper bound math)\n"
        "├── ml/                  # demand_model.py, scenario_generator.py, optimizer.py\n"
        "├── models/              # user.py, shop.py, upload.py, product.py, sales.py, constraint.py\n"
        "├── routers/             # auth.py, shops.py, uploads.py, products.py, constraints.py, analytics.py\n"
        "├── schemas/             # Pydantic request & response validation schemas\n"
        "├── services/            # csv_service.py (Pandas cleaning), product_analysis_service.py\n"
        "├── utils/               # sample_data_generator.py (Seeder script)\n"
        "├── config.py            # App settings & secret keys\n"
        "├── database.py          # SQLAlchemy engine & sessionmaker\n"
        "└── main.py              # FastAPI app initialization, CORS, DB metadata"
    )
    add_code_block(doc, backend_tree)

    # ----------------------------------------------------
    # SECTION 8 — API EXPLANATION
    # ----------------------------------------------------
    add_heading_1(doc, "Section 8 — API Endpoint Documentation")
    add_body_paragraph(doc, "Below is the complete API router manifest implemented in the FastAPI backend:")

    headers_api = ["Method", "Endpoint", "Purpose", "Auth?", "Input / Payload", "Response Output"]
    data_api = [
        ["POST", "/api/auth/register", "Register a new retailer user", "No", "JSON: name, email, password", "JWT Token & bearer type"],
        ["POST", "/api/auth/login", "Authenticate existing user", "No", "JSON: email, password", "JWT Token"],
        ["GET", "/api/auth/me", "Fetch current user profile", "Yes", "Bearer Token", "User ID, name, email"],
        ["GET", "/api/shops", "List user's owned shops", "Yes", "Bearer Token", "List of Shop objects with stats"],
        ["POST", "/api/shops", "Create a new shop outlet", "Yes", "JSON: shop_name, business_type", "Created Shop object"],
        ["POST", "/api/shops/{id}/uploads/preview", "Upload CSV & extract headers", "Yes", "Multipart File (.csv)", "Columns & preview 5 rows"],
        ["POST", "/api/shops/{id}/uploads/validate", "Validate column mapping & stats", "Yes", "Multipart File + mapping_str JSON", "Validation summary JSON"],
        ["POST", "/api/shops/{id}/uploads/process", "Clean & commit sales data to DB", "Yes", "Multipart File + mapping_str JSON", "Upload ID & success summary"],
        ["GET", "/api/shops/{id}/analytics/overview", "Fetch KPI metrics & sales chart", "Yes", "Bearer Token", "KPI stats, chart data, attention list"],
        ["GET", "/api/shops/{id}/products", "List products with search & status filter", "Yes", "Query params: search, status_filter", "List of Product items"],
        ["GET", "/api/shops/{id}/products/{pid}", "Get product analysis details", "Yes", "Product ID", "Product stats, price points, history"],
        ["GET", "/api/shops/{id}/products/{pid}/charts", "Fetch Recharts chart history", "Yes", "Product ID", "Sales & price history arrays"],
        ["POST", "/api/shops/{id}/products/{pid}/constraints/evaluate", "Evaluate constraint bounds", "Yes", "JSON: cost, mrp, max_disc, min_margin, stock", "Valid price range or conflict reasons"],
        ["POST", "/api/shops/{id}/products/{pid}/constraints/save", "Save constraint configuration", "Yes", "JSON: cost, mrp, max_disc, min_margin, stock", "Confirmation & evaluation response"],
        ["POST", "/api/shops/{id}/products/{pid}/recommendations/generate", "Generate ML scenarios & rank by profit", "Yes", "Query param: model_type (sklearn/xgboost)", "Top recommendation & ranked scenario table"]
    ]
    create_styled_table(doc, headers_api, data_api)

    # ----------------------------------------------------
    # SECTION 9 — HOW TO RUN BACKEND
    # ----------------------------------------------------
    add_heading_1(doc, "Section 9 — How to Run the FastAPI Backend / API")
    add_body_paragraph(doc, "Follow these exact step-by-step terminal commands to activate and run the FastAPI backend server:")
    
    cmd_backend = (
        "1. Open Terminal and navigate to the backend directory:\n"
        "   cd /Users/vineethmatta/Desktop/pricewise-app/backend\n\n"
        "2. Create a Python Virtual Environment (if not already created):\n"
        "   python3 -m venv venv\n\n"
        "3. Activate the virtual environment:\n"
        "   source venv/bin/activate    # macOS / Linux\n"
        "   # venv\\Scripts\\activate      # Windows PowerShell\n\n"
        "4. Install backend dependencies:\n"
        "   pip install -r requirements.txt\n\n"
        "5. Seed the database with sample retail data (optional):\n"
        "   PYTHONPATH=. python app/utils/sample_data_generator.py\n\n"
        "6. Start the Uvicorn web server:\n"
        "   PYTHONPATH=. uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload\n\n"
        "7. Open Swagger API Documentation in your browser:\n"
        "   http://127.0.0.1:8000/api/docs"
    )
    add_code_block(doc, cmd_backend)

    # ----------------------------------------------------
    # SECTION 10 — HOW TO RUN FRONTEND
    # ----------------------------------------------------
    add_heading_1(doc, "Section 10 — How to Run the React Frontend")
    add_body_paragraph(doc, "Follow these terminal commands to start the Vite React development server:")

    cmd_frontend = (
        "1. Open a new Terminal tab and navigate to the frontend directory:\n"
        "   cd /Users/vineethmatta/Desktop/pricewise-app/frontend\n\n"
        "2. Install Node.js npm packages:\n"
        "   npm install\n\n"
        "3. Start the Vite development server on port 3000:\n"
        "   npx vite --port 3000 --host 127.0.0.1\n\n"
        "4. Open the web application in your browser:\n"
        "   http://127.0.0.1:3000"
    )
    add_code_block(doc, cmd_frontend)

    # ----------------------------------------------------
    # SECTION 11 — FRONTEND & BACKEND CONNECTION
    # ----------------------------------------------------
    add_heading_1(doc, "Section 11 — How Frontend and Backend Connect")
    add_body_paragraph(doc, "The frontend communicates with the backend asynchronously over HTTP using Axios (`src/services/api.js`). When a user submits a form (e.g., setting constraints), the React component calls `API.post('/shops/2/products/1/constraints/evaluate', payload)`. The Axios instance automatically attaches the stored JWT bearer token (`Authorization: Bearer <token>`). FastAPI parses the JSON payload, verifies JWT validity, executes the Python `ConstraintEngine.evaluate()` logic, and returns a JSON response which React uses to update the UI state.")

    # ----------------------------------------------------
    # SECTION 12 — DATABASE SCHEMA
    # ----------------------------------------------------
    add_heading_1(doc, "Section 12 — Database Schema")
    add_body_paragraph(doc, "The SQLite database (`pricewise.db`) comprises 7 relational tables linked via foreign keys:")

    headers_db = ["Table", "Column", "Type", "Key", "Description"]
    data_db = [
        ["users", "user_id", "INTEGER", "PK", "Unique user identifier"],
        ["users", "name", "VARCHAR(100)", "None", "Full name of retailer"],
        ["users", "email", "VARCHAR(150)", "Unique", "Retailer login email address"],
        ["users", "password_hash", "VARCHAR(255)", "None", "Bcrypt hashed password"],
        ["shops", "shop_id", "INTEGER", "PK", "Unique shop identifier"],
        ["shops", "user_id", "INTEGER", "FK -> users", "Owner user foreign key"],
        ["shops", "shop_name", "VARCHAR(150)", "None", "Name of retail store (e.g. FreshMart)"],
        ["csv_uploads", "upload_id", "INTEGER", "PK", "Unique upload transaction ID"],
        ["csv_uploads", "shop_id", "INTEGER", "FK -> shops", "Target shop foreign key"],
        ["csv_uploads", "total_rows", "INTEGER", "None", "Total raw rows in uploaded CSV"],
        ["csv_uploads", "valid_rows", "INTEGER", "None", "Clean valid rows committed"],
        ["products", "product_id", "INTEGER", "PK", "Unique product identifier"],
        ["products", "shop_id", "INTEGER", "FK -> shops", "Shop foreign key"],
        ["products", "external_code", "VARCHAR(100)", "None", "SKU or Item Code from CSV"],
        ["products", "data_sufficiency_status", "VARCHAR(50)", "None", "ML READY, LIMITED DATA, or COLD START"],
        ["sales_records", "record_id", "INTEGER", "PK", "Unique sales record ID"],
        ["sales_records", "product_id", "INTEGER", "FK -> products", "Target product foreign key"],
        ["sales_records", "sale_date", "DATE", "None", "Transaction date"],
        ["sales_records", "selling_price", "FLOAT", "None", "Recorded selling price"],
        ["sales_records", "quantity_sold", "INTEGER", "None", "Units sold"],
        ["product_constraints", "constraint_id", "INTEGER", "PK", "Unique constraint ID"],
        ["product_constraints", "product_id", "INTEGER", "FK -> products", "Product foreign key (Unique)"],
        ["product_constraints", "cost_price", "FLOAT", "None", "Unit cost price (C)"],
        ["product_constraints", "mrp", "FLOAT", "None", "Maximum retail price (M)"],
        ["product_constraints", "max_discount_pct", "FLOAT", "None", "Max allowed discount percentage"],
        ["product_constraints", "min_margin_pct", "FLOAT", "None", "Minimum profit margin percentage"],
        ["recommendation_scenarios", "scenario_id", "INTEGER", "PK", "Unique scenario ID"],
        ["recommendation_scenarios", "product_id", "INTEGER", "FK -> products", "Product foreign key"],
        ["recommendation_scenarios", "candidate_price", "FLOAT", "None", "Evaluated price point"],
        ["recommendation_scenarios", "estimated_profit", "FLOAT", "None", "Predicted gross profit"]
    ]
    create_styled_table(doc, headers_db, data_db)

    # ----------------------------------------------------
    # SECTION 13 — AUTHENTICATION
    # ----------------------------------------------------
    add_heading_1(doc, "Section 13 — Authentication & Security System")
    add_body_paragraph(doc, "Authentication is handled via OAuth2 Password Bearer flow using JSON Web Tokens (JWT). Passwords are never stored in plain text; they are salted and hashed using `passlib[bcrypt]`. Upon successful login (`POST /api/auth/login`), FastAPI generates a signed JWT access token containing the `sub` user_id claim with a 7-day expiration. The frontend stores this token in browser `localStorage` and includes it in all request headers.")

    # ----------------------------------------------------
    # SECTION 14 — CSV DATA FORMAT
    # ----------------------------------------------------
    add_heading_1(doc, "Section 14 — CSV Data Format Specification")
    add_body_paragraph(doc, "PriceWise accepts arbitrary retailer CSV files. The interactive column mapping UI maps uploaded headers to internal targets:")

    headers_csv = ["Internal Field", "Requirement", "Data Type", "Accepted CSV Header Examples"]
    data_csv = [
        ["product_id", "Required", "String / Code", "Item_Code, SKU, ProductID, ProductCode, Code"],
        ["date", "Required", "Date (YYYY-MM-DD)", "Sale_Date, TxnDate, Date, TransactionDate, Time"],
        ["quantity_sold", "Required", "Integer (>= 0)", "Units, Quantity, Qty, UnitsSold, Volume"],
        ["selling_price", "Required", "Float (> 0)", "Rate, SellingPrice, Price, UnitPrice, Amount"],
        ["promotion", "Optional", "String", "Promo, Promotion, DiscountFlag, Offer"],
        ["category", "Optional", "String", "Category, Dept, Department, Group"]
    ]
    create_styled_table(doc, headers_csv, data_csv)

    # ----------------------------------------------------
    # SECTION 15 & 16 — CSV VALIDATION & CLEANING
    # ----------------------------------------------------
    add_heading_1(doc, "Section 15 & 16 — CSV Validation & Data Cleaning Engine")
    add_body_paragraph(doc, "The Pandas CSV pipeline (`app/services/csv_service.py`) executes 10 automated validation and data cleaning rules:")
    add_bullet_point(doc, "Required Mapping Check:", "Ensures product_id, date, quantity_sold, and selling_price are mapped.")
    add_bullet_point(doc, "Date Parsing:", "Converts arbitrary date strings into Python `datetime.date` objects, flagging unparseable rows.")
    add_bullet_point(doc, "Price & Quantity Sanity:", "Flags selling prices <= 0 or missing values, and quantities < 0.")
    add_bullet_point(doc, "Deduplication:", "Identifies duplicate transaction rows matching (product_id, date, selling_price, quantity_sold).")
    add_bullet_point(doc, "Cleaning Summary:", "Calculates non-hardcoded counts: Total Rows, Valid Rows, Duplicate Rows, Invalid Rows, Date Range, and Products Found.")

    # ----------------------------------------------------
    # SECTION 17 & 18 — PRODUCT ANALYSIS & DATA SUFFICIENCY
    # ----------------------------------------------------
    add_heading_1(doc, "Section 17 & 18 — Product Analysis & Data Sufficiency")
    add_body_paragraph(doc, "Products are classified using transparent rule-based data sufficiency criteria:")
    add_bullet_point(doc, "ML READY:", "Requires >= 30 sales records, >= 60 days history, >= 3 distinct price points, and >= 15 non-zero sales transactions.")
    add_bullet_point(doc, "LIMITED DATA:", "Product has sales records (> 0) but does not meet all ML READY criteria.")
    add_bullet_point(doc, "COLD START:", "0 sales records found in historical dataset.")

    # ----------------------------------------------------
    # SECTION 19 — CONSTRAINT ENGINE
    # ----------------------------------------------------
    add_heading_1(doc, "Section 19 — Constraint Engine (Core Business Logic)")
    add_body_paragraph(doc, "The Constraint Engine (`app/constraint_engine/evaluator.py`) is a core feature enforcing retailer business rules. Given Cost Price (C), MRP (M), Max Discount % (D_max), and Min Margin % (M_min), the lower and upper bounds are derived mathematically:")
    
    math_formulas = (
        "1. Cost Price Lower Bound:      P >= C\n"
        "2. Max Discount Lower Bound:   P >= M * (1 - D_max / 100)\n"
        "3. Min Margin Lower Bound:     P >= C / (1 - M_min / 100)\n\n"
        "Effective Minimum Price (P_min): max( C,  M*(1 - D_max/100),  C/(1 - M_min/100) )\n"
        "Effective Maximum Price (P_max): M"
    )
    add_code_block(doc, math_formulas)

    add_body_paragraph(doc, "Numerical Example (Amul Milk 1L): Cost = ₹52, MRP = ₹68, Max Disc = 15%, Min Margin = 10%.")
    add_bullet_point(doc, "Discount Bound:", "68 * (1 - 0.15) = ₹57.80")
    add_bullet_point(doc, "Margin Bound:", "52 / (1 - 0.10) = 52 / 0.9 = ₹57.78")
    add_bullet_point(doc, "Resulting Valid Range:", "₹57.80 ───────── ₹68.00")
    
    add_body_paragraph(doc, "Conflict Case: If Cost = ₹60, MRP = ₹68, Min Margin = 20% -> Required Min Price = ₹75.00 (> MRP ₹68.00). The engine outputs: '⚠ NO VALID PRICE RANGE - Your selected constraints conflict.'")

    # ----------------------------------------------------
    # SECTION 20, 21, 22 — ML, SCENARIOS & PROFIT OPTIMIZATION
    # ----------------------------------------------------
    add_heading_1(doc, "Section 20, 21 & 22 — Machine Learning & Profit Optimization")
    add_body_paragraph(doc, "The machine learning pipeline (`app/ml/`) trains a regression demand model (`Ridge` or `RandomForest` in Scikit-learn, with `XGBoost` integration) on historical sales data to forecast sales volume Q(P). Candidate price points in [P_min, P_max] are generated in uniform increments. Expected Gross Profit is computed as:")

    add_code_block(doc, "Estimated Gross Profit = (Candidate Price - Cost Price) * Predicted Demand Q(P)")
    add_body_paragraph(doc, "Scenarios are filtered by constraint feasibility and ranked descending by expected gross profit, outputting the optimal recommended price point to the retailer.")

    # ----------------------------------------------------
    # SECTION 23 & 24 — FEATURE MATRIX & FILE STRUCTURE
    # ----------------------------------------------------
    add_heading_1(doc, "Section 23 & 24 — Features & File Breakdown")
    add_body_paragraph(doc, "All 15 major system modules are fully implemented in the current codebase:")
    
    headers_feat = ["Feature Module", "Status", "Description"]
    data_feat = [
        ["Authentication & Security", "IMPLEMENTED", "JWT token auth, bcrypt password hashing, protected routes."],
        ["Shop Management", "IMPLEMENTED", "Multi-shop ownership, shop selector dropdown, ShopContext persistence."],
        ["CSV Upload & Preview", "IMPLEMENTED", "Drag-and-drop CSV uploader, header extraction, sample template."],
        ["Interactive Column Mapping", "IMPLEMENTED", "Dropdown mapping UI for flexible CSV field assignment."],
        ["Pandas Validation & Cleaning", "IMPLEMENTED", "Date parsing, duplicate removal, invalid price/qty handling."],
        ["Validation Summary Screen", "IMPLEMENTED", "Non-hardcoded metric cards, issue breakdown, date range display."],
        ["Products List & Filters", "IMPLEMENTED", "Search box, status filter pills, CSV data export."],
        ["Product Analysis View", "IMPLEMENTED", "Key stats, distinct price point count, Recharts area & step line charts."],
        ["Data Sufficiency Classifier", "IMPLEMENTED", "Rule-based audit (ML READY, LIMITED DATA, COLD START)."],
        ["Constraint Engine", "IMPLEMENTED", "Backend service enforcing cost, MRP, discount, margin bounds & conflict checks."],
        ["Backend Unit Testing", "IMPLEMENTED", "Pytest unit tests verifying constraint math and edge cases."],
        ["Dashboard Analytics", "IMPLEMENTED", "Real-time KPI counters, Sales Overview trend chart, attention list."],
        ["Demand Prediction Engine", "IMPLEMENTED", "Scikit-learn / XGBoost model training and price elasticity estimation."],
        ["Scenario Generator & Ranker", "IMPLEMENTED", "Uniform price stepping, profit calculation, scenario ranking table."],
        ["Interactive Header Notifications", "IMPLEMENTED", "Bell icon popover showing real-time system alerts and ingestion updates."]
    ]
    create_styled_table(doc, headers_feat, data_feat)

    # ----------------------------------------------------
    # SECTION 25 & 26 — SETUP & TROUBLESHOOTING
    # ----------------------------------------------------
    add_heading_1(doc, "Section 25 & 26 — Setup Guide & Troubleshooting")
    add_body_paragraph(doc, "Common installation issues and resolutions:")
    add_bullet_point(doc, "Port 8000 / 3000 In Use:", "Kill existing process: `lsof -ti:8000 | xargs kill -9`.")
    add_bullet_point(doc, "Missing email-validator / bcrypt:", "Install via venv pip: `pip install email-validator 'bcrypt==4.0.1'`.")
    add_bullet_point(doc, "CORS Error:", "Ensure FastAPI backend CORS middleware allows origins `['*']`.")

    # ----------------------------------------------------
    # SECTION 27 — GUIDE / VIVA DEFENSE GUIDE
    # ----------------------------------------------------
    add_heading_1(doc, "Section 27 — Project Guide / Viva Review Defense Guide")
    add_heading_2(doc, "1-Minute Project Pitch")
    add_body_paragraph(doc, "\"PriceWise is an AI-driven, constraint-aware decision support system for small retailers. Unlike static software, PriceWise ingests historical sales data, cleans transaction records, audits data sufficiency, and evaluates pricing rules defined by the retailer—such as cost price, MRP, maximum discount, and minimum profit margin. It uses machine learning to forecast demand elasticity and ranks candidate pricing scenarios by gross profit, helping retailers make optimal data-driven pricing recommendations without automatically altering cash register prices.\"")

    add_heading_2(doc, "Likely Viva Questions & Answers")
    add_bullet_point(doc, "Q: Why is it called constraint-aware?", "A: Because pricing recommendations must respect retailer-defined business limits (Cost, MRP, Discount caps, Min Margin). Scenarios violating these constraints are filtered out.")
    add_bullet_point(doc, "Q: Does PriceWise change prices automatically?", "A: No. It is a decision support system that recommends ranked scenarios to the business owner.")
    add_bullet_point(doc, "Q: Why use FastAPI over Django/Flask?", "A: FastAPI offers asynchronous speed, native Pydantic type validation, and automatic Swagger OpenAPI documentation generator.")

    # ----------------------------------------------------
    # SECTION 28, 29, 30 — LIMITATIONS, FUTURE SCOPE & CHEAT SHEET
    # ----------------------------------------------------
    add_heading_1(doc, "Section 28, 29 & 30 — Limitations, Future Scope & Quick Cheat Sheet")
    add_body_paragraph(doc, "Current limitations and planned future enhancements:")
    add_bullet_point(doc, "Current Limitations:", "Requires initial CSV upload for non-zero sales modeling; local SQLite storage.")
    add_bullet_point(doc, "Future Scope:", "PostgreSQL deployment, competitor web scraping, real-time inventory API integration.")

    add_heading_2(doc, "Project Quick Reference Cheat Sheet")
    cheat_sheet = (
        "Project: PriceWise Decision Support System\n"
        "Frontend: React 18 + Vite + Tailwind CSS + Recharts (Port 3000)\n"
        "Backend: Python 3.13 + FastAPI + Uvicorn (Port 8000)\n"
        "Database: SQLite 3 + SQLAlchemy 2.0 ORM\n"
        "Data & ML: Pandas + NumPy + Scikit-Learn (Ridge/RF) + XGBoost\n"
        "Auth: JWT Bearer Tokens + Bcrypt Password Hashing\n"
        "Core Feature: Pure Python Backend Constraint Engine (P_min to P_max)\n"
        "Flow: Auth -> Shop -> CSV Upload -> Column Mapping -> Cleaning -> Analysis -> Constraints -> ML Recommendations"
    )
    add_code_block(doc, cheat_sheet)

    # Save document
    doc_path = "docs/PriceWise_Project_Detailed_Documentation.docx"
    doc.save(doc_path)
    print(f"Document successfully created at {doc_path}")

if __name__ == "__main__":
    generate_documentation()
