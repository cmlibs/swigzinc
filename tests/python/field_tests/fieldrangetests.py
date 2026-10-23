"""
PyZinc Unit Tests

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

'''
Created on May 23, 2013

@author: hsorby
'''
import os
import unittest

from cmlibs.zinc.context import Context
from cmlibs.zinc.result import RESULT_OK


class FieldrangeTestCase(unittest.TestCase):

    def setUp(self):
        self._context = Context("fieldrange")
        self._root_region = self._context.getDefaultRegion()
        self._fieldmodule = self._root_region.getFieldmodule()

    def tearDown(self):
        del self._fieldmodule
        del self._root_region
        del self._context

    def testEvaluateFieldrange(self):
        """
        Test that python wrappers for Fieldrange APIs work.
        """
        path = os.path.dirname(os.path.realpath(__file__))
        result = self._root_region.readFile(path + '/../resource/cube.exformat')
        self.assertEqual(RESULT_OK, result)

        coordinates = self._fieldmodule.findFieldByName("coordinates")
        self.assertTrue(coordinates.isValid())

        mesh3d = self._fieldmodule.findMeshByDimension(3)
        element1 = mesh3d.findElementByIdentifier(1)
        self.assertTrue(element1.isValid())

        fieldcache = self._fieldmodule.createFieldcache()
        fieldrange = fieldcache.createFieldrange()
        self.assertTrue(fieldrange.isValid())

        self.assertEqual(RESULT_OK, fieldcache.setElement(element1))
        self.assertEqual(RESULT_OK, coordinates.evaluateFieldrange(fieldcache, fieldrange))
        self.assertTrue(fieldrange.hasValidRange())
        self.assertEqual(coordinates, fieldrange.getField())

        TOL = 1.0E-8
        element, xi = fieldrange.getComponentMinimumMeshLocation(1, 3)
        self.assertEqual(element1, element)
        self.assertAlmostEqual(0.0, xi[0], delta=TOL)
        self.assertAlmostEqual(0.0, xi[1], delta=TOL)
        self.assertAlmostEqual(0.0, xi[2], delta=TOL)
        element, xi = fieldrange.getComponentMaximumMeshLocation(1, 3)
        self.assertEqual(element1, element)
        self.assertAlmostEqual(1.0, xi[0], delta=TOL)
        self.assertAlmostEqual(0.0, xi[1], delta=TOL)
        self.assertAlmostEqual(0.0, xi[2], delta=TOL)
        result, x = fieldrange.getComponentMinimumValuesReal(1, 3)
        self.assertEqual(RESULT_OK, result)
        self.assertAlmostEqual(0.0, x[0], delta=TOL)
        self.assertAlmostEqual(0.0, x[1], delta=TOL)
        self.assertAlmostEqual(0.0, x[2], delta=TOL)
        result, x = fieldrange.getComponentMaximumValuesReal(1, 3)
        self.assertEqual(RESULT_OK, result)
        self.assertAlmostEqual(1.0, x[0], delta=TOL)
        self.assertAlmostEqual(0.0, x[1], delta=TOL)
        self.assertAlmostEqual(0.0, x[2], delta=TOL)
        result, minimums, maximums = fieldrange.getRangeReal(3)
        self.assertEqual(RESULT_OK, result)
        self.assertAlmostEqual(0.0, minimums[0], delta=TOL)
        self.assertAlmostEqual(0.0, minimums[1], delta=TOL)
        self.assertAlmostEqual(0.0, minimums[2], delta=TOL)
        self.assertAlmostEqual(1.0, maximums[0], delta=TOL)
        self.assertAlmostEqual(1.0, maximums[1], delta=TOL)
        self.assertAlmostEqual(1.0, maximums[2], delta=TOL)


def suite():
    # import ImportTestCase
    tests = unittest.TestSuite()
    tests.addTests(unittest.TestLoader().loadTestsFromTestCase(FieldrangeTestCase))
    return tests


if __name__ == '__main__':
    unittest.TextTestRunner().run(suite())
