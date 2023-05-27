from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse
from parts import factories


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
