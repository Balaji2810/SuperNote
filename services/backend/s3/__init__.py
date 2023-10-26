import boto3
import os
import io
import uuid
import base64

S3_URI = os.environ["S3_URI"]
S3_ACCESS = os.environ["S3_ACCESS"]
S3_SECRET = os.environ["S3_SECRET"]
S3_BUCKET = os.environ["S3_BUCKET"]

class S3:
    s3_target = None

    @classmethod
    def connect(cls):
        if cls.s3_target == None:
            cls.s3_target = boto3.client('s3',
                  endpoint_url=S3_URI,
                  aws_access_key_id=S3_ACCESS,
                  aws_secret_access_key=S3_SECRET)
        try:
            cls.s3_target.create_bucket(Bucket=S3_BUCKET)
        except:
            pass

    @classmethod
    def put_data(cls, data, note_id):
        for _ in range(3):
            try:
                cls.connect()
                cls.s3_target.put_object(Body=data, Bucket=S3_BUCKET, Key=f'{note_id}/data.txt')
                return True
            except:
                pass
                # Should log error
        return False
    
    @classmethod
    def get_data(cls, note_id):
        for _ in range(3):
            try:
                cls.connect()
                data = cls.s3_target.get_object(Bucket=S3_BUCKET, Key=f'{note_id}/data.txt')
                data = data.get('Body').read().decode('utf-8')
                return data
            except:
                pass
        return None
    

    @classmethod
    def upload_file(cls, note_id, file_obj):
        for _ in range(3):
            try:
                cls.connect()
                key = f'{note_id}/media/{uuid.uuid4().hex}_{file_obj.filename}'
                cls.s3_target.upload_fileobj(file_obj.file, Bucket=S3_BUCKET, Key=key)
                return {"key":base64.b64encode(key.encode()).decode()}
            except Exception as exc:
                print(exc)
                pass
        return None

    @classmethod
    def download_file(cls,key):
        for _ in range(3):
            try:
                key = base64.b64decode(key).decode()

                response = cls.s3_target.get_object(Bucket=S3_BUCKET, Key=key)
                file_data = response['Body'].read()
                return {"file_data":file_data,"filename": key.split("/")[-1]}
            except Exception as exc:
                print(exc)
                pass
        return None



