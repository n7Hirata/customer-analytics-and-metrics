import pytest
from fastapi import HTTPException
from pydantic import ValidationError

from app.services.client_service import ClientService
from app.schemas.client_schema import CreateClient, UpdateClient
from app.services.ticket_service import TicketService
from app.schemas.ticket_schema import CreateTicket, UpdateTicket
from tests.fake_repository import FakeClientRepository


def test_create_cliente_com_dados_validos(client_service):
    
    client = client_service.create_client(CreateClient(name="Joaozinho", email="joao@gmail.com"))
    
    assert client.id == 1
    assert client.name == "Joaozinho"
    assert client.email == "joao@gmail.com"
    
def test_create_cliente_com_dados_invalidos(client_service):
    
    with pytest.raises(ValidationError) as exc_info:
        client_service.create_client(CreateClient(name=123, email=456))
    
    errors = exc_info.value.errors()

    # Verifica a quantidade total de erros retornados
    assert len(errors) == 2

def test_list_client_vazio(client_service):
    
    clients = client_service.list_clients()
    
    assert clients == []
    
def  test_get_client_pelo_id(client_service):
    
    client_service.create_client(CreateClient(name="Joaozinho", email="joao@gmail.com"))
    
    client = client_service.get_client_by_id(id=1)
    
    assert client.name == "Joaozinho"
    assert client.email == "joao@gmail.com"
    
def test_get_client_com_id_inexistente(client_service):
    
    with pytest.raises(HTTPException) as error:    
        client_service.get_client_by_id(id=123)
    
    assert error.value.status_code == 404
    
def  test_get_client_pelo_email(client_service):
    
    client_service.create_client(CreateClient(name="Joaozinho", email="joao@gmail.com"))
    
    client = client_service.get_client_by_email(email="joao@gmail.com")
    
    assert client.name == "Joaozinho"
    assert client.email == "joao@gmail.com"
    
def test_get_client_com_email_inexistente(client_service):
    
    with pytest.raises(HTTPException) as error:    
        client_service.get_client_by_email(email="maria@gmail.com")
    
    assert error.value.status_code == 404
    
def test_update_client_parcial(client_service):
    
    client_service.create_client(CreateClient(name="Joaozinho", email="joao@gmail.com"))

    updated = client_service.update_client(1, UpdateClient(name="Maria"))
    
    assert updated.name == "Maria"
    assert updated.email == "joao@gmail.com"
    
def test_update_client_completo(client_service):
    
    client_service.create_client(CreateClient(name="Joaozinho", email="joao@gmail.com"))
    updated = client_service.update_client(1, UpdateClient(name="Maria", email="maria@gmail.com"))

    assert updated.name == "Maria"
    assert updated.email == "maria@gmail.com"
    
def test_update_client_inexistente(client_service):
    
    with pytest.raises(HTTPException) as error:
        client_service.update_client(234, UpdateClient(name="Maria"))
    
    assert error.value.status_code == 404
    
def test_delete_client(client_service):
    
    client_service.create_client(CreateClient(name="Joaozinho", email="joao@gmail.com"))
    
    result = client_service.delete_client(client_id=1)

    assert result["detail"] == "Cliente deletado"
    assert client_service.list_clients() == []
    
def test_delete_client_inexistente(client_service):
    
    with pytest.raises(HTTPException) as error:
        client_service.delete_client(client_id=214)
        
    assert error.value.status_code == 404
    

# TESTE TICKET

def test_create_ticket_com_dados_validos(ticket_service, client_service):

    client = client_service.create_client(CreateClient(name="Joaozinho", email="joao@gmail.com"))

    payload = CreateTicket(
        ticket_id=1,
        client_id=client.id,
        subject="Problema com acesso",
        status="aberto",
        priority="alta",
        tags="auth, bug"
    )

    ticket = ticket_service.create_ticket(payload)

    assert ticket.ticket_id == 1
    assert ticket.client_id == client.id
    assert ticket.subject == "Problema com acesso"
    assert ticket.status == "aberto"
    assert ticket.priority == "alta"
    assert ticket.tags == "auth, bug"


