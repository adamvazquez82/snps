"""
Copyright (C) 2017 Andrew Riha

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""

import os
import warnings

import pytest


@pytest.fixture(scope='module')
def resource():
    from lineage.resources import Resources
    return Resources(resources_dir='resources')


@pytest.fixture(scope='module')
def resource_assembly_mapping():
    from lineage.resources import Resources
    from lineage.ensembl import EnsemblRestClient
    return Resources(resources_dir='resources', ensembl_rest_client=EnsemblRestClient())


def test_get_genetic_map_HapMapII_GRCh37(resource):
    genetic_map_HapMapII_GRCh37 = resource.get_genetic_map_HapMapII_GRCh37()
    assert len(genetic_map_HapMapII_GRCh37) == 23


def test_get_cytoBand_hg19(resource):
    cytoBand_hg19 = resource.get_cytoBand_hg19()
    assert len(cytoBand_hg19) == 862


def test_get_knownGene_hg19(resource):
    knownGene_hg19 = resource.get_knownGene_hg19()
    assert len(knownGene_hg19) == 82960


def test_get_kgXref_hg19(resource):
    kgXref_hg19 = resource.get_kgXref_hg19()
    assert len(kgXref_hg19) == 82960


def test_get_assembly_mapping_data_bad_tar(resource_assembly_mapping):
    with open('resources/NCBI36_GRCh37.tar.gz', 'w'):
        pass
    assembly_mapping_data = resource_assembly_mapping.get_assembly_mapping_data('NCBI36', 'GRCh37')
    assert len(assembly_mapping_data) == 25


def test_get_assembly_mapping_data(resource_assembly_mapping):
    assembly_mapping_data = resource_assembly_mapping.get_assembly_mapping_data('NCBI36', 'GRCh37')
    assert len(assembly_mapping_data) == 25


def test_get_all_resources(resource_assembly_mapping):
    resources = resource_assembly_mapping.get_all_resources()
    for k, v in resources.items():
        if v is None:
            assert False
    assert True


def test__all_chroms_in_tar(resource_assembly_mapping):
    assert not resource_assembly_mapping._all_chroms_in_tar(['PAR'], 'resources/NCBI36_GRCh37.tar.gz')


def test_get_assembly_mapping_data_no_EnsemblRestClient(resource):
    assembly_mapping_data = resource.get_assembly_mapping_data('NCBI36', 'GRCh37')
    assert assembly_mapping_data == None


def test_get_assembly_mapping_data_invalid_dir(resource_assembly_mapping):
    resource_assembly_mapping._resources_dir = None
    assembly_mapping_data = resource_assembly_mapping.get_assembly_mapping_data('NCBI36', 'GRCh37')
    assert assembly_mapping_data is None


def test_download_example_datasets(resource):
    paths = resource.download_example_datasets()

    for path in paths:
        if path is None or not os.path.exists(path):
            warnings.warn('Example dataset(s) not currently available')
            return

    assert True


def test__load_genetic_map_None(resource):
    result = resource._load_genetic_map(None)
    assert result is None


def test__load_cytoBand_None(resource):
    result = resource._load_cytoBand(None)
    assert result is None


def test__load_knownGene_None(resource):
    result = resource._load_knownGene(None)
    assert result is None


def test__load_kgXref_None(resource):
    result = resource._load_kgXref(None)
    assert result is None


def test__load_assembly_mapping_data_None(resource):
    result = resource._load_assembly_mapping_data(None)
    assert result is None


def test__download_file_compress(resource):
    result = resource._download_file('', '', compress=True)
    assert result is None


def test__download_file_invalid_dir(resource):
    resource._resources_dir = None
    result = resource._download_file('', '')
    assert result is None
