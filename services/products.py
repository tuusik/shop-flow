from uuid import UUID
from typing import List
from sqlalchemy.orm import Session
from repositories.products import ProductRepository
from schemas.products import SProduct, SProductBase, SProductPatch


class ProductService:
    def __init__(self, session: Session):
        self.repo = ProductRepository(session)

    def get_products_list(self) -> List[SProduct]:
        return [SProduct.model_validate(p) for p in self.repo.get_products_list()]

    def get_product(self, id: UUID) -> SProduct | None:
        product = self.repo.get(id)
        if not product:
            return None
        return SProduct.model_validate(product)

    def create_product(self, data: SProductBase) -> SProduct:
        if data.stock < 0:
            raise ValueError("Stock cannot be negative")
        return SProduct.model_validate(self.repo.create(data))

    def update_product(self, id: UUID, data: SProductBase) -> SProduct | None:
        if data.stock < 0:
            raise ValueError("Stock cannot be negative")
        product = self.repo.update(id, data.model_dump())
        if not product:
            return None
        return SProduct.model_validate(product)

    def patch_product(self, id: UUID, data: SProductPatch) -> SProduct | None:
        if data.stock is not None and data.stock < 0:
            raise ValueError("Stock cannot be negative")
        product = self.repo.update(id, data.model_dump(exclude_none=True))
        if not product:
            return None
        return SProduct.model_validate(product)

    def delete_product(self, id: UUID) -> bool:
        return self.repo.delete(id)
