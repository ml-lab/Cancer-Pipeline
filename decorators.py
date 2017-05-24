def with_conda_environment(packages):

    def conda_decorator(template):

        def wrapper(*args, **kwargs):

            options, original_spec = template(*args, **kwargs)

            conda_spec = f'''

            env_dir=$(mktemp -d --tmpdir=/scratch/$SLURM_JOBID)
            conda create -y -q --prefix ${{env_dir}} {' '.join(packages)}
            source activate ${{env_dir}}

            {original_spec}

            source deactivate
            rm -fr ${{env_dir}}

            '''

            return options, conda_spec

        return wrapper

    return conda_decorator
