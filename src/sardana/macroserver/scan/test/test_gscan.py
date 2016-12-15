#!/usr/bin/env python

##############################################################################
##
## This file is part of Sardana
##
## http://www.tango-controls.org/static/sardana/latest/doc/html/index.html
##
## Copyright 2011 CELLS / ALBA Synchrotron, Bellaterra, Spain
##
## Sardana is free software: you can redistribute it and/or modify
## it under the terms of the GNU Lesser General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
##
## Sardana is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU Lesser General Public License for more details.
##
## You should have received a copy of the GNU Lesser General Public License
## along with Sardana.  If not, see <http://www.gnu.org/licenses/>.
##
##############################################################################

SKIP_TEST = False

try:
    from mock import MagicMock, patch
except ImportError:
    SKIP_TEST = True

from taurus.external import unittest
from taurus.test import insertTest

from sardana.taurus.core.tango.sardana.pool import Motor
from sardana.macroserver.msexception import UnknownEnv

@insertTest(helper_name='prepare_waypoint', conf={"acc_time": 0.1,
                                                  "dec_time": 0.1,
                                                  "base_rate": 0,
                                                  "start_user_pos": 0,
                                                  "final_user_pos": 10},
            expected={"initial_pos": -5,
                      "final_pos": 15})
class CTScanTestCase(unittest.TestCase):

    def setUp(self):
        if SKIP_TEST:
            self.skipTest("mock module is not available")

    @staticmethod
    def getEnv(name):
        if name == "ActiveMntGrp":
            return "MockMntGrp"
        elif name == "ScanID":
            return 1
        elif name == "ScanDir":
            return "/tmp"
        elif name == "ScanFile":
            return "MockFile.dat"
        raise UnknownEnv

    @patch("sardana.macroserver.msparameter.Type")
    def prepare_waypoint(self, MockType, conf, expected):
        from sardana.macroserver.scan.gscan import CTScan
        mock_motor = MagicMock(Motor)
        mock_motor.getBaseRate = MagicMock(return_value=conf["base_rate"])

        macro = MagicMock()
        macro.getMinAccTime
        macro.getEnv = self.getEnv
        scan = CTScan(macro)
        scan.get_min_acc_time = MagicMock(return_value=conf["acc_time"])
        scan.get_min_dec_time = MagicMock(return_value=conf["dec_time"])
        scan._physical_moveables = [mock_motor]
        waypoint = {
            "positions": [conf["final_user_pos"]],
            "active_time": 0.1
        }
        start_positions = [conf["start_user_pos"]]
        ideal_paths, _, _ =  scan.prepare_waypoint(waypoint, start_positions)
        path = ideal_paths[0]
        # Asserts
        msg = 'Initial positions do not math. (expected={0}, got={1})'.format(
            expected["initial_pos"], path.initial_pos)
        self.assertEqual(path.initial_pos, expected["initial_pos"], msg)
        msg = 'Final positions do not math. (expected={0}, got={1})'.format(
            expected["final_pos"], path.final_pos)
        self.assertEqual(path.final_pos, expected["final_pos"], msg)
