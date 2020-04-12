import psycopg2


async def sql(query: str, params=None, fetch=0):
    ok = True
    error = ''
    data = []
    conn_string = "host='localhost' dbname='s3http' user='s3http' password='s3http'"
    conn = psycopg2.connect(conn_string)
    with conn.cursor() as cur:
        try:
            cur.execute(query, params)
        except Exception as e:
            ok = False
            error = str(e)
        if fetch:
            data = cur.fetchmany(fetch)  # fetchall
        conn.commit()
    conn.close()
    return {'ok': ok, 'error': error, 'rows': cur.rowcount, 'query': cur.query, 'data': data}


