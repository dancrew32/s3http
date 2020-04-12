import boto3

# from io import BytesIO
# from PIL import Image


async def items(bucket: str, prefix: str):
    s3 = boto3.resource('s3')
    b = s3.Bucket(bucket)
    q = b.objects.filter(Prefix=prefix)
    data = []
    for obj in q:
        data.append({
            'name': obj.key, 
            'last_modified': str(obj.last_modified),
            'size': obj.size,
        })
    return data


async def get_item(bucket: str, name: str, expires=60):
    s3 = boto3.client('s3')
    url = s3.generate_presigned_url('get_object', Params={
        'Bucket': bucket, 'Key': name}, ExpiresIn=expires)
    # obj = s3.Object(bucket, name)
    # img = Image.open(BytesIO(obj.get()['Body'].read()))
    return {'url': url}


async def delete_item(bucket: str, name: str):
    client = boto3.client('s3')
    return client.delete_object(Bucket=bucket, Key=name)
