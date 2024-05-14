FROM python:3.10.6

LABEL author="Rachel Duffin" \
    maintainer="rachel.duffin2@nhs.net"

RUN git clone https://github.com/moka-guys/oncodeep_upload@main
RUN pip3 install -r /oncodeep_upload/requirements.txt
# ADD ./templates/ /qiagen_upload/templates/
WORKDIR /oncodeep_upload/
ENTRYPOINT [ "python3","-m"]