import httpx

resp = httpx.get("http://127.0.0.1:4200/api/health")
resp.raise_for_status()
