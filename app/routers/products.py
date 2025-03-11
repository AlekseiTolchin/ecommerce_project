from fastapi import APIRouter

router = APIRouter(prefix='/products', tags=['products'])


@router.get('/')
async def get_all_products():
    pass


@router.post('/')
async def create_product():
    pass


@router.get('/{category_slug}')
async def get_product_by_category(category_slug: str):
    pass


@router.get('/details/{product_slug}')
async def get_product_details(product_slug: str):
    pass


@router.put('/{product_slug}')
async def update_product(product_slug: str):
    pass


@router.put('/{product_id}')
async def delete_product(product_id: int):
    pass