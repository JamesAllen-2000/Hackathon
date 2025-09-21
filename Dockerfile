FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for headless browser
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Chrome using modern approach
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/googlechrome-linux-keyring.gpg \
    && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/googlechrome-linux-keyring.gpg] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user
RUN useradd -m -u 1000 appuser && \
    mkdir -p /home/appuser/.config /home/appuser/.streamlit && \
    chown -R appuser:appuser /home/appuser

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set ownership of app directory
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Set environment variables to use user directories
ENV HOME=/home/appuser
ENV BROWSER_USE_CONFIG_DIR=/home/appuser/.config/browseruse
ENV STREAMLIT_CONFIG_DIR=/home/appuser/.streamlit

# Expose ports
EXPOSE 8000
EXPOSE 7860

# Start both services
CMD ["sh", "-c", "python api.py & streamlit run streamlit_app.py --server.port 7860 --server.address 0.0.0.0 --server.headless true"]