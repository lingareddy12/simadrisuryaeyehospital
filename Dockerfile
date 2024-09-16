# Step 1: Use Python 3.8 as base image
FROM python:3.11-alpine3.20

# Step 2: Set the working directory in the container
WORKDIR /flask_folder

# Step 3: Copy the requirements file into the container
COPY requirements.txt .

# Step 4: Install any necessary packages specified in requirements.txt
RUN pip install  -r requirements.txt

# Step 5: Copy the rest of the application code into the container
COPY . .

# Step 6: Expose the Flask port
EXPOSE 5000

# Step 7: Run the Flask app
ENV FLASK_APP=app.py
CMD [ "python3", "-m", "flask", "run", "--host=0.0.0.0"]

