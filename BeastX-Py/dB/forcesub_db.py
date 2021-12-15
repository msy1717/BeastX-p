# BeastX - UserBot
# Copyright (C) 2021 msy1717
#
# This file is a part of < https://github.com/msy1717/BeastX/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/msy1717/BeastX-Py/blob/main/LICENSE>.

import ast

from .. import mrunal


def get_chats():
    n = []
    cha = mrunal.get("FORCESUB")
    if not cha:
        cha = "{}"
    n.append(ast.literal_eval(cha))
    return n[0]


def add_forcesub(chat_id, chattojoin):
    omk = get_chats()
    omk.update({str(chat_id): str(chattojoin)})
    mrunal.set("FORCESUB", str(omk))
    return True


def get_forcesetting(chat_id):
    omk = get_chats()
    if str(chat_id) in omk.keys():
        return omk[str(chat_id)]
    else:
        return None


def rem_forcesub(chat_id):
    omk = get_chats()
    if str(chat_id) not in omk.keys():
        return None

    try:
        del omk[str(chat_id)]
        mrunal.set("FORCESUB", str(omk))
        return True
    except KeyError:
        return False
