import sys
import random
import logging

from datacenter.models import Schoolkid, Mark, Chastisement
from datacenter.models import Lesson, Commendation


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
c_handler = logging.StreamHandler(sys.stdout)
c_handler.setLevel(logging.INFO)
logger.addHandler(c_handler)


def get_child(child_name="all"):
    if child_name == "all":
        all_children = Schoolkid.objects.all()
        return all_children
    try:
        child = Schoolkid.objects.get(full_name__contains=child_name)
        return child
    except Schoolkid.DoesNotExist:
        logger.warning("The children with certain name was not found")


def get_marks(child_name, points__lte=5, first="no"):
    marks = Mark.objects.filter(points__lte=points__lte, 
                                schoolkid=get_child(child_name=child_name))
    if first == "yes":
        first_mark = marks.first()
        return first_mark
    return marks


def fix_marks(child_name, points__lte=3, first="no"):
    marks = get_marks(child_name=child_name, points__lte=points__lte, 
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
        chastisements = chastisements.filter(
            schoolkid=get_child(child_name=child_name))  
    return chastisements


def remove_chastisements(child_name):
   chastisements = get_chastisements(child_name=child_name)
   removed_chastisements_number = chastisements.delete()
   logger.info(f"{removed_chastisements_number[0]} \
               chastisements were deleted")
   return removed_chastisements_number


def get_lessons(child_name="all", subject=None):
    child = get_child(child_name=child_name)
    lessons = Lesson.objects.all()
    if child_name == "all":
        return lessons
    lessons = lessons.filter(year_of_study=child.year_of_study, 
                             group_letter=child.group_letter)
    if subject != None:
        lessons = lessons.filter(subject__title=subject)
    return lessons


def get_lesson(child_name, subject, date):
    try:
        subject_lessons = get_lessons(child_name, subject)
        lesson = subject_lessons.get(date=date)
        return lesson
    except Lesson.DoesNotExist:
        logger.warning("The lesson of picked subject with \
                       certain date was not found")


def create_commendation(child_name, subject, commendation_text, date=None):
    try:
        child = Schoolkid.objects.get(full_name__contains=child_name)
    except Schoolkid.DoesNotExist:
        logger.warning("The children with certain name was not found")
        return
    subject_lessons = Lesson.objects.filter(
        subject__title=subject, 
        year_of_study=child.year_of_study, 
        group_letter=child.group_letter).order_by('date')
                                            
    if (type(commendation_text) is str) and date is not None:
        lesson = subject_lessons.get(date=date)
        created_commendation = Commendation.objects.create(
            text=commendation_text, 
            created=lesson.date, 
            schoolkid=child,
            subject=lesson.subject,
            teacher=lesson.teacher)
        created_commendation.save()
        created_date = created_commendation.created.strftime("%Y-%m-%d")
        created_commendation.created = created_date
        return created_commendation

    elif (type(commendation_text) is list) and (date is None):
        ok = False
        while not ok:
            lesson = random.choice(subject_lessons)
            if len(Commendation.objects.filter(created=lesson.date, 
                                               subject=lesson.subject, 
                                               schoolkid=child)) > 0:
                                        
                logger.warning("Schoolkid already has commendation on \
                               this lesson")
            else:
                created_commendation = Commendation.objects.create(
                    text=random.choice(commendation_text), 
                    created=lesson.date, 
                    schoolkid=child,
                    subject=lesson.subject,
                    teacher=lesson.teacher)
                created_commendation.save()
                created_date = created_commendation.created
                created_date = created_date.strftime("%Y-%m-%d")
                created_commendation.created = created_date
                ok = True
                return created_commendation


def main():
    child = get_child(child_name="Фролов Иван")
    logger.info(child)

    all_marks = get_marks(child_name="Фролов Иван")
    logger.info(all_marks)

    bad_marks = get_marks(child_name="Фролов Иван", points__lte=3)
    logger.info(bad_marks)

    first_mark = get_marks(child_name="Фролов Иван", points__lte=3, 
                           first="yes")
    logger.info(first_mark)

    fixed_mark = fix_marks(child_name="Фролов Иван", first="yes")
    if fixed_mark:
        logger.info(fixed_mark.points)

    fixed_marks_number = fix_marks(child_name="Фролов Иван")
    logger.info(fixed_marks_number)

    chastisements = get_chastisements()
    logger.info(chastisements)

    chastisements= get_chastisements(child_name="Фролов Иван")
    logger.info(chastisements)

    result = remove_chastisements(child_name="Фролов Иван")
    logger.info(result)

    removed_chastisements_number = remove_chastisements(
        child_name="Голубев Феофан")
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
    logger.info(f"{created_commendation.text}, {created_commendation.created}, 
                {created_commendation.subject.title}, 
                {created_commendation.schoolkid.full_name}")

    commendation_text = [
        "Молодец!",
        "Отлично!",
        "Хорошо!",
        "Гораздо лучше, чем я ожидал!",
        "Ты меня приятно удивил!",
        "Великолепно!",
        "Прекрасно!",
        "Ты меня очень обрадовал!"
    ]

    created_commendation = create_commendation("Фролов Иван", "Музыка", 
                                               commendation_text)
    logger.info(f"{created_commendation.text}, 
                {created_commendation.created}, 
                {created_commendation.subject.title}, 
                {created_commendation.schoolkid.full_name}")



