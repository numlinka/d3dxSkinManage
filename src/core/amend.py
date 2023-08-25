# -*- coding: utf-8 -*-

import core

import ttkbootstrap

def env_config_amend():
    if not isinstance(core.env.configuration.log_level, (int, str)):
        core.env.configuration.log_level = 0

    if not isinstance(core.env.configuration.annotation_level, int):
        core.env.configuration.annotation_level = 3

    if not isinstance(core.env.configuration.style_theme, str) or core.env.configuration.style_theme not in ttkbootstrap.Style().theme_names():
        core.env.configuration.style_theme = "darkly"

    if not isinstance(core.env.configuration.view_explorer_path, str):
        core.env.configuration.view_explorer_path = "explorer"

    if not isinstance(core.env.configuration.view_file_rule, str):
        core.env.configuration.view_file_rule = "/select,{path}"

    if not isinstance(core.env.configuration.view_directory_rule, str):
        core.env.configuration.view_directory_rule = "{path}"

    if not isinstance(core.env.configuration.thumbnail_approximate_algorithm, str):
        core.env.configuration.thumbnail_approximate_algorithm = "similarity/key-in"
