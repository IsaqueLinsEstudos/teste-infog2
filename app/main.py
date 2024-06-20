from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from . import action, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI")

# Dependência
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoints para Clientes
@app.post("/clients", response_model=schemas.Client)
def criar_cliente(client: schemas.ClientCreate, db: Session = Depends(get_db)):
    db_cliente = action.get_client_by_email(db, email=client.email)
    if db_cliente:
        raise HTTPException(status_code=400, detail="Email já registrado")
    return action.create_client(db=db, client=client)

@app.put("/clients/{cliente_id}", response_model=schemas.Client)
def editar_cliente(client_id: int, client: schemas.ClientUpdate, db: Session = Depends(get_db)):
    return action.edit_client(db=db, id=client_id, client=client)

@app.get("/clients/{cliente_id}", response_model=schemas.Client)
def ler_cliente(client_id: int, db: Session = Depends(get_db)):
    cliente = action.get_client_by_id(db, client_id)
    if cliente is None:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return cliente

@app.delete("/clients/{cliente_id}", response_model=schemas.Client)
def deletar_cliente(client_id: int, db: Session = Depends(get_db)):
    cliente = action.delete_client(db=db, client_id=client_id)
    if cliente is None:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return cliente

@app.get("/clients", response_model=list[schemas.Client])
def listar_clientes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    clientes = action.get_clients(db=db, skip=skip, limit=limit)
    return clientes

# Endpoints para Produtos
@app.post("/products", response_model=schemas.Product)
def criar_produto(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    return action.create_product(db=db, product=product)

@app.get("/products", response_model=list[schemas.Product])
def listar_produtos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    produtos = action.get_products(db=db, skip=skip, limit=limit)
    return produtos

@app.get("/products/{produto_id}", response_model=schemas.Product)
def ler_produto(product_id: int, db: Session = Depends(get_db)):
    produto = action.get_product_by_id(db=db, product_id=product_id)
    if produto is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return produto

@app.put("/products/{produto_id}", response_model=schemas.Product)
def atualizar_produto(product_id: int, product: schemas.ProductUpdate, db: Session = Depends(get_db)):
    db_produto = action.update_product(db=db, product_id=product_id, product=product)
    if db_produto is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return db_produto

@app.delete("/products/{produto_id}", response_model=schemas.Product)
def deletar_produto(product_id: int, db: Session = Depends(get_db)):
    produto = action.delete_product(db=db, product_id=product_id)
    if produto is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return produto

# Endpoints para Pedidos
@app.post("/orders", response_model=schemas.Order)
def criar_pedido(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    return action.create_order(db=db, order=order)

@app.get("/orders/{pedido_id}", response_model=schemas.Order)
def ler_pedido(order_id: int, db: Session = Depends(get_db)):
    pedido = action.get_order_by_id(db=db, order_id=order_id)
    if pedido is None:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    return pedido

@app.put("/orders/{pedido_id}", response_model=schemas.Order)
def atualizar_pedido(order_id: int, order: schemas.OrderUpdate, db: Session = Depends(get_db)):
    db_pedido = action.update_order(db=db, order_id=order_id, order=order)
    if db_pedido is None:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    return db_pedido

@app.delete("/orders/{pedido_id}", response_model=schemas.Order)
def deletar_pedido(order_id: int, db: Session = Depends(get_db)):
    pedido = action.delete_order(db=db, order_id=order_id)
    if pedido is None:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    return pedido


# Endpoints para Autenticação

@app.post("/auth/register", response_model=schemas.User)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = action.get_user(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return action.create_user(db=db, user=user)

@app.post("/auth/login", response_model=schemas.Token)
def login_for_access_token(
    form_data: schemas.UserCreate, db: Session = Depends(get_db)):
    user = action.authenticate_user_and_create_token(
        db, form_data.username, form_data.password
    )
    return user
