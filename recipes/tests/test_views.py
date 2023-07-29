import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.exceptions import ErrorDetail
from recipes.models import Category, Recipe
from users.models import CustomUser


class CategoriesTests(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        admin = CustomUser.objects.create_user(
            username='admin',
            email='admin@gmail.com',
            password='34somepassword34',
            is_staff=True,
            is_superuser=True)
        user = CustomUser.objects.create_user(
            username='test_user',
            email='test_user@gmail.com',
            password='34somepassword34'
        )

        Category.objects.create(
            title='Soups',
            slug='soups'
        )

        Category.objects.create(
            title='Desserts',
            slug='desserts'
        )

        Category.objects.create(
            title='Snacks',
            slug='snacks'
        )

    # GET list
    def test_get_category_list(self):
        url = reverse('category-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        count_categories = Category.objects.count()
        self.assertEqual(dict(response.data)['count'], count_categories)

    # GET detail
    def test_get_category_detail(self):
        test_server_prefix = 'http://testserver'
        category = Category.objects.filter(title='Soups').first()
        url = reverse('category-detail', kwargs={'pk': category.id})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = {'url': test_server_prefix + reverse('category-detail', kwargs={'pk': category.id}),
                         'id': category.id,
                         'title': category.title,
                         'slug': category.slug,
                         'get_recipes': test_server_prefix + reverse('category-get-recipes', kwargs={'pk': category.id})}
        self.assertEqual(response.data, expected_data)

    def test_get_detail_of_nonexistent_category(self):
        url = reverse('category-detail', kwargs={'pk': 78})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # POST
    def test_admin_posts_category_with_not_unique_title_or_slug(self):
        category = Category.objects.filter(title='Soups').first()
        admin = CustomUser.objects.filter(username='admin').first()
        token = AccessToken.for_user(admin)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + str(token))
        url = reverse('category-list')
        response = self.client.post(url, data={'title': category.title,
                                               'slug': category.slug},
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_admin_posts_new_category(self):
        admin = CustomUser.objects.filter(username='admin').first()
        token = AccessToken.for_user(admin)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + str(token))
        url = reverse('category-list')
        response = self.client.post(url, data={'title': 'Pasta and Rissoto',
                                               'slug': 'pasta-and-rissoto'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        test_server_prefix = 'http://testserver'
        new_category = Category.objects.filter(
            title='Pasta and Rissoto').first()
        self.assertTrue(new_category is not None)
        expected_data = {'url': test_server_prefix + reverse('category-detail', kwargs={'pk': new_category.id}),
                         'id': new_category.id,
                         'title': new_category.title,
                         'slug': new_category.slug,
                         'get_recipes': test_server_prefix + reverse('category-get-recipes', kwargs={'pk': new_category.id})}
        self.assertEqual(response.data, expected_data)

    def test_not_admin_user_posts_new_category(self):
        user = CustomUser.objects.filter(username='test_user').first()
        token = AccessToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + str(token))
        url = reverse('category-list')
        response = self.client.post(url, data={'title': 'New category',
                                               'slug': 'new-category'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_not_authorized_user_posts_new_category(self):
        url = reverse('category-list')
        response = self.client.post(url, data={'title': 'New category',
                                               'slug': 'new-category'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # PUT
    def test_admin_updates_category_with_not_unique_title_or_slug(self):
        category_to_update = Category.objects.filter(title='Soups').first()
        existing_category = Category.objects.filter(title='Desserts').first()
        admin = CustomUser.objects.filter(username='admin').first()
        token = AccessToken.for_user(admin)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + str(token))
        url = reverse('category-detail', kwargs={'pk': category_to_update.id})
        response = self.client.put(url, data={'title': existing_category.title,
                                              'slug': existing_category.slug}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_admin_updates_category(self):
        category_to_update = Category.objects.filter(title='Soups').first()
        admin = CustomUser.objects.filter(username='admin').first()
        token = AccessToken.for_user(admin)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + str(token))
        url = reverse('category-detail', kwargs={'pk': category_to_update.id})
        response = self.client.put(url, data={'title': 'Soups and Stews',
                                              'slug': 'soups-and-stews'}, format='json')
        updated_category = Category.objects.filter(
            title='Soups and Stews').first()
        self.assertTrue(updated_category is not None)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        test_server_prefix = 'http://testserver'
        expected_data = {'url': test_server_prefix + reverse('category-detail', kwargs={'pk': updated_category.id}),
                         'id': updated_category.id,
                         'title': updated_category.title,
                         'slug': updated_category.slug,
                         'get_recipes': test_server_prefix + reverse('category-get-recipes', kwargs={'pk': updated_category.id})}
        self.assertEqual(response.data, expected_data)

    def test_admin_updates_nonexistent_category(self):
        admin = CustomUser.objects.filter(username='admin').first()
        token = AccessToken.for_user(admin)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + str(token))
        url = reverse('category-detail', kwargs={'pk': 67})
        response = self.client.put(url, data={'title': 'Soups and Stews',
                                              'slug': 'soups-and-stews'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_not_admin_user_updates_category(self):
        user = CustomUser.objects.filter(username='test_user').first()
        token = AccessToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + str(token))
        url = reverse('category-detail', kwargs={'pk': 67})
        response = self.client.put(url, data={'title': 'Soups and Stews',
                                              'slug': 'soups-and-stews'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_not_authorized_user_updates_category(self):
        category = Category.objects.get(title='Soups')
        url = reverse('category-detail', kwargs={'pk': 67})
        response = self.client.put(url, data={'title': 'Soups and Stews',
                                              'slug': 'soups-and-stews'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # DELETE
    def test_admin_deletes_nonexistent_category(self):
        admin = CustomUser.objects.filter(username='admin').first()
        token = AccessToken.for_user(admin)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + str(token))
        url = reverse('category-detail', kwargs={'pk': 67})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_admin_deletes_category_with_associated_recipes(self):
        user = CustomUser.objects.filter(username='test_user').first()
        category = Category.objects.filter(title='Soups').first()
        recipe = Recipe.objects.create(
            author=user,
            category=category,
            title='Some random recipe',
            instructions='Follow instructions'
        )
        admin = CustomUser.objects.filter(username='admin').first()
        token = AccessToken.for_user(admin)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + str(token))
        url = reverse('category-detail', kwargs={'pk': category.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(response.data['detail'],
                         'Category has recipes associated with it, cannot be deleted.')

    def test_admin_deletes_category(self):
        category = Category.objects.filter(title='Soups').first()
        admin = CustomUser.objects.filter(username='admin').first()
        token = AccessToken.for_user(admin)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + str(token))
        url = reverse('category-detail', kwargs={'pk': category.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        category = Category.objects.filter(title='Soups').first()
        self.assertTrue(category is None)

    def test_not_admin_user_deletes_category(self):
        user = CustomUser.objects.filter(username='test_user').first()
        token = AccessToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + str(token))
        url = reverse('category-detail', kwargs={'pk': 673})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_not_authorized_user_deletes_category(self):
        url = reverse('category-detail', kwargs={'pk': 673})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
