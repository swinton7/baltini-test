from sqlalchemy import create_engine
from datetime import datetime, timedelta
import os
import uuid
from sqlalchemy import text
import urllib.parse
import hashlib
import shutil
from glob import glob

DATE = os.getenv("DATE", datetime.now().strftime("%Y-%m-%d"))

db_user_name = "root"
db_pass_word = "root"
db_host = "localhost"
db_name = "dummy_baltini"
engine = create_engine('mysql+pymysql://{}:{}@{}/{}?local_infile=1'.format(db_user_name, db_pass_word, db_host, db_name))

with engine.connect() as conn:
    conn.execute(text(f"SET GLOBAL local_infile=ON"))
    conn.commit()
    conn.execute(text(f"DELETE FROM product_duplicate_lists where DATE(updated_at) = '{DATE}'"))
    conn.execute(text(f"DELETE FROM product_duplicates where DATE(updated_at) = '{DATE}'"))
    # load product_duplicates
    pd = glob("product_duplicates/*")
    for i in pd:
        q = text(f"""LOAD DATA LOCAL INFILE '{i}' INTO TABLE product_duplicates
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY "\\n"
(id, title, created_at, updated_at)
""")
        conn.execute(q)
        conn.commit()

    # load product_duplicate_lists
    pdl = glob("product_duplicate_lists/*")
    for i in pdl:
        q = text(f"""LOAD DATA LOCAL INFILE '{i}' INTO TABLE product_duplicate_lists
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\\n'""")
        conn.execute(q)
        conn.commit()