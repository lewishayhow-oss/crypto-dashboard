# Bitcoin Live Tracker (CryptoDashboard)

A real-time, full-stack cryptocurrency dashboard that streams live Bitcoin prices using a microservices architecture.

## 🏗 Architecture

*   **Data Engine (Python/gRPC):** Generates simulated market data and streams it via gRPC.
*   **API Gateway (Flask):** Takes the gRPC data and exposes it to the frontend via a REST API.
*   **Frontend (React + Vite):** A simple dashboard that visualizes the data trend in real-time.

## 🚀 How to Run

### Prerequisites
*   Python 3.8+
*   Node.js & npm

### 1. Setup
**Backend:**
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

**Frontend:**
```bash
cd market-stream/frontend
npm install
cd ../..
```

### 2. Start the App
Simply double-click **`run_app.bat`** on Windows.

Or run manually:
```bash
npx concurrently -k -n "ENGINE,API,UI" -c "blue,magenta,green" "venv\Scripts\python market-stream/data-engine/server.py" "venv\Scripts\python market-stream/api-gateway/app.py" "npm run dev --prefix market-stream/frontend"
```

The dashboard will open at `http://localhost:5173`.
