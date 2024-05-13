-- if future changes, run in migrations

-- https://stackoverflow.com/a/18389184
SELECT 'create database rss'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'rss')\gexec

\c rss;

create table if not exists source (
    id varchar(255),
    url text not null,
    primary key(id)
);

create table if not exists content (
    id uuid default gen_random_uuid(),
    source_id varchar(255),
    publication_date timestamp with time zone,
    ingestion_date timestamp with time zone not null default now(),
    url text,
    external_id text,
    title text,
    content text,
    primary key(id),
    constraint fk_source
        foreign key(source_id) 
            references source(id)
            on delete set null
);
