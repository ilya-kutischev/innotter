from botocore.exceptions import ClientError
from models import Statistics
from fastapi import APIRouter, status, HTTPException, Path, Response, Query, Depends
from typing import Optional, Any
from db import initialize_db


class RecipesRouter:
    pass