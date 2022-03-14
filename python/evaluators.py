"""contains definitions of the cost functions"""


def get_single_shape_evaluator(
        in_data_representation, in_shape, in_iter_limit):
    """returns the Evaluator class for single shape"""
    class Evaluator:
        """utilities to evaluate data or curve in problems with single shape"""
        @classmethod
        def _to_curve(cls, in_data):
            return in_data_representation.to_curve(in_data)

        @classmethod
        def evaluate_curve(cls, in_curve):
            """returns the lenth of the in_curve inside given shape"""
            return in_curve.get_max_len_inside(in_shape, in_iter_limit)

        @classmethod
        def evaluate_data(cls, in_data):
            """
            returns the lenth of the curve represented by in_data
            inside given shape
            """
            return cls.evaluate_curve(cls._to_curve(in_data))

    return Evaluator


def get_multiple_shape_evaluator(
        in_data_representation, in_shape_list, in_iter_limit):
    """returns the Evaluator class for multiple shapes"""
    class Evaluator:
        """
        utilities to evaluate data or curve in problems with multiple shapes
        """
        @classmethod
        def _to_curve(cls, in_data):
            return in_data_representation.to_curve(in_data)

        @classmethod
        def _get_result_list_for_curve(cls, in_curve):
            return [in_curve.get_max_len_inside(_, in_iter_limit)
                    for _ in in_shape_list]

        @classmethod
        def evaluate_curve_max(cls, in_curve):
            """
            returns the maximum length of the curve inside in_shapes
            """
            return max(cls._get_result_list_for_curve(in_curve))

        @classmethod
        def evaluate_curve_sum(cls, in_curve):
            """
            returns the sum of the lengths of the curve inside in_shapes
            """
            return sum(cls._get_result_list_for_curve(in_curve))

        @classmethod
        def evaluate_data_max(cls, in_data):
            """
            calls cls.evaluate_curve_max for the curve represented by in_data
            """
            return cls.evaluate_curve_max(cls._to_curve(in_data))

        @classmethod
        def evaluate_data_sum(cls, in_data):
            """
            calls cls.evaluate_curve_sum for the curve represented by in_data
            """
            return cls.evaluate_curve_sum(cls._to_curve(in_data))

    return Evaluator
