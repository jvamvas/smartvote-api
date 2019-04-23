import json
from unittest import TestCase

from requests import HTTPError

from smartvote import elections
from smartvote.client import Client


class SmartVoteAPITestCase(TestCase):

    def setUp(self) -> None:
        self.client = Client(election_id=elections.CH_NR_15)

    def _pretty_print(self, response):
        print(json.dumps(response, indent=2))

    def test_get_languages(self):
        response = self.client.get_languages()
        self._pretty_print(response)

    def test_get_election(self):
        response = self.client.get_election()
        self._pretty_print(response)

    def test_languages(self):
        for language in [
            'de',
            'fr',
            'it',
            'rm',
            'en',
        ]:
            client = Client(election_id=elections.CH_NR_15, language=language)
            response = client.get_election()
            print(response['name'])

    def test_get_election_statistics(self):
        response = self.client.get_election_statistics()
        self._pretty_print(response)

    def test_get_constituencies(self):
        response = self.client.get_constituencies()
        self._pretty_print(response)

    def test_get_constituency(self):
        response = self.client.get_constituency(constituency_id=18800000004)
        self._pretty_print(response)

    def test_get_constituency_statistics(self):
        response = self.client.get_constituency_statistics(constituency_id=18800000022)
        self._pretty_print(response)

    def test_get_parties(self):
        response = self.client.get_parties(root_parties=True)
        self._pretty_print(response)

    def test_get_parties_by_constituency(self):
        response = self.client.get_parties(root_parties=False, constituency_id=18800000004)
        self._pretty_print(response)

    def test_get_party(self):
        response = self.client.get_party(party_id=18800001494)
        self._pretty_print(response)

    def test_get_lists(self):
        response = self.client.get_lists()
        self._pretty_print(response)

    def test_get_lists_by_constituency(self):
        response = self.client.get_lists(constituency_id=18800000004)
        self._pretty_print(response)

    def test_get_lists_by_party(self):
        response = self.client.get_lists(party_id=18800003411)
        self._pretty_print(response)

    def test_get_list(self):
        response = self.client.get_list(list_id=18800023982)
        self._pretty_print(response)

    def test_get_candidates_by_constituency(self):
        response = self.client.get_candidates(constituency_id=18800000004)
        self._pretty_print(response)

    def test_get_candidates_by_party(self):
        response = self.client.get_candidates(party_id=18800001494)
        self._pretty_print(response)

    def test_get_candidates_by_list(self):
        response = self.client.get_candidates(list_id=18800023982)
        self._pretty_print(response)

    def test_get_candidates_by_other_options(self):
        response = self.client.get_candidates(
            firstname='Petra',
            lastname='Gössi',
            age_from=18,
            age_until=99,
            gender='f',
            has_smartvote_profile=True,
            is_elected=True,
            is_incumbent=True,
        )
        self._pretty_print(response)

    def test_get_candidate(self):
        response = self.client.get_candidate(candidate_id=18800023984)
        self._pretty_print(response)

    def test_get_questionnaire(self):
        response = self.client.get_questionnaire()
        self._pretty_print(response)

    def test_get_smartspider_by_candidate(self):
        response = self.client.get_smartspider(responder_id=18800023984)
        self._pretty_print(response)

    def test_get_smartspider_by_list(self):
        response = self.client.get_smartspider(responder_id=18800001009)
        self._pretty_print(response)

    def test_get_answers_by_candidate(self):
        response = self.client.get_answers(responder_id=18800023984)
        self._pretty_print(response)

    def test_get_answers_by_list(self):
        response = self.client.get_answers(responder_id=18800001009)
        self._pretty_print(response)

    def test_invalid_request(self):
        with self.assertRaises(HTTPError):
            self.client._make_request('get', '/invalid-url')
