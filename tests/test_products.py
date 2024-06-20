

def test_create_product(test_app_client, db):
    # Dados de exemplo para criação de produto
    product_data = {
        "name": "string",
        "description": "string",
        "category": "string",
        "price": "string",
        "availability": True,
        "stock": 7
    }

    # Chama o endpoint de criação de produto
    response = test_app_client.post("/products", json=product_data)

    # Verifica se o status da resposta é 200 OK
    assert response.status_code == 200

    # Verifica se a resposta contém 'id', 'name' e 'description'
    assert "id" in response.json()
    assert response.json()["name"] == product_data["name"]

    # Verifica se o produto foi realmente adicionado ao banco de dados
    from app import action
    created_product = action.get_product_by_id(db, response.json()["id"])
    assert created_product is not None
    assert created_product.name == product_data["name"]


