# s3http

FastAPI for indexing S3 buckets into Postgres.

Because Amazon's S3 browser is not good.


## Status

Work in progress.


## Install

```bash
make venv deps up run
```

## Create database

http://localhost:8000/create


## Index all keys in a bucket

http://localhost:8000/create/{bucket}


## List indexed buckets

http://localhost:8000


## List keys in a bucket

http://localhost:8000/list/{bucket}


## Destroy database

http://localhost:8000/destroy
