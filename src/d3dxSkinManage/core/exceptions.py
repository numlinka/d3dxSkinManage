# Licensed under the GNU General Public License v3.0, see <http://www.gnu.org/licenses/gpl-3.0.html>.
# d3dxSkinManage Copyright (C) 2023 numlinka.

class UserDoesNotExist (Exception):
    """The user does not exist."""


class UserLoggedIn (Exception):
    "User logged in."



__all__ = [
    "UserDoesNotExist",
    "UserLoggedIn"
]
