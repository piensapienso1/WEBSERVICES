from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime
from enum import Enum
import uuid

Base = declarative_base()
metadata = Base.metadata

class ResponseType(Enum):
    SUCCESS = 'Success'
    ERROR = 'Error'
    OK = 'Ok'
    NO = 'No'

class Response():
    typeResponse = None
    htmlCode = 0
    description = ''
    value = None

    def __init__(self,typeResponse,code,description,value):
        self.typeResponse = typeResponse.value
        self.htmlCode = code
        self.description = description
        self.value = value

    def serialize(self):
        return {
            'typeResponse': self.typeResponse,
            'htmlCode': self.htmlCode,
            'description': self.description,
            'value' : self.value
        }

class Province(Base):
    __tablename__ = 'province'

    province_id = Column(Integer, primary_key=True)
    name = Column(String(150))

def toProvince(items):
    province = Province()

    if 'name' in items:
        province.name = items['name']

    return province

def provinceToArray(provinces):
    output = []

    for province in provinces:
        province_data = {}
        province_data['province_id'] = province.province_id
        province_data['name'] = province.name
        output.append(province_data)

    return output

def activityToArray(activities):
    output = []

    for activity in activities:
        activity_data = {}
        activity_data['activity_id'] = activity.activity_id
        activity_data['user_id'] = activity.user_id
        activity_data['title'] = activity.title
        activity_data['description'] = activity.description
        activity_data['date'] = activity.date.strftime('%b %d %Y %I:%M%p')
        activity_data['student_name'] = activity.student_name
        output.append(activity_data)

    return output

class Neighborhood(Base):
    __tablename__ = 'neighborhood'

    neighborhood_id = Column(Integer, primary_key=True)
    id_province = Column(ForeignKey('province.province_id'), index=True)
    name = Column(String(150))

    province = relationship('Province')

def toNeighborhood(items):
    neighborhood = Neighborhood()

    if 'id_province' in items:
        neighborhood.id_province = items['id_province']
    if 'name' in items:
        neighborhood.name = items['name']

    return neighborhood

def neighborhoodToArray(neighborhoods):
    output = []

    for neighborhood in neighborhoods:
        neighborhood_data = {}
        neighborhood_data['neighborhood_id'] = neighborhood.neighborhood_id
        neighborhood_data['id_province'] = neighborhood.id_province
        neighborhood_data['name'] = neighborhood.name
        output.append(neighborhood_data)

    return output

