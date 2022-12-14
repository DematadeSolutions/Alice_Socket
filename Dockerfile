FROM python:3.10.6
WORKDIR /work
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip3 install -r requirements.txt
COPY . .
CMD ["python3", "main.py"]
