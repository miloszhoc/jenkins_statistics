import json

import boto3

from utils import read_json_file
from variables import TEST_RESULTS_BUCKET_NAME, NUMBER_OF_DAYS, LOCAL_DOWNLOAD_PATH, JOINED_TEST_DATA_FILE_NAME


class TestResultsJoiner:

    def __init__(self) -> None:
        self.test_result_files = []
        self.s3 = boto3.client('s3')

    def _download_files_from_s3(self):
        get_last_modified = lambda obj: obj['Key']

        objs = self.s3.list_objects_v2(Bucket=TEST_RESULTS_BUCKET_NAME)['Contents']
        last_added = [obj['Key'] for obj in sorted(objs, key=get_last_modified)]
        last_files = list(reversed(last_added))[:NUMBER_OF_DAYS]
        for file in last_files:
            self.test_result_files.append(self._download_object_from_s3(file))

    def _download_object_from_s3(self, file_name):
        download_path = f'{LOCAL_DOWNLOAD_PATH}/{file_name}'
        print(f"Downloading {file_name} to {download_path}")
        self.s3.download_file(TEST_RESULTS_BUCKET_NAME, file_name, str(download_path))
        return str(download_path)

    def _serialize_python_object(self, obj):
        with open(JOINED_TEST_DATA_FILE_NAME, 'w+') as f:
            json.dump(obj, f)

    def join_results(self):
        self._download_files_from_s3()
        result = {}

        for file in self.test_result_files:
            filename = file.split('/')[-1].split('.')[0]
            result.update({filename: read_json_file(file)})
        self._serialize_python_object(result)
