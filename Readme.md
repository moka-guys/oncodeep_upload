# Qiagen Upload

This repository contains the scripts required for use in uploading TSO500 samples to the OncoKDM for analysis via the SFTP server. The repository has a logger script which provides logging functionality. It contains a [Dockerfile](Dockerfile) and a [Makefile](Makefile) for use in building a dockerised version and pushing this dockerised version to Docker Hub. It also contains an [XML template](templates/sample_upload_template.xml) which is used to create the XML metadata file used for each sample upload.


### [oncodeep_upload](oncodeep_upload)

This module contains the [oncodeep_upload script](oncodeep_upload/oncodeep_upload.py), which is run to upload the fastqs onto the oncodeep SFTP server.

#### Requirements

Python packages are specified in the requirements.txt file. Further dependencies are:
* sshpass : ```sudo apt install sshpass```
* docker

#### Usage

##### Inputs

The inputs are as follows:
```bash
usage: Upload a file to the OncoDEEP SFTP server

Upload a file to the OncoDEEP SFTP server

options:
  -h, --help            show this help message and exit
  -R RUN_IDENTIFIER, --run_identifier RUN_IDENTIFIER
                        Run identifier for the run
  -F FILE_PATH, --file_path FILE_PATH
                        Path of file to upload
  -H HOSTNAME, --hostname HOSTNAME
                        Hostname for the OncoDEEP SFTP server
  -U USERNAME, --username USERNAME
                        Username for the OncoDEEP SFTP server
  -P PASSWORD, --password PASSWORD
                        Password for the OncoDEEP SFTP server
```

##### Outputs

The script has 4 output files:
* Logfile - ```outputs/get_user_code_YYYYMMDD_HHMMSS.log``` - Contains log messages documenting script logic
* Code verifier file - ```outputs/qiagen_code_verifier_YYYYMMDD_HHMMSS``` - Contains the code_verifier generated by the script. A high-entropy cryptographic random string
* Device code file - ```outputs/qiagen_device_code_YYYYMMDD_HHMMSS``` - Contains the device_code generated by the script. This code authorises the device.
* User code file - ```outputs/qiagen_user_code_YYYYMMDD_HHMMSS``` - Contains the user code generated by the script. This can be used to register the device in QiaOAuth


##### Script

The script can be run as follows:
```bash
python3 -m oncodeep_upload -R $RUN_IDENTIFIER -F $SRC_FILEPATH -H $HOSTNAME -U $USERNAME -P $PASSWORD
```

##### Docker Image

The docker image is built, tagged and saved as a .tar.gz file using the [Makefile](Makefile) as follows:

```bash
sudo make build
```

The docker image can be pushed to Docker Hub as follows:
```bash
sudo make push
```

The current and all previous versions of the tool are stored as dockerised versions in 001_ToolsReferenceData project as .tar.gz files. They are also stored in the seglh Docker Hub.

The docker image can be run as follows:

```bash
docker run --rm -v $FILE_PATH:/oncodeep_upload/$FILE_NAME -v $OUTPUT_DIR:/oncodeep_upload/outputs/ seglh/oncodeep_upload:$VERSION -R $RUN_IDENTIFIER -F $FILE_PATH -H $HOSTNAME -U $USERNAME -P $PASSWORD
```

### Developed by the Synnovis Genome Informatics Team
