import numpy as np
from ._base_gate import Gate
from ..dimension import RatioDimension
from ..._utils import gate_utils


class RectangleGate(Gate):
    """
    Represents a GatingML Rectangle Gate

    A RectangleGate can have one or more dimensions, and each dimension must
    specify at least one of a minimum or maximum value (or both). From the
    GatingML specification (sect. 5.1.1):

        Rectangular gates are used to express range gates (n = 1, i.e., one
        dimension), rectangle gates (n = 2, i.e., two dimensions), box regions
        (n = 3, i.e., three dimensions), and hyper-rectangular regions
        (n > 3, i.e., more than three dimensions).
    """
    def __init__(
            self,
            gate_name,
            parent_gate_name,
            dimensions
    ):
        super().__init__(
            gate_name,
            parent_gate_name,
            dimensions
        )
        self.gate_type = "RectangleGate"

    def __repr__(self):
        return (
            f'{self.__class__.__name__}('
            f'{self.gate_name}, parent: {self.parent}, dims: {len(self.dimensions)})'
        )

    def apply(self, df_events):
        results = np.ones(df_events.shape[0], dtype=bool)

        for i, dim in enumerate(self.dimensions):
            if isinstance(dim, RatioDimension):
                dim_id = dim.ratio_ref
            else:
                dim_id = dim.id

            if dim.min is not None:
                results = np.bitwise_and(results, df_events[dim_id].values >= dim.min)
            if dim.max is not None:
                results = np.bitwise_and(results, df_events[dim_id].values < dim.max)

        return results


class PolygonGate(Gate):
    """
    Represents a GatingML Polygon Gate

    A PolygonGate must have exactly 2 dimensions, and must specify at least
    three vertices. Polygons can have crossing boundaries, and interior regions
    are defined by the winding number method:

    https://en.wikipedia.org/wiki/Winding_number
    """
    def __init__(
            self,
            gate_name,
            parent_gate_name,
            dimensions,
            vertices
    ):
        super().__init__(
            gate_name,
            parent_gate_name,
            dimensions
        )
        self.vertices = vertices
        self.gate_type = "PolygonGate"

    def __repr__(self):
        return (
            f'{self.__class__.__name__}('
            f'{self.gate_name}, parent: {self.parent}, vertices: {len(self.vertices)})'
        )

    def apply(self, df_events):
        path_vertices = []

        dim_ids_ordered = []
        for i, dim in enumerate(self.dimensions):
            if isinstance(dim, RatioDimension):
                dim_ids_ordered.append(dim.ratio_ref)
            else:
                dim_ids_ordered.append(dim.id)

        for vert in self.vertices:
            path_vertices.append(vert.coordinates)

        results = gate_utils.points_in_polygon(
            np.array(path_vertices, dtype=np.float64),
            df_events[dim_ids_ordered]
        )

        return results


class EllipsoidGate(Gate):
    """
    Represents a GatingML Ellipsoid Gate

    An EllipsoidGate must have at least 2 dimensions, and must specify a mean
    value (center of the ellipsoid), a covariance matrix, and a distance
    square (the square of the Mahalanobis distance).
    """
    def __init__(
            self,
            gate_name,
            parent_gate_name,
            dimensions,
            coordinates,
            covariance_matrix,
            distance_square
    ):
        super().__init__(
            gate_name,
            parent_gate_name,
            dimensions
        )
        self.gate_type = "EllipsoidGate"
        self.coordinates = coordinates
        self.covariance_matrix = covariance_matrix
        self.distance_square = distance_square

        if len(coordinates) == 1:
            raise ValueError(
                'Ellipsoids must have at least 2 dimensions'
            )

        if len(covariance_matrix) != len(self.coordinates):
            raise ValueError(
                'Covariance row entry value count must match # of dimensions'
            )

    def __repr__(self):
        return (
            f'{self.__class__.__name__}('
            f'{self.gate_name}, parent: {self.parent}, coords: {self.coordinates})'
        )

    def apply(self, df_events):
        dim_ids_ordered = []
        for i, dim in enumerate(self.dimensions):
            if isinstance(dim, RatioDimension):
                dim_ids_ordered.append(dim.ratio_ref)
            else:
                dim_ids_ordered.append(dim.id)

        results = gate_utils.points_in_ellipsoid(
            self.covariance_matrix,
            self.coordinates,
            self.distance_square,
            df_events[dim_ids_ordered]
        )

        return results


