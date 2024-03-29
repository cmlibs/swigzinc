"""
PyZinc Unit Tests

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

'''
Created on May 22, 2013

@author: hsorby
'''
import os
import sys
import unittest

from cmlibs.zinc.context import Context
from cmlibs.zinc.field import Field
from cmlibs.zinc.glyph import Glyph
from cmlibs.zinc.graphics import Graphics
from cmlibs.zinc.scenecoordinatesystem import SCENECOORDINATESYSTEM_LOCAL, SCENECOORDINATESYSTEM_WORLD, \
    ScenecoordinatesystemEnumFromString, ScenecoordinatesystemEnumToString
from cmlibs.zinc.sceneviewer import Sceneviewer
from cmlibs.zinc import status


class GraphicsTestCase(unittest.TestCase):

    def setUp(self):
        self.context = Context('graphicstest')
        self.root_region = self.context.getDefaultRegion()
        self.scene = self.root_region.getScene()

    def tearDown(self):
        del self.scene
        del self.root_region
        del self.context

    def testGraphicsCreation(self):
        graphics = self.scene.createGraphicsPoints()
        self.assertTrue(graphics.isValid())
        result = graphics.setFieldDomainType(Field.DOMAIN_TYPE_NODES)
        self.assertEqual(status.OK, result)
        attributes = graphics.getGraphicspointattributes()
        self.assertTrue(attributes.isValid())
        glyph_module = self.context.getGlyphmodule()
        glyph_module.defineStandardGlyphs()
        result = attributes.setGlyphShapeType(Glyph.SHAPE_TYPE_SPHERE)
        self.assertEqual(status.OK, result)
        result = attributes.setGlyphShapeType(Glyph.SHAPE_TYPE_INVALID)
        self.assertEqual(status.ERROR_ARGUMENT, result)
        shapeType = attributes.getGlyphShapeType()
        self.assertEqual(Glyph.SHAPE_TYPE_SPHERE, shapeType)

    def testGraphicsPointsSetBaseSize(self):
        graphics = self.scene.createGraphicsPoints()
        self.assertTrue(graphics.isValid())
        attributes = graphics.getGraphicspointattributes()
        result = attributes.setBaseSize([1])
        self.assertEqual(status.OK, result)
        result = attributes.setBaseSize([6, 2, 0.3])
        self.assertEqual(status.OK, result)
        result = attributes.setBaseSize(3)
        self.assertEqual(status.OK, result)

    def testGraphicsPointsGetBaseSize(self):
        graphics = self.scene.createGraphicsPoints()
        self.assertTrue(graphics.isValid())
        attributes = graphics.getGraphicspointattributes()
        result = attributes.setBaseSize(5.4)
        self.assertEqual(status.OK, result)
        base_size = attributes.getBaseSize(1)
        self.assertEqual(status.OK, base_size[0])
        self.assertEqual(5.4, base_size[1])
        attributes.setBaseSize([4.8, 2.1, 7])
        base_size = attributes.getBaseSize(3)
        self.assertEqual([4.8, 2.1, 7], base_size[1])

    def testSceneviewerBackgroundColour(self):
        svm = self.context.getSceneviewermodule()
        sv = svm.createSceneviewer(Sceneviewer.BUFFERING_MODE_DOUBLE, Sceneviewer.STEREO_MODE_MONO)
        result = sv.setBackgroundColourComponentRGB(0.3, 0.8, 0.65)
        self.assertEqual(status.OK, result)
        (result, rgb) = sv.getBackgroundColourRGB()
        self.assertEqual(status.OK, result)
        self.assertEqual([0.3, 0.8, 0.65], rgb)
        result = sv.setBackgroundColourRGB([0.1, 0.9, 0.4])
        self.assertEqual(status.OK, result)
        (result, rgb) = sv.getBackgroundColourRGB()
        self.assertEqual(status.OK, result)
        self.assertEqual([0.1, 0.9, 0.4], rgb)
        self.assertRaises(TypeError, sv.setBackgroundColourRGB, [3.0, 2.0])

    def testSceneExport(self):
        path = os.path.dirname(os.path.realpath(__file__))
        result = self.root_region.readFile(path + '/../resource/cube.exformat')
        self.assertEqual(status.OK, result)
        surfaces = self.scene.createGraphicsSurfaces()
        coordinatesField = self.root_region.getFieldmodule().findFieldByName("coordinates")
        self.assertTrue(coordinatesField.isValid())
        result = surfaces.setCoordinateField(coordinatesField)
        self.assertEqual(status.OK, result)
        si = self.scene.createStreaminformationScene()
        si.setIOFormat(si.IO_FORMAT_THREEJS)
        result = si.getNumberOfResourcesRequired()
        self.assertEqual(2, result)
        result = si.setIODataType(si.IO_DATA_TYPE_COLOUR)
        self.assertEqual(status.OK, result)
        memory_sr1 = si.createStreamresourceMemory()
        memory_sr2 = si.createStreamresourceMemory()
        result = self.scene.write(si)
        self.assertEqual(status.OK, result)
        result, outputBytes1 = memory_sr1.getBuffer()
        self.assertEqual(status.OK, result)
        self.assertIsNotNone(outputBytes1)
        self.assertTrue(b'Surfaces' in outputBytes1, 'keyword \'vertices\' not found')
        result, outputBytes2 = memory_sr2.getBuffer()
        self.assertEqual(status.OK, result)
        self.assertIsNotNone(outputBytes2)
        self.assertTrue(b'vertices' in outputBytes2, 'keyword \'vertices\' not found')

    def testGraphicsToGlyph(self):
        path = os.path.dirname(os.path.realpath(__file__))
        # print(path + '/../resource/cube.exformat')
        result = self.root_region.readFile(path + '/../resource/cube.exformat')
        self.assertEqual(status.OK, result)
        surfaces = self.scene.createGraphicsSurfaces()
        coordinatesField = self.root_region.getFieldmodule().findFieldByName("coordinates")
        self.assertTrue(coordinatesField.isValid())
        result = surfaces.setCoordinateField(coordinatesField)
        self.assertEqual(status.OK, result)
        glyphModule = self.context.getGlyphmodule()
        glyph = glyphModule.createStaticGlyphFromGraphics(surfaces)
        self.assertTrue(glyph.isValid())

    def testScenecoordinatesystem(self):
        self.assertEqual("LOCAL", ScenecoordinatesystemEnumToString(SCENECOORDINATESYSTEM_LOCAL))
        self.assertEqual("WORLD", ScenecoordinatesystemEnumToString(SCENECOORDINATESYSTEM_WORLD))
        self.assertEqual(SCENECOORDINATESYSTEM_LOCAL, ScenecoordinatesystemEnumFromString("LOCAL"))
        self.assertEqual(SCENECOORDINATESYSTEM_WORLD, ScenecoordinatesystemEnumFromString("WORLD"))
        graphics = self.scene.createGraphicsSurfaces()
        self.assertTrue(graphics.isValid())
        self.assertEqual(SCENECOORDINATESYSTEM_LOCAL, graphics.getScenecoordinatesystem())
        self.assertEqual(status.OK, graphics.setScenecoordinatesystem(SCENECOORDINATESYSTEM_WORLD))
        self.assertEqual(SCENECOORDINATESYSTEM_WORLD, graphics.getScenecoordinatesystem())

    def testGraphicsSurfacesBoundaryMode(self):
        self.assertEqual("BOUNDARY", Graphics.BoundaryModeEnumToString(Graphics.BOUNDARY_MODE_BOUNDARY))
        self.assertEqual(Graphics.BOUNDARY_MODE_BOUNDARY, Graphics.BoundaryModeEnumFromString("BOUNDARY"))
        graphics = self.scene.createGraphicsSurfaces()
        self.assertTrue(graphics.isValid())
        self.assertFalse(graphics.isExterior())
        self.assertEqual(Graphics.BOUNDARY_MODE_ALL, graphics.getBoundaryMode())
        self.assertEqual(status.OK, graphics.setBoundaryMode(Graphics.BOUNDARY_MODE_BOUNDARY))
        self.assertEqual(Graphics.BOUNDARY_MODE_BOUNDARY, graphics.getBoundaryMode())
        self.assertTrue(graphics.isExterior())


def suite():
    tests = unittest.TestSuite()
    tests.addTests(unittest.TestLoader().loadTestsFromTestCase(GraphicsTestCase))
    return tests


if __name__ == '__main__':
    res = unittest.TextTestRunner().run(suite())
    sys.exit(len(res.failures))
