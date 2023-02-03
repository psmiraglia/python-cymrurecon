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

import logging

from restfly.endpoint import APIEndpoint

LOG = logging.getLogger(__name__)


class ResultsAPIEndpoint(APIEndpoint):
    _path = 'results'

    def details(self, query_id, **kwargs):
        params = {}

        # format
        arg = kwargs.pop('format', None)
        if arg and arg in ['csv', 'json', 'xml', 'xlsx']:
            params['format'] = arg

        # data_variant
        arg = kwargs.pop('data_variant', None)
        if arg and arg in ['flows', 'conversations', 'initiators', 'historic']:
            params['data_variant'] = arg

        # other fields
        for key in kwargs:
            arg = kwargs.pop(key, None)
            if arg:
                params[key] = arg
        return self._api.get(f'{self._path}/{query_id}', params=params)

    def delete(self, query_id, **kwargs):
        return self._api.delete(f'{self._path}/{query_id}')