class Quadrant(object):
    """
    Represents a single quadrant of a QuadrantGate.
    """
    def __init__(self, quadrant_id, divider_refs, divider_ranges):
        self.id = quadrant_id

        div_count = len(divider_refs)

        if div_count != len(divider_ranges):
            raise ValueError("A min/max range must be specified for each divider reference")

        self.divider_refs = divider_refs
        self._divider_ranges = {}

        for i, div_range in enumerate(divider_ranges):
            if len(div_range) != 2:
                raise ValueError("Each divider range must have both a min & max value")

            self._divider_ranges[self.divider_refs[i]] = div_range

        if self._divider_ranges is None or len(self._divider_ranges) != div_count:
            raise ValueError("Failed to parse divider ranges")

    def get_divider_range(self, div_ref):
        return self._divider_ranges[div_ref]

    def __repr__(self):
        return (
            f'{self.__class__.__name__}('
            f'{self.id}, dividers: {len(self.divider_refs)})'
        )


class QuadrantGate(Gate):
    """
    Represents a GatingML Quadrant Gate

    A QuadrantGate must have at least 1 divider, and must specify the labels
    of the resulting quadrants the dividers produce. Quadrant gates are
    different from other gate types in that they are actually a collection of
    gates (quadrants), though even the term quadrant is misleading as they can
    divide a plane into more than 4 sections.

    Note: Only specific quadrants may be referenced as parent gates or as a
    component of a Boolean gate. If a QuadrantGate has a parent, then the
    parent gate is applicable to all quadrants in the QuadrantGate.
    """
    def __init__(
            self,
            gate_name,
            parent_gate_name,
            dividers,
            quadrants
    ):
        super().__init__(
            gate_name,
            parent_gate_name,
            dividers
        )
        self.gate_type = "QuadrantGate"

        # First, check dimension count
        if len(self.dimensions) < 1:
            raise ValueError('Quadrant gates must have at least 1 divider')

        # Parse quadrants
        for quadrant in quadrants:
            for divider_ref in quadrant.divider_refs:
                dim_id = None

                # self.dimensions in a QuadrantGate are dividers
                # make sure all divider IDs are referenced in the list of quadrants
                # and verify there is a dimension ID (for each quad)
                for dim in self.dimensions:
                    if dim.id != divider_ref:
                        continue
                    else:
                        dim_id = dim.dimension_ref

                if dim_id is None:
                    raise ValueError(
                        'Quadrant must define a divider reference'
                    )

        self.quadrants = {q.id: q for q in quadrants}

    def __repr__(self):
        return (
            f'{self.__class__.__name__}('
            f'{self.gate_name}, parent: {self.parent}, quadrants: {len(self.quadrants)})'
        )

    def apply(self, df_events):

        results = {}

        for q_id, quadrant in self.quadrants.items():
            q_results = np.ones(df_events.shape[0], dtype=bool)

            dim_lut = {dim.id: dim.dimension_ref for dim in self.dimensions}

            # quadrant is a list of dicts containing quadrant bounds and
            # the referenced dimension
            for div_ref in quadrant.divider_refs:
                dim_ref = dim_lut[div_ref]
                div_ranges = quadrant.get_divider_range(div_ref)

                if div_ranges[0] is not None:
                    q_results = np.bitwise_and(
                        q_results,
                        df_events[dim_ref].values >= div_ranges[0]
                    )
                if div_ranges[1] is not None:
                    q_results = np.bitwise_and(
                        q_results,
                        df_events[dim_ref].values < div_ranges[1]
                    )

                results[quadrant.id] = q_results

        return results


class BooleanGate(Gate):
    """
    Represents a GatingML Boolean Gate

    A BooleanGate performs the boolean operations AND, OR, or NOT on one or
    more other gates. Note, the boolean operation XOR is not supported in the
    GatingML specification but can be implemented using a combination of the
    supported operations.
    """
    def __init__(
            self,
            gate_name,
            parent_gate_name,
            bool_type,
            gate_refs
    ):
        super().__init__(
            gate_name,
            parent_gate_name,
            None
        )
        self.gate_type = "BooleanGate"

        bool_type = bool_type.lower()
        if bool_type not in ['and', 'or', 'not']:
            raise ValueError(
                "Boolean gate must specify one of 'and', 'or', or 'not'"
            )
        self.type = bool_type
        self.gate_refs = gate_refs

    def __repr__(self):
        return (
            f'{self.__class__.__name__}('
            f'{self.gate_name}, parent: {self.parent}, type: {self.type})'
        )

    def apply(self, df_events):
        all_gate_results = []

        for gate_ref_dict in self.gate_refs:
            res_key = (gate_ref_dict['ref'], "/".join(gate_ref_dict['path']))
            gate_ref_events = df_events[res_key]

            if gate_ref_dict['complement']:
                gate_ref_events = ~gate_ref_events

            all_gate_results.append(gate_ref_events)

        if self.type == 'and':
            results = np.logical_and.reduce(all_gate_results)
        elif self.type == 'or':
            results = np.logical_or.reduce(all_gate_results)
        elif self.type == 'not':
            # gml spec states only 1 reference is allowed for 'not' gate
            results = np.logical_not(all_gate_results[0])
        else:
            raise ValueError(
                "Boolean gate must specify one of 'and', 'or', or 'not'"
            )

        return results
