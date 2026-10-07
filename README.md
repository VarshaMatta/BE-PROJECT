# PriceWise: An AI-Based Constraint-Aware Pricing and Promotion Decision Support System for Retailers

> **Final-Year Engineering Project Demonstration & Production Codebase**

PriceWise is an AI-based decision-support system designed for small and medium-sized retailers. It analyzes historical sales transaction data, validates and cleans datasets, evaluates product data sufficiency (`ML READY`, `LIMITED DATA`, `COLD START`), enforces retailer-defined business constraints (Cost Price, MRP, Maximum Discount %, Minimum Profit Margin %, and Stock Availability), and ranks candidate pricing/promotion scenarios according to estimated gross profit.

*Note: PriceWise recommends pricing decisions to retailers; it does **not** automatically change prices.*

---

## 🎨 Visual Design & Theme
- **Theme**: Dark navy modern SaaS theme (`#0B0E17` backdrop, `#121726` surface background, `#1A2035` cards).
- **Accents**: Violet / Purple gradients (`from-purple-600 to-indigo-600`).
- **Status Badges**:
  - 🟢 **ML READY / Valid / Success**: Emerald Green (`bg-emerald-500/10 text-emerald-400`)
  - 🟡 **LIMITED DATA / Warning**: Amber Yellow (`bg-amber-500/10 text-amber-400`)
  - 🔴 **COLD START / Conflict / Error**: Rose Red (`bg-rose-500/10 text-rose-400`)

---

## 🛠️ Technology Stack

| Layer | Technology | Purpose |
| :--- | :--- | :--- |
| **Frontend** | React 18, Vite 6, Tailwind CSS 3, Recharts 2 | Responsive modern dark SaaS dashboard UI, interactive charts, forms, and modals. |
| **Backend** | Python 3.13, FastAPI 0.110, Uvicorn | High-performance asynchronous REST API, OpenAPI docs, Pydantic schemas. |
| **Database** | SQLite 3, SQLAlchemy 2.0 ORM | Relational storage for users, shops, products, sales records, and constraints. |
| **Data & ML** | Pandas 2.2, NumPy, Scikit-learn, XGBoost | Flexible CSV column mapping, data validation/cleaning, demand prediction models. |
| **Security** | PyJWT / Jose, Passlib / Bcrypt | Stateless JWT bearer authentication and bcrypt salted password hashing. |

---

## 🚀 Quick Start Guide (Start From Zero)

### 1. Start the FastAPI Backend

```bash
# Navigate to backend directory
cd backend

# Create Python virtual environment (if not already created)
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate       # macOS / Linux
# venv\Scripts\activate          # Windows PowerShell

# Install requirements
pip install -r requirements.txt

# Seed sample database (Optional demo data)
PYTHONPATH=. python app/utils/sample_data_generator.py

# Start Uvicorn API server on port 8000
PYTHONPATH=. uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

- **Backend Health Check**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Swagger Interactive API Documentation**: [http://127.0.0.1:8000/api/docs](http://127.0.0.1:8000/api/docs)

---

### 2. Start the React Frontend

```bash
# Open a new terminal tab and navigate to frontend directory
cd frontend

# Install Node modules
npm install

# Launch Vite development server on port 3000
npx vite --port 3000 --host 127.0.0.1
```

- **Frontend Application URL**: [http://127.0.0.1:3000/](http://127.0.0.1:3000/)

---

## 🔑 Pre-Seeded Demo Account

- **Email**: `alex@freshmart.com`
- **Password**: `Password123!`

*(You can also register a brand new account from the `/register` view.)*

---

## 📁 Project Directory Structure

```
pricewise-app/
├── docs/
│   └── PriceWise_Project_Detailed_Documentation.docx   # Complete Word Documentation
│
├── backend/
│   ├── app/
│   │   ├── auth/                 # jwt.py, password.py, dependencies.py
│   │   ├── constraint_engine/    # evaluator.py (Pure Python lower/upper bound math)
│   │   ├── ml/                   # demand_model.py, scenario_generator.py, optimizer.py
│   │   ├── models/               # user.py, shop.py, upload.py, product.py, sales.py, constraint.py
│   │   ├── schemas/              # Pydantic validation schemas
│   │   ├── routers/              # auth.py, shops.py, uploads.py, products.py, constraints.py, analytics.py
│   │   ├── services/             # csv_service.py (Pandas cleaning), product_analysis_service.py
│   │   ├── utils/                # sample_data_generator.py, generate_docx.py
│   │   ├── config.py             # Settings & keys
│   │   ├── database.py           # SQLAlchemy engine & sessionmaker
│   │   └── main.py               # FastAPI entrypoint
│   ├── tests/
│   │   └── test_constraint_engine.py # Pytest backend unit tests
│   ├── pricewise.db              # SQLite Database file
│   └── requirements.txt
│
└── frontend/
    ├── src/
    │   ├── components/           # Sidebar, Header, Badge, Layouts
    │   ├── context/              # AuthContext.jsx, ShopContext.jsx
    │   ├── pages/                # Login, Register, Shops, Dashboard, Upload, ColumnMapping, Validation, Products, ProductAnalysis, SetConstraints, Recommendations
    │   ├── services/             # api.js (Axios client to http://127.0.0.1:8000/api)
    │   ├── App.jsx               # React Router routes
    │   └── main.jsx
    ├── package.json
    ├── tailwind.config.js
    └── vite.config.js
```

---

## 🧮 Constraint Engine Logic & Formulas

Given retailer inputs:
- Cost Price $C > 0$
- Maximum Retail Price $M > 0$
- Maximum Allowed Discount $D_{max} \in [0, 100]\%$
- Minimum Required Margin $M_{min} \in [0, 100]\%$

Mathematical Effective Price Bounds:
$$P_{min\_effective} = \max\left( C, \quad M \times \left(1 - \frac{D_{max}}{100}\right), \quad \frac{C}{1 - \frac{M_{min}}{100}} \right)$$

$$P_{max\_effective} = M$$

Feasibility Criterion:
- If $P_{min\_effective} \le P_{max\_effective}$, a **VALID PRICE RANGE** exists: $[P_{min\_effective}, P_{max\_effective}]$.
- If $P_{min\_effective} > P_{max\_effective}$, the system flags **NO VALID PRICE RANGE** with detailed conflict diagnostics.

---

## 🧪 Unit Testing

Run unit tests for backend constraint logic:

```bash
cd backend
PYTHONPATH=. ./venv/bin/pytest tests/test_constraint_engine.py
```

---

## 📄 Documentation File

The complete Microsoft Word detailed documentation is generated and saved at:
`docs/PriceWise_Project_Detailed_Documentation.docx`
