import asyncio
import asyncpg
from datetime import datetime
import feedparser
import os
from prefect import flow, task
import time

db_conn_str = os.environ["RSS_DB"]

@task
async def get_feed_list():
    """
    Get feed URLs from db
    """
    feeds = []
    conn = await asyncpg.connect(db_conn_str)
    async with conn.transaction():
        async for r in conn.cursor('select id, url from source'):
            feeds.append({"id": r[0], "url": r[1]})
    await conn.close()
    return feeds

@task(retries=4)
async def query_feed(feed):
    """
    Get new entries for a feed
    """
    source_id = feed.get("id")
    url = feed.get("url")
    response = feedparser.parse(url)
    print(f"querying {source_id}")
    return source_id, response

@task(retries=4)
async def save_entries(source_id, response):
    """
    Write entries to db
    """
    query = """
        insert into
        content(source_id, publication_date, url, external_id, title, content)
        values ($1, $2, $3, $4, $5, $6)
    """
    entries = []
    for entry in response.entries:
        publication_date = None
        try:
            publication_date = datetime.fromtimestamp(time.mktime(entry.published_parsed))
        except:
            pass
        row = (
            source_id,
            publication_date,
            entry.link,
            entry.id,
            entry.title,
            entry.summary
        )
        entries.append(row)
    conn = await asyncpg.connect(db_conn_str)
    _result = await conn.executemany(query, entries)
    await conn.close()
    print(f"saving {len(entries)} entries for {source_id}")
    return True

@flow(log_prints=True)
async def update(feed):
    """
    Flow for updating single feed
    """
    source_id, response = await query_feed(feed)
    _save = await save_entries(source_id, response)
    return True

@flow(log_prints=True)
async def update_all():
    """
    Main flow for updating rss feeds
    """
    feeds = await get_feed_list()
    feed_update_tasks = tuple(update(feed) for feed in feeds)
    await asyncio.gather(*feed_update_tasks)
    return True
