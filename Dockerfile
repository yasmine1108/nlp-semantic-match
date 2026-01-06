# 1. Base Image
FROM python:3.9-slim

# 2. Set Working Directory
WORKDIR /code

# 3. Copy Requirements
COPY requirements.txt .

# 4. Install Dependencies (OPTIMIZED)
# First, install CPU-only PyTorch to save ~1.5GB of space
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu

# Then install the rest (pip will see torch is already installed and skip the huge download)
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the Application Code
COPY app ./app

# 6. Command to run the app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]