

def test_register_user(test_app_client, db):
    # Dados de exemplo para registro
    user_data = {
        "username": "teste",
        "password": "1234526789"
    }

    # Chama o endpoint de registro
    response = test_app_client.post("/auth/register", json=user_data)

    # Verifica se o status da resposta é 200 OK
    assert response.status_code == 200

    # Verifica se a resposta contém 'id', 'username' e 'password'
    assert "id" in response.json()
    assert response.json()["username"] == user_data["username"]

    # Verifica se o usuário foi realmente adicionado ao banco de dados
    from app import action
    created_user = action.get_user(db, username=user_data["username"])
    assert created_user is not None
    assert created_user.username == user_data["username"]
