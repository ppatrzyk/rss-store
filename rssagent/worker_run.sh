prefect work-pool create --type process rss-pool
prefect work-queue create -p rss-pool rss-queue
prefect worker start -p rss-pool -n rss-worker -q rss-queue
