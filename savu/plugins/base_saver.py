# Copyright 2014 Diamond Light Source Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
.. module:: base_saver
   :platform: Unix
   :synopsis: A base class for all saver plugins

.. moduleauthor:: Nicola Wadeson <scientificsoftware@diamond.ac.uk>

"""

import h5py

from savu.plugins.plugin import Plugin


class BaseSaver(Plugin):
    """
    A base plugin from which all data saver plugins should inherit.

    :param in_datasets: A list of the dataset(s) to process. Default: [].
    :param out_datasets: A list of the dataset(s) to create. Default: [].
    :param pattern: How to slice the data. Default: 'VOLUME_XZ'.
    """

    def __init__(self, name="BaseSaver"):
        super(BaseSaver, self).__init__(name)
        self.frame = None

    def setup(self):
        in_pData = self.get_plugin_in_datasets()
        pattern = self.parameters['pattern']
        in_pData[0].plugin_data_setup(pattern, self.get_max_frames())

    def _link_datafile_to_nexus_file(self, name, filename, path):
        nxs_file = self.exp.nxs_file
        nxs_entry = '/entry/final_result_' + name
        nxs_entry = nxs_file[nxs_entry]
        nxs_entry.attrs['signal'] = 'data'
        data_entry = nxs_entry.name + '/data'

        if data_entry not in nxs_file:
            h5file = filename.split('/')[-1]
            nxs_file[data_entry] = h5py.ExternalLink(h5file, path)

#    def base_process(self):
#        self.frame = self.

    def _get_group_name(self, name):
        nPlugin = self.exp.meta_data.get('nPlugin')
        plugin_dict = \
            self.exp._get_experiment_collection()['plugin_dict'][nPlugin]
        return "%i-%s-%s" % (nPlugin, plugin_dict['name'], name)

    def get_frame(self):
        return self.frame

    def nInput_datasets(self):
        return 1

    def nOutput_datasets(self):
        return 0

    def get_max_frames(self):
        return 1
