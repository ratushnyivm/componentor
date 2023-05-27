from http import HTTPStatus

from assemblies import factories
from django.test import Client, TestCase
from django.urls import reverse


class AssemblyListViewTest(TestCase):
    """Test case for the AssemblyListView."""

    def setUp(self) -> None:
        self.client = Client()
        self.part_set = factories.AssemblyFactory.create_batch(3)
        self.part1 = factories.AssemblyFactory(
            designation='10.00', name='assembly_1'
        )
        self.part2 = factories.AssemblyFactory(
            designation='20.00', name='assembly_2'
        )
        self.part3 = factories.AssemblyFactory(
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
        part_list = response.context['assemblies']
        self.assertIn(self.part3, part_list)
        self.assertNotIn(self.part1, part_list)
        self.assertNotIn(self.part2, part_list)

    def test_assembly_name_search(self) -> None:
        response = self.client.get(
            reverse('assemblies:assembly_list'), {'search_query': 'bLy_2'}
        )
        part_list = response.context['assemblies']
        self.assertIn(self.part2, part_list)
        self.assertNotIn(self.part1, part_list)
        self.assertNotIn(self.part3, part_list)
