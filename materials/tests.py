from http import HTTPStatus

import parts.factories
from django.core.exceptions import ObjectDoesNotExist
from django.test import Client, TestCase
from django.urls import reverse
from materials import factories
from materials.models import Material


class MaterialListViewTest(TestCase):
    """Test case for the MaterialListView."""

    def setUp(self) -> None:
        self.client = Client()
        self.material1 = factories.MaterialFactory(name='material_1')
        self.material2 = factories.MaterialFactory(name='material_2')
        self.material3 = factories.MaterialFactory(name='material_3')

    def test_view_url_exists_at_desired_location(self) -> None:
        response = self.client.get('/materials/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_view_url_accessible_by_name(self) -> None:
        response = self.client.get(reverse('materials:material_list'))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_view_uses_correct_template(self) -> None:
        response = self.client.get(reverse('materials:material_list'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'materials/material_list.html')

    def test_list_all_materials(self) -> None:
        response = self.client.get(reverse('materials:material_list'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(len(response.context['materials']), 3)

    def test_material_name_search(self) -> None:
        response = self.client.get(
            reverse('materials:material_list'), {'name': 'Al_2'}
        )
        material_list = response.context['materials']
        self.assertIn(self.material2, material_list)
        self.assertNotIn(self.material1, material_list)
        self.assertNotIn(self.material3, material_list)


class MaterialDetailViewTest(TestCase):
    """Test case for the MaterialDetailView."""

    def setUp(self) -> None:
        self.client = Client()
        self.material = factories.MaterialFactory(name='material_1')

    def test_view_url_exists_at_desired_location(self) -> None:
        response = self.client.get('/materials/1/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_view_url_accessible_by_name(self) -> None:
        response = self.client.get(reverse(
            'materials:material_detail', args=[1])
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_view_uses_correct_template(self) -> None:
        response = self.client.get(reverse(
            'materials:material_detail', args=[1])
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'materials/material_detail.html')

    def test_view_has_all_data(self) -> None:
        response = self.client.get(reverse(
            'materials:material_detail', args=[1])
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, self.material.name)
        self.assertContains(response, self.material.density)
        self.assertContains(
            response, self.material.created.strftime("%d.%m.%Y %H:%M")
        )
        self.assertContains(
            response, self.material.updated.strftime("%d.%m.%Y %H:%M")
        )

    def test_view_has_links_to_update_and_delete(self) -> None:
        response = self.client.get(reverse(
            'materials:material_detail', args=[1])
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(
            response, reverse('materials:material_update', args=[1])
        )
        self.assertContains(
            response, reverse('materials:material_delete', args=[1])
        )


class MaterialCreateViewTest(TestCase):
    """Test case for MaterialCreateView."""

    def setUp(self) -> None:
        self.client = Client()
        self.valid_data = {
            'name': 'Steel',
            'density': 7800,
        }

    def test_view_url_exists_at_desired_location(self) -> None:
        response = self.client.get('/materials/create/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_view_url_accessible_by_name(self) -> None:
        response = self.client.get(reverse('materials:material_create'))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_view_uses_correct_template(self) -> None:
        response = self.client.get(reverse('materials:material_create'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'materials/material_form.html')

    def test_create_material_with_valid_data(self) -> None:
        response = self.client.post(
            reverse('materials:material_create'),
            self.valid_data,
            follow=True
        )
        self.assertRedirects(response, reverse('materials:material_list'))

        material = Material.objects.get(pk=1)
        self.assertEqual(material.name, self.valid_data['name'])
        self.assertEqual(material.density, self.valid_data['density'])

        message = list(response.context.get('messages'))[0]
        self.assertEqual(message.message, 'The material successfully created')
        self.assertEqual(message.tags, 'success')

    def test_create_material_without_density(self) -> None:
        valid_data = self.valid_data
        del valid_data['density']

        response = self.client.post(
            reverse('materials:material_create'),
            self.valid_data,
            follow=True
        )
        self.assertRedirects(response, reverse('materials:material_list'))

        material = Material.objects.get(pk=1)
        self.assertEqual(material.name, self.valid_data['name'])
        self.assertEqual(material.density, None)

        message = list(response.context.get('messages'))[0]
        self.assertEqual(message.message, 'The material successfully created')
        self.assertEqual(message.tags, 'success')

    def test_do_not_create_material_without_name(self) -> None:
        invalid_data = self.valid_data
        invalid_data['name'] = ''

        response = self.client.post(
            reverse('materials:material_create'),
            self.valid_data,
            follow=True
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertFalse(Material.objects.all())

    def test_do_not_create_material_with_invalid_name(self) -> None:
        invalid_data = self.valid_data

        # numbers of invalid characters in ASCII table
        invalid_set = set(range(33, 48)) | set(range(58, 65)) | \
            set(range(91, 97)) | set(range(123, 127))

        for i in invalid_set:
            invalid_data['name'] = f'Steel {chr(i)}01'

            response = self.client.post(
                reverse('materials:material_create'),
                self.valid_data,
                follow=True
            )
            self.assertEqual(response.status_code, HTTPStatus.OK)
            self.assertFalse(Material.objects.all())


class MaterialUpdateViewTest(TestCase):
    """Test case for MaterialUpdateView."""

    def setUp(self) -> None:
        self.client = Client()
        self.material = factories.MaterialFactory()
        self.valid_data = {
            'name': 'Steel',
            'density': 7800,
        }

    def test_view_url_exists_at_desired_location(self) -> None:
        response = self.client.get('/materials/1/update/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_view_url_accessible_by_name(self) -> None:
        response = self.client.get(
            reverse('materials:material_update', args=[1])
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_view_uses_correct_template(self) -> None:
        response = self.client.get(
            reverse('materials:material_update', args=[1])
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'materials/material_form.html')

    def test_update_material_with_valid_data(self) -> None:
        response = self.client.post(
            reverse('materials:material_update', args=[1]),
            self.valid_data,
            follow=True
        )
        self.assertRedirects(
            response, reverse('materials:material_detail', args=[1])
        )

        material = Material.objects.get(pk=1)
        self.assertEqual(material.name, self.valid_data['name'])
        self.assertEqual(material.density, self.valid_data['density'])

        message = list(response.context.get('messages'))[0]
        self.assertEqual(message.message, 'The material successfully updated')
        self.assertEqual(message.tags, 'success')

    def test_update_material_without_density(self) -> None:
        valid_data = self.valid_data
        del valid_data['density']

        response = self.client.post(
            reverse('materials:material_update', args=[1]),
            self.valid_data,
            follow=True
        )
        self.assertRedirects(
            response, reverse('materials:material_detail', args=[1])
        )

        material = Material.objects.get(pk=1)
        self.assertEqual(material.name, self.valid_data['name'])
        self.assertEqual(material.density, None)

        message = list(response.context.get('messages'))[0]
        self.assertEqual(message.message, 'The material successfully updated')
        self.assertEqual(message.tags, 'success')

    def test_do_not_update_material_without_name(self) -> None:
        material_before = self.material
        invalid_data = self.valid_data
        invalid_data['name'] = ''

        response = self.client.post(
            reverse('materials:material_update', args=[1]),
            self.valid_data,
            follow=True
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

        material_after = Material.objects.get(pk=1)
        self.assertEqual(material_before, material_after)

    def test_do_not_update_material_with_invalid_name(self) -> None:
        material_before = self.material
        invalid_data = self.valid_data

        # numbers of invalid characters in ASCII table
        invalid_set = set(range(33, 48)) | set(range(58, 65))

        for i in invalid_set:
            invalid_data['name'] = f'Steel{chr(i)}'

            response = self.client.post(
                reverse('materials:material_create'),
                self.valid_data,
                follow=True
            )
            self.assertEqual(response.status_code, HTTPStatus.OK)

            material_after = Material.objects.get(pk=1)
            self.assertEqual(material_before, material_after)


class MaterialDeleteViewTest(TestCase):
    """Test case for MaterialDeleteView."""

    def setUp(self) -> None:
        self.client = Client()
        self.material_set = factories.MaterialFactory.create_batch(2)
        self.material = factories.MaterialFactory()
        self.part = parts.factories.PartFactory(material=self.material)

    def test_view_url_exists_at_desired_location(self) -> None:
        response = self.client.get('/materials/1/delete/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_view_url_accessible_by_name(self) -> None:
        response = self.client.get(
            reverse('materials:material_delete', args=[1])
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_view_uses_correct_template(self) -> None:
        response = self.client.get(
            reverse('materials:material_delete', args=[1])
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'materials/material_delete.html')

    def test_delete_material(self) -> None:
        length_of_material_list_before = len(Material.objects.all())

        response = self.client.post(
            reverse('materials:material_delete', args=[1]),
            follow=True
        )
        self.assertRedirects(response, reverse('materials:material_list'))

        length_of_material_list_after = len(Material.objects.all())
        self.assertTrue(
            length_of_material_list_after == length_of_material_list_before - 1
        )
        with self.assertRaises(ObjectDoesNotExist):
            Material.objects.get(pk=1)

        message = list(response.context.get('messages'))[0]
        self.assertEqual(message.message, 'The material successfully deleted')
        self.assertEqual(message.tags, 'success')

    def test_do_not_delete_material_linked_to_part(self) -> None:
        material_before = Material.objects.get(pk=3)

        response = self.client.post(
            reverse('materials:material_delete', args=[3]),
            follow=True
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertRedirects(response, reverse('materials:material_list'))

        material_after = Material.objects.get(pk=3)
        self.assertEqual(material_before, material_after)

        message = list(response.context.get('messages'))[0]
        self.assertEqual(
            message.message,
            "Can't delete material because it's in use"
        )
        self.assertEqual(message.tags, 'error')
