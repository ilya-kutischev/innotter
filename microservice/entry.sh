#!/bin/bash

uvicorn statistics.main:app

#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]