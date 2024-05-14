# Oncodeep Upload

This repository contains the [oncodeep_upload script](oncodeep_upload/oncodeep_upload.py) required for use in uploading files to the OncoKDM for analysis via the SFTP server. The repository has a logger script which provides logging functionality. It contains a [Dockerfile](Dockerfile) and a [Makefile](Makefile) for use in building a dockerised version and pushing this dockerised version to Docker Hub.

## Usage

### Requirements

Python packages are specified in the requirements.txt file. Further dependencies are:
* docker

### Inputs

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

### Outputs

The script has 1 output file:
* Logfile - ```outputs/oncodeep_upload.$FILESTEM.YYYYMMDD_HHMMSS.log``` - Contains log messages documenting script logic


### Script

The script can be run as follows:
```bash
python3 -m oncodeep_upload -R $RUN_IDENTIFIER -F $SRC_FILEPATH -H $HOSTNAME -U $USERNAME -P $PASSWORD
```

### Docker Image

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
