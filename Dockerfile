FROM alpine:latest

RUN apk add py3-flask curl py3-requests py3-brotli py3-pip
RUN pip install yt-dlp

COPY ytmd.py /
ENTRYPOINT []
EXPOSE 5000
HEALTHCHECK --timeout=1s --interval=3s CMD ["curl", "-s", "http://localhost:5000"]
CMD ["python", "/ytmd.py"]

