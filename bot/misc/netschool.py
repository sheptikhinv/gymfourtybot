import os

from netschoolapi import NetSchoolAPI

from bot.database.attachment import Attachment
from bot.misc import xlsx, NetSchoolKeys


async def get_new_timetables(classrooms):
    ns = NetSchoolAPI('http://schoolroo.ru/')

    await ns.login(NetSchoolKeys.LOGIN, NetSchoolKeys.PASSWORD, "МАОУ Гимназия № 40")

    announcements = await ns.announcements()

    result = []
    for announcement in announcements:
        if "расписание" in announcement.name.lower() and announcement.attachments != []:
            for attachment in announcement.attachments:
                name = attachment.name.replace(".xlsx", "") + str(attachment.id) + ".xlsx"
                attachmentObj = Attachment(name, attachment.id, announcement.post_date)
                if "11)" in attachment.name and attachmentObj.is_new():
                    attachmentObj.create_new()
                    attachment_file = await ns.download_attachment_as_bytes(attachment)
                    try:
                        with open("files/" + name, "wb") as f:
                            f.write(attachment_file.getbuffer())
                    except FileNotFoundError as error:
                        os.mkdir("files")
                        with open("files/" + name, "wb") as f:
                            f.write(attachment_file.getbuffer())
                    result.append(xlsx.getTimetable("files/" + name, classrooms))

    await ns.logout()
    return result
