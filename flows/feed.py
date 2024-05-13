import itertools
import feedparser
from prefect import flow, task

@task
def get_feed_list():
    """
    Get feed URLs from db
    """
    # TODO get from db
    feeds = ["a", "b", ]
    return feeds

@task(retries=4)
def query_feed(feed):
    """
    Get new entries for a feed
    """
    # TODO get feed
    entries = tuple(f"{feed}-entry-{i}" for i in range(5))
    print(f"querying {feed}")
    print(f"entries {entries}")
    return entries

@task
def save_entries(entries):
    """
    Write entries to db
    """
    # TODO write
    print("saving entries")
    print(entries)
    return True

@flow(log_prints=True)
def update():
    """
    Main flow for updating rss feeds
    """
    feeds = get_feed_list()
    responses = tuple(query_feed(feed) for feed in feeds)
    entries = tuple(itertools.chain(*responses))
    save_entries(entries)
    return True
