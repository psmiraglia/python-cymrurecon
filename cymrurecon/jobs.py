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
import re

from restfly.endpoint import APIEndpoint

LOG = logging.getLogger(__name__)
DATE_FMT = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$'


class JobsIterator:
    # query
    _per_page = 10
    _page = 1

    # total number of jobs
    count = 0
    total = 1

    # current page of results
    page = []
    page_count = 0

    # debug
    _pages_requested = 1

    def __init__(self, api, path, params, **kwargs):
        self._api = api
        self._path = path
        self._params = params

    def _get_page(self):
        # make the API call
        resp = self._get_data()

        # obtain last_page
        self.total = resp.get('total')

        # reset the page counter and get the data
        self.page_count = 0
        self.page = resp.get('data', [])

        # debug
        LOG.debug(f'Requested pages: {self._pages_requested}')
        LOG.debug(f'Records in current page: {len(self.page)}')
        self._pages_requested += 1

    def _get_data(self):
        # build the query with pagination params
        params = self._params
        params['page'] = self._page
        params['per_page'] = self._per_page

        # make the API call
        resp = self._api.get(self._path, params=params).json()

        # increase the "page" parameter for the next call
        self._page += 1

        return resp

    def __iter__(self):
        return self

    def __next__(self):
        return self.next()

    def next(self):
        # ending conditions
        if self.count >= self.total:
            raise StopIteration()

        if self.page_count >= len(self.page) and self.count <= self.total:
            # ask for a new page
            self._get_page()
            if len(self.page) == 0:
                raise StopIteration()

        # consume the iterator
        job = self.page[self.page_count]
        self.count += 1
        self.page_count += 1

        LOG.debug(f'Consumed {self.count} of {self.total} jobs')
        return job


class JobsAPIEndpoint(APIEndpoint):
    _path = 'jobs'

    def list(self, **kwargs):
        params = {}

        # start_date, end_date
        # fmt: 2019-08-01T00:00:00Z
        for key in ['start_date', 'end_date']:
            par = kwargs.pop(key, None)
            if par:
                if re.search(DATE_FMT, par):
                    params[key] = par
                else:
                    raise Exception(f'Bad format for "{key}": {par}')

        # system_origin
        # values: schedule, web, api
        key = 'system_origin'
        par = kwargs.pop(key, None)
        if par:
            if par in ['schedule', 'web', 'api']:
                params[key] = par
            else:
                raise Exception(f'Value not allowed for "{key}": {par}')

        # status
        # values: completed, started, pending
        key = 'status'
        par = kwargs.pop(key, None)
        if par:
            if par in ['completed', 'started', 'pending']:
                params[key] = par
            else:
                raise Exception(f'Value not allowed for "{key}": {par}')

        # other parameters
        for key in ['search', 'group_id', 'page', 'per_page']:
            par = kwargs.pop(key, None)
            if par:
                params[key] = par

        return JobsIterator(self._api, self._path, params)

    def create(self, job_name, start_date, end_date, queries, **kwargs):
        params = {
            'job_name': job_name,
            'queries': queries
        }

        # start_date
        if re.search(DATE_FMT, start_date):
            params['start_date'] = start_date
        else:
            raise Exception(f'Bad format for "start_date": {start_date}')

        # end_date
        if re.search(DATE_FMT, end_date):
            params['end_date'] = end_date
        else:
            raise Exception(f'Bad format for "end_date": {end_date}')

        # priority
        key = 'priority'
        par = kwargs.pop(key, None)
        if par:
            if par >= 1 and par <= 100:
                params[key] = par
            else:
                raise Exception(f'Value not allowed for "{key}": {par}')

        # optional parameters
        for k in ['job_description', 'timeout', 'group_id']:
            v = kwargs.pop(k)
            if v:
                params[k] = v

        return self._api.post(self._path, params=params).json()

    def details(self, job_id, **kwargs):
        return self._api.get(f'{self._path}/{job_id}/details').json()

    def results(self, job_id, **kwargs):
        params = {}

        # format
        key = 'format'
        par = kwargs.pop(key, None)
        if par:
            if par in ['csv', 'json', 'xml', 'xslx']:
                params[key] = par
            else:
                raise Exception(f'Value not allowed for "{key}": {par}')

        return self._api.get(f'{self._path}/{job_id}', params=params)

    def delete(self, job_id, **kwargs):
        return self._api.delete(f'{self._path}/{job_id}')
