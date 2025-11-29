from datetime import datetime
from lib.enrollment import Student, Course, Enrollment


def test_course_count():
    Enrollment.all = []
    student = Student("Alice")
    course1 = Course("Math")
    course2 = Course("History")
    student.enroll(course1)
    student.enroll(course2)

    assert student.course_count() == 2
    assert len(student.get_enrollments()) == 2


def test_aggregate_enrollments_per_day():
    Enrollment.all = []
    s1 = Student("S1")
    s2 = Student("S2")
    c = Course("Chemistry")

    s1.enroll(c)
    s2.enroll(c)

    d1 = datetime(2020, 1, 1, 10, 0, 0)
    # set the first two enrollments to the same date
    for e in Enrollment.all[:2]:
        e._enrollment_date = d1

    # add another enrollment on a different date
    s3 = Student("S3")
    c2 = Course("Physics")
    s3.enroll(c2)
    Enrollment.all[-1]._enrollment_date = datetime(2020, 1, 2, 11, 0, 0)

    counts = Enrollment.aggregate_enrollments_per_day()
    assert counts.get(d1.date()) == 2
    assert counts.get(datetime(2020, 1, 2).date()) == 1


def test_aggregate_average_grade_and_no_grades():
    Enrollment.all = []
    student = Student("Tom")
    # no grades yet -> 0.0
    assert student.aggregate_average_grade() == 0.0

    # create two enrollments and assign grades
    c1 = Course("Art")
    c2 = Course("Music")
    student.enroll(c1)
    student.enroll(c2)

    e1, e2 = student.get_enrollments()
    student.set_grade(e1, 80)
    student.set_grade(e2, 90)

    assert student.aggregate_average_grade() == 85.0
