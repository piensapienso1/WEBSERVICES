# coding: utf-8
from sqlalchemy import Column, DateTime, ForeignKey, INTEGER, String, text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class City(Base):
    __tablename__ = 'city'

    city_id = Column(INTEGER(11), primary_key=True)
    name = Column(String(150))


class Province(City):
    __tablename__ = 'province'

    province_id = Column(ForeignKey('city.city_id'), primary_key=True)
    id_city = Column(INTEGER(11))
    name = Column(String(150))


class MemoType(Base):
    __tablename__ = 'memo_type'

    memo_type_id = Column(INTEGER(11), primary_key=True)
    name = Column(String(45))
    name_description = Column(String(100))


class QualificationType(Base):
    __tablename__ = 'qualification_type'

    qualification_type_id = Column(INTEGER(11), primary_key=True)
    name = Column(String(50))
    description = Column(String(100))
    weight_value = Column(INTEGER(11))


class UserType(Base):
    __tablename__ = 'user_type'

    user_type_id = Column(INTEGER(11), primary_key=True)
    name = Column(String(45))


class Memo(Base):
    __tablename__ = 'memo'

    memo_id = Column(INTEGER(11), primary_key=True)
    id_memo_type = Column(ForeignKey('memo_type.memo_type_id'), index=True)
    desc = Column(String(100))
    date = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))

    memo_type = relationship('MemoType')


class RuleTypeUsr(Base):
    __tablename__ = 'rule_type_usr'

    rule_type_usr_id = Column(INTEGER(11), primary_key=True)
    id_user_type = Column(ForeignKey('user_type.user_type_id'), index=True)
    menu = Column(String(200))

    user_type = relationship('UserType')


class User(Base):
    __tablename__ = 'user'

    user_id = Column(INTEGER(11), primary_key=True)
    id_type = Column(ForeignKey('user_type.user_type_id'), index=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    phone = Column(String(45))
    cell_phone = Column(String(45))
    status = Column(String(45))
    date = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    public_id = Column(String(200), nullable=False, unique=True)

    user_type = relationship('UserType')


class LoggedUser(Base):
    __tablename__ = 'logged_users'

    logged_users_id = Column(INTEGER(11), primary_key=True)
    id_user = Column(ForeignKey('user.user_id'), index=True)
    user_name = Column(String(45))
    password = Column(String(45))
    status = Column(INTEGER(11))
    date = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))

    user = relationship('User')


class MemoDistribution(Base):
    __tablename__ = 'memo_distribution'

    memo_distribution_id = Column(INTEGER(11), primary_key=True)
    id_memo = Column(ForeignKey('memo.memo_id'), index=True)
    id_user_pather = Column(ForeignKey('user.user_id'), index=True)

    memo = relationship('Memo')
    user = relationship('User')


class Neighborhood(Base):
    __tablename__ = 'neighborhood'

    neighborhood_id = Column(INTEGER(11), primary_key=True)
    id_province = Column(ForeignKey('province.province_id'), index=True)
    name = Column(String(150))

    province = relationship('Province')


class Zone(Base):
    __tablename__ = 'zone'

    zone_id = Column(INTEGER(11), primary_key=True)
    id_neigborhood = Column(ForeignKey('neighborhood.neighborhood_id'), index=True)
    name = Column(String(150))

    neighborhood = relationship('Neighborhood')


class School(Base):
    __tablename__ = 'school'

    school_id = Column(INTEGER(11), primary_key=True)
    name = Column(String(100))
    id_city = Column(ForeignKey('city.city_id'), index=True)
    id_province = Column(ForeignKey('province.province_id'), index=True)
    id_neighborhood = Column(ForeignKey('neighborhood.neighborhood_id'), index=True)
    id_zone = Column(ForeignKey('zone.zone_id'), index=True)
    street = Column(String(100))
    block = Column(String(45))
    apartment = Column(String(45))
    logo = Column(String(200))
    location = Column(String(60))
    date = Column(DateTime)

    city = relationship('City')
    neighborhood = relationship('Neighborhood')
    province = relationship('Province')
    zone = relationship('Zone')


class Grade(Base):
    __tablename__ = 'grade'

    grade_id = Column(INTEGER(11), primary_key=True)
    name = Column(String(45))
    description = Column(String(100))
    id_school = Column(ForeignKey('school.school_id'), index=True)

    school = relationship('School')


class UserSchool(Base):
    __tablename__ = 'user_school'

    user_school_id = Column(INTEGER(11), primary_key=True)
    user_id = Column(ForeignKey('user.user_id'), index=True)
    school_id = Column(ForeignKey('school.school_id'), index=True)
    date = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))

    school = relationship('School')
    user = relationship('User')


class Course(Base):
    __tablename__ = 'course'

    course_id = Column(INTEGER(11), primary_key=True)
    name = Column(String(45))
    description = Column(String(100))
    id_grade = Column(ForeignKey('grade.grade_id'), index=True)

    grade = relationship('Grade')


class Subject(Base):
    __tablename__ = 'subject'

    subject_id = Column(INTEGER(11), primary_key=True)
    id_grade = Column(ForeignKey('grade.grade_id'), index=True)
    name = Column(String(45))

    grade = relationship('Grade')


class Qualification(Base):
    __tablename__ = 'qualification'

    qualification_id = Column(INTEGER(11), primary_key=True)
    id_qualification_type = Column(ForeignKey('qualification_type.qualification_type_id'), index=True)
    id_course = Column(ForeignKey('course.course_id'), index=True)
    id_usr_student = Column(ForeignKey('user.user_id'), index=True)
    id_subject = Column(ForeignKey('subject.subject_id'), index=True)
    value = Column(INTEGER(11))

    course = relationship('Course')
    qualification_type = relationship('QualificationType')
    subject = relationship('Subject')
    user = relationship('User')


class StudentCourse(Base):
    __tablename__ = 'student_course'

    student_course_id = Column(INTEGER(11), primary_key=True)
    id_usr_student = Column(ForeignKey('user.user_id'), index=True)
    id_course = Column(ForeignKey('course.course_id'), index=True)
    date = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))

    course = relationship('Course')
    user = relationship('User')


class TeacherCourse(Base):
    __tablename__ = 'teacher_course'

    teacher_course_id = Column(INTEGER(11), primary_key=True)
    id_usr_teacher = Column(ForeignKey('user.user_id'), index=True)
    id_course = Column(ForeignKey('course.course_id'), index=True)
    date = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))

    course = relationship('Course')
    user = relationship('User')
