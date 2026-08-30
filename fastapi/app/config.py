from pathlib import Path
import os
BASE_DIR=Path(__file__).resolve().parent.parent
DB_PATH=Path(os.getenv("TASKFLOW_DB_PATH",BASE_DIR/"data"/"taskflow_product_health.db"))