class User(Base):
    __tablename__ = 'user'

    user_id = Column(Integer, primary_key=True)
    id_type = Column(ForeignKey('user_type.user_type_id'), index=True)
    id_neighborhood = Column(ForeignKey('neighborhood.neighborhood_id'), index=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    phone = Column(String(45))
    cell_phone = Column(String(45))
    status = Column(String(45))
    date = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    public_id = Column(String(200), nullable=False, unique=True)
    document_id = Column(String(45))
    date_birth = Column(DateTime)
    age = Column(Integer)
    gender = Column(String(40))
    email = Column(String(150))
    user_code = Column(String(45))

    user_type = relationship('UserType')
    neighborhood = relationship('Neighborhood')

def toUser(items):
    user = User()

    if 'id_type' in items:
        user.id_type = items['id_type']
    if 'first_name' in items:
        user.first_name = items['first_name']
    if 'last_name' in items:
        user.last_name = items['last_name']
    if 'id_neighborhood' in items:
        user.id_neighborhood = items['id_neighborhood']
    if 'phone' in items:
        user.phone = items['phone']
    if 'cell_phone' in items:
        user.cell_phone = items['cell_phone']
    if 'status' in items:
        user.status = items['status']
    if 'document_id' in items:
        user.document_id = items['document_id']
    if 'date_birth' in items:
        user.date_birth = items['date_birth']
    if 'age' in items:
        user.age = items['age']
    if 'gender' in items:
        user.gender = items['gender']
    if 'email' in items:
        user.email = items['email']
    if 'user_code' in items:
        user.user_code = items['user_code']

    user.public_id = str(uuid.uuid4())
    user.date = datetime.datetime.now()

    return user

def userToArray(users):
    output = []

    for user in users:
        user_data = {}
        user_data['user_id'] = user.user_id
        user_data['first_name'] = user.first_name
        user_data['last_name'] = user.last_name
        user_data['phone'] = user.phone
        user_data['id_neighborhood'] = user.id_neighborhood
        user_data['cell_phone'] = user.cell_phone
        user_data['status'] = user.status
        user_data['date'] = user.date
        user_data['public_id'] = user.public_id
        user_data['type'] = user.user_type.name
        user_data['date_birth'] = user.date_birth
        user_data['document_id'] = user.document_id
        user_data['age'] = user.age
        user_data['gender'] = user.gender
        user_data['email'] = user.email
        user_data['user_code'] = user.user_code
        output.append(user_data)

    return output

def userToArrayStudents(users):
    output = []

    for user in users:
        user_data = {}
        user_data['user_id'] = user.user_id
        user_data['first_name'] = user.first_name
        user_data['last_name'] = user.last_name
        user_data['phone'] = user.phone
        user_data['cell_phone'] = user.cell_phone
        user_data['status'] = user.status
        user_data['date'] = user.date
        user_data['public_id'] = user.public_id
        user_data['type'] = user.type
        user_data['date_birth'] = user.date_birth
        user_data['document_id'] = user.document_id
        user_data['age'] = user.age
        user_data['gender'] = user.gender
        user_data['email'] = user.email
        user_data['user_code'] = user.user_code
        output.append(user_data)

    return output

def userToArrayStudentsbyTutor(users):
    output = []

    for user in users:
        user_data = {}
        user_data['user_id'] = user.user_id
        user_data['first_name'] = user.first_name
        user_data['last_name'] = user.last_name
        user_data['status'] = user.status
        user_data['course_id'] = user.course_id
        user_data['course_name'] = user.course_name
        user_data['public_id'] = user.public_id
        user_data['age'] = user.age
        user_data['user_code'] = user.user_code
        output.append(user_data)

    return output

def studentToArraySchool(users):
    output = []

    for user in users:
        user_data = {}
        user_data['school_id'] = user.school_id
        user_data['school_name'] = user.school_name
        user_data['school_code'] = user.school_code
        user_data['count_students'] = user.count_students
        output.append(user_data)

    return output

def subjectStudentToArray(users):
    output = []

    for user in users:
        user_data = {}
        user_data['course_id'] = user.course_id
        user_data['course_name'] = user.course_name
        user_data['subject_id'] = user.subject_id
        user_data['subject_name'] = user.subject_name
        user_data['time_from'] = user.time_from
        user_data['time_to'] = user.time_to
        user_data['count_students'] = user.count_students
        output.append(user_data)

    return output

def infoStudentToArraySchool(users):
    output = []

    for user in users:
        user_data = {}
        user_data['school_name'] = user.school_name
        user_data['school_phone'] = user.school_phone
        user_data['school_address'] = user.school_address
        user_data['school_code'] = user.school_code
        user_data['director_code'] = user.director_code
        user_data['director_name'] = user.director_name
        user_data['user_id'] = user.user_id
        user_data['user_code'] = user.user_code
        user_data['student_name'] = user.student_name
        output.append(user_data)

    return output

def infoListStudentToArray(users):
    output = []

    for user in users:
        user_data = {}
        user_data['user_id'] = user.user_id
        user_data['user_code'] = user.user_code
        user_data['student_name'] = user.student_name
        user_data['age'] = user.age
        user_data['gender'] = user.gender
        user_data['date_birth'] = user.date_birth
        output.append(user_data)

    return output


def infoListTeacherToArray(users):
    output = []

    for user in users:
        user_data = {}
        user_data['user_id'] = user.user_id
        user_data['user_code'] = user.user_code
        user_data['teacher_name'] = user.teacher_name
        user_data['subject_id'] = user.subject_id
        user_data['subject_name'] = user.subject_name
        user_data['time_from'] = user.time_from
        user_data['time_to'] = user.time_to
        output.append(user_data)

    return output

def infoListCourseToArray(users):
    output = []

    for user in users:
        user_data = {}
        user_data['course_id'] = user.course_id
        user_data['course_name'] = user.course_name
        user_data['subject_name'] = user.subect_name
        user_data['time_from'] = user.time_from
        user_data['time_to'] = user.time_to
        user_data['teacher_name'] = user.teacher_name
        output.append(user_data)

    return output

def InfoUserCode(users):
    output = []

    for user in users:
        user_data = {}
        user_data['user_id'] = user.user_id
        user_data['public_id'] = user.public_id
        user_data['user_code'] = user.user_code
        user_data['user_name'] = user.user_name
        user_data['document_id'] = user.document_id
        user_data['gender'] = user.gender
        user_data['age'] = user.age
        user_data['date_birth'] = user.date_birth
        output.append(user_data)

    return output

def infoListTutorToArray(users):
    output = []

    for user in users:
        user_data = {}
        user_data['user_id'] = user.user_id
        user_data['user_code'] = user.user_code
        user_data['tutor_name'] = user.tutor_name
        user_data['document_id'] = user.document_id
        user_data['gender'] = user.gender
        user_data['date_birth'] = user.date_birth
        output.append(user_data)

    return output

def infoTeacherToArraySchool(users):
    output = []

    for user in users:
        user_data = {}
        user_data['school_id'] = user.school_id
        user_data['school_name'] = user.school_name
        user_data['school_phone'] = user.school_phone
        user_data['school_address'] = user.school_address
        user_data['school_code'] = user.school_code
        user_data['director_code'] = user.director_code
        user_data['director_name'] = user.director_name
        user_data['class_name'] = user.class_name
        user_data['subject_id'] = user.subject_id
        user_data['subject_name'] = user.subject_name
        user_data['subject_horario'] = user.subject_horario
        user_data['count_students'] = user.count_students
        output.append(user_data)

    return output

def listStudentToArray(users):
    output = []

    for user in users:
        user_data = {}
        user_data['student_name'] = user.student_name
        user_data['age'] = user.age
        user_data['user_id'] = user.user_id
        user_data['user_code'] = user.user_code
        user_data['subject_name'] = user.subject_name
        user_data['time_from'] = user.time_from
        user_data['time_to'] = user.time_to
        user_data['course_name'] = user.course_name
        user_data['course_id'] = user.course_id
        output.append(user_data)

    return output

class UserImage(Base):
    __tablename__ = 'user_image'

    user_image_id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('user.user_id'), index=True)
    url_image = Column(String(150))
    date = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))

    user = relationship('User')

