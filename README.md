# Info
This is just a playground project to get my hands dirty with grapQL. Currently not used and not maintained :)

#### Start cloud SQL proxy
Run provided script "cloud_proxy.sh". Requires the actual database connetion
information being set in file ".env".
```bash
> cloud_proxy.sh
```

#### Deploy
First get all static files:
```bash
> python manage.py collectstatic
```
Then issue upload:
```bash
> gcloud app deploy
```
