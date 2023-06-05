from http import HTTPStatus

import materials.factories
from django.core.exceptions import ObjectDoesNotExist
from django.test import Client, TestCase
from django.urls import reverse
from parts import factories
from parts.models import Part


class PartListViewTest(TestCase):
    """Test case for the PartListView."""

    def setUp(self) -> None:
        self.client = Client()
        self.part_set = factories.PartFactory.create_batch(3)
        self.part1 = factories.PartFactory(designation='01.00', name='part_1')
        self.part2 = factories.PartFactory(designation='02.00', name='part_2')
        self.part3 = factories.PartFactory(designation='03.00', name='part_3')

    def test_view_url_exists_at_desired_location(self) -> None:
        response = self.client.get('/parts/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_view_url_accessible_by_name(self) -> None:
        response = self.client.get(reverse('parts:part_list'))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_view_uses_correct_template(self) -> None:
        response = self.client.get(reverse('parts:part_list'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'parts/part_list.html')

    def test_list_all_parts(self) -> None:
        response = self.client.get(reverse('parts:part_list'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(len(response.context['parts']), 6)

    def test_part_designation_search(self) -> None:
        response = self.client.get(
            reverse('parts:part_list'), {'search_query': '03'}
        )
        part_list = response.context['parts']
        self.assertIn(self.part3, part_list)
        self.assertNotIn(self.part1, part_list)
        self.assertNotIn(self.part2, part_list)

    def test_part_name_search(self) -> None:
        response = self.client.get(
            reverse('parts:part_list'), {'search_query': 'Rt_2'}
        )
        part_list = response.context['parts']
        self.assertIn(self.part2, part_list)
        self.assertNotIn(self.part1, part_list)
        self.assertNotIn(self.part3, part_list)


class PartDetailViewTest(TestCase):
    """Test case for the PartDetailView."""

    def setUp(self) -> None:
        self.client = Client()
        self.material = materials.factories.MaterialFactory()
        self.part = factories.PartFactory(material=self.material)

    def test_view_url_exists_at_desired_location(self) -> None:
        response = self.client.get('/parts/1/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_view_url_accessible_by_name(self) -> None:
        response = self.client.get(reverse('parts:part_detail', args=[1]))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_view_uses_correct_template(self) -> None:
        response = self.client.get(reverse('parts:part_detail', args=[1]))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'parts/part_detail.html')

    def test_view_has_all_data(self) -> None:
        response = self.client.get(reverse('parts:part_detail', args=[1]))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, self.part.designation)
        self.assertContains(response, self.part.name)
        self.assertContains(response, self.part.material)
        self.assertContains(
            response, self.part.created.strftime("%d.%m.%Y %H:%M")
        )
        self.assertContains(
            response, self.part.updated.strftime("%d.%m.%Y %H:%M")
        )

    def test_view_has_links_to_update_and_delete(self) -> None:
        response = self.client.get(reverse('parts:part_detail', args=[1]))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, reverse('parts:part_update', args=[1]))
        self.assertContains(response, reverse('parts:part_delete', args=[1]))


class PartCreateViewTest(TestCase):
    """Test case for PartCreateView."""

    def setUp(self) -> None:
        self.client = Client()
        self.material = materials.factories.MaterialFactory()
        self.valid_data = {
            'designation': '01.000',
            'name': 'Part',
            'material': self.material.id,
        }

    def test_view_url_exists_at_desired_location(self) -> None:
        response = self.client.get('/parts/create/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_view_url_accessible_by_name(self) -> None:
        response = self.client.get(reverse('parts:part_create'))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_view_uses_correct_template(self) -> None:
        response = self.client.get(reverse('parts:part_create'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'parts/part_form.html')

    def test_create_part_with_valid_data(self) -> None:
        response = self.client.post(
            reverse('parts:part_create'),
            self.valid_data,
            follow=True
        )
        self.assertRedirects(response, reverse('parts:part_list'))

        part = Part.objects.get(pk=1)
        self.assertEqual(part.designation, self.valid_data['designation'])
        self.assertEqual(part.name, self.valid_data['name'])
        self.assertEqual(part.material, self.material)

        message = list(response.context.get('messages'))[0]
        self.assertEqual(message.message, 'The part successfully created')
        self.assertEqual(message.tags, 'success')

    def test_do_not_create_part_without_designation(self) -> None:
        invalid_data = self.valid_data
        invalid_data['designation'] = ''

        response = self.client.post(
            reverse('parts:part_create'),
            self.valid_data,
            follow=True
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertFalse(Part.objects.all())

    def test_do_not_create_part_without_name(self) -> None:
        invalid_data = self.valid_data
        invalid_data['name'] = ''

        response = self.client.post(
            reverse('parts:part_create'),
            self.valid_data,
            follow=True
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertFalse(Part.objects.all())

    def test_do_not_create_part_without_material(self) -> None:
        invalid_data = self.valid_data
        invalid_data['material'] = ''

        response = self.client.post(
            reverse('parts:part_create'),
            self.valid_data,
            follow=True
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertFalse(Part.objects.all())

    def test_do_not_create_part_with_invalid_designation(self) -> None:
        invalid_data = self.valid_data

        # numbers of invalid characters in ASCII table
        invalid_set = set(range(32, 45)) | set(range(58, 65)) | \
            set(range(91, 97)) | set(range(123, 127)) | {47}

        for i in invalid_set:
            invalid_data['designation'] = f'123.0{chr(i)}-01'

            response = self.client.post(
                reverse('parts:part_create'),
                self.valid_data,
                follow=True
            )
            self.assertEqual(response.status_code, HTTPStatus.OK)
            self.assertFalse(Part.objects.all())

    def test_do_not_create_part_with_invalid_name(self) -> None:
        invalid_data = self.valid_data

        # numbers of invalid characters in ASCII table
        invalid_set = set(range(33, 48)) | set(range(58, 65)) | \
            set(range(91, 97)) | set(range(123, 127))

        for i in invalid_set:
            invalid_data['name'] = f'Part {chr(i)}01'

            response = self.client.post(
                reverse('parts:part_create'),
                self.valid_data,
                follow=True
            )
            self.assertEqual(response.status_code, HTTPStatus.OK)
            self.assertFalse(Part.objects.all())


class PartUpdateViewTest(TestCase):
    """Test case for PartUpdateView."""

    def setUp(self) -> None:
        self.client = Client()
        self.part = factories.PartFactory()
        self.material = materials.factories.MaterialFactory()
        self.valid_data = {
            'designation': '01.000',
            'name': 'Part',
            'material': self.material.id,
        }

    def test_view_url_exists_at_desired_location(self) -> None:
        response = self.client.get('/parts/1/update/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_view_url_accessible_by_name(self) -> None:
        response = self.client.get(reverse('parts:part_update', args=[1]))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_view_uses_correct_template(self) -> None:
        response = self.client.get(reverse('parts:part_update', args=[1]))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'parts/part_form.html')

    def test_update_part_with_valid_data(self) -> None:
        response = self.client.post(
            reverse('parts:part_update', args=[1]),
            self.valid_data,
            follow=True
        )
        self.assertRedirects(response, reverse('parts:part_detail', args=[1]))

        part = Part.objects.get(pk=1)
        self.assertEqual(part.designation, self.valid_data['designation'])
        self.assertEqual(part.name, self.valid_data['name'])
        self.assertEqual(part.material, self.material)

        message = list(response.context.get('messages'))[0]
        self.assertEqual(message.message, 'The part successfully updated')
        self.assertEqual(message.tags, 'success')

    def test_do_not_update_part_without_designation(self) -> None:
        part_before = self.part
        invalid_data = self.valid_data
        invalid_data['designation'] = ''

        response = self.client.post(
            reverse('parts:part_update', args=[1]),
            self.valid_data,
            follow=True
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

        part_after = Part.objects.get(pk=1)
        self.assertEqual(part_before, part_after)

    def test_do_not_update_part_without_name(self) -> None:
        part_before = self.part
        invalid_data = self.valid_data
        invalid_data['name'] = ''

        response = self.client.post(
            reverse('parts:part_update', args=[1]),
            self.valid_data,
            follow=True
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

        part_after = Part.objects.get(pk=1)
        self.assertEqual(part_before, part_after)

    def test_do_not_update_part_with_invalid_designation(self) -> None:
        part_before = self.part
        invalid_data = self.valid_data

        # numbers of invalid characters in ASCII table
        invalid_set = set(range(32, 45)) | set(range(58, 65)) | \
            set(range(91, 97)) | set(range(123, 127)) | {47}

        for i in invalid_set:
            invalid_data['designation'] = f'123.0{chr(i)}-01'

            response = self.client.post(
                reverse('parts:part_create'),
                self.valid_data,
                follow=True
            )
            self.assertEqual(response.status_code, HTTPStatus.OK)

            part_after = Part.objects.get(pk=1)
            self.assertEqual(part_before, part_after)

    def test_do_not_update_part_with_invalid_name(self) -> None:
        part_before = self.part
        invalid_data = self.valid_data

        # numbers of invalid characters in ASCII table
        invalid_set = set(range(33, 48)) | set(range(58, 65)) | \
            set(range(91, 97)) | set(range(123, 127))

        for i in invalid_set:
            invalid_data['name'] = f'Part {chr(i)}01'

            response = self.client.post(
                reverse('parts:part_create'),
                self.valid_data,
                follow=True
            )
            self.assertEqual(response.status_code, HTTPStatus.OK)

            part_after = Part.objects.get(pk=1)
            self.assertEqual(part_before, part_after)


class PartDeleteViewTest(TestCase):
    """Test case for PartDeleteView."""

    def setUp(self) -> None:
        self.client = Client()
        self.part_set = factories.PartFactory.create_batch(2)
        self.part = factories.PartFactory()

    def test_view_url_exists_at_desired_location(self) -> None:
        response = self.client.get('/parts/1/delete/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_view_url_accessible_by_name(self) -> None:
        response = self.client.get(reverse('parts:part_delete', args=[1]))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_view_uses_correct_template(self) -> None:
        response = self.client.get(reverse('parts:part_delete', args=[1]))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'parts/part_delete.html')

    def test_delete_part(self) -> None:
        length_of_part_list_before = len(Part.objects.all())

        response = self.client.post(
            reverse('parts:part_delete', args=[1]),
            follow=True
        )
        self.assertRedirects(response, reverse('parts:part_list'))

        length_of_part_list_after = len(Part.objects.all())
        self.assertTrue(
            length_of_part_list_after == length_of_part_list_before - 1
        )
        with self.assertRaises(ObjectDoesNotExist):
            Part.objects.get(pk=1)

        message = list(response.context.get('messages'))[0]
        self.assertEqual(message.message, 'The part successfully deleted')
        self.assertEqual(message.tags, 'success')
