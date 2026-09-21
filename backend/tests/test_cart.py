from decimal import Decimal
from sqlalchemy import select

from app.schemas.cart_item_schema import CartItemResponse
from app.models.cart_item_model import CartItem
from tests.factories.base import create
from tests.factories import ProductFactory



class TestBaseCart:
    async def test_cart(self, client, cart, category, product, user, auth_headers, db_session):
        #Test add item to cart
        first_add_response = await client.post('/api/cart/add', json={'product_id': product.id, 'quantity': 3},
                                               headers=auth_headers)
        first_add_data = first_add_response.json()
        cart_item_id = first_add_data['id']

        assert first_add_response.status_code == 201
        assert isinstance(first_add_data['id'], int)
        assert first_add_data['cart_id'] == cart.id
        assert first_add_data['product_id'] == product.id
        assert first_add_data['quantity'] == 3
        assert Decimal(first_add_data['price']) == product.price * 3


        #Test add added item to cart
        second_add_response = await client.post('api/cart/add', json={'product_id': product.id, 'quantity': 2},
                                                headers=auth_headers)
        second_add_data = second_add_response.json()

        assert second_add_response.status_code == 201
        assert second_add_data['quantity'] == first_add_data['quantity'] + 2
        assert Decimal(second_add_data['price']) == Decimal(first_add_data['price']) + (product.price * 2)


        #Test update item in cart
        update_response = await client.patch(f'/api/cart/update/{cart_item_id}',
                                             json={'quantity': 4}, headers=auth_headers)
        update_data = update_response.json()

        assert update_response.status_code == 200
        assert isinstance(update_data['id'], int)
        assert update_data['cart_id'] == cart.id
        assert update_data['product_id'] == product.id
        assert update_data['quantity'] == second_add_data['quantity'] + 4
        assert Decimal(update_data['price']) == Decimal(second_add_data['price']) + (product.price*4)


        #Test decrease quantity
        decrease_response = await client.patch(f'/api/cart/update/{cart_item_id}', json={'quantity': -1},
                                               headers=auth_headers)
        decrease_data = decrease_response.json()

        assert decrease_response.status_code == 200
        assert decrease_data['quantity'] == update_data['quantity'] - 1
        assert Decimal(decrease_data['price']) == Decimal(update_data['price']) - product.price


        #Test get cart
        another_product = await create(ProductFactory, db_session, category_id=category.id)
        add_for_testing_response = await client.post('/api/cart/add', json={'product_id': another_product.id, 'quantity': 3},
                                            headers=auth_headers)
        add_for_testing_data = add_for_testing_response.json()
        assert add_for_testing_response.status_code == 201

        cart_response = await client.get('/api/cart', headers=auth_headers)
        cart_data = cart_response.json()
        
        assert cart_response.status_code == 200
        assert cart_data['user_id'] == user.id
        assert cart_data['id'] == cart.id
        assert isinstance(cart_data['items'], list)
        assert cart_data['items'] == [decrease_data, add_for_testing_data]
        assert cart_data['total_items_quantity'] == decrease_data['quantity'] + add_for_testing_data['quantity']
        assert Decimal(cart_data['total_price']) == Decimal(decrease_data['price']) + Decimal(add_for_testing_data['price'])


        #Test decrease quantity to 0(Карт айтем для тестирования в блоке Test decrease quantity)
        delete_item_response = await client.patch(f'/api/cart/update/{cart_item_id}',
                                                  json={'quantity': -decrease_data['quantity']}, headers=auth_headers)
        db_cart_item = await db_session.execute(select(CartItem).where(CartItem.id==cart_item_id))

        assert delete_item_response.status_code == 200
        assert db_cart_item.scalar_one_or_none() is None



class TestCartRemoves:
    async def test_delete_cart_item(self, client, cart_item, auth_headers, db_session):
        delete_cart_item_response = await client.delete(f'/api/cart/remove/cart-item/{cart_item.id}',
                                                        headers=auth_headers)
        db_cart_item = await db_session.execute(select(CartItem).where(CartItem.id==cart_item.id))

        assert delete_cart_item_response.status_code == 204
        assert db_cart_item.scalar_one_or_none() is None


    async def test_clear_cart(self, client, cart_items, auth_headers, db_session):
        clear_cart_response = await client.delete('/api/cart/remove/cart', headers=auth_headers)
        assert clear_cart_response.status_code == 204
        for item in cart_items:
            db_item = await db_session.execute(select(CartItem).where(CartItem.id==item.id))
            assert db_item.scalar_one_or_none() is None



class TestCartTokenErrors:
    async def test_cart_with_invalid_token_return_error(self, client, cart, cart_item, product, auth_headers):
        get_response = await client.get('/api/cart', headers={'Authorization': 'Bearer invalid_token'})
        assert get_response.status_code == 401


        add_response = await client.post('/api/cart/add', json={'product_id': product.id, 'quantity': 3},
                                         headers={'Authorization': 'Bearer invalid_token'})
        assert add_response.status_code == 401


        update_response = await client.patch(f'/api/cart/update/{cart_item.id}', json={'quantity': 3},
                                            headers={'Authorization': 'Bearer invalid_token'})
        assert update_response.status_code == 401


        delete_cart_item_response = await client.delete(f'/api/cart/remove/cart-item/{cart_item.id}',
                                                        headers={'Authorization': 'Bearer invalid_token'})
        assert delete_cart_item_response.status_code == 401


        clear_cart_response = await client.delete(f'/api/cart/remove/cart',
                                                  headers={'Authorization': 'Bearer invalid_token'})
        assert clear_cart_response.status_code == 401



    async def test_cart_without_token_return_error(self, client, cart, cart_item, product, auth_headers):
        get_response = await client.get('/api/cart')
        assert get_response.status_code == 401


        add_response = await client.post('/api/cart/add', json={'product_id': product.id, 'quantity': 3})
        assert add_response.status_code == 401


        update_response = await client.patch(f'/api/cart/update/{cart_item.id}', json={'quantity': 3})
        assert update_response.status_code == 401


        delete_cart_item_response = await client.delete(f'/api/cart/remove/cart-item/{cart_item.id}')
        assert delete_cart_item_response.status_code == 401


        clear_cart_response = await client.delete(f'/api/cart/remove/cart')
        assert clear_cart_response.status_code == 401



#Testing cart errors
class TestCartAddErrors:
    async def test_add_cart_with_missing_fields(self, client, product, cart, auth_headers):
        #missing product_id
        first_response = await client.post('/api/cart/add', json={'quantity': 3}, headers=auth_headers)
        assert first_response.status_code == 422

        #missing quantity
        second_response = await client.post('/api/cart/add', json={'product_id': product.id}, headers=auth_headers)
        assert second_response.status_code == 422


    async def test_update_cart_with_missing_fields(self, client, product, cart, cart_item, auth_headers):
        #missing quantity
        response = await client.patch(f'/api/cart/update/{cart_item.id}', headers=auth_headers)
        assert response.status_code == 422


    async def test_update_cart_with_invalid_id(self, client, cart, cart_item, auth_headers):
        response = await client.patch(f'/api/cart/update/{cart_item.id + 1}', json={'quantity': 3}, headers=auth_headers)
        assert response.status_code == 404


    async def test_delete_cart_item_with_invalid_id(self, client, cart, cart_item, auth_headers):
        response = await client.delete(f'/api/cart/remove/cart-item/{cart_item.id + 1}', headers=auth_headers)
        assert response.status_code == 404