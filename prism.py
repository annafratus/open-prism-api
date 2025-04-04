# -*- coding: utf-8 -*-
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# Copyright (c) 2024-2025 Anna Fratus <https://annafratus.com>
#
# This library is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This library is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public
# License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this library. If not, see <https://www.gnu.org/licenses/>.

"""
Open Prism API v2025.4.4

Tested with Prism 2.0.13, compatibility with older or newer versions are
not guaranteed.

This is a simple Prism API to access some prism functions from inside DCCs
programs.It currently automatically supports Prism inside Maya and Houdini,
but a Prism core reference can be set with set_core() for partial DCC support.

Put this module (prism.py) with your plugin modules to call its functions from
inside your code (import prism). This module needs to be loaded by the DCC you
are developing for to be accessible in runtime.
"""

import os


class OpenPrismAPIError(Exception):
    """
    Exception class for Prism related errors.
    """


# Standalone Prism core reference
CORE = None


def get_core():
    """
    Tries to get the DCC level Prism core reference,
    if not found returns the standalone reference defined by set_core().

    Returns:
        the prism core reference.
    """
    try:
        import PrismInit
    except ModuleNotFoundError:
        return CORE

    return PrismInit.pcore


def set_core(new_core):
    """
    Sets the Prism core used by this API.

    Args:
        new_core: the Prism core object to be set as the Prism core of this API.
    """
    global CORE
    CORE = new_core


def is_prism():
    """
    Returns:
        bool: True if prism is active.
    """
    if not get_core():
        return False
    return True


def get_maya_plugin():
    """
    Returns:
        the prism Maya plugin reference.
    """
    core = get_core()

    if core is None:
        return None

    return core.plugins.getPlugin("Maya")


def is_maya_plugin():
    """
    Returns:
        bool: true if the prism Maya plugin is loaded.
    """
    if not get_maya_plugin():
        return False
    return True


def get_houdini_plugin():
    """
    Returns:
        the prism Houdini plugin reference.
    """
    core = get_core()

    if core is None:
        return None

    return core.plugins.getPlugin("Houdini")


def is_houdini_plugin():
    """
    Returns:
        bool: true if the prism Houdini plugin is loaded.
    """
    if not get_houdini_plugin():
        return False
    return True


def get_project_name():
    """
    Returns:
        str: the current prism project name.
    """
    core = get_core()

    if core is None:
        return ""

    return core.projectName


def get_project_path():
    """
    Returns:
        str: the current prism project path.
    """
    core = get_core()

    if core is None:
        return ""

    return core.projectPath.replace("\\", "/")


def get_prism_folder():
    """
    Returns:
        str: the prism root folder.
    """
    core = get_core()

    if core is None:
        return None

    return core.prismRoot.replace("\\", "/")


def get_curr_scene_file_path():
    """
    Get the current scene file path. Works with Maya and Houdini.

    Returns:
        str: the current dcc scene file path (Only Maya and Houdini).
    """
    scene_file = None

    # If Maya
    try:
        from maya import cmds

        scene_file = cmds.file(sceneName=True, q=True)
    except ModuleNotFoundError:
        pass

    # If Houdini
    try:
        import hou

        scene_file = hou.hipFile.path()
    except ModuleNotFoundError:
        pass

    if not scene_file:
        return ""

    return scene_file.replace("\\", "/")


def is_scene_in_prism():
    """
    Returns:
        bool: true if the current scene opened in the dcc resides into prism.
    """
    curr_scene = get_curr_scene_file_path()
    prism_project = get_project_path()

    if not curr_scene or not prism_project:
        return False

    return curr_scene.startswith(prism_project)


def get_scene_file_data(scene_path: str):
    """
    Args:
        scene_path (str): the scene path to get the scene file data.

    Returns:
        dict: scene file data for the specified scene_path.

    Raises:
        OpenPrismAPIError
    """
    # Prism core
    core = get_core()
    if not core:
        raise OpenPrismAPIError("(get_scene_file_data) Prism core was not found.")

    return core.getScenefileData(scene_path)


def get_task(scene_path: str = None):
    """
    Get the prism task from the informed scene, or from the current scene if not informed.

    Args:
        scene_path (str): the scene path to get the task. None to get from the current scene.

    Returns:
        str: the task of the informed scene or from the current scene.

    Raises:
        OpenPrismAPIError
    """
    if not is_scene_in_prism:
        raise OpenPrismAPIError("(get_task) The current scene is not in Prism.")

    if not scene_path:
        scene_path = get_curr_scene_file_path()

    return get_scene_file_data(scene_path).get("task")


