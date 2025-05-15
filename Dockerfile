FROM public.ecr.aws/lambda/python:3.10

RUN yum -y install ffmpeg

COPY app /var/task

WORKDIR /var/task

RUN pip install -r requirements.txt

CMD ["lambda_main.handler"]