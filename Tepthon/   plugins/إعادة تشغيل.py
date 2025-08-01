import os
from asyncio.exceptions import CancelledError
from time import sleep

from Tepthon import zedub

from ..core.logger import logging
from ..core.managers import edit_or_reply
from ..sql_helper.global_collection import (
    add_to_collectionlist,
    del_keyword_collectionlist,
    get_collectionlist_items,
)
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
from . import BOTLOG, BOTLOG_CHATID, HEROKU_APP, mention

LOGS = logging.getLogger(__name__)
plugin_category = "الادوات"


@zedub.zed_cmd(
    pattern="اعادة تشغيل$",
    command=("اعادة تشغيل", plugin_category),
    info={
        "header": "لـ إعـادة تشغيـل البـوت",
        "الاستخـدام": "{tr}اعادة تشغيل",
    },
    disable_errors=True,
)
async def _(event):
    "لـ إعـادة تشغيـل البـوت"
    if BOTLOG:
        await event.client.send_message(BOTLOG_CHATID, "#إعــادة_التشغيــل\n\n" "**⪼ بـوت عبودثون في وضـع إعادة التشغيـل انتظـر**\n\n" "**⪼ إذا لـم يستجـب البـوت بعـد خمـس دقائـق .. قـم بالذهـاب إلى حسـاب هيـروكو وإعـادة التشغيـل اليـدوي**")
    sandy = await edit_or_reply(
        event,
        f"**• مرحبًـــا 👋** - {mention}\n\n"
        f"**• جـاري إعـادة تشغيـل بوت عبودثون قد يستغرق الأمر ( 1-2 ) دقيقة ⏲️ ...**",
    )
    try:
        ulist = get_collectionlist_items()
        for i in ulist:
            if i == "restart_update":
                del_keyword_collectionlist("restart_update")
    except Exception as e:
        LOGS.error(e)
    try:
        add_to_collectionlist("restart_update", [sandy.chat_id, sandy.id])
    except Exception as e:
        LOGS.error(e)
    try:
        await zedub.disconnect()
    except CancelledError:
        pass
    except Exception as e:
        LOGS.error(e)


@zedub.zed_cmd(
    pattern="ايقاف البوت$",
    command=("ايقاف البوت", plugin_category),
    info={
        "header": "لـ إطفـاء البـوت",
        "الوصـف": "لـ إطفـاء الداينـو الخاص بتنصيبك بهيروكـو .. لا تستطيع اعادة التشغيل مرة أخرى عبر حسابك عليك الذهاب لحساب هيروكو واتباع الشرح التالي https://t.me/Tepthon",
        "الاستخـدام": "{tr}ايقاف البوت",
    },
)
async def _(event):
    "لـ إطفـاء البـوت"
    if BOTLOG:
        await event.client.send_message(BOTLOG_CHATID, "#إيقـاف البــوت\n\n" "**- بـوت عبودثون فـي وضــع الإيقـاف 🚫 .**")
    await edit_or_reply(event, "**✾╎جــارِ إيقـاف تشغيـل بـوت عبودثون الآن 📟 ...**\n\n**✾╎شغِّـلنـي يـدويًـا لاحقًــا**\n**✾╎باتبـاع الشـرح** https://t.me/AbodThon")
    if HEROKU_APP is not None:
        HEROKU_APP.process_formation()["worker"].scale(0)
    else:
        os._exit(143)


@zedub.zed_cmd(
    pattern="نوم( [0-9]+)?$",
    command=("نوم", plugin_category),
    info={
        "header": "البـوت الخـاص بك سيتوقف موقتـاً .. حسب الثوانـي المدخلـه",
        "الاستخـدام": "{tr}نوم <عـدد الثـواني>",
        "مثــال": "{tr}نوم 60",
    },
)
async def _(event):
    "لـ إيقـاف البـوت مؤقـتـًا"
    if " " not in event.pattern_match.group(1):
        return await edit_or_reply(event, "**- عـذراً .. قم بادخـال عـدد الثواني للامـر**\n**- مثــال :**\n`.نوم 60`")
    counter = int(event.pattern_match.group(1))
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID, f"**- لقـد تم وضـع البـوت في وضـع النـوم لمـدة {counter} ثـانيـه✓**"
        )

    event = await edit_or_reply(event, f"**- تم وضـع البـوت في وضـع النـوم لمـدة {counter} ثـانيـه✓**")
    sleep(counter)
    await event.edit("**✾╎لقـد عـدت 🏃...**\n**✾╎أنا الآن في وضـع التشغيـل 🧑‍💻**")


@zedub.zed_cmd(
    pattern="الاشعارات (تفعيل|تعطيل)$",
    command=("notify", plugin_category),
    info={
        "header": "To update the your chat after restart or reload .",
        "الوصـف": "Will send the ping cmd as reply to the previous last msg of (restart/reload/update cmds).",
        "الاستخـدام": [
            "{tr}الاشعارات <تفعيل/تعطيل>",
        ],
    },
)
async def set_pmlog(event):
    "To update the your chat after restart or reload ."
    input_str = event.pattern_match.group(1)
    if input_str == "تعطيل":
        if gvarstatus("restartupdate") is None:
            return await edit_delete(event, "__Notify already disabled__")
        delgvar("restartupdate")
        return await edit_or_reply(event, "__Notify is disable successfully.__")
    if gvarstatus("restartupdate") is None:
        addgvar("restartupdate", "turn-oned")
        return await edit_or_reply(event, "__Notify is enable successfully.__")
    await edit_delete(event, "__Notify already enabled.__")
