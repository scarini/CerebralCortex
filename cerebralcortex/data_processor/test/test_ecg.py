# Copyright (c) 2017, MD2K Center of Excellence
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

import unittest

from cerebralcortex.data_processor.signalprocessing.ecg import rr_interval_update, check_peak


class TestECG(unittest.TestCase):
    def setUp(self):
        pass

    def test_classify_ecg_window(self):
        # TODO: Complete this test
        pass

    def test_filter_bad_ecg(self):
        # TODO: Complete this test
        pass

    def test_compute_rr_intervals(self):
        # TODO: Complete this test
        pass

    def test_rr_interval_update(self):
        rpeak_temp1 = [i for i in range(0, 100, 10)]
        rr_ave = 4.5
        self.assertEqual(rr_interval_update(rpeak_temp1, rr_ave), 10.0)

    def test_rr_interval_update_small(self):
        rpeak_temp1 = [i for i in range(0, 100, 100)]
        rr_ave = 4.5
        self.assertEqual(rr_interval_update(rpeak_temp1, rr_ave), 4.5)

    def test_rr_interval_update_min_size(self):
        rpeak_temp1 = [i for i in range(0, 100, 10)]
        rr_ave = 4.5
        self.assertEqual(rr_interval_update(rpeak_temp1, rr_ave, min_size=4), 10)
        self.assertEqual(rr_interval_update(rpeak_temp1, rr_ave, min_size=1), 10)
        self.assertEqual(rr_interval_update(rpeak_temp1, rr_ave, min_size=10), 9)
        self.assertEqual(rr_interval_update(rpeak_temp1, rr_ave, min_size=25), 4.5)

    def test_compute_moving_window_int(self):
        # TODO: Complete this test
        pass

    def test_check_peak(self):
        data = [0, 1, 2, 1, 0]
        self.assertTrue(check_peak(data))

        data = [0, 1, 0, 1, 0]
        self.assertFalse(check_peak(data))

        data = [0, 1, 2, 3, 4, 3, 2, 1]
        self.assertTrue(check_peak(data))

        data = [0, 1]
        self.assertRaises(Exception, check_peak, data)

    def test_compute_r_peaks(self):
        # TODO: Complete this test
        pass

    def test_remove_close_peaks(self):
        # TODO: Complete this test
        pass

    def test_confirm_peaks(self):
        # TODO: Complete this test
        pass

    def test_detect_rpeak(self):
        # TODO: Complete this test
        pass

    def test_emwa(self):
        # TODO: Complete this test
        pass


if __name__ == '__main__':
    unittest.main()
