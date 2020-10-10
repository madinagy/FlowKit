"""
Unit tests for Transform sub-classes
"""
import unittest
import numpy as np

from flowkit import Sample, transforms

data1_fcs_path = 'examples/gate_ref/data1.fcs'
data1_sample = Sample(data1_fcs_path)
data1_raw_events = data1_sample.get_raw_events()

test_data_range1 = np.linspace(0.0, 10.0, 101)


class TransformsTestCase(unittest.TestCase):
    """Tests for loading FCS files as Sample objects"""
    def test_transform_sample_linear(self):
        xform = transforms.LinearTransform('lin', param_t=data1_raw_events.max(), param_a=0.0)
        data1_sample.apply_transform(xform)

        xform_events = xform.apply(data1_raw_events)

        self.assertIsInstance(xform_events, np.ndarray)
        self.assertEqual(np.max(xform_events), 1.0)
        self.assertEqual(np.min(xform_events), 0.0)

    @staticmethod
    def test_inverse_linear_transform():
        xform = transforms.LinearTransform('asinh', param_t=10000, param_a=0)
        y = xform.apply(test_data_range1)
        x = xform.inverse(y)

        np.testing.assert_array_almost_equal(test_data_range1, x, decimal=10)

    def test_transform_sample_asinh(self):
        xform = transforms.AsinhTransform('asinh', param_t=10000, param_m=4.5, param_a=0)
        data1_sample.apply_transform(xform)

        self.assertIsInstance(data1_sample._transformed_events, np.ndarray)

    @staticmethod
    def test_inverse_asinh_transform():
        xform = transforms.AsinhTransform('asinh', param_t=10000, param_m=4.5, param_a=0)
        y = xform.apply(test_data_range1)
        x = xform.inverse(y)

        np.testing.assert_array_almost_equal(test_data_range1, x, decimal=10)

    def test_transform_sample_logicle(self):
        xform = transforms.LogicleTransform('logicle', param_t=10000, param_w=0.5, param_m=4.5, param_a=0)
        data1_sample.apply_transform(xform)

        self.assertIsInstance(data1_sample._transformed_events, np.ndarray)

    @staticmethod
    def test_inverse_logicle_transform():
        xform = transforms.LogicleTransform('logicle', param_t=10000, param_w=0.5, param_m=4.5, param_a=0)
        y = xform.apply(test_data_range1.reshape(-1, 1))
        x = xform.inverse(y)[:, 0]

        np.testing.assert_array_almost_equal(test_data_range1, x, decimal=10)

    def test_transform_sample_hyperlog(self):
        xform = transforms.HyperlogTransform('hyper', param_t=10000, param_w=0.5, param_m=4.5, param_a=0)
        data1_sample.apply_transform(xform)

        self.assertIsInstance(data1_sample._transformed_events, np.ndarray)

    def test_transform_sample_wsp_log(self):
        xform = transforms.WSPLogTransform('wsp_log', offset=0.5, decades=4.5)
        data1_sample.apply_transform(xform)

        self.assertIsInstance(data1_sample._transformed_events, np.ndarray)
