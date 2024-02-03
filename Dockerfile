FROM python:3.9

WORKDIR /BettingTrendsWebsite

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "src/data_generation/data_generator.py", ";", "python", "src/playground.py"]
