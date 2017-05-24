import os

from decorators import with_conda_environment


@with_conda_environment(packages=['trim-galore'])
def trim_paired_end_fastq(r1_file, r2_file, trimmed_r1_file, trimmed_r2_file, r1_trimming_report, r2_trimming_report):

    inputs = [r1_file, r2_file]
    outputs = [trimmed_r1_file, trimmed_r2_file, r1_trimming_report, r2_trimming_report]

    options = {

        'cores': 1,
        'memory': '4g',
        'walltime': '04:00:00'

    }

    r1_file_basename = os.path.basename(r1_file)
    r2_file_basename = os.path.basename(r2_file)

    assert r1_file_basename.endswith('.fastq.gz')
    assert r2_file_basename.endswith('.fastq.gz')

    # There is no way to control the name of output files in TrimGalore!
    trimmed_r1_file_basename = r1_file_basename.replace('.fastq.gz', '_val_1.fq.gz')
    trimmed_r2_file_basename = r2_file_basename.replace('.fastq.gz', '_val_2.fq.gz')

    spec = f'''

    tmp_dir=$(mktemp -d --tmpdir=/scratch/$SLURM_JOBID)

    trim_galore --paired {r1_file} {r2_file} -o ${{tmp_dir}}

    mv ${{tmp_dir}}/{trimmed_r1_file_basename} {trimmed_r1_file}
    mv ${{tmp_dir}}/{trimmed_r2_file_basename} {trimmed_r2_file}

    mv ${{tmp_dir}}/{r1_file_basename}_trimming_report.txt {r1_trimming_report}
    mv ${{tmp_dir}}/{r2_file_basename}_trimming_report.txt {r2_trimming_report}

    '''

    return inputs, outputs, options, spec
