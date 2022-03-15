"""contains TeX-string utilities"""


def includegraphics_str(in_output_paths, in_num, in_width_ratio):
    """
    returns a TeX-string including a pdf file with given number
    """
    return \
        f'\\includegraphics[width={in_width_ratio}\\textwidth]' \
        f'{{{in_output_paths.get_short_pdf_path(in_num)}}}'


def simple_overprint_frame(in_output_paths, in_num_limit, in_width_ratio):
    """
    returns a TeX-string representing a frame with simple overprint
    """
    tex_str = \
        '\\begin{frame}\n' \
        '  \\begin{center}\n' \
        '    \\begin{overprint}\n'

    for _ in range(in_num_limit):
        tex_str += \
            f'        \\onslide<{_+1}>\\centerline{{' + \
            includegraphics_str(in_output_paths, _, in_width_ratio) + \
            '}\n'
    tex_str += \
        '    \\end{overprint}\n' \
        '  \\end{center}\n' \
        '\\end{frame}\n'
    return tex_str


def animategraphics_str(
        in_output_paths, in_frame_rate, in_options_str,
        in_first_frame_num, in_last_frame_num):
    """returns a TeX-string including an animation"""
    assert in_options_str[0] != '[' and in_options_str[-1] != ']'
    core_path = str(in_output_paths.get_short_pdf_path(-1))
    assert core_path.endswith('_-1.pdf')
    core_path = core_path[0:-6]
    return \
        f'\\animategraphics[{in_options_str}]{{{in_frame_rate}}}' \
        f'{{{core_path}}}' \
        f'{{{in_first_frame_num}}}{{{in_last_frame_num}}}'


def save_to_tex_file(in_tex_str, in_output_paths):
    """saves in_tex_str to the given file"""
    with open(in_output_paths.get_tex_file_path(), 'w', encoding='utf-8') \
            as tex_file:
        tex_file.write(in_tex_str)


def save_simple_overprint_frame(in_output_paths, in_num_limit, in_width_ratio):
    """creates a TeX-file with a frame with simple overprint"""
    tex_str = simple_overprint_frame(
        in_output_paths, in_num_limit, in_width_ratio)
    save_to_tex_file(tex_str, in_output_paths)


def save_animategraphics_str(
        in_output_paths,
        in_frame_rate, in_options_str, in_first_frame_num, in_last_frame_num):
    """creates a TeX-file with an animation"""
    tex_str = animategraphics_str(
        in_output_paths, in_frame_rate, in_options_str,
        in_first_frame_num, in_last_frame_num)
    save_to_tex_file(tex_str, in_output_paths)
