# rss-store

System for gathering rss feed entries. Written with python ([prefect](https://github.com/PrefectHQ/prefect)) and PostgreSQL.

## Instructions

1. Build agent images

```
# from ./rssagent
docker build . -t rssagent:latest

# from ./mlagent
docker build . -t mlagent:latest
```

2. Run

```
docker-compose up -d
```

Prefect dashboard is exposed at: http://localhost:4200/dashboard

3. Add rss sources into postgres instance

```
-- e.g.
insert into source(id, url) values ('onet', 'https://wiadomosci.onet.pl/.feed'), ('wpolityce', 'https://feeds.feedburner.com/wPolitycepl'), ('fakt', 'https://www.fakt.pl/rss');
```

4. Trigger tasks

```
prefect deploy --prefect-file /flows/prefect.yaml
```



testing with exposed postgres:
```
db_conn_str = "postgresql://postgres:postgres@localhost:15432/rss"
source_id = []
content = []
async def get_data():
    conn = await asyncpg.connect(db_conn_str)
    async with conn.transaction():
        async for r in conn.cursor("select source_id, content from content"):
            source_id.append(r[0])
            content.append(r[1])
    await conn.close()
    return True

asyncio.get_event_loop().run_until_complete(get_data())
```

todo 
postgres backend test
serve
https://mlflow.org/docs/latest/model-registry.html#serving-an-mlflow-model-from-model-registry
update dynamically which one is served?
how to access the same vectorizer (tfidf) to transform unseen data for predict
