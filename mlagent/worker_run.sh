prefect work-pool create --type process ml-pool
prefect work-queue create -p ml-pool ml-queue
prefect worker start -p ml-pool -n ml-worker -q ml-queue
