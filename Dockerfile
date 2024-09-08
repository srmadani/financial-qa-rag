# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install curl for the wait script
RUN apt-get update && apt-get install -y curl

# Make wait script executable
RUN chmod +x wait-for-elasticsearch.sh

# Make port 8501 available to the world outside this container
EXPOSE 8501

# Create a startup script
RUN echo '#!/bin/bash\n\
./wait-for-elasticsearch.sh elasticsearch\n\
python data_prep.py\n\
streamlit run app.py\n\
' > /app/start.sh && chmod +x /app/start.sh

# Run the startup script
CMD ["/app/start.sh"]