def toUserImage(items):
    userimage = UserImage()

    if 'user_id' in items:
        userimage.user_id = items['user_id']
    if 'url_image' in items:
        userimage.url_image = items['url_image']
    if 'date' in items:
        userimage.date = items['date']

    return userimage

def infoResponseUserToArray(users):
    output = []

    for userimage in users:
        userimage_data = {}
        userimage_data['user_response'] = userimage.user_response
        output.append(userimage_data)

    return output

def userimageToArray(userimages):
    output = []

    for userimage in userimages:
        userimage_data = {}
        userimage_data['user_id'] = userimage.user_id
        if userimage.url_image != "":
            userimage_data['url_image'] = userimage.url_image
        else:
            userimage_data['url_image'] = ''
        userimage_data['first_name'] = userimage.user.first_name
        userimage_data['last_name'] = userimage.user.last_name
        userimage_data['phone'] = userimage.user.phone
        userimage_data['cell_phone'] = userimage.user.cell_phone
        userimage_data['status'] = userimage.user.status
        userimage_data['date'] = userimage.user.date
        userimage_data['public_id'] = userimage.user.public_id
        userimage_data['name'] = userimage.user.user_type.name
        userimage_data['date_birth'] = userimage.user.date_birth
        userimage_data['document_id'] = userimage.user.document_id
        userimage_data['age'] = userimage.user.age
        userimage_data['email'] = userimage.user.email
        userimage_data['gender'] = userimage.user.gender
        userimage_data['user_code'] = userimage.user.user_code
        output.append(userimage_data)

    return output

def infoDirectorToArray(users):
    output = []

    for userDirector in users:
        userDirector_data = {}
        userDirector_data['user_id'] = userDirector.user_id
        userDirector_data['user_code'] = userDirector.user_code
        userDirector_data['director_name'] = userDirector.director_name
        output.append(userDirector_data)

    return output

def infoUserImageToArray(users):
    output = []

    for userimage in users:
        userimage_data = {}
        userimage_data['user_id'] = userimage.user_id
        userimage_data['url_image'] = userimage.url_image
        userimage_data['first_name'] = userimage.first_name
        userimage_data['last_name'] = userimage.last_name
        userimage_data['phone'] = userimage.phone
        userimage_data['cell_phone'] = userimage.cell_phone
        userimage_data['status'] = userimage.status
        userimage_data['date'] = userimage.date
        userimage_data['public_id'] = userimage.public_id
        userimage_data['date_birth'] = userimage.date_birth
        userimage_data['document_id'] = userimage.document_id
        userimage_data['age'] = userimage.age
        userimage_data['email'] = userimage.email
        userimage_data['gender'] = userimage.gender
        userimage_data['user_code'] = userimage.user_code
        output.append(userimage_data)

    return output


class MemoType(Base):
    __tablename__ = 'memo_type'

    memo_type_id = Column(Integer, primary_key=True)
    name = Column(String(45))
    name_description = Column(String(100))


class QualificationType(Base):
    __tablename__ = 'qualification_type'

    qualification_type_id = Column(Integer, primary_key=True)
    name = Column(String(50))
    description = Column(String(100))
    weight_value = Column(Integer)


class UserType(Base):
    __tablename__ = 'user_type'

    user_type_id = Column(Integer, primary_key=True)
    name = Column(String(45))


class Memo(Base):
    __tablename__ = 'memo'

    memo_id = Column(Integer, primary_key=True)
    id_memo_type = Column(ForeignKey('memo_type.memo_type_id'), index=True)
    description = Column(String(100))
    date = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    title = Column(String(45))
    user_id = Column(ForeignKey('user.user_id'), index=True)
    school_id = Column(ForeignKey('school.school_id'), index=True)
    public_id_change = Column(String(50))
    memo_type = relationship('MemoType')
    user = relationship('User')
    school = relationship('School')

