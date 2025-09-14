from fastapi import HTTPException
from fastapi import APIRouter

router = APIRouter()

products = []


@router.get('/')
async def get_products():
    return products


@router.post('/')
async def create_product(product: str):
    products.append(product)
    return {"message": "Muvoffaqiyatli qo'shildi."}


# path variable
@router.get('/{product_id}/')
async def detail_product(product_id: int):
    try:
        return products[product_id]
    except Exception as e:
        raise HTTPException(404, f"{e}")


@router.put('/{product_id}')
def update_product(product_id: int, value: str):
    try:
        product = products[product_id]
        products[product_id] = value
        return {"status": 200, "updated_product": f"Mahsulot {product} dan {value} o'zgardi."}
    except Exception as e:
        raise HTTPException(404, f"{e}")


@router.delete('/{product_id}')
def delete_product(product_id: int):
    try:
        return {"status": 204, "deleted_product": products.pop(product_id)}
    except Exception as e:
        raise HTTPException(404, f"{e}")
