from datacenter.models import Schoolkid, Mark, Chastisement, Lesson, Commendation
import random

# Вывод всех учеников:
children = Schoolkid.objects.all()
print(children)

# Вывод имени Фролова Ивана
child = Schoolkid.objects.get(full_name__contains = "Фролов Иван")
print(child)

# Вывод всех оценок ученика
all_marks = Mark.objects.filter(schoolkid=child)
print(all_marks)

# Вывод плохих оценок ученика
bad_marks = Mark.objects.filter(points__lte = 3, schoolkid=child)
print(bad_marks)

# Исправление первой двойки
first_mark = bad_marks.first()
first_mark.points = 5
first_mark.save()
print (first_mark.points)

# Функция исправления плохих оценок ученика
def fix_marks(schoolkid):
    marks = Mark.objects.filter(points__lte = 3, schoolkid=schoolkid)
    marks.update(points=5)

result = fix_marks(child)
print(result)

# Вывод всех замечаний
bad_notes = Chastisement.objects.all()
print(bad_notes)

# Фильтрация замечаний ученика
bad_notes = bad_notes.filter(schoolkid=child)
print(bad_notes)

# Удаление замечаний ученика
bad_notes.delete()

# Функция удаления замечений
def remove_chastisements(schoolkid):
   bad_notes = Chastisement.objects.filter(schoolkid=schoolkid)
   bad_notes.delete()

another_child = Schoolkid.objects.get(full_name__contains = "Голубев Феофан")

remove_chastisements(another_child)

# Вывод всех занятий
all_lessons = Lesson.objects.all()
print(all_lessons)

# Вывод занятий ученика
lessons = Lesson.objects.filter(year_of_study=child.year_of_study, 
                                group_letter=child.group_letter)

print(lessons)

math_lessons = lessons.filter(subject__title="Математика")
print(math_lessons)

# Похвала для ученика
lesson = math_lessons.get(date="2018-10-01")
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

def create_commendation(child, subj):
    child = Schoolkid.objects.get(full_name__contains=child)
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

create_commendation('Фролов Иван', 'Музыка')