class User_Memo(Base):
    __tablename__ = 'user_memo'

    user_memo_id = Column(Integer, primary_key=True)
    memo_id = Column(ForeignKey('memo.memo_id'), index=True)
    public_id = Column(String(50))
    memo = relationship('Memo')

def toMemo(items):
    memo = Memo()

    if 'id_memo_type' in items:
        memo.id_memo_type = items['id_memo_type']
    if 'description' in items:
        memo.description = items['description']
    if 'date' in items:
        memo.date = items['date']
    if 'public_id_change' in items:
        memo.public_id_change = items['public_id_change']
    if 'title' in items:
        memo.title = items['title']
    if 'user_id' in items:
        memo.user_id = items['user_id']
    if 'school_id' in items:
        memo.school_id = items['school_id']

    return memo

def memoToArray(memos):
    output = []

    for memo in memos:
        memo_data = {}
        memo_data['id_memo_type'] = memo.id_memo_type
        memo_data['description'] = memo.description
        memo_data['title'] = memo.title
        memo_data['memo_id'] = memo.memo_id
        memo_data['user_id'] = memo.user_id
        memo_data['school_id'] = memo.school_id
        memo_data['user_public_id'] = memo.user.public_id
        memo_data['public_id_change'] = memo.public_id_change
        memo_data['memo_date'] = memo.date.strftime('%b %d %Y %I:%M%p')
        output.append(memo_data)

    return output

def usermemoToArray(usermemos):
    output = []

    for memo in usermemos:
        memo_data = {}
        memo_data['user_memo_id'] = memo.user_memo_id
        memo_data['public_id'] = memo.public_id
        output.append(memo_data)

    return output

def taskToArray(tasks):
    output = []

    for task in tasks:
        task_data = {}
        task_data['task_id'] = task.task_id
        task_data['subject_id'] = task.subject_id
        task_data['description'] = task.description
        task_data['user_id'] = task.user_id
        task_data['school_id'] = task.school_id
        task_data['school_name'] = task.school_name
        task_data['status_teacher'] = task.status_teacher
        task_data['status_student'] = task.status_student
        task_data['public_id_teacher'] = task.public_id_teacher
        task_data['subject_name'] = task.subject_name
        task_data['date'] = task.date.strftime('%b %d %Y %I:%M%p')
        output.append(task_data)

    return output

# Modificacion task
def tasksToArrayByStudentId(tasks):
    output = []

    for task in tasks:
        task_data = {}
        task_data['task_id'] = task.task_id
        task_data['subject_id'] = task.subject_id
        task_data['description'] = task.description
        task_data['course_id'] = task.id_course
        task_data['couse_name'] = task.course_name
        task_data['status_teacher'] = task.status_teacher
        task_data['status_student'] = task.status_student
        task_data['subject_name'] = task.subject_name
        task_data['public_id_teacher'] = task.public_id_teacher
        task_data['date'] = task.date.strftime('%b %d %Y %I:%M%p')
        output.append(task_data)

    return output


class RuleTypeUsr(Base):
    __tablename__ = 'rule_type_usr'

    rule_type_usr_id = Column(Integer, primary_key=True)
    id_user_type = Column(ForeignKey('user_type.user_type_id'), index=True)
    menu = Column(String(200))

    user_type = relationship('UserType')


class LoggedUser(Base):
    __tablename__ = 'logged_users'

    logged_users_id = Column(Integer, primary_key=True)
    id_user = Column(ForeignKey('user.user_id'), index=True)
    user_name = Column(String(45))
    password = Column(String(45))
    status = Column(Integer)
    date = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    id_type = Column(ForeignKey('user_type.user_type_id'), index=True)

    user = relationship('User')
    user_type = relationship('UserType')


def toLoggedUser(items):
    logged_users = LoggedUser()

    if 'id_user' in items:
        logged_users.id_user = items['id_user']
    if 'user_name' in items:
        logged_users.user_name = items['user_name']
    if 'password' in items:
        logged_users.password = items['password']
    if 'id_type' in items:
        logged_users.id_type = items['id_type']

    return logged_users

def loggeduserToArray(logged_users):
    output = []

    for loggedusers in logged_users:
        loggeduser_data = {}

        loggeduser_data['id_user'] = loggedusers.id_user
        loggeduser_data['user_name'] = loggedusers.user_name
        loggeduser_data['password'] = loggedusers.password
        loggeduser_data['first_name'] = loggedusers.user.first_name
        loggeduser_data['last_name'] = loggedusers.user.last_name
        loggeduser_data['public_id'] = loggedusers.user.public_id
        loggeduser_data['document_id'] = loggedusers.user.document_id
        loggeduser_data['type'] = loggedusers.user_type.name

        output.append(loggeduser_data)

    return output

class MemoDistribution(Base):
    __tablename__ = 'memo_distribution'

    memo_distribution_id = Column(Integer, primary_key=True)
    id_memo = Column(ForeignKey('memo.memo_id'), index=True)
    id_user_pather = Column(ForeignKey('user.user_id'), index=True)

    memo = relationship('Memo')
    user = relationship('User')




