FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

RUN printf '#!/bin/sh\n\
set -e\n\
echo "Running Alembic migrations..."\n\
python -m alembic upgrade head\n\
echo "Starting FastAPI..."\n\
exec python -m uvicorn main:app --host 0.0.0.0 --port $PORT\n' > /start.sh \
 && chmod +x /start.sh

CMD ["/start.sh"]