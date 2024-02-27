from sqlalchemy import create_engine
from datetime import datetime, timedelta
import os
import uuid
from sqlalchemy import text
import urllib.parse
import hashlib
import shutil

DATE = os.getenv("DATE", datetime.now().strftime("%Y-%m-%d"))
TIMESTAMP = DATE + " 00:00:00"

db_user_name = "root"
db_pass_word = "root"
db_host = "localhost"
db_name = "dummy_baltini"
engine = create_engine('mysql+pymysql://{}:{}@{}/{}'.format(db_user_name, db_pass_word, db_host, db_name))



if os.path.exists("product_duplicates"):
    shutil.rmtree("product_duplicates")

if os.path.exists("product_duplicate_lists"):
    shutil.rmtree("product_duplicate_lists")

os.mkdir("product_duplicates")
os.mkdir("product_duplicate_lists")

### get data, idea is to try batch the get data and insertion process utilizing upsert for duplicate removal within a day
with engine.connect() as conn:
    q = text(f"SELECT id , tags, UPPER(category) as category, external_id, UPPER(gender) FROM products WHERE DATE(updated_at) = '{DATE}'")
    proxy = conn.execution_options(stream_results=True).execute(q)
    count = 0
    while True:
        count += 1
        batch = proxy.fetchmany(100000)
        if not batch:
            break

        batch_data = {}
        for x in batch:
            try:
                product_id = [ y for y in x[1].split(",") if "ProductID" in y ][0].strip().replace("ProductID: ", "")
            except:
                print(x[0])
                raise False
            unique_key = f"{product_id}|{x[4]}|{x[2]}"
            if unique_key not in batch_data:
                batch_data[unique_key] = []

            batch_data[unique_key].append(x)
        for k,v in batch_data.items():
            product_duplicate_id = hashlib.md5(k.encode()).hexdigest()
            with open(f"product_duplicates/{DATE}-{count}.csv","a") as f:
                f.write("""{},"{}","{}","{}"\n""".format(product_duplicate_id, k, TIMESTAMP, TIMESTAMP))
            
            with open(f"product_duplicate_lists/{DATE}-{count}.csv","a") as f:
                f.write("")
                for x in v:
                    f.write("""{},{},{},{},{},"{}","{}"\n""".format(
                            str(uuid.uuid4()),
                            product_duplicate_id,
                            x[3],
                            x[0],
                            "NULL",
                            TIMESTAMP,
                            TIMESTAMP
                        ))
                    f.write("\n")
    proxy.close()


