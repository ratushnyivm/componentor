from http import HTTPStatus

from assemblies import factories
from assemblies.models import Assembly
from django.core.exceptions import ObjectDoesNotExist
from django.test import Client, TestCase
from django.urls import reverse


class AssemblyListViewTest(TestCase):
    """Test case for the AssemblyListView."""

    def setUp(self) -> None:
        self.client = Client()
        self.assembly_set = factories.AssemblyFactory.create_batch(3)
        self.assembly1 = factories.AssemblyFactory(
            designation='10.00', name='assembly_1'
        )
        self.assembly2 = factories.AssemblyFactory(
            designation='20.00', name='assembly_2'
        )
        self.assembly3 = factories.AssemblyFactory(
            designation='30.00', name='assembly_3'
        )

    def test_view_url_exists_at_desired_location(self) -> None:
        response = self.client.get('/assemblies/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_view_url_accessible_by_name(self) -> None:
        response = self.client.get(reverse('assemblies:assembly_list'))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_view_uses_correct_template(self) -> None:
        response = self.client.get(reverse('assemblies:assembly_list'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'assemblies/assembly_list.html')

    def test_list_all_assemblies(self) -> None:
        response = self.client.get(reverse('assemblies:assembly_list'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(len(response.context['assemblies']), 6)

    def test_assembly_designation_search(self) -> None:
        response = self.client.get(
            reverse('assemblies:assembly_list'), {'search_query': '30.'}
        )
        assembly_list = response.context['assemblies']
        self.assertIn(self.assembly3, assembly_list)
        self.assertNotIn(self.assembly1, assembly_list)
        self.assertNotIn(self.assembly2, assembly_list)

    def test_assembly_name_search(self) -> None:
        response = self.client.get(
            reverse('assemblies:assembly_list'), {'search_query': 'bLy_2'}
        )
        assembly_list = response.context['assemblies']
        self.assertIn(self.assembly2, assembly_list)
        self.assertNotIn(self.assembly1, assembly_list)
        self.assertNotIn(self.assembly3, assembly_list)


class AssemblyDetailViewTest(TestCase):
    """Test case for the AssemblyDetailView."""

    def setUp(self) -> None:
        self.client = Client()
        self.assembly = factories.AssemblyFactory(
            designation='10.00', name='assembly_1'
        )

    def test_view_url_exists_at_desired_location(self) -> None:
        response = self.client.get('/assemblies/1/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_view_url_accessible_by_name(self) -> None:
        response = self.client.get(
            reverse('assemblies:assembly_detail', args=[1])
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_view_uses_correct_template(self) -> None:
        response = self.client.get(
            reverse('assemblies:assembly_detail', args=[1])
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'assemblies/assembly_detail.html')

    def test_view_has_all_data(self) -> None:
        response = self.client.get(
            reverse('assemblies:assembly_detail', args=[1])
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, self.assembly.designation)
        self.assertContains(response, self.assembly.name)
        self.assertContains(
            response, self.assembly.created.strftime("%d.%m.%Y %H:%M")
        )
        self.assertContains(
            response, self.assembly.updated.strftime("%d.%m.%Y %H:%M")
        )

    def test_view_has_links_to_update_and_delete(self) -> None:
        response = self.client.get(
            reverse('assemblies:assembly_detail', args=[1])
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(
            response, reverse('assemblies:assembly_update', args=[1])
        )
        self.assertContains(
            response, reverse('assemblies:assembly_delete', args=[1])
        )


class AssemblyCreateViewTest(TestCase):
    """Test case for AssemblyCreateView."""

    def setUp(self) -> None:
        self.client = Client()
        self.valid_data = {
            'designation': '12345',
            'name': 'Assembly',
            'parts-TOTAL_FORMS': 0,
            'parts-INITIAL_FORMS': 0
        }

    def test_view_url_exists_at_desired_location(self) -> None:
        response = self.client.get('/assemblies/create/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_view_url_accessible_by_name(self) -> None:
        response = self.client.get(reverse('assemblies:assembly_create'))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_view_uses_correct_template(self) -> None:
        response = self.client.get(reverse('assemblies:assembly_create'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'assemblies/assembly_form.html')

    def test_create_assembly_with_valid_data(self) -> None:
        response = self.client.post(
            reverse('assemblies:assembly_create'),
            self.valid_data,
            follow=True
        )
        self.assertRedirects(response, reverse('assemblies:assembly_list'))

        assembly = Assembly.objects.get(pk=1)
        self.assertEqual(assembly.designation, self.valid_data['designation'])
        self.assertEqual(assembly.name, self.valid_data['name'])

        message = list(response.context.get('messages'))[0]
        self.assertEqual(message.message, 'The assembly successfully created')
        self.assertEqual(message.tags, 'success')


class AssemblyUpdateViewTest(TestCase):
    """Test case for AssemblyUpdateView."""

    def setUp(self) -> None:
        self.client = Client()
        self.assembly = factories.AssemblyFactory()
        self.valid_data = {
            'designation': '12345',
            'name': 'Assembly',
            'parts-TOTAL_FORMS': 0,
            'parts-INITIAL_FORMS': 0
        }

    def test_view_url_exists_at_desired_location(self) -> None:
        response = self.client.get('/assemblies/1/update/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_view_url_accessible_by_name(self) -> None:
        response = self.client.get(
            reverse('assemblies:assembly_update', args=[1])
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_view_uses_correct_template(self) -> None:
        response = self.client.get(
            reverse('assemblies:assembly_update', args=[1])
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'assemblies/assembly_form.html')

    def test_update_assembly_with_valid_data(self) -> None:
        response = self.client.post(
            reverse('assemblies:assembly_update', args=[1]),
            self.valid_data,
            follow=True
        )
        self.assertRedirects(
            response, reverse('assemblies:assembly_detail', args=[1])
        )

        assembly = Assembly.objects.get(pk=1)
        self.assertEqual(assembly.designation, self.valid_data['designation'])
        self.assertEqual(assembly.name, self.valid_data['name'])

        message = list(response.context.get('messages'))[0]
        self.assertEqual(message.message, 'The assembly successfully updated')
        self.assertEqual(message.tags, 'success')


class AssemblyDeleteViewTest(TestCase):
    """Test case for AssemblyDeleteView."""

    def setUp(self) -> None:
        self.client = Client()
        self.assembly_set = factories.AssemblyFactory.create_batch(3)
        self.assembly = factories.AssemblyFactory()

    def test_view_url_exists_at_desired_location(self) -> None:
        response = self.client.get('/assemblies/1/delete/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_view_url_accessible_by_name(self) -> None:
        response = self.client.get(
            reverse('assemblies:assembly_delete', args=[1])
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_view_uses_correct_template(self) -> None:
        response = self.client.get(
            reverse('assemblies:assembly_delete', args=[1])
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'assemblies/assembly_delete.html')

    def test_delete_assembly(self) -> None:
        length_of_assembly_list_before = len(Assembly.objects.all())

        response = self.client.post(
            reverse('assemblies:assembly_delete', args=[1]),
            follow=True
        )
        self.assertRedirects(response, reverse('assemblies:assembly_list'))

        length_of_assembly_list_after = len(Assembly.objects.all())
        self.assertTrue(
            length_of_assembly_list_after == length_of_assembly_list_before - 1
        )
        with self.assertRaises(ObjectDoesNotExist):
            Assembly.objects.get(pk=1)

        message = list(response.context.get('messages'))[0]
        self.assertEqual(message.message, 'The assembly successfully deleted')
        self.assertEqual(message.tags, 'success')
