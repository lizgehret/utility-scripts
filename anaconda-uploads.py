#!/usr/bin/env python

import os
import re
import sys
import subprocess

# NOTES/REQS:
# this must be run by someone with write permissions for QIIME 2's anaconda account
# run `conda install anaconda-client` in the environment where you'll be running this script (if not already installed)

q2_packages = [
    "q2-alignment",
    "q2-composition",
    "q2-cutadapt",
    "q2-dada2",
    "q2-deblur",
    "q2-demux",
    "q2-diversity-lib",
    "q2-diversity-20",
    "q2-emperor",
    "q2-feature-classifier",
    "q2-feature-table",
    "q2-fragment-insertion",
    "q2-longitudinal",
    "q2-metadata",
    "q2-mystery-stew",
    "q2-phylogeny",
    "q2-quality-control",
    "q2-quality-filter",
    "q2-sample-classifier",
    "q2-stats",
    "q2-taxa",
    "q2-types",
    "q2-vizard",
    "q2-vsearch",
    "q2cli",
    "q2galaxy",
    "q2templates",
    "qiime2",
    "rescript"
]


def _download_pkgs(epoch):
    for opsys in ['linux-64', 'osx-64']:
        url = \
            f'https://packages.qiime2.org/qiime2/{epoch}/amplicon/released/{opsys}'
        subprocess.run(
            ['wget', '-r', url, '-nd', '-P', f'{epoch}-{opsys}']
        )


def _upload_pkg_files(epoch, pkgs=q2_packages):
    _download_pkgs(epoch=epoch)

    for pkg in pkgs:
        regex = rf"^{pkg}.*\.tar\.bz2$"
        re_obj = re.compile(regex)
        for opsys in ['linux-64', 'osx-64']:
            for _, _, files in os.walk(f'{epoch}-{opsys}'):
                for filename in files:
                    if re_obj.match(filename):
                        subprocess.run(
                            ['anaconda', 'upload', '-u', 'qiime2',
                             f'{epoch}-{opsys}/{filename}',
                             '-l', 'main', '-l', f'r{epoch}'])


def _remove_pkg_dirs(epoch):
    for opsys in ['linux-64', 'osx-64']:
        subprocess.run(['rm', '-rf', f'{epoch}-{opsys}'])


if __name__ == '__main__':
    rel_epoch = sys.argv[1]

    _upload_pkg_files(epoch=rel_epoch)
    _remove_pkg_dirs(epoch=rel_epoch)
