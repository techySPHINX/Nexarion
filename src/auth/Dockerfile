FROM python:3.9

# Install PostgreSQL development package required by psycopg2
RUN apt-get update && \
    apt-get install -y libpq-dev --no-install-recommends --no-install-suggests && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY ./requirements.txt /app
RUN pip install --no-cache-dir --requirement /app/requirements.txt

# Copy the rest of the application code
COPY . /app
