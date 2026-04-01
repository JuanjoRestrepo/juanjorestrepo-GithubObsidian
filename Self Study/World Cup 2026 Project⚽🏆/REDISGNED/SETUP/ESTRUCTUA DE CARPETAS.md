
```bash
world-cup-predictor/
│
├── docker/
│   ├── docker-compose.yml
│
├── data/
│   ├── raw/        (bronze)
│   ├── processed/  (silver)
│   ├── features/   (gold)
│
├── pipelines/
│   ├── ingestion/
│   ├── processing/
│   ├── feature_engineering/
│
├── models/
│   ├── train.py
│   ├── predict.py
│
├── api/
│   ├── server.js   (o FastAPI)
│
├── dbt/
│
├── notebooks/
│
└── README.md
```


