from datacenter.models import Schoolkid, Mark, Chastisement, Lesson, Commendation
import random, logging, sys

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
c_handler = logging.StreamHandler(sys.stdout)
c_handler.setLevel(logging.INFO)
logger.addHandler(c_handler)


def get_child(child_name = "all"):
    if child_name == "all":
        all_children = Schoolkid.objects.all()
        return all_children
    try:
        child = Schoolkid.objects.get(full_name__contains = child_name)
        return child
    except Schoolkid.DoesNotExist:
        logger.warning("The children with certain name was not found")

def get_marks(child_name, points__lte = 5, first="no"):
    marks = Mark.objects.filter(points__lte = points__lte, schoolkid=get_child(child_name = child_name))
    if first=="yes":
        first_mark = marks.first()
        return first_mark
    return marks

def fix_marks(child_name, points__lte = 3, first = "no"):

    marks = get_marks(child_name = child_name, points__lte = points__lte, first= first)
    if marks and first == "yes":
        marks.points = 5
        result = "First mark was changed"
        logger.info(result)
        return marks
    elif marks:
        result = marks.update(points=5)
        logger.info(f"{str(result)} marks were changed")
        return result
    else:
        logger.info("There are no bad points")

def get_notes(child_name="all"):
    bad_notes = Chastisement.objects.all()
    if child_name != "all":
        bad_notes = bad_notes.filter(schoolkid=get_child(child_name=child_name))  
    return bad_notes

def remove_chastisements(child_name):
   bad_notes = get_notes(child_name=child_name)
   result = bad_notes.delete()
   logger.info(f"{result[0]} notes were deleted")
   return result

def get_lessons(child_name="all", subject = None):
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
        logger.warning("The lesson of picked subject with certain date was not found")

def create_commendation(child_name, subject, words, date = None):
    try:
        child = Schoolkid.objects.get(full_name__contains=child_name)
    except Schoolkid.DoesNotExist:
        logger.warning("The children with certain name was not found")
        return
    subject_lessons = Lesson.objects.filter(subject__title=subject, 
                                        year_of_study=child.year_of_study, 
                                        group_letter=child.group_letter).order_by('date')
    if (type(words) is str) and date is not None:
        lesson = subject_lessons.get(date=date)
        result = Commendation.objects.create(text=words, 
                                        created=lesson.date, 
                                        schoolkid=child,
                                        subject=lesson.subject,
                                        teacher=lesson.teacher
                                        )
        result.save()
        created_date = result.created.strftime("%Y-%m-%d")
        result.created = created_date
        return result

    elif (type(words) is list) and date is None:
        ok = False
        while not ok:
            lesson = random.choice(subject_lessons)
            if len(Commendation.objects.filter(created=lesson.date, subject=lesson.subject, 
                                        schoolkid=child)) > 0:
                                        
                logger.warning('Schoolkid already has commendation on this lesson')
            else:
                result = Commendation.objects.create(text=random.choice(words), 
                                                    created=lesson.date, 
                                                    schoolkid=child,
                                                    subject=lesson.subject,
                                                    teacher=lesson.teacher
                                                    )
                result.save()
                created_date = result.created.strftime("%Y-%m-%d")
                result.created = created_date
                ok = True
                return result


def main():
    child = get_child(child_name="Фролов Иван")
    logger.info(child)

    all_marks = get_marks(child_name="Фролов Иван")
    logger.info(all_marks)

    bad_marks = get_marks(child_name="Фролов Иван", points__lte=3)
    logger.info(bad_marks)

    first_mark = get_marks(child_name="Фролов Иван", points__lte = 3, first="yes")
    logger.info(first_mark)

    fixed_mark = fix_marks(child_name="Фролов Иван", first="yes")
    if fixed_mark:
        logger.info(fixed_mark.points)

    result = fix_marks(child_name="Фролов Иван")
    logger.info(result)

    bad_notes = get_notes()
    logger.info(bad_notes)

    bad_notes = get_notes(child_name="Фролов Иван")
    logger.info(bad_notes)

    result = remove_chastisements(child_name="Фролов Иван")
    logger.info(result)

    result = remove_chastisements(child_name="Голубев Феофан")
    logger.info(result)

    all_lessons = get_lessons()
    logger.info(all_lessons)

    lessons = get_lessons(child_name="Фролов Иван")
    logger.info(lessons)

    math_lessons = get_lessons(child_name="Фролов Иван",
                               subject="Математика")
    logger.info(math_lessons)


    lesson = get_lesson("Фролов Иван", "Математика", "2018-10-01")
    logger.info(lesson)
        
    result = create_commendation("Фролов Иван", "Математика", "Хвалю", "2018-10-01")
    logger.info(f"{result.text}, {result.created}, {result.subject.title}, {result.schoolkid.full_name}")

    words = ["Молодец!",
            "Отлично!",
            "Хорошо!",
            "Гораздо лучше, чем я ожидал!",
            "Ты меня приятно удивил!",
            "Великолепно!",
            "Прекрасно!",
            "Ты меня очень обрадовал!"]

    result = create_commendation("Фролов Иван", "Музыка", words)
    logger.info(f"{result.text}, {result.created}, {result.subject.title}, {result.schoolkid.full_name}")



