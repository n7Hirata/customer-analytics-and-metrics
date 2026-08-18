from app.repositories.base_repository import BaseClientRepository, BaseTicketRepository
from app.models.clients_model import ClientModel
from app.models.tickets_model import TicketModel
from app.schemas.client_schema import CreateClient, UpdateClient
from app.schemas.ticket_schema import CreateTicket, UpdateTicket

class FakeClientRepository(BaseClientRepository):
    def __init__(self):
        self.clients: list[ClientModel] = []
        self.next_id: int = 1
        
    def create(self, client_data: CreateClient) -> ClientModel:
        client = ClientModel(id=self.next_id, name=client_data.name, email=client_data.email)
        self.clients.append(client)
        self.next_id += 1
        return client
    
    def get_all(self) -> list:
        return self.clients
    
    def get_by_email(self, email):
        for client in self.clients:
            if client.email == email:
                return client
        return None
                
    def get_by_id(self, id):
        for client in self.clients:
            if client.id == id:
                return client
        return None
            
    def update(self, client_data: UpdateClient, client: ClientModel) -> ClientModel:
        if client_data.email is not None:
            client.email = client_data.email
        if client_data.name is not None:
            client.name = client_data.name
        return client
    
    def delete(self, client):
        self.clients.remove(client)

class FakeTicketRepository(BaseTicketRepository):
    def __init__(self):
        self.tickets: list[dict] = []
        self.next_id: int = 1
        
    def create(self, ticket_data: CreateTicket) -> TicketModel:
        ticket = TicketModel(ticket_id=ticket_data.ticket_id, client_id=ticket_data.client_id,
                             subject=ticket_data.subject, status=ticket_data.status,
                             priority=ticket_data.priority, tags=ticket_data.tags)
        self.tickets.append(ticket)
        return ticket
        
    def get_all(self) -> list:
        return self.tickets 
    
    def get_by_id(self, id: int):
        for ticket in self.tickets:
            if ticket.ticket_id == id:
                return ticket
        return None
    
    def get_by_client_id(self, client_id: int):
        for ticket in self.tickets:
            if ticket.client_id == client_id:
                return ticket
        return None
    
    def update(self, ticket_data: UpdateTicket, ticket: TicketModel) -> TicketModel:
        if ticket_data.subject is not None:
            ticket.subject = ticket_data.subject
        if ticket_data.status is not None:
            ticket.status = ticket_data.status
        if ticket_data.priority is not None:
            ticket.priority = ticket_data.priority
        if ticket_data.tags is not None:
            ticket.tags = ticket_data.tags
        return ticket
            
    def delete(self, ticket: TicketModel) -> None:
        self.tickets.remove(ticket)