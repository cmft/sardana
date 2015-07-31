from taurus.test.base import insertTest
from taurus.external import unittest

from sardana.pool.pooltggeneration import PoolTGGeneration

from sardana.pool.test import (FakePool, createPoolController,
                               createPoolTriggerGate, dummyPoolTGCtrlConf01,
                               dummyTriggerGateConf01, 
                               createPoolTGGenerationConfiguration)

@insertTest(helper_name='generation', offset=0, active_period=.1,
                                              passive_period=.1, repetitions=0)
@insertTest(helper_name='generation', offset=0, active_period=.01,
                                              passive_period=.01, repetitions=10)
@insertTest(helper_name='generation', offset=0, active_period=.01,
                                             passive_period=.02, repetitions=10)
@insertTest(helper_name='generation', offset=0, active_period=.01,
                                             passive_period=.05, repetitions=10)
class PoolDummyTriggerGateTestCase(unittest.TestCase):
    """Parameterizable integration test of the PoolTGGeneration action and
    the DummTriggerGateController.

    Using insertTest decorator, one can add tests of a particular trigger/gate
    characteristic.    
    """

    def setUp(self):
        """Create a Controller, TriggerGate and PoolTGGeneration objects from 
        dummy configurations
        """
        unittest.TestCase.setUp(self)
        pool = FakePool()

        dummy_tg_ctrl = createPoolController(pool, dummyPoolTGCtrlConf01)
        self.dummy_tg = createPoolTriggerGate(pool, dummy_tg_ctrl,
                                              dummyTriggerGateConf01)
        # marrying the element with the controller
        dummy_tg_ctrl.add_element(self.dummy_tg)

        self.cfg = createPoolTGGenerationConfiguration((dummy_tg_ctrl,),
                                                       ((self.dummy_tg,),))

        # marrying the element with the action
        self.tg_action = PoolTGGeneration(self.dummy_tg)
        self.tg_action.add_element(self.dummy_tg)

    def generation(self, offset, active_period, passive_period, repetitions):
        """Verify that the created PoolTGAction start_action starts correctly 
        the involved controller."""
        args = ()
        kwargs = {'config': self.cfg,
                  'offset': offset,
                  'active_period': active_period,
                  'passive_period': passive_period,
                  'repetitions': repetitions
                 }
        self.tg_action.start_action(*args, **kwargs)
        self.tg_action.action_loop()
        # TODO: add asserts applicable to a dummy controller e.g. listen to 
        # state changes and verify if the change ON->MOVING-ON was emitted

    def tearDown(self):
        unittest.TestCase.tearDown(self)