import json

from fastapi import FastAPI
from starlette.responses import RedirectResponse as redirect

import s3bucket
from psql import sql


app = FastAPI()


def format_url(path):
    return f'http://127.0.0.1:8000{path}'
    

@app.get("/")
async def root():
    query = """
    SELECT
      DISTINCT bucket
    FROM items
    """
    data = []
    q = await sql(query, fetch=100)
    for row in q['data']:
        bucket = row[0]
        url = format_url(f'/list/{bucket}')
        data.append({'url': url})
    return data


# TODO: app.post
@app.get("/create")
async def create():
    """Create database."""
    query = """
    CREATE TABLE items (
	name varchar NOT NULL,
	bucket varchar NOT NULL,
	data json NOT NULL,
        UNIQUE(bucket, name)
    );
    """.strip()
    data = await sql(query)
    return data


# TODO: app.delete
@app.get("/destroy")
async def destroy():
    """Destroy database."""
    query = "DROP TABLE items;"
    data = await sql(query)
    return data


# TODO: app.post
@app.get("/create/{bucket}")
async def create_bucket(bucket: str, prefix: str):
    """Download all items from bucket by prefix, store in DB."""
    items = await s3bucket.items(bucket=bucket, prefix=prefix)
    ok, fail = 0, 0
    for item in items:
        query = """
        INSERT INTO items(name, bucket, data)
        VALUES (%s, %s, %s)
        """
        print(item['name'])
        extra = {
            'last_modified': item['last_modified'],
            'size': item['size'],
        }
        params = (item['name'], bucket, json.dumps(extra))
        data = await sql(query, params)
        if data['ok']:
            ok += 1
        else:
            fail += 1
    return {'ok': ok, 'fail': fail}


@app.get("/list/{bucket}")
async def list_bucket(bucket: str):
    query = """
    SELECT
      name,
      (data->>'last_modified')::timestamp,
      (data->>'size')::integer
    FROM items
    WHERE bucket = %s
      -- AND (data->>'last_modified')::timestamp >= now() - interval '30 day'
      -- AND (data->>'size')::integer < 1000 -- small files
    ORDER BY 2 DESC
    """
    params = (bucket, )
    data = []
    q = await sql(query, params, fetch=500)
    for row in q['data']:
        name = row[0]
        last_modified = row[1]
        size = row[2]
        url = format_url(f'/read/{bucket}?name={name}')
        delete_url = format_url(f'/delete/{bucket}?name={name}')
        data.append({
            'url': url, 
            'delete': delete_url, 
            'last_modified': last_modified, 
            'size': size,
        })
    return q['rows'], data


@app.get("/read/{bucket}")
async def read_key(bucket: str, name: str):
    data = await s3bucket.get_item(bucket, name)
    return redirect(url=data['url'])


# TODO: app.delete
@app.get("/delete/{bucket}")
async def delete_key(bucket: str, name: str):
    s3_delete = await s3bucket.delete_item(bucket, name)
    query = """
    DELETE FROM items
    WHERE bucket = %s
      AND name = %s
    """
    params = (bucket, name)
    data = await sql(query, params)
    return data

