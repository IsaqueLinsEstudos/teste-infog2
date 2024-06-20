from datetime import datetime, timezone
from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from fastapi.exceptions import HTTPException
from . import action, schemas
from typing import Optional

from . import models, schemas

#Clients

def get_clients(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Client).offset(skip).limit(limit).all()

def get_client_by_email(db: Session, email: str):
    return db.query(models.Client).filter(models.Client.email == email).first()

def get_client_by_cpf( db: Session, cpf: int):
    return db.query(models.Client).filter(models.Client.cpf == cpf).first()

def get_client_by_id( db: Session, id: int):
    return db.query(models.Client).filter(models.Client.id == id).first()

def get_client( db: Session, skip: int =0, limit: int = 100):
    return db.query(models.Client).offset(skip).limit(limit).all()


def create_client(db: Session, client: schemas.ClientCreate):
    db_client = models.Client(
        name=client.name,
        email=client.email,
        cpf= client.cpf
    )
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client

def edit_client(db: Session, id: int, client: schemas.ClientUpdate):
    db_client = db.query(models.Client).filter(models.Client.id == id).first()
    if db_client:
        update_data = client.model_dump(client, exclude_unset=True)  
        for key, value in update_data.items():
            setattr(db_client, key, value)
        db.commit()
        db.refresh(db_client)
    return db_client

def delete_client(db: Session, client_id: int):
    client = db.query(models.Client).filter(models.Client.id == client_id).first()
    if client:
        db.delete(client)
        db.commit()
    return client



# Products

def get_products(db: Session, skip: int = 0, limit: int = 100, category: str = None,
                price: str = None, availability: str = None):
    query = db.query(models.Product)
    
    if category:
        query = query.filter(models.Product.category == category)
    
    if price is not None:
        query = query.filter(models.Product.price >= price)
    
    if availability:
        query = query.filter(models.Product.availability == availability)
    
    return query.offset(skip).limit(limit).all()

def get_product_by_id(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def create_product(db: Session, product: schemas.ProductCreate):

    db_product = models.Product(
        name=product.name,
        description=product.description,
        category=product.category,
        price=product.price,
        availability=product.availability,
        stock=product.stock
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def update_product(db: Session, product_id: int, product: schemas.ProductUpdate):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if db_product:
        update_data = product.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_product, key, value)
        db.commit()
        db.refresh(db_product)
    return db_product

def delete_product(db: Session, product_id: int):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
    return db_product



#Orders



def get_orders(
    db: Session,
    period_start: Optional[str] = None,
    period_end: Optional[str] = None,
    products_section: Optional[str] = None,
    order_id: Optional[str] = None,
    status: Optional[str] = None,
    client_id: Optional[int] = None
):
    query = db.query(models.Order)

    if period_start:
        query = query.filter(models.Order.created_at >= period_start)
    if period_end:
        query = query.filter(models.Order.created_at <= period_end)
    if products_section:
        query = query.filter(models.Order.products_section == products_section)
    if order_id:
        query = query.filter(models.Order.order_id == order_id)
    if status:
        query = query.filter(models.Order.status == status)
    if client_id:
        query = query.filter(models.Order.client_id == client_id)

    return query.all()



# Função para verificar se um cliente existe pelo ID
def get_client_by_id(db: Session, client_id: int):
    return db.query(models.Client).filter(models.Client.id == client_id).first()

# Função para verificar se um produto existe pelo ID
def get_product_by_id(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()

# Função para criar um pedido
def create_order(db: Session, order: schemas.OrderCreate):
    # Verifica se o cliente existe
    client = get_client_by_id(db, order.client_id)
    if not client:
        raise HTTPException(status_code=404, detail=f"Client with id {order.client_id} not found")

    # Verifica se todos os produtos no pedido têm estoque disponível
    for order_item in order.order_items:
        product = get_product_by_id(db, order_item.product_id)
        if not product or product.stock < order_item.quantity:
            raise HTTPException(status_code=400, detail=f"Product {order_item.product_id} does not have enough stock.")

    # Cria o pedido no banco de dados
    db_order = models.Order(
        products_section=order.products_section,
        status=order.status,
        client_id=order.client_id,
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    # Cria os itens do pedido no banco de dados
    for order_item in order.order_items:
        db_order_item = models.OrderItem(
            order_id=db_order.id,
            product_id=order_item.product_id,
            quantity=order_item.quantity
        )
        db.add(db_order_item)

    db.commit()
    return db_order




def get_order_by_id(db: Session, order_id: int):
    return db.query(models.Order).filter(models.Order.id == order_id).first()


def update_order(db: Session, order_id: int, order: schemas.OrderUpdate):
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if db_order:
        db_order.status = order.status
        db.commit()
        db.refresh(db_order)
    return db_order

def delete_order(db: Session, order_id: int):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if order:
        db.delete(order)
        db.commit()
    return order


# Configuração de autenticação
SECRET_KEY = "your-secret-key"  
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Funções auxiliares de autenticação
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Funções de operação no banco de dados
def get_user(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def authenticate_user(db: Session, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(username=user.username, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Funções de autenticação
def create_access_token_for_user(username: str):
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": username}, expires_delta=access_token_expires
    )
    return access_token

def authenticate_user_and_create_token(db: Session, username: str, password: str):
    user = authenticate_user(db, username, password)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    access_token = create_access_token_for_user(user.username)
    return {"access_token": access_token, "token_type": "bearer"}