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

@task(retries=4)
def save_entries(entries):
    """
    Write entries to db
    """
    # TODO write
    print("saving entries")
    print(entries)
    return True

@flow(log_prints=True)
def update(feed):
    """
    Flow for updating single feed
    """
    entries = query_feed(feed)
    _save = save_entries(entries)
    return True

@flow(log_prints=True)
def update_all():
    """
    Main flow for updating rss feeds
    """
    feeds = get_feed_list()
    _update = tuple(update(feed) for feed in feeds)
    return True
