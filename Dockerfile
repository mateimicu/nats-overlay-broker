FROM python:3.7

COPY ./ /nats_overlay_broker

WORKDIR /nats_overlay_broker
RUN pip3 install -r requirements.txt
RUN pip3 install -e .
CMD ["/nats_overlay_broker/entrypoint.sh"]