def toSchedule(items):
    schedule = Schedule()
    if 'task' in items:
        schedule.task = items['task']
    if 'datetime_todo' in items:
        schedule.datetime_todo = items['datetime_todo']

    schedule.done = 0

    return schedule

class School(Base):
    __tablename__ = 'school'

    school_id = Column(Integer, primary_key=True)
    name = Column(String(100))
    id_province = Column(ForeignKey('province.province_id'), index=True)
    id_neighborhood = Column(ForeignKey('neighborhood.neighborhood_id'), index=True)
    street = Column(String(100))
    block = Column(String(45))
    apartment = Column(String(45))
    logo = Column(String(200))
    location = Column(String(60))
    telephone = Column(String(60))
    date = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    document_id = Column(String(45))
    school_code = Column(String(45))
    public_id_school = Column(String(100))

    neighborhood = relationship('Neighborhood')
    province = relationship('Province')

def toSchool(items):
    school = School()

    if 'name' in items:
        school.name = items['name']
    if 'id_province' in items:
        school.id_province = items['id_province']
    if 'id_neighborhood' in items:
        school.id_neighborhood = items['id_neighborhood']
    if 'street' in items:
        school.street = items['street']
    if 'block' in items:
        school.block = items['block']
    if 'apartment' in items:
        school.apartment = items['apartment']
    if 'logo' in items:
        school.logo = items['logo']
    if 'location' in items:
        school.location = items['location']
    if 'telephone' in items:
        school.telephone = items['telephone']
    if 'document_id' in items:
        school.document_id = items['document_id']
   # if 'school_code' in items:
   #    school.school_code = items['school_code']

    code = str(uuid.uuid4())
    generate_code = code[:8]
    school.public_id_school =  generate_code

    return school

def schoolToArray(zones):
    output = []

    for school in zones:
        school_data = {}
        school_data['school_id'] = school.school_id
        school_data['name'] = school.name
        school_data['id_neighborhood'] = school.id_neighborhood
        school_data['id_province'] = school.id_province
        school_data['street'] = school.street
        school_data['block'] = school.block
        school_data['apartment'] = school.apartment
        school_data['logo'] = school.logo
        school_data['location'] = school.location
        school_data['document_id'] = school.document_id
        school_data['school_code'] = school.school_code

        output.append(school_data)

    return output

def schoolUserToArray(zones):
    output = []

    for school in zones:
        school_data = {}
        school_data['school_id'] = school.school_id
        school_data['school_name'] = school.school_name
        school_data['id_neighborhood'] = school.id_neighborhood
        school_data['id_province'] = school.id_province
        school_data['street'] = school.street
        school_data['block'] = school.block
        school_data['apartment'] = school.apartment
        school_data['logo'] = school.logo
        school_data['location'] = school.location
        school_data['document_id'] = school.document_id
        school_data['school_code'] = school.school_code
        school_data['telephone'] = school.telephone
        school_data['latitude'] = str(school.latitude)
        school_data['longitude'] = str(school.longitude)
        school_data['public_id_school'] = school.public_id_school

        output.append(school_data)

    return output

class Grade(Base):
    __tablename__ = 'grade'

    grade_id = Column(Integer, primary_key=True)
    name = Column(String(45))
    description = Column(String(100))
    id_school = Column(ForeignKey('school.school_id'), index=True)

    school = relationship('School')


def toGrade(items):
    grade = Grade()

    if 'name' in items:
        grade.name = items['name']
    if 'description' in items:
        grade.description = items['description']
    if 'id_school' in items:
        grade.id_school = items['id_school']
    if 'id_school' in items:
        grade.id_school = items['id_school']

    return grade

def gradeToArray(grades):
    output = []

    for grade in grades:
        grade_data = {}
        grade_data['name'] = grade.name
        grade_data['grade_id'] = grade.grade_id
        grade_data['id_school'] = grade.id_school
        output.append(grade_data)

    return output

def gradeDirectorToArray(grades):
    output = []

    for grade in grades:
        grade_data = {}
        grade_data['school_name'] = grade.school_name
        grade_data['school_code'] = grade.school_code
        grade_data['grade_id'] = grade.grade_id
        grade_data['grade_name'] = grade.grade_name #Nombre de escuela
        output.append(grade_data)

    return output

def studentSubjectToArray(students):
    output = []

    for student in students:
        student_data = {}
        student_data['student_name'] = student.student_name
        student_data['user_code'] = student.user_code
        student_data['public_id_student'] = student.public_id_student
        student_data['user_id'] = student.user_id
        student_data['parent_id'] = student.parent_id
        student_data['public_id_tutor'] = student.public_id_tutor
        student_data['average_qualification'] = str(student.average_qualification)
        student_data['student_image'] = student.student_image
        output.append(student_data)

    return output

