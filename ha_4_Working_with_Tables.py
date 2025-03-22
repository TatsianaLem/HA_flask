from sqlalchemy import (
    create_engine,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Numeric,
    Identity,
    func
)
from sqlalchemy.orm import sessionmaker, relationship, Mapped, mapped_column, declarative_base
#from sqlalchemy.ext.declarative import declarative_base

from datetime import datetime


Base = declarative_base()
engine = create_engine('sqlite:///:memory:')


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(
        Integer,
        Identity(always=True),
        primary_key=True,
        autoincrement=True
    )
    name: Mapped[str] = mapped_column(String(25))
    age: Mapped[int] = mapped_column(Integer)

    orders: Mapped['Order'] = relationship("Order", back_populates="user")


class Order(Base):
    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(
        Integer,
        Identity(always=True),
        primary_key=True,
        autoincrement=True
    )
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
    amount: Mapped[float] = mapped_column(Numeric(6, 2))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    user: Mapped['User'] = relationship("User", back_populates="orders")


class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(
        Integer,
        Identity(always=True),
        primary_key=True,
        autoincrement=True
    )
    name: Mapped[str] = mapped_column(String(50), unique=True)
    description: Mapped[str] = mapped_column(String(255))

    products: Mapped[list['Product']] = relationship("Product", back_populates="category")


class Product(Base):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(
        Integer,
        Identity(always=True),
        primary_key=True,
        autoincrement=True
    )
    name: Mapped[str] = mapped_column(String(50))
    price: Mapped[float] = mapped_column(Numeric(10, 2))
    in_stock: Mapped[bool] = mapped_column(Integer)  # Используем Integer для хранения True/False
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey('categories.id'))

    category: Mapped['Category'] = relationship("Category", back_populates="products")


Base.metadata.create_all(engine)


Session = sessionmaker(bind=engine)
session = Session()

# Задание 1: Наполнение данными. Добавьте в базу данных категории и продукты.
categories = [
    Category(name="Электроника", description="Гаджеты и устройства."),
    Category(name="Книги", description="Печатные книги и электронные книги."),
    Category(name="Одежда", description="Одежда для мужчин и женщин.")
]

session.add_all(categories)
session.commit()

# Получение id категорий для добавления продуктов
electronics_id = session.query(Category).filter_by(name="Электроника").first().id
books_id = session.query(Category).filter_by(name="Книги").first().id
clothing_id = session.query(Category).filter_by(name="Одежда").first().id

# Добавление продуктов
products = [
    Product(name="Смартфон", price=299.99, in_stock=True, category_id=electronics_id),
    Product(name="Ноутбук", price=499.99, in_stock=True, category_id=electronics_id),
    Product(name="Научно-фантастический роман", price=15.99, in_stock=True, category_id=books_id),
    Product(name="Джинсы", price=40.50, in_stock=True, category_id=clothing_id),
    Product(name="Футболка", price=20.00, in_stock=True, category_id=clothing_id)
]

session.add_all(products)
session.commit()


# Задание 2: Чтение данных.  Для каждой категории извлеките и выведите все связанные с ней продукты, включая их названия и цены.
# with Session() as session:
#     categories = session.query(Category).all()
#
#     for category in categories:
#         print(f"Категория: {category.name} - {category.description}")
#         for product in category.products:
#             print(f"  Продукт: {product.name}, Цена: {product.price}")

# Задание 3: Обновление данных. Найдите в таблице products первый продукт с названием "Смартфон". Замените цену этого продукта на 349.99.
# with Session() as session:
#     smartphone = session.query(Product).filter_by(name="Смартфон").first()
#     if smartphone:
#         smartphone.price = 349.99
#         session.commit()
#         print(f"Цена продукта '{smartphone.name}' обновлена на {smartphone.price}.")
#     else:
#         print("Продукт 'Смартфон' не найден.")
#
#
# # Задание 4: Агрегация и группировка. Подсчитайте общее количество продуктов в каждой категории.
# with Session() as session:
#     category_product_counts = (
#         session.query(Category.name, func.count(Product.id))
#         .join(Product, Category.id == Product.category_id, isouter=True)
#         .group_by(Category.id)
#         .all()
#     )
#
#     # Вывод результатов
#     for category_name, product_count in category_product_counts:
#         print(f"Категория: {category_name}, Общее количество продуктов: {product_count}")

# Задание 5: Группировка с фильтрацией. Отфильтруйте и выведите только те категории, в которых более одного продукта.
# with Session() as session:
#     categories_with_multiple_products = (
#         session.query(Category.name, func.count(Product.id))
#         .join(Product, Category.id == Product.category_id, isouter=True)
#         .group_by(Category.id)
#         .having(func.count(Product.id) > 1)
#         .all()
#     )
#
#     # Вывод результатов
#     for category_name, product_count in categories_with_multiple_products:
#         print(f"Категория: {category_name}, Общее количество продуктов: {product_count}")

session.close()