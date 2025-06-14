import pytest
from unittest.mock import MagicMock, patch
from datetime import date, datetime, timedelta

from api.services.scheduling_services import SchedulingService
from api.models.dto.scheduling_dto import Scheduling as SchedulingDTO
from api.models.scheduling import Scheduling as SchedulingModel
from api.exceptions import scheduling_exceptions, user_exceptions

@pytest.fixture
def mock_scheduling_repo():
    return MagicMock()

@pytest.fixture
def mock_user_repo():
    return MagicMock()

@pytest.fixture
def scheduling_service(mock_scheduling_repo, mock_user_repo):
    return SchedulingService(scheduling_repo=mock_scheduling_repo, user_repo=mock_user_repo)

def test_create_scheduling_success(scheduling_service, mock_scheduling_repo, mock_user_repo):
    dto = SchedulingDTO(
        date=date.today() + timedelta(days=1),
        hour=10,
        name="Test User",
        user_id=1,
        phone="1234567890"
    )
    mock_user_repo.get_user.return_value = MagicMock() # Simula usuário existente
    mock_scheduling_repo.find_scheduling_by_date_and_hour.return_value = None # Simula não haver agendamento existente

    new_scheduling_model = SchedulingModel(id=1, **dto.model_dump())
    mock_scheduling_repo.create.return_value = new_scheduling_model

    result = scheduling_service.create_scheduling(dto)

    mock_user_repo.get_user.assert_called_once_with(dto.user_id)
    mock_scheduling_repo.find_scheduling_by_date_and_hour.assert_called_once_with(dto.date, dto.hour)
    mock_scheduling_repo.create.assert_called_once()
    assert result.id == 1
    assert result.name == dto.name

def test_create_scheduling_already_exists(scheduling_service, mock_scheduling_repo, mock_user_repo):
    dto = SchedulingDTO(
        date=date.today() + timedelta(days=1),
        hour=10,
        name="Test User",
        user_id=1,
        phone="1234567890"
    )
    mock_user_repo.get_user.return_value = MagicMock()
    mock_scheduling_repo.find_scheduling_by_date_and_hour.return_value = SchedulingModel(id=1, **dto.model_dump()) # Simula agendamento existente

    with pytest.raises(scheduling_exceptions.AlreadyExist):
        scheduling_service.create_scheduling(dto)

def test_create_scheduling_user_not_found(scheduling_service, mock_user_repo):
    dto = SchedulingDTO(
        date=date.today() + timedelta(days=1),
        hour=10,
        name="Test User",
        user_id=1,
        phone="1234567890"
    )
    mock_user_repo.get_user.return_value = None # Simula usuário não encontrado

    with pytest.raises(user_exceptions.UserNotFound):
        scheduling_service.create_scheduling(dto)

def test_update_scheduling_success(scheduling_service, mock_scheduling_repo):
    scheduling_id = 1
    dto = SchedulingDTO(
        date=date.today() + timedelta(days=2), # Nova data
        hour=15, # Nova hora
        name="Updated User Test",
        user_id=1, # user_id não deve ser alterado pelo update_scheduling do serviço
        phone="0987654321"
    )

    existing_scheduling = SchedulingModel(
        id=scheduling_id,
        date=date.today() + timedelta(days=1),
        hour=10,
        name="Old User Test",
        user_id=1,
        phone="1234567890",
        is_deleted=False
    )
    mock_scheduling_repo.find_one_scheduling.return_value = existing_scheduling

    # O método update_scheduling do repo deve retornar o objeto atualizado
    # Para simplificar, vamos fazer com que ele retorne o mesmo objeto que foi modificado
    mock_scheduling_repo.update_scheduling.return_value = existing_scheduling

    result = scheduling_service.update_scheduling(scheduling_id, dto)

    mock_scheduling_repo.find_one_scheduling.assert_called_once_with(scheduling_id)
    mock_scheduling_repo.update_scheduling.assert_called_once_with(scheduling_id, existing_scheduling)

    assert result.name == dto.name
    assert result.date == dto.date
    assert result.hour == dto.hour
    assert result.phone == dto.phone
    assert existing_scheduling.name == dto.name # Verifica se o objeto original foi modificado

def test_update_scheduling_not_found(scheduling_service, mock_scheduling_repo):
    scheduling_id = 99
    dto = SchedulingDTO(
        date=date.today() + timedelta(days=1),
        hour=10,
        name="Test User",
        user_id=1,
        phone="1234567890"
    )
    mock_scheduling_repo.find_one_scheduling.return_value = None # Simula não encontrado

    with pytest.raises(scheduling_exceptions.NotFound):
        scheduling_service.update_scheduling(scheduling_id, dto)

# Adicione mais testes para get_all_schedulings, get_scheduling, delete_scheduling, restore_scheduling
