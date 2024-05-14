FROM python:3.10.6

LABEL author="Rachel Duffin" \
    maintainer="rachel.duffin2@nhs.net"

RUN git clone https://github.com/moka-guys/oncodeep_upload && cd oncodeep_upload && git checkout v1.0.0
RUN pip3 install -r /oncodeep_upload/requirements.txt
WORKDIR /oncodeep_upload/
ENTRYPOINT [ "python3","-m", "oncodeep_upload"]
