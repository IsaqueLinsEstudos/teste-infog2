from pydantic import BaseModel
from typing import List, Optional

# Esquemas de Clientes
class ClientBase(BaseModel):
    email: str
    name: str
    cpf: str

# Esquema para criar um Cliente
class ClientCreate(ClientBase):
    pass

# Esquema para atualizar um Cliente
class ClientUpdate(ClientBase):
    id: int

# Esquema para retornar um Cliente
class Client(ClientBase):
    id: int

    class Config:
        orm_mode = True

# Esquemas de Produtos
class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    category: str
    price: str
    availability: bool = True  
    stock: int

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    pass

class Product(ProductBase):
    id: int

    class Config:
        orm_mode = True

# Esquemas de Pedidos
class OrderItem(BaseModel):
    product_id: int
    quantity: int

class OrderCreate(BaseModel):
    products_section: str
    status: str
    order_items: List[OrderItem]
    client_id: int

class OrderUpdate(BaseModel):
    status: Optional[str]

class Order(OrderCreate):
    id: int

    class Config:
        orm_mode = True

# Esquema de Autenticação


class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    username: str

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str = None
