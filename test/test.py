#!/bin/env python
"""
Unit tests for ``pyth_grib``.

Author: Daniel Lee, DWD, 2014
"""

import os
import unittest

from pyth_grib import GribFile, GribIndex, GribMessage
from pyth_grib.gribmessage import IndexNotSelectedError


TESTGRIB = "test.grib2"
MESSAGE_KEYS = ['parametersVersion', 'thousand', 'hundred', 'globalDomain',
                'GRIBEditionNumber', 'grib2divider', 'missingValue',
                'ieeeFloats', 'section0Length', 'identifier', 'discipline',
                'editionNumber', 'totalLength', 'sectionNumber',
                'section1Length', 'numberOfSection', 'centre',
                'centreDescription', 'subCentre', 'tablesVersion',
                'masterDir', 'localTablesVersion', 'localDir',
                'significanceOfReferenceTime', 'year', 'month', 'day', 'hour',
                'minute', 'second', 'dataDate', 'julianDay', 'dataTime',
                'productionStatusOfProcessedData', 'typeOfProcessedData',
                'md5Section1', 'selectStepTemplateInterval',
                'selectStepTemplateInstant', 'stepType', 'sectionNumber',
                'grib2LocalSectionPresent', 'section2Length',
                'numberOfSection', 'addEmptySection2',
                'grib2LocalSectionNumber', 'marsClass', 'marsType',
                'marsStream', 'experimentVersionNumber', 'class', 'type',
                'stream', 'productDefinitionTemplateNumberInternal',
                'localDefinitionNumber', 'eps', 'oceanAtmosphereCoupling',
                'legBaseDate', 'legBaseTime', 'legNumber', 'referenceDate',
                'climateDateFrom', 'climateDateTo', 'addExtraLocalSection',
                'deleteExtraLocalSection', 'extraLocalSectionPresent',
                'section2Padding', 'sectionNumber',
                'gridDescriptionSectionPresent', 'section3Length',
                'numberOfSection', 'sourceOfGridDefinition',
                'numberOfDataPoints', 'numberOfOctectsForNumberOfPoints',
                'interpretationOfNumberOfPoints', 'PLPresent',
                'gridDefinitionTemplateNumber', 'shapeOfTheEarth',
                'scaleFactorOfRadiusOfSphericalEarth',
                'scaledValueOfRadiusOfSphericalEarth',
                'scaleFactorOfEarthMajorAxis', 'scaledValueOfEarthMajorAxis',
                'scaleFactorOfEarthMinorAxis', 'scaledValueOfEarthMinorAxis',
                'radius', 'Ni', 'Nj',
                'basicAngleOfTheInitialProductionDomain', 'mBasicAngle',
                'angleMultiplier', 'mAngleMultiplier',
                'subdivisionsOfBasicAngle', 'angleDivisor',
                'latitudeOfFirstGridPoint', 'longitudeOfFirstGridPoint',
                'resolutionAndComponentFlags', 'resolutionAndComponentFlags1',
                'resolutionAndComponentFlags2', 'iDirectionIncrementGiven',
                'jDirectionIncrementGiven', 'uvRelativeToGrid',
                'resolutionAndComponentFlags6',
                'resolutionAndComponentFlags7',
                'resolutionAndComponentFlags8', 'ijDirectionIncrementGiven',
                'latitudeOfLastGridPoint', 'longitudeOfLastGridPoint',
                'iDirectionIncrement', 'N', 'scanningMode',
                'iScansNegatively', 'jScansPositively',
                'jPointsAreConsecutive', 'alternativeRowScanning',
                'iScansPositively', 'scanningMode5', 'scanningMode6',
                'scanningMode7', 'scanningMode8', 'g2grid',
                'latitudeOfFirstGridPointInDegrees',
                'longitudeOfFirstGridPointInDegrees',
                'latitudeOfLastGridPointInDegrees',
                'longitudeOfLastGridPointInDegrees',
                'iDirectionIncrementInDegrees', 'global', 'latLonValues',
                'latitudes', 'longitudes', 'distinctLatitudes',
                'distinctLongitudes', 'section3Padding', 'gridType',
                'md5Section3', 'sectionNumber', 'section4Length',
                'numberOfSection', 'NV', 'neitherPresent',
                'productDefinitionTemplateNumber', 'Parameter information',
                'parameterCategory', 'parameterNumber', 'parameterUnits',
                'parameterName', 'typeOfGeneratingProcess',
                'backgroundProcess', 'generatingProcessIdentifier',
                'hoursAfterDataCutoff', 'minutesAfterDataCutoff',
                'indicatorOfUnitOfTimeRange', 'stepUnits', 'forecastTime',
                'startStep', 'endStep', 'stepRange', 'stepTypeInternal',
                'validityDate', 'validityTime', 'typeOfFirstFixedSurface',
                'unitsOfFirstFixedSurface', 'nameOfFirstFixedSurface',
                'scaleFactorOfFirstFixedSurface',
                'scaledValueOfFirstFixedSurface', 'typeOfSecondFixedSurface',
                'unitsOfSecondFixedSurface', 'nameOfSecondFixedSurface',
                'scaleFactorOfSecondFixedSurface',
                'scaledValueOfSecondFixedSurface', 'pressureUnits',
                'typeOfLevel', 'level', 'bottomLevel', 'topLevel',
                'EPS information', 'typeOfEnsembleForecast',
                'perturbationNumber', 'numberOfForecastsInEnsemble', 'x',
                'paramIdECMF', 'paramId', 'shortNameECMF', 'shortName',
                'unitsECMF', 'units', 'nameECMF', 'name', 'cfNameECMF',
                'cfName', 'cfVarNameECMF', 'cfVarName', 'ifsParam',
                'genVertHeightCoords', 'PVPresent', 'md5Section4',
                'sectionNumber',
                'grib 2 Section 5 DATA REPRESENTATION SECTION',
                'section5Length', 'numberOfSection', 'numberOfValues',
                'dataRepresentationTemplateNumber', 'packingType',
                'referenceValue', 'referenceValueError', 'binaryScaleFactor',
                'decimalScaleFactor', 'bitsPerValue',
                'typeOfOriginalFieldValues', 'md5Section5', 'lengthOfHeaders',
                'md5Headers', 'sectionNumber',
                'grib 2 Section 6 BIT-MAP SECTION', 'section6Length',
                'numberOfSection', 'bitMapIndicator', 'bitmapPresent',
                'md5Section6', 'sectionNumber', 'grib 2 Section 7 data',
                'section7Length', 'numberOfSection', 'codedValues', 'values',
                'packingError', 'unpackedError', 'maximum', 'minimum',
                'average', 'numberOfMissing', 'standardDeviation', 'skewness',
                'kurtosis', 'isConstant', 'changeDecimalPrecision',
                'decimalPrecision', 'setBitsPerValue', 'getNumberOfValues',
                'scaleValuesBy', 'offsetValuesBy', 'productType',
                'md5Section7', 'section8Length', '7777']