def test_create_ticket_com_dados_invalidos():
    # Valida se tipos incorretos disparam ValidationError no schema
    with pytest.raises(ValidationError) as exc_info:
        CreateTicket(
            ticket_id="nao_numerico",
            client_id="nao_numerico",
            subject=123,
            status=456,
            priority=789,
            tags=["eh_uma_lista"]
        )

    errors = exc_info.value.errors()
    campos_com_erro = [err["loc"][0] for err in errors]

    assert len(errors) >= 3
    assert "client_id" in campos_com_erro
    assert "subject" in campos_com_erro


def test_create_ticket_com_cliente_inexistente(ticket_service):
    # Caso o service valide se o client_id realmente existe antes de criar
    payload = CreateTicket(
        ticket_id=1,
        client_id=999,  # ID que não existe
        subject="Dúvida financeira",
        status="aberto",
        priority="baixa",
        tags="duvida"
    )

    with pytest.raises(HTTPException) as exc_info:
        ticket_service.create_ticket(payload)

    assert exc_info.value.status_code == 404


def test_get_ticket_por_id(ticket_service, client_service):
    client = client_service.create_client(CreateClient(name="Joaozinho", email="joao@gmail.com"))
    ticket_service.create_ticket(CreateTicket(
        ticket_id=1,
        client_id=client.id,
        subject="Bug no checkout",
        status="aberto",
        priority="urgente",
        tags="checkout"
    ))

    ticket = ticket_service.get_ticket_by_id(ticket_id=1)

    assert ticket.ticket_id == 1
    assert ticket.subject == "Bug no checkout"


def test_get_ticket_inexistente(ticket_service):
    with pytest.raises(HTTPException) as exc_info:
        ticket_service.get_ticket_by_id(ticket_id=999)

    assert exc_info.value.status_code == 404


def test_list_tickets(ticket_service, client_service):
    client = client_service.create_client(CreateClient(name="Joaozinho", email="joao@gmail.com"))
    ticket_service.create_ticket(CreateTicket(
        ticket_id=1,
        client_id=client.id,
        subject="Ticket 1",
        status="aberto",
        priority="baixa",
        tags=""
    ))
    ticket_service.create_ticket(CreateTicket(
        ticket_id=2,
        client_id=client.id,
        subject="Ticket 2",
        status="em_andamento",
        priority="media",
        tags=""
    ))

    tickets = ticket_service.list_tickets()

    assert len(tickets) == 2


def test_update_ticket_status(ticket_service, client_service):
    client = client_service.create_client(CreateClient(name="Joaozinho", email="joao@gmail.com"))
    ticket_service.create_ticket(CreateTicket(
        ticket_id=1,
        client_id=client.id,
        subject="Chamado inicial",
        status="aberto",
        priority="media",
        tags=""
    ))

    updated = ticket_service.update_ticket(ticket_data=UpdateTicket(status="resolvido"), ticket_id=1)

    assert updated.status == "resolvido"

def test_update_ticket_completo(ticket_service, client_service):
    # 1. Cria os clientes necessários para o teste
    client_1 = client_service.create_client(CreateClient(name="Joao", email="joao@gmail.com"))
    client_2 = client_service.create_client(CreateClient(name="Maria", email="maria@gmail.com"))

    # 2. Cria o ticket com dados iniciais
    ticket_service.create_ticket(
        CreateTicket(
            ticket_id=1,
            client_id=client_1.id,
            subject="Erro no login",
            status="aberto",
            priority="baixa",
            tags="auth"
        )
    )

    # 3. Executa o update completo com todos os novos valores
    payload_update = UpdateTicket(
        subject="Falha crítica no pagamento",
        status="em_andamento",
        priority="urgente",
        tags="financeiro, pagamentos"
    )
    
    updated = ticket_service.update_ticket(ticket_id=1, ticket_data=payload_update)

    # 4. Asserções de todos os campos atualizados
    assert updated.subject == "Falha crítica no pagamento"
    assert updated.status == "em_andamento"
    assert updated.priority == "urgente"
    assert updated.tags == "financeiro, pagamentos"

def test_delete_ticket(ticket_service, client_service):
    client = client_service.create_client(CreateClient(name="Joaozinho", email="joao@gmail.com"))
    ticket_service.create_ticket(CreateTicket(
        ticket_id=1,
        client_id=client.id,
        subject="Para deletar",
        status="aberto",
        priority="baixa",
        tags="financeiro, pagamentos"
    ))

    result = ticket_service.delete_ticket(ticket_id=1)

    assert result["detail"] == "Ticket deletado"
    assert ticket_service.list_tickets() == []