import pytest
import mongomock
import pymongo
import sys

@pytest.fixture(autouse=True)
def patch_mongo(monkeypatch):
    # Patch przed importem podmienia pymongo.MongoClient na mongomock.Mongoclient
    monkeypatch.setattr(pymongo, "MongoClient", mongomock.MongoClient)
    # Usuwanie DatabaseManager z cache sys.modules, inaczej będzie już załadowany i połączy się z prawdziwą bazą
    sys.modules.pop("database.DatabaseManager", None)
    yield


@pytest.fixture
def db(tmp_path):
    # Import po patchu
    from database.DatabaseManager import DatabaseManager
    json_path = tmp_path / "data.json"
    return DatabaseManager(
        uri="mongodb://localhost",
        db_name="testdb",
        json_path=str(json_path)
    )


def test_user_crud(db):
    from database.models import User

    # CREATE
    user = db.create_user("userTestUser", "userTestPassword")
    assert isinstance(user, User)
    assert user.username == "userTestUser"

    # READ
    fetched = db.get_user("userTestUser")
    assert isinstance(fetched, User)
    assert fetched.username == "userTestUser"
    assert fetched.password != "userTestPassword"
    assert db._check_password("userTestPassword", fetched.password)
    assert not db._check_password("wrongPassword", fetched.password)

    # UPDATE
    new_password = db._hash_password("newHashedPassword")
    fetched.password = new_password
    db.update_user("userTestUser", fetched)

    updated = db.get_user("userTestUser")
    assert updated.password == new_password
    assert db._check_password("newHashedPassword", updated.password)

    # DELETE
    db.delete_user("userTestUser")
    assert db.get_user("userTestUser") is None


def test_game_session_crud(db):
    from database.models import GameSession

    db.create_user("gsTestUser", "gsTestPassword")

    # CREATE
    session = db.create_game_session(
        username="gsTestUser",
        board_size=(10, 10),
        points=5,
        game_time="00:30",
        pause_count=2
    )
    assert isinstance(session, GameSession)
    assert session.id is not None

    # READ
    sessions = db.get_game_sessions_for_user("gsTestUser")
    assert len(sessions) == 1
    s = sessions[0]
    assert s.points == 5

    # UPDATE
    s.points = 10
    db.update_game_session(s)
    sessions2 = db.get_game_sessions_for_user("gsTestUser")
    assert sessions2[0].points == 10

    # DELETE
    db.delete_game_session(s.id)
    assert db.get_game_sessions_for_user("gsTestUser") == []


def test_export_and_load_json(db):
    from database.models import User, GameSession
    from database.DatabaseManager import DatabaseManager

    db.create_user("exportTestUSer", "exportTestPassword")
    db.create_game_session(
        username="exportTestUSer",
        board_size=20,
        points=7,
        game_time="01:00",
        pause_count=1
    )

    db.export_to_json()

    # Nowy manager, inny db_name, ale mongomock
    db2 = DatabaseManager(
        uri="mongodb://localhost",
        db_name="anotherdb",
        json_path=db.json_path
    )
    db2.load_from_json()

    # Weryfikacja
    u = db2.get_user("exportTestUSer")
    assert isinstance(u, User)
    sessions = db2.get_game_sessions_for_user("exportTestUSer")
    assert len(sessions) == 1
    assert sessions[0].points == 7
