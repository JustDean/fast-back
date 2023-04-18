from sqlalchemy import Column, Integer, String, SmallInteger, ForeignKey

from web.postgres import Base


__all__ = [
    "Product",
    "Tag",
    "ProductTag",
]


class Product(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True)
    title = Column(String(64), nullable=False)
    amount = Column(SmallInteger, nullable=False)

    def to_dict(self) -> dict:
        return {"id": self.id, "title": self.title, "amount": self.amount}


class Tag(Base):
    __tablename__ = "tag"

    id = Column(Integer, primary_key=True)
    title = Column(String(64), nullable=False, unique=True)


class ProductTag(Base):
    __tablename__ = "product_tag"

    id = Column(Integer, primary_key=True)
    product = Column(ForeignKey("product.id"))
    tag = Column(ForeignKey("tag.id"))
