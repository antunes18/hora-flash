import pytest
from unittest.mock import MagicMock, patch
from datetime import date, datetime, timedelta
from sqlalchemy import extract

from api.repository.scheduling_repository import SchedulingReposistory
from api.models.scheduling import Scheduling as SchedulingModel

# Mock da sessão do SQLAlchemy para não interagir com o banco
@pytest.fixture
def mock_db_session():
    session = MagicMock()
    # Mock para o query e seus encadeamentos (filter, first, all, etc.)
    session.query.return_value.filter.return_value.first.return_value = None
    session.query.return_value.filter.return_value.all.return_value = []
    session.query.return_value.offset.return_value.limit.return_value.all.return_value = []
    return session

@pytest.fixture
def scheduling_repository(mock_db_session):
    return SchedulingReposistory(session=mock_db_session)

def test_find_scheduling_by_date_and_hour_found(scheduling_repository, mock_db_session):
    target_date = date.today() + timedelta(days=1)
    target_hour = 10

    expected_scheduling = SchedulingModel(
        id=1,
        date=datetime.combine(target_date, datetime.min.time()).replace(hour=target_hour),
        hour=target_hour,
        name="Test",
        phone="123",
        user_id=1
    )

    # Configurar o mock para retornar o agendamento esperado
    # A consulta exata pode ser complexa de mockar diretamente com filter().first()
    # Uma abordagem mais simples para este template é mockar o resultado final de first()
    # ao qual a query filtrada resolveria.

    # Criamos um mock para o objeto query
    mock_query = MagicMock()
    mock_db_session.query.return_value = mock_query

    # Mockamos o encadeamento de filter().first()
    mock_query.filter.return_value.first.return_value = expected_scheduling

    result = scheduling_repository.find_scheduling_by_date_and_hour(target_date, target_hour)

    # Verifique se o session.query foi chamado com SchedulingModel
    mock_db_session.query.assert_called_with(SchedulingModel)

    # Verificar se o filtro foi chamado (aqui é mais complexo verificar os argumentos exatos do filtro sem mais detalhes)
    # No mínimo, podemos verificar se filter foi chamado.
    mock_query.filter.assert_called()

    assert result == expected_scheduling

def test_find_scheduling_by_date_and_hour_not_found(scheduling_repository, mock_db_session):
    target_date = date.today() + timedelta(days=1)
    target_hour = 11

    mock_query = MagicMock()
    mock_db_session.query.return_value = mock_query
    mock_query.filter.return_value.first.return_value = None # Simula não encontrar

    result = scheduling_repository.find_scheduling_by_date_and_hour(target_date, target_hour)

    assert result is None

# Adicione mais testes para create, find_all, find_one_scheduling, delete_scheduling,
# restore_scheduling, update_scheduling no repositório.
# Lembre-se que para create, commit, refresh, add devem ser mockados na sessão.
# Exemplo para create:
# def test_create_scheduling_repo(scheduling_repository, mock_db_session):
#     scheduling_data = SchedulingModel(date=datetime.now(), hour=10, name="Test", phone="123", user_id=1)
#
#     # O método create deve retornar o objeto scheduling após adicioná-lo e dar refresh
#     # Podemos fazer o mock de refresh para simplesmente retornar o objeto
#     mock_db_session.refresh = lambda obj: obj
#
#     result = scheduling_repository.create(scheduling_data)
#
#     mock_db_session.add.assert_called_once_with(scheduling_data)
#     mock_db_session.commit.assert_called_once()
#     # mock_db_session.refresh.assert_called_once_with(scheduling_data) # Comentado pois o lambda acima é mais simples para o template
#     assert result == scheduling_data
