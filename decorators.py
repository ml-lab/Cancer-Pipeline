def with_conda_environment(packages):
    """Wraps gwf spec with a conda enviroment.

    This decorator assumes that gwf is run on a SLURM backend, and that a
    temporary folder /scratch/$SLURM_JOBID is available for the process.

    The wrapper first creates and activates a temporary conda enviroment with
    the packages specfied in the `packages` list. It then runs the original
    spec and finally deactivates and deletes the temporary enviroment.
    """

    def conda_decorator(template):

        def wrapper(*args, **kwargs):

            inputs, outputs, options, original_spec = template(*args, **kwargs)

            conda_spec = f'''

            env_dir=$(mktemp -d --tmpdir=/scratch/$SLURM_JOBID)
            conda create -y -q --prefix ${{env_dir}} {' '.join(packages)}
            source activate ${{env_dir}}

            {original_spec}

            source deactivate
            rm -fr ${{env_dir}}

            '''

            return inputs, outputs, options, conda_spec

        return wrapper

    return conda_decorator
