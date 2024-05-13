prefect work-pool create --type process my-pool
prefect work-queue create -p my-pool my-queue
# deploy here as one-job only, normally trigger from outside
prefect deploy --prefect-file /flows/prefect.yaml --pool my-pool
prefect worker start -p my-pool -n my-worker -q my-queue