def teacherStudentToArray(teachers):
    output = []

    for teacher in teachers:
        teacher_data = {}
        teacher_data['teacher_name'] = teacher.teacher_name
        teacher_data['subject_name'] = teacher.subject_name
        output.append(teacher_data)

    return output

def tutorStudentToArray(tutor):
    output = []

    for tut in tutor:
        tut_data = {}
        tut_data['public_id_tutor'] = tut.public_id_tutor
        output.append(tut_data)

    return output


def childStudentToArray(tutor):
    output = []

    for tut in tutor:
        tut_data = {}
        tut_data['school_name'] = tut.school_name
        tut_data['student_name'] = tut.student_name
        tut_data['user_code'] = tut.user_code
        tut_data['public_id_child'] = tut.public_id_child
        tut_data['age'] = tut.age
        tut_data['course_name'] = tut.course_name
        tut_data['num_course_students'] = tut.num_course_students
        tut_data['user_id'] = tut.user_id
        tut_data['course_id'] = tut.course_id
        output.append(tut_data)

    return output

def studentbyCourseToArray(students):
    output = []

    for student in students:
        student_data = {}
        student_data['student_name'] = student.student_name
        student_data['student_id'] = student.student_id
        student_data['user_code'] = student.user_code
        output.append(student_data)

    return output

def subjectStudentQualificationToArray(students):
    output = []

    for student in students:
        student_data = {}
        student_data['student_name'] = student.student_name
        student_data['user_code'] = student.user_code
        student_data['subject_name'] = student.subject_name
        student_data['average_value'] = str(student.average_value)
        student_data['id_subject'] = student.id_subject

        output.append(student_data)

    return output


def studentQualificationToArray(students):
    output = []

    for student in students:
        student_data = {}
        student_data['student_name'] = student.student_name
        student_data['user_code'] = student.user_code
        student_data['subject_name'] = student.subject_name
        student_data['average_value'] = str(student.average_value)
        student_data['test_type'] = student.test_type
        student_data['test_date'] = student.test_date
        student_data['value'] = str(student.value)

        output.append(student_data)

    return output

def qualificationToArray(qualifications):
    output = []

    for qualification in qualifications:
        qualification_data = {}
        qualification_data['qualification_id'] = qualification.qualification_id
        qualification_data['id_qualification_type'] = qualification.id_qualification_type
        qualification_data['id_course'] = qualification.id_course
        qualification_data['id_subject'] = qualification.id_subject
        qualification_data['value'] = qualification.value
        qualification_data['test_type'] = qualification.test_type
        qualification_data['test_date'] = qualification.test_date

        output.append(qualification_data)

    return output

def teacherDirectorToArray(teachers):
    output = []

    for teach in teachers:
        teach_data = {}
        teach_data['teacher_user_id'] = teach.teacher_user_id
        teach_data['teacher_name'] = teach.teacher_name
        teach_data['school_code'] = teach.school_code
        teach_data['school_name'] = teach.school_name
        output.append(teach_data)

    return output


#Parents School
class UserSchool(Base):
    __tablename__ = 'user_school'

    user_school_id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('user.user_id'), index=True)
    school_id = Column(ForeignKey('school.school_id'), index=True)
    date = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    id_type = Column(ForeignKey('user_type.user_type_id'), index=True)

    school = relationship('School')
    user = relationship('User')
    user_type = relationship('UserType')

def toUserSchool(items):
    user_school = UserSchool()

    if 'user_id' in items:
        user_school.user_id = items['user_id']
    if 'school_id' in items:
        user_school.school_id = items['school_id']
    if 'id_type' in items:
        user_school.id_type = items['id_type']

    return user_school

def userSchoolToArray(user_schools):
    output = []

    for user_school in user_schools:
        user_school_data = {}
        user_school_data['user_id'] = user_school.user_id
        user_school_data['school_id'] = user_school.school_id
        user_school_data['school_name'] = user_school.school.name #Nombre de escuela
        user_school_data['school_rnc'] = user_school.school.document_id #RNC de escuela
        user_school_data['school_street'] = user_school.school.street #Direccion de escuela
        user_school_data['school_phone'] = user_school.school.apartment #Apartment de escuela
        user_school_data['director_name'] = user_school.user.first_name + ' ' +  user_school.user.last_name#Nombre del director
        user_school_data['director_code'] = user_school.user.user_code#Codigo del director
        output.append(user_school_data)

    return output

    #User Parents School
class UserParent(Base):
    __tablename__ = 'user_parent'

    user_parent_id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    parent_id = Column(Integer)
    date = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))

    #user = relationship('User')
    #parent = relationship('User')

def toUserParent(items):
    user_parent = UserParent()

    if 'user_id' in items:
        user_parent.user_id = items['user_id']
    if 'parent_id' in items:
        user_parent.parent_id = items['parent_id']

    return user_parent

