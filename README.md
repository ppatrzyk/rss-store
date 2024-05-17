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
rows = []
async def get_data():
    conn = await asyncpg.connect(db_conn_str)
    async with conn.transaction():
        async for r in conn.cursor("select source_id, content from content"):
            rows.append({"source_id": r[0], "content": r[1], })
    await conn.close()
    return True
```