from fastapi import HTTPException, status


from app.repositories import BaseClientRepository
from app.schemas import CreateClient, UpdateClient


class ClientService:
    def __init__(self, repository: BaseClientRepository):
        self.repository = repository
        
    def create_client(self, client_data: CreateClient):
        client = self.repository.get_by_email(client_data.email)
        if client:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT)
        return self.repository.create(client_data)
    
    def list_clients(self):
        return self.repository.get_all()
    
    def get_client_by_id(self, id: int):
        client = self.repository.get_by_id(id)
        if not client:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return client
    
    def get_client_by_email(self, email: str):
        client = self.repository.get_by_email(email)
        if not client:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return client
    
    def update_client(self, client_id: int, client_data: UpdateClient):
        client = self.get_client_by_id(client_id)
        if client_data.email is not None and client_data.email != client.email:
            exist = self.repository.get_by_email(client_data.email)
            if exist:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT)
        return self.repository.update(client_data, client)
    
    def delete_client(self, client_id: int):
        client = self.get_client_by_id(client_id)
        self.repository.delete(client)
        return {"detail": "Cliente deletado"}