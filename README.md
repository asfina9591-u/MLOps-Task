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
```

## 🐳 Docker Run
```bash
docker build -t mlops-task .
docker run --rm mlops-task
```

## 📊 Example metrics.json
```json
{
  "version": "v1",
  "rows_processed": 9996,
  "metric": "signal_rate",
  "value": 0.4986,
  "latency_ms": 39,
  "seed": 42,
  "status": "success"
}
```
