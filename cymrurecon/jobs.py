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


class JobsAPIEndpoint(APIEndpoint):
    _path = 'jobs'

    def list(self, **kwargs):
        params = {}
        # optional parameters
        for k in ['search', 'group_id', 'start_date', 'end_date',
                  'system_origin', 'status', 'page', 'per_page']:
            v = kwargs.get(k)
            if v:
                params[k] = v
        return self._api.get(self._path, params=params).json()

    def create(self, job_name, start_date, end_date, queries, **kwargs):
        # mandatory parameters
        params = {
            'end_date': end_date,
            'job_name': job_name,
            'queries': queries,
            'start_date': start_date
        }

        # optional parameters
        for k in ['job_description', 'timeout', 'priority', 'group_id']:
            v = kwargs.get(k)
            if v:
                params[k] = v

        return self._api.post(self._path, params=params).json()

    def details(self, job_id, **kwargs):
        return self._api.get(f'{self._path}/{job_id}/details').json()

    def results(self, job_id, **kwargs):
        params = {}
        # optional parameters
        for k in ['format']:
            v = kwargs.get(k)
            if v:
                params[k] = v
        return self._api.get(f'{self._path}/{job_id}', params=params)

    def delete(self, job_id, **kwargs):
        return self._api.delete(f'{self._path}/{job_id}')
