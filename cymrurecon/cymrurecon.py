'''
Copyright 2023 Paolo Smiraglia <paolo.smiraglia@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

import base64
import logging

from restfly.session import APISession

from .jobs import JobsAPIEndpoint
from .results import ResultsAPIEndpoint

LOG = logging.getLogger(__name__)


class CymruRecon(APISession):
    _url = 'https://recon.cymru.com/api'

    def _authenticate(self, **kwargs):
        api_key = kwargs.get('api_key', None)
        username = kwargs.get('username', None)
        password = kwargs.get('password', None)

        if api_key:
            self._session.headers.update({
                'Authorization': f'Token {api_key}'
            })
            LOG.debug(f'Authenticated (apikey: {api_key})')
        elif username and password:
            basic = base64.b64encode(f'{username}:{password}'.encode()).decode()  # noqa
            LOG.debug(basic)
            self._session.headers.update({
                'Authorization': f'Basic {basic}'
            })
            LOG.debug(f'Authenticated (username: {username}, password: {password})')  # noqa
        else:
            LOG.error('Unable to authenticate')

    def _deauthenticate(self, **kwargs):
        self._session.headers.update({'Authorization': None})
        LOG.debug('Deauthenticated')

    @property
    def jobs(self):
        return JobsAPIEndpoint(self)

    @property
    def results(self):
        return ResultsAPIEndpoint(self)
