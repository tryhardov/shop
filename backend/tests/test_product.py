from app.schemas.product_schema import ProductResponse



class TestGetProducts:
    async def test_get_list_of_created_products(self, client, products):
        response = await client.get('/api/products')
        data = response.json()

        assert response.status_code == 200
        assert isinstance(data, list)
        assert len(data) == len(products)

        products_response = {prod.id: ProductResponse.model_validate(prod) for prod in products}

        for item in data:
            item_response = ProductResponse.model_validate(item)
            assert item_response == products_response[item_response.id]


    async def test_return_empty_list_of_products(self, client):
        response = await client.get('/api/products')

        assert response.status_code == 200
        assert response.json() == []



class TestGetProductBySlug:
    async def test_get_created_product_by_slug(self, client, product):
        response = await client.get(f'/api/products/{product.slug}')
        data = response.json()
        response_data = ProductResponse.model_validate(data)
        expected_product_data = ProductResponse.model_validate(product)

        assert response.status_code == 200
        assert response_data == expected_product_data


    async def test_invalid_slug_returns_404(self, client):
        response = await client.get('/api/products/non-slug')
        assert response.status_code == 404



class TestGetProductsByCategory:
    async def test_get_products_by_category(self, client, products, category):
        response = await client.get(f'/api/products/category/{category.id}')
        data = response.json()

        assert response.status_code == 200
        assert isinstance(data, list)
        assert len(data) == len(products)

        products_response = {prod.id: ProductResponse.model_validate(prod) for prod in products}

        for item in data:
            item_response = ProductResponse.model_validate(item)
            assert item_response == products_response[item_response.id]


    async def test_invalid_category_id_return_empty_list(self, client, products, category, db_session):
        for product in products:
            await db_session.delete(product)

        await db_session.delete(category)
        await db_session.commit()

        response = await client.get(f'/api/products/category/{category.id}') 

        assert response.status_code == 200
        assert response.json() == []