import json
import logging
from time import sleep
from typing import Union

import requests


class SmartvoteApiError(Exception):
    pass


class Client:

    def __init__(self,
                 election_id: int,
                 api_url: str = 'https://api.smartvote.ch',
                 language: str = 'en',
                 timeout: int = 30,
                 delay: float = 0,
                 ) -> None:
        self.election_id = election_id
        self.url = api_url.rstrip('/')
        self.session = requests.Session()
        self.base_params = {
            'lang': language,
        }
        self.timeout = timeout
        self.delay = delay
        self._refresh_token()

    def get_languages(self) -> list:
        return self._make_request('get', '/2.0/languages')

    def get_election(self) -> dict:
        return self._make_request('get', '/2.0/elections/{}'.format(self.election_id))

    def get_election_statistics(self) -> dict:
        return self._make_request('get', '/2.0/elections/{}/statistics'.format(self.election_id))

    def get_constituencies(self) -> list:
        return self._make_request('get', '/2.0/elections/{}/constituencies'.format(self.election_id))

    def get_constituency(self, constituency_id: int = None) -> dict:
        return self._make_request('get',
                                  '/2.0/elections/{}/constituencies/{}'.format(self.election_id, constituency_id))

    def get_constituency_statistics(self, constituency_id: int) -> dict:
        return self._make_request('get', '/2.0/elections/{}/constituencies/{}/statistics'.format(self.election_id,
                                                                                                 constituency_id))

    def get_parties(self, constituency_id: int = None, root_parties: bool = True) -> list:
        params = {}
        if constituency_id is not None:
            params['constituencyId'] = constituency_id
        if root_parties is not None:
            params['rootParties'] = str(root_parties).lower()
        return self._make_request('get', '/2.0/elections/{}/parties'.format(self.election_id), params=params)

    def get_party(self, party_id: int = None) -> dict:
        return self._make_request('get', '/2.0/elections/{}/parties/{}'.format(self.election_id, party_id))

    def get_lists(self, constituency_id: int = None, party_id: int = None) -> list:
        params = {}
        if constituency_id is not None:
            params['constituencyId'] = constituency_id
        if party_id is not None:
            params['partyId'] = party_id
        return self._make_request('get', '/2.0/elections/{}/lists'.format(self.election_id), params=params)

    def get_list(self, list_id: int = None) -> dict:
        return self._make_request('get', '/2.0/elections/{}/lists/{}'.format(self.election_id, list_id))

    def get_candidates(self,
                       constituency_id: int = None,
                       party_id: int = None,
                       list_id: int = None,
                       firstname: str = None,
                       lastname: str = None,
                       age_from: int = None,
                       age_until: int = None,
                       gender: str = None,
                       has_smartvote_profile: bool = None,
                       is_elected: bool = None,
                       is_incumbent: bool = None,
                       ) -> list:
        params = {}
        if constituency_id is not None:
            params['constituencyId'] = constituency_id
        if party_id is not None:
            params['partyId'] = party_id
        if list_id is not None:
            params['listId'] = list_id
        if firstname is not None:
            params['firstname'] = firstname
        if lastname is not None:
            params['lastname'] = lastname
        if age_from is not None:
            params['ageFrom'] = age_from
        if age_until is not None:
            params['ageuntil'] = age_until
        if gender is not None:
            params['gender'] = gender
        if has_smartvote_profile is not None:
            params['hasSmartvoteProfile'] = str(has_smartvote_profile).lower()
        if is_elected is not None:
            params['isElected'] = str(is_elected).lower()
        if is_incumbent is not None:
            params['isIncumbent'] = str(is_incumbent).lower()
        return self._make_request('get', '/2.0/elections/{}/candidates'.format(self.election_id), params=params)

    def get_candidate(self, candidate_id: int = None) -> dict:
        return self._make_request('get', '/2.0/elections/{}/candidates/{}'.format(self.election_id, candidate_id))

    def get_questionnaire(self):
        return self._make_request('get', '/2.0/elections/{}/questionnaires'.format(self.election_id))

    def get_smartspider(self, responder_id: int = None) -> list:
        params = {}
        if responder_id is not None:
            params['responderId'] = responder_id
        return self._make_request('get', '/2.0/elections/{}/smartspiders'.format(self.election_id), params=params)

    def get_answers(self, responder_id: int = None) -> list:
        params = {}
        if responder_id is not None:
            params['responderId'] = responder_id
        return self._make_request('get', '/2.0/elections/{}/answers'.format(self.election_id), params=params)

    def _refresh_token(self) -> None:
        response = self._make_request('get', '/auth/token')
        token = response['token']
        self.session.headers.update({
            'x-auth-token': token
        })

    def _delay(self):
        sleep(self.delay)

    def _make_request(self, method, endpoint, params=None, data=None) -> Union[list, dict]:
        url = self.url + endpoint
        request_params = self.base_params
        if params is not None:
            request_params.update(params)
        response = self.session.request(method, url, params=request_params, data=data, timeout=self.timeout)
        if response.status_code == 401:
            self._refresh_token()
            response = self.session.request(method, url, params=request_params, data=data, timeout=self.timeout)
        response.raise_for_status()

        self._delay()

        try:
            return response.json()
        except json.decoder.JSONDecodeError:
            logging.error(response.text)
            raise SmartvoteApiError("Cannot parse the above response")
