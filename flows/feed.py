import asyncio
import feedparser
import os
from prefect import flow, task
from sqlalchemy.ext.asyncio import create_async_engine

db_conn_str = os.environ["RSS_DB"]
engine = create_async_engine(db_conn_str)

@task
async def get_feed_list():
    """
    Get feed URLs from db
    """
    # TODO get from db
    feeds = ["a", "b", ]
    return feeds

@task(retries=4)
async def query_feed(feed):
    """
    Get new entries for a feed
    """
    # TODO get feed
    entries = tuple(f"{feed}-entry-{i}" for i in range(5))
    print(f"querying {feed}")
    print(f"entries {entries}")
    return entries

@task(retries=4)
async def save_entries(entries):
    """
    Write entries to db
    """
    # TODO write
    print("saving entries")
    print(entries)
    return True

@flow(log_prints=True)
async def update(feed):
    """
    Flow for updating single feed
    """
    entries = await query_feed(feed)
    _save = await save_entries(entries)
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
