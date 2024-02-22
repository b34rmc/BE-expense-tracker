import os
import boto3
from botocore.exceptions import NoCredentialsError

from flask import jsonify
import flask

from db import db
from models.profile_image import Profile, profile_schema
from util.authenticate import authenticate
from util.reflection import populate_object
from dotenv import load_dotenv
load_dotenv()

B2_KEY_ID = os.environ.get('B2_KEY_ID')
B2_APPLICATION_KEY = os.environ.get('B2_APPLICATION_KEY')
B2_BUCKET_NAME = os.environ.get('B2_BUCKET_NAME')

s3_client = boto3.client('s3',
                         endpoint_url='https://s3.us-east-005.backblazeb2.com',
                         aws_access_key_id=B2_KEY_ID,
                         aws_secret_access_key=B2_APPLICATION_KEY,)


@authenticate
def profile_update(req: flask.Request, auth_info) -> flask.Response:
    post_data = req.form
    profile_id = auth_info.user.profile_id

    profile_data = db.session.query(Profile).filter(Profile.profile_id == profile_id).first()

    if not profile_data:
        return jsonify({"message": "no avatar to update"}), 409

    if 'file' in req.files:
        file = req.files['file']
        if file.filename != '':
            file_name = f"{profile_id}.{file.filename}"
            extra_args = {'ContentType': file.content_type, 'ContentDisposition': 'inline'}
            
            try:
                s3_client.upload_fileobj(file, B2_BUCKET_NAME, file_name, ExtraArgs=extra_args)
                image_url = f"https://f005.backblazeb2.com/file/{B2_BUCKET_NAME}/{file_name}"
                profile_data.image_url = image_url
            except NoCredentialsError:
                return jsonify("AWS credentials not available"), 500

    populate_object(profile_data, post_data)

    try:
        db.session.commit()
        return jsonify({"message": "avatar updated", "avatar": profile_schema.dump(profile_data)}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "an error occurred while updating the avatar"}), 500