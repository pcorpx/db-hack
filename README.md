# db-hack

This script was made for studying data manipulation of Django database using  shell

## Getting Started

You can use it by copying content into Django shell directly or putting this script into folder with manage.py and importing it in a shell.

To import script in a shell use command:

```python 
from script import *
```

###### Getting all children
To get all children from db use function get_child wihout arguments (default argument have value "all"):

`all_chilren = get_child()`

###### Getting a child
To get child use function get_child with argument child_name. Use unique name of a child to pass it.

`child = get_child(child_name="Фролов Иван")`

###### Getting marks
To get all marks of a child use function get_marks with only one compulsory argument child_name.

`all_marks = get_marks(child_name="Фролов Иван")`

To get bad marks use function get_marks. You should provide it with two arguments: first positional argument child_name is compulsory, second optional argument point_lte serves to filter marks by their value accordingly less or equal than value passed in the argument. (default value of point_lte is 5)

`bad_marks = get_marks(child_name="Фролов Иван", points__lte=3)`

If you want to get only first mark add an optional argument first with the value of "yes" to the function get_marks:

`first_mark = get_marks(child_name="Фролов Иван", points__lte = 3, first="yes")`

###### Fixing marks

To fix marks use function fix_marks. It has first positional argument child_name which is compulsory and two optional arguments: point_lte (default value is 3) and first (default value is "no").
To fix all bad marks just provide function with child_name:

`fixed_marks_number = fix_marks(child_name="Фролов Иван")`

The function will return the number of bad marks were fixed.

To fix only first bad mark provide function with optional argument first with the value of "yes":

`fixed_mark = fix_marks(child_name="Фролов Иван", first="yes")`

The function will retun the fixed mark.

###### Getting chastisements

To get all chastisements use function get_notes without arguments:

`bad_notes = get_notes()`

To get chastisements of a child use function get_notes() with argument child_name:

`bad_notes = get_notes(child_name="Фролов Иван")`

###### Removing chastisements

To remove chastisments of a child use function remove_chastisements with child_name argument:

`result = remove_chastisements(child_name="Фролов Иван")`

###### Getting lessons

To get all lessons use functions get_lessons without arguments:

`all_lessons = get_lessons()`

To get lessons of a child provide function with child_name argument:

`lessons = get_lessons(child_name="Фролов Иван")`

To get child lessons of certain subject use optional argument subject:

`math_lessons = get_lessons(child_name="Фролов Иван", subject="Математика")`


###### Getting a lesson

To get certain lesson of child use get_lesson function with three positional arguments child_name, subject, date:

`lesson = get_lesson("Фролов Иван", "Математика", "2018-10-01")`

###### Creating commendation

To create one commendation for certain lesson use create_commendation fumction with four arguments child_name, subject, words, date:

`result = create_commendation("Фролов Иван", "Математика", "Хвалю", "2018-10-01")`

To create several commendations of a child you should define list of notes named words, than you should use create_commendation function with arguments child_name, subject and words (which was previously defined as a list):

```
words = ["Молодец!",
         "Отлично!",
         "Хорошо!",
         "Гораздо лучше, чем я ожидал!",
         "Ты меня приятно удивил!",
         "Великолепно!",
         "Прекрасно!",
         "Ты меня очень обрадовал!"]

result = create_commendation("Фролов Иван", "Музыка", words)
```

### Prerequisites

You should clone and deploy e-diary using instructions in README there https://github.com/devmanorg/e-diary

### Installation

To start Django shell just use:

`python manage.py shell`

## Tests

To pass all tasks of the module use function:

`main()`

Use your browser to follow this address: [127.0.0.1:8000](http://127.0.0.1:8000) and check for data modifications
