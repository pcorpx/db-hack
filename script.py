import sys
import logging

from datacenter.models import Schoolkid, Mark, Chastisement
from datacenter.models import Lesson, Commendation


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
c_handler = logging.StreamHandler(sys.stdout)
c_handler.setLevel(logging.INFO)
logger.addHandler(c_handler)


def get_all_children():
    all_children = Schoolkid.objects.all()
    return all_children


def get_child(child_name):
    try:
        child = Schoolkid.objects.get(full_name__contains=child_name)
        return child
    except Schoolkid.MultipleObjectsReturned:
        logger.warning("There were several children found with defined name")
    except Schoolkid.DoesNotExist:
        logger.warning("The children with certain name was not found")


def get_marks(child_name, points_lte=5, first="no"):
    child = get_child(child_name=child_name)
    if child:
        marks = Mark.objects.filter(points__lte=points_lte,
                                    schoolkid=child)
        if first == "yes":
            first_mark = marks.first()
            return first_mark
        return marks


def fix_marks(child_name, points_lte=3, first="no"):
    marks = get_marks(child_name=child_name, points_lte=points_lte,
                      first=first)
    if marks and first == "yes":
        marks.points = 5
        logger.info("First mark was changed")
        return marks
    elif marks:
        fixed_marks_number = marks.update(points=5)
        logger.info(f"{str(fixed_marks_number)} marks were changed")
        return fixed_marks_number
    else:
        logger.info("There are no bad points")


def get_chastisements(child_name="all"):
    chastisements = Chastisement.objects.all()
    if child_name != "all":
        child = get_child(child_name=child_name)
        if child:
            chastisements = chastisements.filter(
                schoolkid=child)
        else:
            return
    return chastisements


def remove_chastisements(child_name):
    chastisements = get_chastisements(child_name=child_name)
    if chastisements:
        removed_chastisements_number = chastisements.delete()
        removed_chastisements_number = removed_chastisements_number[0]
        message_info = (
            f"{removed_chastisements_number} "
            f"chastisements were removed"
        )
    else:
        removed_chastisements_number = 0
        message_info = "There were no chastisement removed"
    logger.info(message_info)
    return removed_chastisements_number


def get_lessons(child_name="all", subject=None):
    child = get_child(child_name=child_name)
    if child:
        lessons = Lesson.objects.all()
        if child_name == "all":
            return lessons
        lessons = lessons.filter(year_of_study=child.year_of_study,
                                 group_letter=child.group_letter)
        if subject:
            lessons = lessons.filter(subject__title=subject)
        return lessons


def get_lesson(child_name, subject, date):
    try:
        subject_lessons = get_lessons(child_name, subject)
        if subject_lessons:
            lesson = subject_lessons.get(date=date)
            return lesson
    except Lesson.DoesNotExist:
        logger.warning("The lesson of picked subject with \
                       certain date was not found")


def create_commendation(child_name, subject, commendation_content, date=None):
    try:
        child = Schoolkid.objects.get(full_name__contains=child_name)
    except Schoolkid.MultipleObjectsReturned:
        logger.warning("There were several children found with defined name")
        return
    except Schoolkid.DoesNotExist:
        logger.warning("The children with certain name was not found")
        return
    subject_lessons = Lesson.objects.filter(
        subject__title=subject,
        year_of_study=child.year_of_study,
        group_letter=child.group_letter
    ).order_by('date')

    if (isinstance(commendation_content, str) and date):
        lesson = subject_lessons.get(date=date)
        created_commendation = Commendation.objects.create(
            text=commendation_content,
            created=lesson.date,
            schoolkid=child,
            subject=lesson.subject,
            teacher=lesson.teacher
        )
        created_commendation.save()
        created_date = created_commendation.created.strftime("%Y-%m-%d")
        created_commendation.created = created_date
        return created_commendation


def main():
    child = get_child(child_name="Фролов Иван")
    logger.info(child)

    all_marks = get_marks(child_name="Фролов Иван")
    logger.info(all_marks)

    bad_marks = get_marks(child_name="Фролов Иван", points_lte=3)
    logger.info(bad_marks)

    first_mark = get_marks(child_name="Фролов Иван", points_lte=3,
                           first="yes")
    logger.info(first_mark)

    fixed_mark = fix_marks(child_name="Фролов Иван", first="yes")
    if fixed_mark:
        logger.info(fixed_mark.points)

    fixed_marks_number = fix_marks(child_name="Фролов Иван")
    logger.info(fixed_marks_number)

    chastisements = get_chastisements()
    logger.info(chastisements)

    chastisements = get_chastisements(child_name="Фролов Иван")
    logger.info(chastisements)

    removed_chastisements_number = remove_chastisements(
        child_name="Фролов Иван"
    )
    logger.info(removed_chastisements_number)

    removed_chastisements_number = remove_chastisements(
        child_name="Голубев Феофан"
    )

    logger.info(removed_chastisements_number)

    all_lessons = get_lessons()
    logger.info(all_lessons)

    lessons = get_lessons(child_name="Фролов Иван")
    logger.info(lessons)

    math_lessons = get_lessons(child_name="Фролов Иван",
                               subject="Математика")
    logger.info(math_lessons)

    lesson = get_lesson("Фролов Иван", "Математика", "2018-10-01")
    logger.info(lesson)

    created_commendation = create_commendation("Фролов Иван", "Математика",
                                               "Хвалю", "2018-10-01")

    message_info = (
        f"{created_commendation.text}, "
        f"{created_commendation.created}, "
        f"{created_commendation.subject.title}, "
        f"{created_commendation.schoolkid.full_name}"
    )

    logger.info(message_info)
