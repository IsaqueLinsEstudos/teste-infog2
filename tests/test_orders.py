

def test_create_order(test_app_client, db):
    # Dados de exemplo para criação de pedido
    order_data = {
        "products_section": "Eletrônicos",
        "status": "string",
        "order_items": [
         {
            "product_id": 1,
            "quantity": 1
         }
        ],
        "client_id": 2
    }

    # Chama o endpoint de criação de pedido
    response = test_app_client.post("/orders", json=order_data)

    # Verifica se o status da resposta é 200 OK
    assert response.status_code == 200

    # Verifica se a resposta contém 'id', 'client_id' e 'product_id'
    assert "id" in response.json()
    assert response.json()["client_id"] == order_data["client_id"]

    # Verifica se o pedido foi realmente adicionado ao banco de dados
    from app import action
    created_order = action.get_order_by_id(db, response.json()["id"])
    assert created_order is not None
    assert created_order.client_id == order_data["client_id"]


