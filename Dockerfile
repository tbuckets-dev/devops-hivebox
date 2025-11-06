FROM python:3.11-slim
ADD hivebox.py .
CMD ["python", "./hivebox.py"]
