class Dimension(object):
    def __init__(
            self,
            label,
            compensation_ref,
            transformation_ref=None,
            range_min=None,
            range_max=None
    ):
        # a compensation reference is required, although the value can be
        # the string 'uncompensated' for non-compensated dimensions, or 'FCS'
        # for using the embedded spill in the FCS file. Otherwise it is a
        # reference to a Matrix in the GatingStrategy
        self.compensation_ref = compensation_ref

        # label is required
        self.label = label

        # transformation is optional
        self.transformation_ref = transformation_ref

        if range_min is not None:
            self.min = float(range_min)
        else:
            self.min = range_min
        if range_max is not None:
            self.max = float(range_max)
        else:
            self.max = range_max

    def __repr__(self):
        return f'{self.__class__.__name__}(label: {self.label})'


class RatioDimension(object):
    def __init__(
            self,
            ratio_ref,
            compensation_ref,
            transformation_ref=None,
            range_min=None,
            range_max=None
    ):
        # ratio dimension has no label, but does have a reference to a
        # RatioTransform
        self.ratio_ref = ratio_ref

        # a compensation reference is required, although the value can be
        # the string 'uncompensated' for non-compensated dimensions, or 'FCS'
        # for using the embedded spill in the FCS file. Otherwise it is a
        # reference to a Matrix in the GatingStrategy
        self.compensation_ref = compensation_ref

        # transformation is optional
        self.transformation_ref = transformation_ref

        if range_min is not None:
            self.min = float(range_min)
        if range_max is not None:
            self.max = float(range_max)

    def __repr__(self):
        return (
            f'{self.__class__.__name__}('
            f'ratio_reference: {self.ratio_ref})'
        )


class Divider(object):
    def __init__(
            self,
            divider_id,
            dimension_ref,
            compensation_ref,
            values,
            transformation_ref=None
    ):
        self.id = divider_id
        self.dimension_ref = dimension_ref

        # a compensation reference is required, although the value can be
        # the string 'uncompensated' for non-compensated dimensions, or 'FCS'
        # for using the embedded spill in the FCS file. Otherwise it is a
        # reference to a Matrix in the GatingStrategy
        self.compensation_ref = compensation_ref

        # transformation is optional
        self.transformation_ref = transformation_ref

        self.values = values