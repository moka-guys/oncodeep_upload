#!/usr/bin/env python3
""" oncodeep_upload.py

This script uploads an input file to a specified destination folder on an SFTP server with specified
hostname, username and password, using paramiko
"""

import sys
import os
import paramiko
import logging


class OncoDeepUpload:
    """
    Class to upload files to the OncoDEEP server.

    Attributes
        file_path (str):                    File path of file to upload
        run_identifier (str):               Name of the run, to be used to create SFTP server subdir
        subfolder (str):                    Subfolder on SFTP server to load file into
        sftp_destination (str):             File path to destination on SFTP server
        logger (logging.Logger):            Logger object
        hostname (str):                     SFTP server login hostname
        username (str):                     SFTP server login username
        password (str):                     SFTP server login password
        ssh_client
        (paramiko.client.SSHClient):        SSH client object for use in file upload
        sftp_client
        (paramiko.sftp_client.SFTPClient):  SFTP client object for use in file upload

    Methods
        create_ssh_client()
            Create SFTP client object for use in file upload
        create_sftp_client()
            Create the SFTP client object for use in file upload
        upload_file()
            Upload file from local file path to remote server location
        close_connection()
            Close the SFTP and SSH connection
    """

    def __init__(
        self,
        file_path: str,
        run_identifier: str,
        hostname: str,
        username: str,
        password: str,
        logger: logging.Logger,
    ):
        """
        Constructor for the OncoDeepUpload class
            :param file_path (str):         File path of file to upload
            :param run_identifier (str):    Name of the run, to be used to create SFTP server subdir
            :param hostname (str):          SFTP server hostname
            :param username (str):          SFTP server login username
            :param password (str):          SFTP server login password
            :param logger (logging.Logger): Logger object
        """
        self.file_path = file_path
        self.run_identifier = run_identifier
        self.subfolder = f"/data/{self.run_identifier}/"
        self.sftp_destination = os.path.join(
            self.subfolder, os.path.basename(file_path)
        )
        self.logger = logger
        # Remote server credentials
        self.hostname = hostname
        self.username = username
        self.password = password
        self.ssh_client = self.create_ssh_client()
        self.sftp_client = self.create_sftp_client()

    def create_ssh_client(self) -> paramiko.client.SSHClient:
        """
        Create SFTP client object for use in file upload
            :return ssh_client
            (paramiko.client.SSHClient):    SSH client object for use in file upload
        """
        try:
            self.logger.info(f"Creating ssh client")
            ssh_client = paramiko.SSHClient()  # Create ssh client
            self.logger.info(f"Successfully created ssh client")
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.logger.info(f"Connecting to ssh client")
            ssh_client.connect(
                hostname=self.hostname, username=self.username, password=self.password
            )
            self.logger.info(f"Successfully connected to ssh client")
            return ssh_client
        except Exception as exception:
            self.logger.error(
                f"An exception was encountered when creating the ssh client: {exception}"
            )
            sys.exit(1)

    def create_sftp_client(self) -> paramiko.sftp_client.SFTPClient:
        """
        Create the SFTP client object for use in file upload
            :return
            (paramiko.sftp_client.SFTPClient):  SFTP client object for use in file upload
        """
        try:
            self.logger.info(f"Creating SFTP client object")
            return self.ssh_client.open_sftp()
        except Exception as exception:
            self.logger.error(
                f"An exception was encountered when creating the SFTP client object: {exception}"
            )
            sys.exit(1)

    def upload_file(self) -> None:
        """
        Upload file from local file path to remote server location
            :return None:
        """
        try:
            self.logger.info(
                f"Uploading file to SFTP server subfolder. Src: {self.file_path} Dest: {self.sftp_destination}"
            )
            self.sftp_client.put(self.file_path, self.sftp_destination)
            self.logger.info("File upload successful")
        except Exception as exception:
            self.logger.error(
                f"An exception was encountered when uploading the file to the SFTP server: {exception}"
            )
            sys.exit(1)

    def close_connection(self) -> None:
        """
        Close the SFTP and SSH connection
            :return None:
        """
        self.sftp_client.close()
        self.ssh_client.close()