def get_department(scene_path: str = None):
    """
    Get the prism department from the informed scene, or from the current scene if not informed.

    Args:
        scene_path (str): the scene path to get the department. None to get from the current scene.

    Returns:
        str: the department of the informed scene or from the current scene.

    Raises:
        OpenPrismAPIError
    """
    if not is_scene_in_prism:
        raise OpenPrismAPIError("(get_department) The current scene is not in Prism.")

    if not scene_path:
        scene_path = get_curr_scene_file_path()

    return get_scene_file_data(scene_path).get("department")


def get_product_export_data(
    identifier: str,
    extension: str,
    start_frame=None,
    end_frame=None,
    comment=None,
    location=None,
):
    """
    Get a dict of a new Product Data for the specified arguments.

    Args:
        identifier (str): the product name shown in prism.
        extension (str): the file extension, example: .abc
        start_frame (int): the export start frame.
        end_frame (int): the export end frame.
        comment (str): a comment shown in prism.
        location (str): the prism location where the product would be created.

    Returns:
        dict: product export data.

    Raises:
        OpenPrismAPIError
    """
    # Prism core
    core = get_core()
    if not core:
        raise OpenPrismAPIError("(get_product_export_data) Prism core was not found.")

    if not is_scene_in_prism():
        raise OpenPrismAPIError(
            "(get_product_export_data) the current scene is not in Prism."
        )

    # Current scene path
    scene_path = get_curr_scene_file_path()
    # Get prism_scene_data
    prism_scene_data = core.getScenefileData(scene_path)
    # Get prism_product_data
    prism_product_data = core.products.generateProductPath(
        prism_scene_data,
        identifier,
        extension=extension,
        startframe=start_frame,
        endframe=end_frame,
        comment=comment,
        location=location,
        returnDetails=True,
    )
    return prism_product_data


def get_product_export_file_path(identifier: str, extension: str, location=None):
    """
    Get the path for a new Product for the specified arguments.

    Args:
        identifier (str): the product name shown in prism.
        extension (str): the file extension, example: .abc
        location (str): the prism location where the product would be created.

    Returns:
        str: the correspondent product file path to the arguments.

    Raises:
        OpenPrismAPIError
    """
    path = get_product_export_data(identifier, extension, location=location).get("path")
    if path:
        return path.replace("\\", "/")
    return None


def set_product_master_version(path: str):
    """
    Set Product master version from file path.

    Args:
        path (str): the file path to set as master.

    Raises:
        OpenPrismAPIError
    """
    if not os.path.exists(path):
        raise OpenPrismAPIError(
            f"(set_product_master_version) the path do not exist: {path}"
        )

    # Prism core
    core = get_core()
    if not core:
        raise OpenPrismAPIError(
            "(set_product_master_version) Prism core was not found."
        )

    # Set master version
    core.products.updateMasterVersion(path)


def get_media_product_data(
    identifier: str, extension: str, comment=None, location=None
):
    """
    Get a dict of a new Media Product Data for the specified arguments.

    Args:
        identifier (str): the product name shown in prism.
        extension (str): the file extension, example: .exr
        comment (str): a comment shown in prism.
        location (str): the prism location where the product would be created.

    Returns:
        dict: media product export data.

    Raises:
        OpenPrismAPIError
    """
    # Prism core
    core = get_core()
    if not core:
        raise OpenPrismAPIError("(get_media_product_data) Prism core was not found.")

    if not is_scene_in_prism():
        raise OpenPrismAPIError(
            "(get_media_product_data) the current scene is not in Prism."
        )

    # Current scene path
    scene_path = get_curr_scene_file_path()
    # Get prism_scene_data
    prism_scene_data = core.getScenefileData(scene_path)
    # Get prism_media_product_data
    prism_media_product_data = core.mediaProducts.generateMediaProductPath(
        prism_scene_data,
        identifier,
        extension=extension,
        comment=comment,
        location=location,
        returnDetails=True,
    )
    return prism_media_product_data


def get_media_export_file_path(identifier: str, extension: str, location=None):
    """
    Get the path for a new Media Product for the specified arguments.

    Args:
        identifier (str): the media product name shown in prism.
        extension (str): the file extension, example: .exr
        location (str): the prism location where the media product would be created.

    Returns:
        str: the correspondent media product file path to the arguments.

    Raises:
        OpenPrismAPIError
    """
    path = get_media_product_data(identifier, extension, location=location).get("path")
    if path:
        return path.replace("\\", "/")
    return None


