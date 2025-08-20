FROM apache/airflow:airflow:3.0.4

# Copy your wheel into the image
COPY dist/coin_pipeline-0.1.0-py3-none-any.whl /wheels/

# Install it
RUN pip install /wheels/coin_pipeline-0.1.0-py3-none-any.whl