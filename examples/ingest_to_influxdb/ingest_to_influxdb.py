#!/usr/bin/env python

import json
import os

from influxdb_client import InfluxDBClient, Point

from cymrurecon import CymruRecon


def to_point(data):
    return Point.from_dict(
        data,
        record_measurement_key='query_type',
        record_time_key='start_time',
        record_tag_keys=[
            'client_cc',
            'client_ip_addr',
            'dst_cc',
            'dst_ip_addr',
            'dst_ip_categories',
            'server_cc',
            'server_ip_addr',
            'src_cc',
            'src_ip_addr',
            'src_ip_categories',
        ],
        record_field_keys=[
            'client_port',
            'dst_port',
            'num_octets',
            'num_pkts',
            'proto',
            'sample_algo',
            'sample_interval',
            'server_port',
            'src_port',
            'tcp_flags',
        ],
    )


if __name__ == '__main__':
    recon_api_key = os.getenv('RECON_API_KEY',
                              '0000000000000000000000000000000000000000')
    recon_query_id = os.getenv('RECON_QUERY_ID',
                               '00000000')
    influxdb_url = os.getenv('INFLUXDB_URL',
                             'http://localhost:8086')
    influxdb_token = os.getenv('INFLUXDB_TOKEN',
                               '00000000-0000-0000-0000-000000000000')
    influxdb_org = os.getenv('INFLUXDB_ORG',
                             'acme')
    influxdb_bucket = os.getenv('INFLUXDB_BUCKET',
                                'my-bucket')

    #
    # Get data from TeamCymru Recon
    #

    f_format = 'json'
    f_name = f'recon-query-{recon_query_id}.{f_format}'
    with CymruRecon(api_key=recon_api_key) as recon:
        with open(f_name, 'wb') as fp:
            f_size = recon.results.details(recon_query_id,
                                           fp,
                                           format=f_format,
                                           data_variant='flows')
            fp.close()
            print(f'File size: {f_size} bytes')

    #
    # Ingest into InfluxDB
    #

    with InfluxDBClient(url=influxdb_url,
                        token=influxdb_token,
                        org=influxdb_org,
                        debug=False) as influxdb:
        with influxdb.write_api() as write_api:
            with open(f_name, 'rb') as fp:
                count = 0
                for line in fp:
                    data = json.loads(line)
                    point = to_point(data)
                    write_api.write(bucket=influxdb_bucket, record=point)
                    count += 1
                fp.close()
            print(f'Ingested records: {count}')
            write_api.close()
