import openpyxl


def getTimetable(excel_file, classrooms):
    table = openpyxl.load_workbook(excel_file)
    sheet = table.active
    classRows = ["C", "E", "G"]
    timeRow = "B"
    cabRows = ["D", "F", "M"]
    timetables = {}

    for row in classRows:
        for i in range(1, 80):
            classCell = str(sheet[row + str(i)].value).replace(" ", "")
            if classCell in classrooms:
                timetables[classCell] = []
                j = 1
                while True:
                    subjCell = sheet[row + str(i + j)].value
                    lessonNumberCell = sheet["A" + str(i + j)].value
                    cabCell = sheet[cabRows[classRows.index(row)] + str(i + j)].value
                    timeCell = sheet[timeRow + str(i+j)].value

                    if isinstance(subjCell, str) and subjCell.__contains__("2 смена") or isinstance(subjCell,
                                                                                                    str) and subjCell.replace(
                            " ", "") in classrooms or lessonNumberCell is None:
                        break
                    if isinstance(sheet[row + str(i + j)], openpyxl.cell.cell.MergedCell):
                        for cell in sheet.merged_cells:
                            if row + str(i + j) in cell:
                                subjCell = sheet.cell(cell.left[0][0], cell.left[0][1]).value
                                break
                    lesson = {"number": lessonNumberCell, "lesson": subjCell, "cabinet": cabCell, "time": timeCell}
                    timetables[classCell].append(lesson)
                    j += 1

    return timetables