def get_playblast_product_data(
    identifier: str, extension: str, comment=None, location=None
):
    """
    Get a dict of Playblast Product Data for the specified arguments.

    Args:
        identifier (str): the playblast product name shown in prism.
        extension (str): the file extension, example: .mov
        comment (str): a comment shown in prism.
        location (str): the prism location where the playblast product would be created.

    Returns:
        dict: playblast product export data.

    Raises:
        OpenPrismAPIError
    """
    # Prism core
    core = get_core()
    if not core:
        raise OpenPrismAPIError(
            "(get_playblast_product_data) Prism core was not found."
        )

    if not is_scene_in_prism():
        raise OpenPrismAPIError(
            "(get_playblast_product_data) the current scene is not in Prism."
        )

    # Current scene path
    scene_path = get_curr_scene_file_path()
    # Get prism_scene_data
    prism_scene_data = core.getScenefileData(scene_path)
    # Get prism_playblast_product_data
    prism_playblast_product_data = core.mediaProducts.generatePlayblastPath(
        prism_scene_data,
        identifier,
        extension=extension,
        comment=comment,
        location=location,
        returnDetails=True,
    )
    return prism_playblast_product_data


def get_playblast_export_file_path(identifier: str, extension: str, location=None):
    """
    Get the path for a new Playblast Product for the specified arguments.

    Args:
        identifier (str): the playblast product name shown in prism.
        extension (str): the file extension, example: .mov
        location (str): the prism location where the playblast product would be created.

    Returns:
        str: the correspondent playblast product file path to the arguments.

    Raises:
        OpenPrismAPIError
    """
    path = get_playblast_product_data(identifier, extension, location=location).get(
        "path"
    )
    if path:
        return path.replace("\\", "/")
    return None


def set_media_master_version(path: str, is_playblast=False, is_2d_render=False):
    """
    Set Media/Playblast master version from file path.

    Args:
        path (str): the file path to set as master.
        is_playblast (bool): flag for playblast files.
        is_2d_render (bool): flag for 2d render files.

    Raises:
        OpenPrismAPIError
    """
    if not os.path.exists(path):
        raise OpenPrismAPIError(
            f"(set_media_master_version) the path do not exist: {path}"
        )

    # Prism core
    core = get_core()
    if not core:
        raise OpenPrismAPIError("(set_media_master_version) Prism core was not found.")

    if is_playblast:
        media_type = "playblasts"
    elif is_2d_render:
        media_type = "2drenders"
    else:
        media_type = None

    # Set master version
    core.mediaProducts.updateMasterVersion(path, mediaType=media_type)


def set_render_master_version(path: str):
    """
    Set Render master version from file path.

    Args:
        path (str): the file path to set as master.

    Raises:
        OpenPrismAPIError
    """
    set_media_master_version(path)


def set_playblast_master_version(path: str):
    """
    Set Playblast master version from file path.

    Args:
        path (str): the file path to set as master.

    Raises:
        OpenPrismAPIError
    """
    set_media_master_version(path, is_playblast=True)


def set_2d_render_master_version(path: str):
    """
    Set 2D Render master version from file path.

    Args:
        path (str): the file path to set as master.

    Raises:
        OpenPrismAPIError
    """
    set_media_master_version(path, is_2d_render=True)


def get_export_locations():
    """
    Get a dict of Export Locations from Prism.

    Returns:
        dict: dict of location_name:location_path.

    Raises:
        OpenPrismAPIError
    """
    # Prism core
    core = get_core()
    if not core:
        raise OpenPrismAPIError("(get_export_locations) Prism core was not found.")

    return core.paths.getExportProductBasePaths()


def get_render_locations():
    """
    Get a dict of Render Locations from Prism.

    Returns:
        dict: dict of location_name:location_path.

    Raises:
        OpenPrismAPIError
    """
    # Prism core
    core = get_core()
    if not core:
        raise OpenPrismAPIError("(get_render_locations) Prism core was not found.")

    return core.paths.getRenderProductBasePaths()


def request_products():
    """
    Open prism product browser to select a product. Returns a list of paths.

    Returns:
        list: list of paths.

    Raises:
        OpenPrismAPIError
    """
    # Prism core
    core = get_core()
    if not core:
        raise OpenPrismAPIError("(request_products) Prism core was not found.")

    # Prism alternative import window
    # result = core.callback("requestImportPath")
    # for res in result:
    #     if isinstance(res, dict) and res.get("importPaths") is not None:
    #         return res["importPaths"]

    import ProductBrowser

    ts = ProductBrowser.ProductBrowser(core=core)
    core.parentWindow(ts)
    ts.exec_()

    import_paths = [ts.productPath] if ts.productPath else []

    return import_paths


def get_shot_range(scene_path: str = None):
    """
    Get the start and end frames of the shot from the informed scene, or use the shot of the current scene
    if not informed.

    Args:
        scene_path (str): a scene path from the desired shot. None to use the shot of the current scene.

    Returns:
        list: list of the start and end frames for the informed or current shot.

    Raises:
        OpenPrismAPIError
    """
    # Prism core
    core = get_core()
    if not core:
        raise OpenPrismAPIError("(get_shot_range) Prism core was not found.")

    if not scene_path:
        scene_path = get_curr_scene_file_path()

    return core.entities.getShotRange(get_scene_file_data(scene_path))
