import asyncpg
import mlflow
import os
from prefect import flow, task

db_conn_str = os.environ["RSS_DB"]

@flow(log_prints=True)
def train():
    """
    test
    """
    print("ml agent exec test")
    return True

async def get_data():
    rows = []
    conn = await asyncpg.connect(db_conn_str)
    async with conn.transaction():
        async for r in conn.cursor("select source_id, content from content"):
            rows.append({"source_id": r[0], "content": r[1], })
    await conn.close()
    return True