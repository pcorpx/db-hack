# db-hack

This script was made for studying data manipulation of Django database using  shell

## Getting Started

You can use it by copying content into Django shell directly or putting this script into folder with manage.py and importing it in a shell.

To import script in a shell use command:

```python 
from script import *
```

###### Getting all children
To get all children from db use function get_all_children:

```python
all_chilren = get_all_children()
```

###### Getting a child
To get child use function get_child with argument child_name. Use unique name of a child to pass it.

```python
child = get_child(child_name="Фролов Иван")
```

###### Getting marks
To get all marks of a child use function get_marks with only one compulsory argument child_name.

```python
all_marks = get_marks(child_name="Фролов Иван")
```

To get bad marks use function get_marks. You should provide it with two arguments: first positional argument child_name is compulsory, second optional argument point_lte serves to filter marks by their value accordingly less or equal than value passed in the argument. (default value of point_lte is 5)

```python
bad_marks = get_marks(child_name="Фролов Иван", points_lte=3)
```

###### Fixing marks

To fix marks use function fix_marks. It has first positional argument child_name which is compulsory and two optional arguments: point_lte (default value is 3) and first (default value is "no").
To fix all bad marks just provide function with child_name:

```python
fixed_marks_number = fix_marks(child_name="Фролов Иван")
```

The function will return the number of bad marks were fixed.

###### Getting chastisements

To get all chastisements use function get_notes without arguments:

```python
bad_notes = get_notes()
```

To get chastisements of a child use function get_notes() with argument child_name:

```python
bad_notes = get_notes(child_name="Фролов Иван")
```

###### Removing chastisements

To remove chastisments of a child use function remove_chastisements with child_name argument:

```python
removed_chastisements_number = remove_chastisements(child_name="Фролов Иван")
```

###### Getting lessons

To get all lessons use functions get_lessons without arguments:

```python
all_lessons = get_lessons()
```

To get lessons of a child provide function with child_name argument:

```python
lessons = get_lessons(child_name="Фролов Иван")
```

To get child lessons of certain subject use optional argument subject:

```python
math_lessons = get_lessons(child_name="Фролов Иван", subject="Математика")
```


###### Getting a lesson

To get certain lesson of child use get_lesson function with three positional arguments child_name, subject, date:

```python
lesson = get_lesson("Фролов Иван", "Математика", "2018-10-01")
```

###### Creating commendation

To create one commendation for certain lesson use create_commendation fumction with four arguments child_name, subject, words, date:

```python
created_commendation = create_commendation("Фролов Иван", "Математика", "Хвалю", "2018-10-01")
```

### Checking modifications made by script

Use your browser to follow this address: [127.0.0.1:8000](http://127.0.0.1:8000) and check for data modifications

### Prerequisites

You should clone and deploy e-diary using instructions in README there https://github.com/devmanorg/e-diary

### Installation

To start Django shell just use:

```bash
python manage.py shell
```
