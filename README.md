# MLOps Task

## 📌 Project Overview
This project demonstrates a simple MLOps workflow:
- Data ingestion from CSV
- Metrics calculation
- Logging and error handling
- Containerization with Docker

## ⚙️ Local Run
```bash
pip install -r requirements.txt
python run.py --input data.csv --config config.yaml --output metrics.json --log-file run.log
