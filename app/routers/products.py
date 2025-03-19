from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from slugify import slugify
from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.backend.db_depends import get_db
from app.models.category import Category
from app.models.products import Product
from app.routers.auth import get_current_user
from app.schemas import CreateProduct


router = APIRouter(prefix='/products', tags=['products'], dependencies=[Depends(get_current_user)])


@router.get('/')
async def get_all_products(db: Annotated[AsyncSession, Depends(get_db)]):
    products = await db.scalars(
        select(Product)
        .join(Category)
        .where(
            Product.is_active,
            Category.is_active,
        )
    )

    return products.all()


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_product(db: Annotated[AsyncSession, Depends(get_db)], create_product: CreateProduct):
    category = await db.scalar(select(Category).where(Category.id == create_product.category))
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There is no category found'
        )
    await db.execute(
        insert(Product).values(
            name=create_product.name,
            slug=slugify(create_product.name),
            description=create_product.description,
            price=create_product.price,
            image_url=create_product.image_url,
            stock=create_product.stock,
            category_id=create_product.category,
            rating=0.0,
        )
    )
    await db.commit()
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful'
    }


@router.get('/{category_slug}')
async def get_product_by_category(db: Annotated[AsyncSession, Depends(get_db)], category_slug: str):
    category = await db.scalar(select(Category).where(Category.slug == category_slug))
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Category not found'
        )
    subcategories = await db.scalars(
        select(Category)
        .where(Category.parent_id == category.id)
    )

    categories_and_subcategories = [category.id] + [subcategory.id for subcategory in subcategories]

    product_category = await db.scalars(
        select(Product)
        .where(Product.category_id.in_(categories_and_subcategories),
               Product.is_active,
               Product.stock > 0
               )
    )

    return product_category.all()


@router.get('/details/{product_slug}')
async def get_product_details(db: Annotated[AsyncSession, Depends(get_db)], product_slug: str):
    product = await db.scalar(
        select(Product).where(
            Product.slug == product_slug,
            Product.is_active,
            Product.stock > 0,
        )
    )
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There are not product'
        )
    return product


@router.put('/{product_slug}')
async def update_product(
        db: Annotated[AsyncSession, Depends(get_db)],
        product_slug: str,
        update_product: CreateProduct
):
    product = await db.scalar(select(Product).where(Product.slug == product_slug))
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There is no product found'
        )
    category = await db.scalar(select(Category).where(Category.id == update_product.category))
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There is no category found'
        )

        product.name = update_product.name
        product.description = update_product.description
        product.price = update_product.price
        product.image_url = update_product.image_url,
        product.stock = update_product.stock
        product.category_id = update_product.category
        product.slug = slugify(update_product.name)

    await db.commit()

    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Product update is successful'
    }


@router.delete('/{product_slug}')
async def delete_product(db: Annotated[Session, Depends(get_db)], product_slug: str):
    product = db.scalar(
        select(Product)
        .where(
            Product.slug == product_slug,
            Product.is_active,
        )
    )
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There is no product found'
        )
    db.execute(update(Product).where(Product.slug == product_slug).values(is_active=False))
    db.commit()

    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Product delete is successful'
    }
