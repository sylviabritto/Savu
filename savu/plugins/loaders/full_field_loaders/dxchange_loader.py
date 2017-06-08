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
.. module:: dxchange_loader
   :platform: Unix
   :synopsis: Load tomography data in dxchange format.

.. moduleauthor:: Nicola Wadeson <scientificsoftware@diamond.ac.uk>

"""

import numpy as np

from savu.data.data_structures.data_types.data_plus_darks_and_flats import \
    NoImageKey
from savu.plugins.loaders.full_field_loaders.nxtomo_loader import NxtomoLoader
from savu.plugins.utils import register_plugin


@register_plugin
class DxchangeLoader(NxtomoLoader):
    """
    A class to load tomography data from a hdf5 file

    :param data_path: Path to the data. Default: 'exchange/data'.
    :param dark: dark data path and scale \
        value. Default: ['exchange/data_dark', 1].
    :param flat: flat data path and scale \
        value. Default: ['exchange/data_white', 1].
    :u*param logfile: path to the log file. Default: None.

    :*param angles: Hidden. Default: [1, 2, 3].
    :~param image_key_path: Not required Default: None.
    """

    def __init__(self, name='DxchangeLoader'):
        super(DxchangeLoader, self).__init__(name)

    def _set_dark_and_flat(self, data_obj):
        data_obj.data = NoImageKey(data_obj, None, 0)
        self._set_data(data_obj, 'flat', data_obj.data._set_flat_path)
        self._set_data(data_obj, 'dark', data_obj.data._set_dark_path)

    def _set_data(self, data_obj, name, func):
        entry, scale = self.parameters[name]
        ffile = data_obj.backing_file
        func(ffile[entry])
        data_obj.data._set_scale(name, scale)

    def _set_rotation_angles(self, data_obj):
        # set parameters here
        with open(self.parameters['logfile'], 'r') as fp:
            for i, line in enumerate(fp):
                if i == 23:
                    n_proj = int(line.split(':')[1].strip())
        angles = np.linspace(0, 180, n_proj)
        data_obj.meta_data.set("rotation_angle", angles)
        return len(angles)
