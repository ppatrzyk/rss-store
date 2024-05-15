# rss-store

System for gathering rss feed entries. Written with python ([prefect](https://github.com/PrefectHQ/prefect)) and PostgreSQL.

## Instructions

1. Build agent image

```
docker build . -t rssagent:latest
```

2. Run

```
docker-compose up -d
```

Prefect dashboard is exposed at: http://localhost:4200/dashboard

3. Add rss sources into postgres instance

```
-- e.g.
insert into source(id, url) values ('onet', 'https://wiadomosci.onet.pl/.feed');
```