def userParentToArray(user_parents):
    output = []

    for user_parent in user_parents:
        user_parent_data = {}
        user_parent_data['user_id'] = user_parent.user_id
        user_parent_data['parent_id'] = user_parent.parent_id
        #user_parent_data['tutor_name'] = user_parent.user.first_name + ' ' +  user_parent.user.last_name#Nombre del usuario
        output.append(user_parent_data)

    return output

class Course(Base):
    __tablename__ = 'course'

    course_id = Column(Integer, primary_key=True)
    name = Column(String(45))
    description = Column(String(100))
    id_grade = Column(ForeignKey('grade.grade_id'), index=True)
    status = Column(Integer)

    grade = relationship('Grade')

def toCourse(items):
    course = Course()

    if 'id_grade' in items:
        course.id_grade = items['id_grade']
    if 'name' in items:
        course.name = items['name']

    return course

def courseToArrayModel(courses):
    output = []

    for course in courses:
        course_data = {}
        course_data['course_id'] = course.course_id     #Id Aula
        course_data['name'] = course.name #Nombre Aula
        course_data['id_grade'] = course.id_grade       #Id Grado
        #course_data['grade_name'] = course.grade.name   #Nombre del Grado
        output.append(course_data)

    return output


def courseToArray(courses):
    output = []

    for course in courses:
        course_data = {}
        course_data['course_id'] = course.course_id     #Id Aula
        course_data['course_name'] = course.course_name #Nombre Aula
        course_data['id_grade'] = course.id_grade       #Id Grado
        course_data['grade_name'] = course.grade_name   #Nombre del Grado
        course_data['school_code'] = course.school_code #Codigo de la escuella
        course_data['school_name'] = course.school_name #Nombre de escuela
        output.append(course_data)

    return output

class Subject(Base):
    __tablename__ = 'subject'

    subject_id = Column(Integer, primary_key=True)
    id_grade = Column(ForeignKey('grade.grade_id'), index=True)
    name = Column(String(45))
    time_from = Column(String(20))
    time_to = Column(String(20))
    status = Column(Integer)

    grade = relationship('Grade')

def toSubject(items):
    subject = Subject()

    if 'id_grade' in items:
        subject.id_grade = items['id_grade']
    if 'name' in items:
        subject.name = items['name']
    if 'time_from' in items:
        subject.time_from = items['time_from']
    if 'time_to' in items:
        subject.time_to = items['time_to']

    return subject

def subjectToArray(subjects):
    output = []

    for subject in subjects:
        subject_data = {}
        subject_data['subject_id'] = subject.subject_id
        subject_data['name'] = subject.name
        subject_data['id_grade'] = subject.id_grade
        subject_data['grade_name'] = subject.grade.name #Nombre de grade
        subject_data['time_from'] = subject.time_from
        subject_data['time_to'] = subject.time_to
        output.append(subject_data)

    return output

class Qualification(Base):
    __tablename__ = 'qualification'

    qualification_id = Column(Integer, primary_key=True)
    id_qualification_type = Column(ForeignKey('qualification_type.qualification_type_id'), index=True)
    id_course = Column(ForeignKey('course.course_id'), index=True)
    id_usr_student = Column(ForeignKey('user.user_id'), index=True)
    id_subject = Column(ForeignKey('subject.subject_id'), index=True)
    test_date = Column(DateTime)
    test_type = Column(String(60))
    value = Column(Integer)
    course = relationship('Course')
    qualification_type = relationship('QualificationType')
    subject = relationship('Subject')
    user = relationship('User')

def toQualification(items):
    qualification = Qualification()

    if 'id_qualification_type' in items:
        qualification.id_qualification_type = items['id_qualification_type']
    if 'id_course' in items:
        qualification.id_course = items['id_course']
    if 'id_usr_student' in items:
        qualification.id_usr_student = items['id_usr_student']
    if 'id_subject' in items:
        qualification.id_subject = items['id_subject']
    if 'value' in items:
        qualification.value = items['value']
    if 'test_date' in items:
        qualification.test_date = items['test_date']
    if 'test_type' in items:
        qualification.test_type = items['test_type']

    return qualification

class AssitanceType(Base):
    __tablename__ = 'assitance_type'

    assitance_type_id = Column(Integer, primary_key=True)
    name = Column(String(50))

class Assitance(Base):
    __tablename__ = 'assitance'

    assitance_id = Column(Integer, primary_key=True)
    id_assitance_type = Column(ForeignKey('assitance_type.assitance_type_id'), index=True)
    id_course = Column(ForeignKey('course.course_id'), index=True)
    id_usr_student = Column(ForeignKey('user.user_id'), index=True)
    id_subject = Column(ForeignKey('subject.subject_id'), index=True)
    value = Column(Integer)
    comments = Column(String(100))
    date = Column(String(100))

    course = relationship('Course')
    assitance_type = relationship('AssitanceType')
    subject = relationship('Subject')
    user = relationship('User')

