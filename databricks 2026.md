

1. - **Authenticate CLI**:
        
        bash
        
        databricks configure --host https://<your-databricks-workspace>.azuredatabricks.net
        
    - **Deploy Bundle (Dev Environment)**:
        
        bash
        
        databricks bundle deploy --target dev
        
    - **Trigger Workflow Run**:
        
        bash
        
        databricks bundle run --target dev f1_2026_daily_predictions_job