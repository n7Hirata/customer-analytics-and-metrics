from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session


from app.core import get_db
from app.repositories import ClientRepository
from app.schemas import CreateClient, UpdateClient, ResponseClient
from app.services import ClientService


client_router = APIRouter(
    prefix="/clients",
    tags=["Client"]
)

def get_service(db: Session=Depends(get_db)) -> ClientService:
    '''
        Inicia sessão no banco de dados, 
        cria o repositorio concreto com a sessão
        e cria o service e injeta o repository nele.
    '''

    repository = ClientRepository(db)
    return ClientService(repository)

@client_router.post("", response_model=ResponseClient)
def create_client(client_data: CreateClient, service: ClientService = Depends(get_service)):
    return service.create_client(client_data)

@client_router.get("", response_model=list[ResponseClient])
def list_clients(service: ClientService = Depends(get_service)):
    return service.list_clients()

@client_router.get("/{id}", response_model=ResponseClient)
def get_client_by_id(id: int, service: ClientService = Depends(get_service)):
    return service.get_client_by_id(id)

@client_router.get("/email/{email}", response_model=ResponseClient)
def get_client_by_email(email: str, service: ClientService = Depends(get_service)):
    return service.get_client_by_email(email)

@client_router.patch("/{id}", response_model=ResponseClient)
def update_client(client_data: UpdateClient, id: int, service: ClientService = Depends(get_service)):
    return service.update_client(client_data, id)

@client_router.delete("/{id}")
def delete_client(id: int, service: ClientService = Depends(get_service)):
    return service.delete_client(id)