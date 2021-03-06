# Copyright (c) 2016, MD2K Center of Excellence
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
# list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import datetime
import gzip
import os
import unittest
from random import random

import pytz

from cerebralcortex.data_processor.signalprocessing.accelerometer import window_std_dev, accelerometer_features
from cerebralcortex.kernel.datatypes.datapoint import DataPoint
from cerebralcortex.kernel.datatypes.datastream import DataStream


class TestAccelerometer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super(TestAccelerometer, cls).setUpClass()
        tz = pytz.timezone('US/Eastern')
        cls.accelx = []
        with gzip.open(os.path.join(os.path.dirname(__file__), 'res/accelx.csv.gz'), 'rt') as f:
            for l in f:
                values = list(map(int, l.split(',')))
                cls.accelx.append(
                    DataPoint.from_tuple(datetime.datetime.fromtimestamp(values[0] / 1000000.0, tz=tz), values[1]))

        cls.accely = []
        with gzip.open(os.path.join(os.path.dirname(__file__), 'res/accely.csv.gz'), 'rt') as f:
            for l in f:
                values = list(map(int, l.split(',')))
                cls.accely.append(
                    DataPoint.from_tuple(datetime.datetime.fromtimestamp(values[0] / 1000000.0, tz=tz), values[1]))

        cls.accelz = []
        with gzip.open(os.path.join(os.path.dirname(__file__), 'res/accelz.csv.gz'), 'rt') as f:
            for l in f:
                values = list(map(int, l.split(',')))
                cls.accelz.append(
                    DataPoint.from_tuple(datetime.datetime.fromtimestamp(values[0] / 1000000.0, tz=tz), values[1]))

    def setUp(self):
        self.size = 100000
        self.ds = DataStream(None, None)
        data = [DataPoint.from_tuple(datetime.datetime.now(), [random()]) for i in range(0, self.size)]
        self.ds.datapoints = data

    def test_window_std_dev(self):
        ts = datetime.datetime.now(tz=pytz.timezone('US/Central'))
        dev = window_std_dev(self.ds.datapoints, ts)
        self.assertEqual(dev.start_time, ts)
        self.assertAlmostEqual(dev.sample, 0.2886751346, delta=0.01)

    def test_window_std_dev_sample_data(self):
        ts = datetime.datetime.now(tz=pytz.timezone('US/Central'))
        ax = window_std_dev(self.accelx, ts)
        self.assertEqual(ax.start_time, ts)
        self.assertAlmostEqual(ax.sample, 32.6139, delta=0.001)

        ay = window_std_dev(self.accely, ts)
        self.assertEqual(ay.start_time, ts)
        self.assertAlmostEqual(ay.sample, 19.72426, delta=0.001)

        az = window_std_dev(self.accelz, ts)
        self.assertEqual(az.start_time, ts)
        self.assertAlmostEqual(az.sample, 37.00211, delta=0.001)

    def test_window_std_dev_one(self):
        ts = datetime.datetime.now(tz=pytz.timezone('US/Central'))
        dev = window_std_dev([DataPoint.from_tuple(ts, 10)], ts)
        self.assertEqual(dev.sample, 0.0)

    def test_accelerometer_features(self):
        ds = DataStream(None, None)

        data = []
        # TODO: Fix the test case once timestamp correction and sequence alignment is written
        for i in range(min(len(self.accelx), len(self.accely), len(self.accelz))):
            data.append(DataPoint.from_tuple(self.accelx[i].start_time, [self.accelx[i].sample,
                                                                         self.accely[i].sample,
                                                                         self.accelz[i].sample]))

        ds.datapoints = data

        accelerometer_magnitude, accelerometer_win_mag_deviations, accel_activity = accelerometer_features(ds)

        self.assertEqual(len(accelerometer_magnitude.datapoints), 62870)
        self.assertEqual(len(accelerometer_win_mag_deviations.datapoints), 687)
        self.assertEqual(len(accel_activity.datapoints), 687)

        self.assertEqual(len([dp for dp in accel_activity.datapoints if dp.sample]),
                         0)  # TODO: Is this correct


if __name__ == '__main__':
    unittest.main()
