from app.schemas.category_schema import CategoryResponse



class TestGetCategories:
    async def test_return_list_of_created_categories(self, client, categories):
        response = await client.get('/api/categories')
        data = response.json()

        assert response.status_code == 200
        assert isinstance(data, list)
        assert len(data) == len(categories)

        categories_response = {category.id: CategoryResponse.model_validate(category) for category in categories}

        for item in data:
            item_response = CategoryResponse.model_validate(item)
            assert item_response == categories_response[item_response.id]


    async def test_return_empty_list_of_categories(self, client):
        response = await client.get('/api/categories')

        assert response.status_code == 200
        assert response.json() == []