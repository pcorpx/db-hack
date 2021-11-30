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


def get_marks(child_name, points_lte=5):
    child = get_child(child_name=child_name)
    if child:
        marks = Mark.objects.filter(points__lte=points_lte,
                                    schoolkid=child)
        return marks


def fix_marks(child_name, points_lte=3):
    marks = get_marks(child_name=child_name, points_lte=points_lte)
    if marks:
        fixed_marks_number = marks.update(points=5)
        logger.info(f"{fixed_marks_number} mark(`s) were changed")
        return fixed_marks_number
    else:
        logger.info("There are no bad points")


def get_chastisements(child_name):
    chastisements = Chastisement.objects.all()
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


def get_lessons(child_name, subject=None):
    child = get_child(child_name=child_name)
    if child:
        lessons = Lesson.objects.all()
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
        return created_commendation
