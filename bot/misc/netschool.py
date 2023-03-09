import os

from netschoolapi import NetSchoolAPI

from bot.database.attachment import Attachment
from bot.misc import xlsx, NetSchoolKeys

from io import BytesIO


async def get_new_timetables(classrooms):
    ns = NetSchoolAPI('http://schoolroo.ru/')

    await ns.login(NetSchoolKeys.LOGIN, NetSchoolKeys.PASSWORD, "МАОУ Гимназия № 40")

    announcements = await ns.announcements()

    result = []
    for announcement in announcements:
        if "расписание" in announcement.name.lower() and announcement.attachments != [] or "расписании" in announcement.name.lower() and announcement.attachments != []:
            for attachment in announcement.attachments:
                name = attachment.name.replace(".xlsx", "") + str(attachment.id) + ".xlsx"
                attachmentObj = Attachment(name, attachment.id, announcement.post_date)
                if "11)" in attachment.name and attachmentObj.is_new():
                    attachmentObj.create_new()
                    file_bytes = BytesIO()
                    attachment_file = await ns.download_attachment(attachment.id, file_bytes)
                    try:
                        with open("files/" + name, "wb") as f:
                            f.write(file_bytes.getbuffer())
                    except FileNotFoundError as error:
                        os.mkdir("files")
                        with open("files/" + name, "wb") as f:
                            f.write(file_bytes.getbuffer())
                    result.append(xlsx.getTimetable("files/" + name, classrooms))

    await ns.logout()
    return result
