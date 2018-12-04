FROM python:3
EXPOSE 7013
ENV FLASK_DEBUG=1
ENV PORT=7013
RUN pip install flask
RUN pip install docx-mailmerge
RUN pip install boto3
RUN pip install cerberus