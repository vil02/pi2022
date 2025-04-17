"""contains utilities releated to generation of the optimsation data"""

import time
import collections
import scipy.optimize

import evaluators as ev


RowType = collections.namedtuple('RowType', ['data', 'time'])


def _append_res_data(cur_data, in_opt_res, in_start_time):
    cur_data.append(RowType(in_opt_res.x, time.time()-in_start_time))


def _get_callback_fun(cur_data, in_start_time):
    def callback_fun(in_data, _function_value, _context):
        cur_data.append(RowType(in_data, time.time()-in_start_time))
    return callback_fun


def generate_single_shape_optimisation_data(
        in_data_representation, in_shape, in_iter_limit, **kwargs):
    """returns the optimisation data"""
    cur_evaluator = ev.get_single_shape_evaluator(
        in_data_representation, in_shape, in_iter_limit)
    res_data = []
    start_time = time.time()

    opt_res = scipy.optimize.dual_annealing(
        cur_evaluator.evaluate_data,
        in_data_representation.bounds,
        callback=_get_callback_fun(res_data, start_time),
        **kwargs)
    _append_res_data(res_data, opt_res, start_time)
    return res_data


def generate_multiple_shape_optimisation_data(
        in_data_representation, in_shape_list, in_iter_limit,
        sum_step_args, max_step_args):
    """returns the optimisation data"""
    cur_evaluator = ev.get_multiple_shape_evaluator(
        in_data_representation, in_shape_list, in_iter_limit)
    res_data = []
    start_time = time.time()

    sum_opt_res = scipy.optimize.dual_annealing(
        cur_evaluator.evaluate_data_sum,
        in_data_representation.bounds,
        callback=_get_callback_fun(res_data, start_time),
        **sum_step_args)
    _append_res_data(res_data, sum_opt_res, start_time)

    max_opt_res = scipy.optimize.dual_annealing(
        cur_evaluator.evaluate_data_max,
        in_data_representation.bounds,
        callback=_get_callback_fun(res_data, start_time),
        x0=sum_opt_res.x,
        **max_step_args)
    _append_res_data(res_data, max_opt_res, start_time)
    return res_data
