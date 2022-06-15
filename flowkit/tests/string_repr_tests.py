"""
Unit tests for string representations
"""
import unittest
import flowkit as fk
from . import gating_strategy_prog_gate_tests as prog_test_data

data1_fcs_path = 'data/gate_ref/data1.fcs'
data1_sample = fk.Sample(data1_fcs_path)


class StringReprTestCase(unittest.TestCase):
    """Tests related to string representations of FlowKit classes"""
    def test_vert_repr(self):
        vert = fk.Vertex([500, 5])
        vert_string = "Vertex([500, 5])"

        self.assertEqual(repr(vert), vert_string)

    def test_dim_repr(self):
        poly1_dim1 = fk.Dimension('FL2-H', compensation_ref='FCS')
        dim_string = "Dimension(id: FL2-H)"

        self.assertEqual(repr(poly1_dim1), dim_string)

    def test_ratio_dim_repr(self):
        dim_rat1 = fk.RatioDimension(
            'FL2Rat1',
            compensation_ref='uncompensated',
            range_min=3,
            range_max=16.4
        )
        dim_string = "RatioDimension(ratio_reference: FL2Rat1)"

        self.assertEqual(repr(dim_rat1), dim_string)

    def test_quad_div_repr(self):
        quad1_div1 = fk.QuadrantDivider('FL2', 'FL2-H', 'FCS', [12.14748])
        quad_div_string = "QuadrantDivider(id: FL2, dim_ref: FL2-H)"

        self.assertEqual(repr(quad1_div1), quad_div_string)

    def test_linear_transform_repr(self):
        xform = fk.transforms.LinearTransform('lin', param_t=10000.0, param_a=0.0)
        xform_string = "LinearTransform(lin, t: 10000.0, a: 0.0)"

        self.assertEqual(repr(xform), xform_string)

    def test_log_transform_repr(self):
        xform = fk.transforms.LogTransform('log', param_t=10000.0, param_m=4.5)
        xform_string = "LogTransform(log, t: 10000.0, m: 4.5)"

        self.assertEqual(repr(xform), xform_string)

    def test_ratio_transform_repr(self):
        ratio_dims = ['FL1-H', 'FL2-H']
        xform = fk.transforms.RatioTransform('ratio', ratio_dims, param_a=1.0, param_b=0.0, param_c=0.0)
        xform_string = "RatioTransform(ratio, FL1-H / FL2-H, a: 1.0, b: 0.0, c: 0.0)"

        self.assertEqual(repr(xform), xform_string)

    def test_hyperlog_transform_repr(self):
        xform = fk.transforms.HyperlogTransform('hyperlog', param_t=10000.0, param_w=0.5, param_m=4.5, param_a=0.0)
        xform_string = "HyperlogTransform(hyperlog, t: 10000.0, w: 0.5, m: 4.5, a: 0.0)"

        self.assertEqual(repr(xform), xform_string)

    def test_logicle_transform_repr(self):
        xform = fk.transforms.LogicleTransform('logicle', param_t=10000.0, param_w=0.5, param_m=4.5, param_a=0.0)
        xform_string = "LogicleTransform(logicle, t: 10000.0, w: 0.5, m: 4.5, a: 0.0)"

        self.assertEqual(repr(xform), xform_string)

    def test_asinh_transform_repr(self):
        xform = fk.transforms.AsinhTransform('asinh', param_t=10000.0, param_m=4.5, param_a=0.0)
        xform_string = "AsinhTransform(asinh, t: 10000.0, m: 4.5, a: 0.0)"

        self.assertEqual(repr(xform), xform_string)

    def test_wsp_log_xform_repr(self):
        xform = fk.transforms.WSPLogTransform('wsp_log', offset=0.5, decades=4.5)
        xform_string = "WSPLogTransform(wsp_log, offset: 0.5, decades: 4.5)"

        self.assertEqual(repr(xform), xform_string)

    def test_sample_repr(self):
        fcs_file_path = "data/gate_ref/data1.fcs"
        sample = fk.Sample(fcs_path_or_data=fcs_file_path)
        sample_string = "Sample(v2.0, B07, 8 channels, 13367 events)"

        self.assertEqual(repr(sample), sample_string)

    def test_rect_gate_repr(self):
        gate = prog_test_data.range1_gate

        repr_string = "RectangleGate(Range1, parent: None, dims: 1)"

        self.assertEqual(repr(gate), repr_string)

    def test_poly_gate_repr(self):
        gate = prog_test_data.poly1_gate

        repr_string = "PolygonGate(Polygon1, parent: None, vertices: 3)"

        self.assertEqual(repr(gate), repr_string)

    def test_ellipsoid_gate_repr(self):
        gate = prog_test_data.ellipse1_gate

        repr_string = "EllipsoidGate(Ellipse1, parent: None, coords: [12.99701, 16.22941])"

        self.assertEqual(repr(gate), repr_string)

    def test_quad_gate_repr(self):
        gate = prog_test_data.quad1_gate

        repr_string = "QuadrantGate(Quadrant1, parent: None, quadrants: 4)"

        self.assertEqual(repr(gate), repr_string)

    def test_bool_gate_repr(self):
        gate_refs = [
            {
                'ref': 'Polygon1',
                'path': ('root',),
                'complement': False
            },
            {
                'ref': 'Range2',
                'path': ('root',),
                'complement': False
            }
        ]

        gate = fk.gates.BooleanGate('And1', None, 'and', gate_refs)

        repr_string = "BooleanGate(And1, parent: None, type: and)"

        self.assertEqual(repr(gate), repr_string)

    def test_gating_strategy_repr(self):
        gs = fk.GatingStrategy()

        gs.add_comp_matrix(prog_test_data.comp_matrix_01)

        gs.add_transform(prog_test_data.logicle_xform1)
        gs.add_transform(prog_test_data.hyperlog_xform1)

        gs.add_gate(prog_test_data.poly1_gate)

        dim1 = fk.Dimension('PE', 'MySpill', 'Logicle_10000_0.5_4.5_0', range_min=0.31, range_max=0.69)
        dim2 = fk.Dimension('PerCP', 'MySpill', 'Logicle_10000_0.5_4.5_0', range_min=0.27, range_max=0.73)
        dims1 = [dim1, dim2]

        rect_gate1 = fk.gates.RectangleGate('ScaleRect1', None, dims1)
        gs.add_gate(rect_gate1)

        dim3 = fk.Dimension('FITC', 'MySpill', 'Hyperlog_10000_1_4.5_0', range_min=0.12, range_max=0.43)
        dims2 = [dim3]

        rect_gate2 = fk.gates.RectangleGate('ScalePar1', 'ScaleRect1', dims2)
        gs.add_gate(rect_gate2)

        gs_string = "GatingStrategy(3 gates, 2 transforms, 1 compensations)"

        self.assertEqual(repr(gs), gs_string)

    def test_session_repr(self):
        wsp_path = "data/8_color_data_set/8_color_ICS_simple.wsp"
        session = fk.Session()
        session.import_flowjo_workspace(wsp_path, ignore_missing_files=True)

        session_string = "Session(3 samples [0 loaded], 3 sample groups)"

        self.assertEqual(repr(session), session_string)
