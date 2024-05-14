import asyncio
import feedparser
import os

from prefect import flow, task

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text

db_conn_str = os.environ["RSS_DB"]
engine = create_async_engine(db_conn_str)

@task
async def get_feed_list():
    """
    Get feed URLs from db
    """
    async with engine.connect() as conn:
        result = await conn.execute(text("select id, url from source"))
    feeds = tuple(result.mappings())
    return feeds

@task(retries=4)
async def query_feed(feed):
    """
    Get new entries for a feed
    """
    # TODO get feed
    source_id = feed.get("id")
    url = feed.get("url")
    entries = tuple(f"{source_id}-entry-{i}" for i in range(5))
    print(f"querying {source_id}")
    print(f"entries {entries}")
    return source_id, entries

@task(retries=4)
async def save_entries(source_id, entries):
    """
    Write entries to db
    """
    # TODO batch write all entries
    query = """
        insert into
        content(source_id, publication_date, url, external_id, title, content)
        values (:source_id, :publication_date, :url, :external_id, :title, :content)
    """
    params = {
        "source_id": source_id,
        "publication_date": "2024-05-01T20:20:20+00:00",
        "url": "todo",
        "external_id": "todo",
        "title": "todo",
        "content": entries[0]
    }
    async with engine.connect() as conn:
        _result = await conn.execute(text(query), params)
        # _commit = await conn.commit()
    print("saving entries")
    print(entries)
    return True

@flow(log_prints=True)
async def update(feed):
    """
    Flow for updating single feed
    """
    source_id, entries = await query_feed(feed)
    _save = await save_entries(source_id, entries)
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