def toAssitance(items):
    assitance = Assitance()

    if 'id_assitance_type' in items:
        assitance.id_assitance_type = items['id_assitance_type']
    if 'id_course' in items:
        assitance.id_course = items['id_course']
    if 'id_usr_student' in items:
        assitance.id_usr_student = items['id_usr_student']
    if 'id_subject' in items:
        assitance.id_subject = items['id_subject']
    if 'value' in items:
        assitance.value = items['value']
    if 'date' in items:
        assitance.date = items['date']
    if 'comments' in items:
        assitance.comments = items['comments']

    return assitance

def assistantToArray(assistance_list):
    output = []

    for assistance in assistance_list:
        assistance_data = {}
        assistance_data['assitance_id'] = assistance.assitance_id
        assistance_data['id_assitance_type'] = assistance.id_assitance_type
        assistance_data['id_course'] = assistance.id_course
        assistance_data['id_usr_student'] = assistance.id_usr_student
        assistance_data['id_subject'] = assistance.id_subject
        assistance_data['date'] = assistance.date
        assistance_data['value'] = assistance.value
        assistance_data['comments'] = assistance.comments
        output.append(assistance_data)

    return output

def assistantStudentToArray(teacher_subjects):
    output = []

    for user_parent in teacher_subjects:
        user_parent_data = {}
        user_parent_data['assistance'] = user_parent.assistance
        user_parent_data['count_assistance'] = user_parent.count_assistance
        output.append(user_parent_data)

    return output

def assistanceToArray(assistances):
    output = []

    for assistance in assistances:
        assistance_data = {}
        assistance_data['presences'] = assistance.presences
        assistance_data['absences'] = assistance.absences
        assistance_data['excuses'] = assistance.excuses
        output.append(assistance_data)

    return output

class StudentCourse(Base):
    __tablename__ = 'student_course'

    student_course_id = Column(Integer, primary_key=True)
    id_usr_student = Column(ForeignKey('user.user_id'), index=True)
    id_course = Column(ForeignKey('course.course_id'), index=True)
    date = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))

    course = relationship('Course')
    user = relationship('User')

class TeacherSubject(Base):
    __tablename__ = 'teacher_subject'

    teacher_subject_id = Column(Integer, primary_key=True)
    id_usr_teacher = Column(ForeignKey('user.user_id'), index=True)
    id_subject = Column(ForeignKey('subject.subject_id'), index=True)
    id_school = Column(ForeignKey('school.school_id'), index=True)
    date = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    status = Column(Integer)

    subject = relationship('Subject')
    user = relationship('User')
    school = relationship('School')


def toTeacherSubject(items):
    teacher_subject = UserParent()

    if 'user_id' in items:
        teacher_subject.user_id = items['user_id']
    if 'parent_id' in items:
        teacher_subject.parent_id = items['parent_id']

    return teacher_subject

def teacherSubjectToArray(teacher_subjects):
    output = []

    for user_parent in user_parents:
        user_parent_data = {}
        user_parent_data['user_id'] = user_parent.user_id
        user_parent_data['parent_id'] = user_parent.parent_id
        #user_parent_data['tutor_name'] = user_parent.user.first_name + ' ' +  user_parent.user.last_name#Nombre del usuario
        output.append(user_parent_data)

    return output


class TeacherCourse(Base):
    __tablename__ = 'teacher_course'

    teacher_course_id = Column(Integer, primary_key=True)
    id_usr_teacher = Column(ForeignKey('user.user_id'), index=True)
    id_course = Column(ForeignKey('course.course_id'), index=True)
    date = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))

    course = relationship('Course')
    user = relationship('User')


class Schedule(Base):
    __tablename__ = 'schedule'

    id = Column(Integer, primary_key=True)
    task = Column(String(100))
    datetime_todo = Column(DateTime,)
    date = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    done = Column(Integer, default=1)

class Task(Base):
    __tablename__ = 'task'

    task_id = Column(Integer, primary_key=True)
    subject_id = Column(ForeignKey('subject.subject_id'), index=True)
    description = Column(String(500))
    date = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    user_id = Column(ForeignKey('user.user_id'), index=True)
    school_id = Column(ForeignKey('school.school_id'), index=True)
    school_name = Column(String(100))
    public_id_teacher = Column(String(50))
    subject_name = Column(String(100))
    status_teacher = Column(Integer)
    status_student = Column(Integer)


    subject = relationship('Subject')
    user = relationship('User')
    school = relationship('School')

class Activity(Base):
    __tablename__ = 'activity'

    activity_id = Column(Integer, primary_key=True)
    description = Column(String(200))
    date = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    title = Column(String(45))
    user_id = Column(ForeignKey('user.user_id'), index=True)
    student_name = Column(String(50))

    user = relationship('User')