TEST_OUTPUT = "test-output.grib"
TEST_INDEX = "test.index"
TEST_KEYS = (MESSAGE_KEYS[MESSAGE_KEYS.index("dataDate")],
        MESSAGE_KEYS[MESSAGE_KEYS.index("stepRange")])
TEST_VALUES = 20110225, 0
SELECTION_DICTIONARY = {}
for i in range(len(TEST_KEYS)):
    SELECTION_DICTIONARY[TEST_KEYS[i]] = TEST_VALUES[i]
TEST_INDEX_OUTPUT = TESTGRIB
TEST_STEPRANGE = ('0', '12', '18', '24', '6')

class TestGribFile(unittest.TestCase):
    """Test GribFile functionality."""
    def test_memory_management(self):
        """Messages in GribFile can be opened and closed properly."""
        with GribFile(TESTGRIB) as grib:
            self.assertEqual(len(grib), 5)
            for msg in grib:
                self.assertEqual(msg["shortName"], "msl")
            self.assertEqual(len(grib.open_messages), 5)
        self.assertEqual(len(grib.open_messages), 0)

class TestGribMessage(unittest.TestCase):
    """Test GribMessage functionality."""
    def test_metadata(self):
        """Metadata is read correctly from GribMessage."""
        with GribFile(TESTGRIB) as grib:
            msg = grib.next()
            self.assertEqual(len(msg), 243)
            self.assertEqual(msg.size, 160219)
            self.assertSequenceEqual(msg.keys(), MESSAGE_KEYS)
    def test_missing_message_behavior(self):
        """Missing messages are detected properly."""
        with GribFile(TESTGRIB) as grib:
            msg = grib.next()
            self.assertTrue(msg.missing("scaleFactorOfSecondFixedSurface"))
            msg["scaleFactorOfSecondFixedSurface"] = 5
            msg.set_missing("scaleFactorOfSecondFixedSurface")
            with self.assertRaises(KeyError):
                msg["scaleFactorOfSecondFixedSurface"]
    def test_value_setting(self):
        """Keys can be set properly."""
        with GribFile(TESTGRIB) as grib:
            msg = grib.next()
            msg["scaleFactorOfSecondFixedSurface"] = 5
            msg["values"] = [1, 2, 3]
    def test_serialize(self):
        """Message can be serialized to file."""
        with GribFile(TESTGRIB) as grib:
            msg = grib.next()
            with open(TEST_OUTPUT, "w") as test:
                msg.write(test)
        os.unlink(TEST_OUTPUT)
    def test_clone(self):
        """Messages can be used to produce clone Messages."""
        with GribFile(TESTGRIB) as grib:
            msg = grib.next()
            msg2 = GribMessage(clone=msg)
            self.assertSequenceEqual(msg.keys(), msg2.keys())


class TestGribIndex(unittest.TestCase):
    """Test GribIndex functionality."""
    def test_memory_management(self):
        """GribIndex closes GribMessages properly."""
        with GribIndex(TESTGRIB, TEST_KEYS) as idx:
            msg = idx.select(SELECTION_DICTIONARY)
            self.assertEqual(len(idx.open_messages), 1)
        self.assertEqual(len(idx.open_messages), 0)
    def test_create_and_serialize_index(self):
        """GribIndex can be saved to file, file can be added to index."""
        with GribIndex(TESTGRIB, TEST_KEYS) as idx:
            idx.write(TEST_INDEX)
        with GribIndex(file_index=TEST_INDEX) as idx:
            idx.add(TESTGRIB)
        os.unlink(TEST_INDEX)
    def test_index_comprehension(self):
        """GribIndex understands underlying GRIB index properly."""
        with GribIndex(TESTGRIB, TEST_KEYS) as idx:
            self.assertEqual(idx.size(TEST_KEYS[1]), 5)
            self.assertSequenceEqual(idx.values(TEST_KEYS[1]), TEST_STEPRANGE)
            with self.assertRaises(IndexNotSelectedError):
                msg = idx.select({TEST_KEYS[1]: TEST_VALUES[0]})
            idx.select(SELECTION_DICTIONARY)
            self.assertEqual(len(idx.open_messages), 1)

if __name__ == "__main__":
    unittest.main()
