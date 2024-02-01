import os
from typing import Dict

from urllib3.fields import RequestField

from icometrix_sdk.models.base import PaginatedResponse
from icometrix_sdk.models.upload_entity import StartUploadDto, UploadEntity, UploadEntityFiles
from icometrix_sdk.utils.api_client import ApiClient


class Uploads:
    def __init__(self, api: ApiClient):
        self._api = api

    def get_all(self, project_id: str, **kwargs) -> PaginatedResponse[UploadEntity]:
        """
        List all uploads within a project

        :param: The ID of the project
        :return: A Paginated response containing upload entries
        """
        page = self._api.get(f"/uploads-service/api/v1/projects/{project_id}/dicom-uploads", **kwargs)
        return PaginatedResponse[UploadEntity](**page)

    def get_one(self, upload_uri: str) -> UploadEntity:
        """
        Get a single upload entry based on the upload uri

        :param upload_uri: the uri of the upload
        :return: A single patient or 404
        """
        resp = self._api.get(upload_uri)
        return UploadEntity(**resp)

    def get_uploaded_files(self, upload_folder_uri: str, **kwargs) -> UploadEntityFiles:
        """
        List all files that have been uploaded to a UploadEntry
        Once the upload has been completed, and imported the files will be removed

        For name conflict avoidance; the original file name will be prepended with a UUID and sanitized:
        Only ASCII alphanumerals, ``'.'``, ``'-'`` and ``'_'`` are allowed for
        maximum portability and safety wrt using this name as a filename on a
        regular file system. All other characters will be replaced with an
        underscore (``'_'``).

        The `filename` is normalized to the Unicode ``NKFD`` form prior to
        ASCII conversion in order to extract more alphanumerals where a
        decomposition is available. For instance:

        'Bold Digit 𝟏'  => 'Bold_Digit_1'
        'Ångström unit physics.pdf' => 'A_ngstro_m_unit_physics.pdf'

        :param upload_folder_uri: the folder uri of the upload (UploadEntry.folder_uri)
        :return: An object containing all file names (If the upload has been imported, the file list will be empty)
        """
        resp = self._api.get(f"{upload_folder_uri}/files", **kwargs)
        return UploadEntityFiles(**resp)

    def upload_dicom_dir(self, project_id: str, dicom_dir_path: str, options: StartUploadDto) -> UploadEntity:
        """
        A higher level function to upload all DICOMs of a directory AND all of its subdirectories

        :param project_id: The ID of the project you want to upload to
        :param dicom_dir_path: The path to the directory
        :param options: Extra upload options
        :return:
        """
        upload = self.start_upload(project_id, options)

        # Loop over all files in a DIR and upload them to the before created upload entry
        for path, subdirs, files in os.walk(dicom_dir_path):
            for name in files:
                if name.startswith("."):
                    continue
                self.upload_dicom_path(upload.uri, os.path.join(path, name))

        # Once all files have been uploaded, signal that they are all there and start the import/processing
        return self.complete_upload(upload.uri)

    def start_upload(self, project_id: str, start_upload: StartUploadDto, **kwargs) -> UploadEntity:
        """
        A function to create an upload entry, that can be used to upload a block of data

        :param project_id: The ID of the project you want to upload to
        :param start_upload: Extra upload options
        :return:
        """
        body = start_upload.model_dump()
        resp = self._api.post(f"/uploads-service/api/v1/projects/{project_id}/multi-upload", data=body, **kwargs)
        return UploadEntity(**resp)

    def upload_dicom_path(self, upload_uri: str, file_path: str):
        """
        Upload a file to an upload entry

        :param upload_uri: Uri to upload to (UploadEntity.uri)
        :param file_path: The path to the file
        :return:
        """
        with open(file_path, "rb") as fp:
            self.upload_dicom(upload_uri, fields={"file": (file_path, fp.read(), "application/octet-stream")})

    def upload_dicom(self, upload_uri: str, fields):
        """
        Upload files to an upload entry, these can be DICOMs or zips

        :param upload_uri: A uri to upload to
        :param fields: Dictionary of fields or list of (key, :class:`~urllib3.fields.RequestField`).
        :return:
        """
        self._api.put_file(upload_uri, fields=fields)

    def complete_upload(self, upload_uri: str) -> UploadEntity:
        """
        A function to complete an upload entry, and start the importing the files

        :param upload_uri: A uri to upload to
        :return:
        """
        resp = self._api.post(upload_uri, data={})
        return UploadEntity(**resp)
