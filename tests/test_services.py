import pytest
from fastapi import HTTPException

from app.services.client_service import ClientService
from app.schemas.client_schema import CreateClient, UpdateClient
from tests.fake_repository import FakeClientRepository


