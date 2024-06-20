def test_create_client(test_app_client, db):
    # Dados de exemplo para criação de cliente
    client_data = {
        "name": "Test Client",
        "email": "test@example.com",
        "cpf": "07385917289"
    }

    # Chama o endpoint de criação de cliente
    response = test_app_client.post("/clients", json=client_data)

    # Verifica se o status da resposta é 200 OK
    assert response.status_code == 200

    # Verifica se a resposta contém 'id', 'name' e 'email'
    assert "id" in response.json()
    assert response.json()["name"] == client_data["name"]

    # Verifica se o cliente foi realmente adicionado ao banco de dados
    from app import action
    created_client = action.get_client_by_email(db, email=client_data["email"])
    assert created_client is not None
    assert created_client.name == client_data["name"]

# Implemente testes semelhantes para os outros endpoints de clientes (editar, deletar, listar, ler)
