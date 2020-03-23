FROM python:3.7

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

# Install production dependencies.
RUN pip install ludwig
RUN pip install flask
RUN pip install flask-cors

ENV FLASK_APP predict-international.py

CMD exec flask run -h 0.0.0.0 -p $PORT 