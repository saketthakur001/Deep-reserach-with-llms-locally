# base like image with python installed
FROM  python:3.13-slim

# Set working directory inside the container.
WORKDIR /app

#current dir content into the app
COPY . /app

# Install system dependencies 


# Install system dependencies (for some libraries, like 'playwright' and 'newspaper4k', you may need these)
RUN apt-get update && apt-get install -y \
    build-essential \
    libffi-dev \
    libssl-dev \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    wget \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies (this will install the libraries you've mentioned)
RUN pip install --no-cache-dir \
    google-genai \
    google-api-python-client \
    keyring \
    requests \
    transformers \
    llama-cpp-python \
    torch \
    sentencepiece \
    playwright \
    newspaper4k \
    trafilatura \
    accelerate \
    bitsandbytes \
    indic-nlp-library \
    langchain \
    langchain-google-genai

# Expose port (if your application needs a web server or API running inside the container)
EXPOSE 5000

# Define environment variable (Optional: Set this to avoid a warning from Python)
ENV PYTHONUNBUFFERED 1

# Command to run your application, e.g., a Python script (replace 'your_script.py' with the actual script name)
CMD ["python", "your_script.py"]

