import pytest

from app.services.client_service import ClientService
from app.services.metrics_service import MetricsServices
from app.services.ticket_service import TicketService

from tests.fake_repository import FakeClientRepository, FakeTicketRepository

@pytest.fixture
def fake_repo_client():
    return FakeClientRepository()

@pytest.fixture
def fake_repo_ticket():
    return FakeTicketRepository()

@pytest.fixture()
def client_service(fake_repo):
    return ClientService(repository=fake_repo_client)

@pytest.fixture
def ticket_service(fake_repo):
    return TicketService(ticket_repository=fake_repo_ticket)

@pytest.fixture
def metrics_serivce(fake_repo_client, fake_repo_ticket):
    pass