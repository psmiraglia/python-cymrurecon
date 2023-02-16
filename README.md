# Recon by Team Cymru

Python library for interacting with Recon REST API.

## Install and use

1.  Setup a Python 3 virtual environment

        $ virtualenv -p python3 .venv
        $ . .venv/bin/activate
        $ pip install -r requirements.txt

2.  Install the module

        $ pip install -e .

3.  Use it

    ~~~.py
    from cymrurecon import CymruRecon

    if __name__ == '__main__':
        username = 'alice'
        password = 's3cr3t'
        with CymruRecon(username=username, password=password) as cli:
            # list all jobs
            for job in cli.jobs.list():
                do_something(job)

            # get job details
            job_id = 123456
            details = cli.jobs.details(job_id)
            
            # download query results
            query_id = 789456
            f_name = 'results.json'
            with open(f_name, 'wb') as fp:
                f_size = cli.results.details(query_id, fp, format='json', data_variant='flows')
                print(f'File size: {f_size} bytes')
                fp.close()

            # delete job
            job_id = 123456
            details = cli.jobs.delete(job_id)
    ~~~

## References

*   [Recon](https://www.team-cymru.com/cyber-threat-hunting-tools)
