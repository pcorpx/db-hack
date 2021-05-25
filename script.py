from datacenter.models import Schoolkid, Mark, Chastisement, Lesson, Commendation
import random


def get_child(child_name = "all"):
    if child_name == "all":
        all_children = Schoolkid.objects.all()
        return all_children
    try:
        child = Schoolkid.objects.get(full_name__contains = child_name)
        return child
    except Schoolkid.DoesNotExist:
        print("The children with certain name was not found")

def get_marks(child_name, points__lte = 5, first="no"):
    marks = Mark.objects.filter(points__lte = points__lte, schoolkid=get_child(child_name = child_name))
    if first="yes":
        first_mark = marks.first()
        return first_mark
    return marks

def fix_marks(child_name, points__lte = 3, first = "no"):
    marks = get_marks(child_name = child_name, points__lte = points__lte, first= first)
    result = marks.update(points=5)
    marks.save()
    print(f"{result} marks were changed")
    return result

def get_notes(child_name="all"):
    bad_notes = Chastisement.objects.all()
    if child_name != "all":s
        bad_notes = bad_notes.filter(schoolkid=get_child(child_name=child_name))  
    return bad_notes

def remove_chastisements(child_name):
   bad_notes = get_notes(child_name=child_name)
   result = bad_notes.delete()
   print(f"{result} notes were deleted")
   return result

def get_lessons(year_of_study=None, group_letter=None, subject = None):
    lessons = Lesson.objects.all()
    if ((year_of_study is not None) and  (group_letter is not None)):
        lessons = lessons.filter(year_of_study=child.year_of_study, 
                                group_letter=child.group_letter)
    if subject != None:
        lesson = lesson.filter(subject__title=subject)
    return lessons

def get_lesson(subject, date):
    try:
        subject_lessons = lessons.filter(subject__title=subject)
        lesson = subject_lessons.get(date=date)
        return lesson
    except Lesson.DoesNotExist:
        print("The lesson of picked subject with certain date was not found")

def create_commendation(child_name, subj, words):
    try:
        child = Schoolkid.objects.get(full_name__contains=child_name)
    except Schoolkid.DoesNotExist:
        print("The children with certain name was not found")
        return
    subj_lessons = Lesson.objects.filter(subject__title=subj, 
                                        year_of_study=child.year_of_study, 
                                        group_letter=child.group_letter).order_by('date')
    ok = False
    while not ok:
        lesson = random.choice(subj_lessons)
        if len(Commendation.objects.filter(created=lesson.date, subject=lesson.subject, 
                                    schoolkid=child)) > 0:
                                    
            print('Schoolkid already has commendation on this lesson')
        else:
            result = Commendation.objects.create(text=random.choice(words), 
                                                 created=lesson.date, 
                                                 schoolkid=child,
                                                 subject=lesson.subject,
                                                 teacher=lesson.teacher
                                                 )
            print(result.text, result.created, result.subject, result.schoolkid)
            result.save()
            ok = True



child = get_child()
print(child)

all_marks = get_marks(child_name="Фролов Иван")
print(all_marks)

bad_marks = get_marks(child_name="Фролов Иван", points__lte=3)
print(bad_marks)

first_mark = get_marks(child_name="Фролов Иван", first="yes")

result = fix_marks(child_name="Фролов Иван", first="yes")

print (first_mark.points)

result = fix_marks(child_name="Фролов Иван")

bad_notes = get_notes()
print(bad_notes)

bad_notes = get_notes(child_name="Фролов Иван")
print(bad_notes)

result = remove_chastisements(child_name="Фролов Иван")

result = remove_chastisements(child_name="Голубев Феофан")

all_lessons = get_lessons()
print(all_lessons)

lessons = get_lessons(year_of_study=child.year_of_study, 
                      group_letter=child.group_letter)

print(lessons)

math_lessons = get_lessons(year_of_study=child.year_of_study, 
                           group_letter=child.group_letter,
                           subject__title="Математика")
print(math_lessons)


lesson = get_lesson("Математика", "2018-10-01")
    

result = Commendation.objects.create(text="Хвалю", 
                                        created=lesson.date, 
                                        schoolkid=child,
                                        subject=lesson.subject,
                                        teacher=lesson.teacher
                                        )
print(result)

# Функция для создания похвалы
words = ["Молодец!",
         "Отлично!",
         "Хорошо!",
         "Гораздо лучше, чем я ожидал!",
         "Ты меня приятно удивил!",
         "Великолепно!",
         "Прекрасно!",
         "Ты меня очень обрадовал!"]



create_commendation('Фролов Иван', 'Музыка')