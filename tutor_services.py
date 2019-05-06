from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from tutor_model import *
import pickle
import tutor_param

import json
from collections import namedtuple

db = None

def getAllUser():
    try:
        users = db.session.query(User).all()
        output = userToArray(users)

        return jsonify(Response(ResponseType.SUCCESS,200,'Usuario retornado',output).serialize())
    except Exception as ex:
        return jsonify(Response(ResponseType.ERROR,404,str(ex),"").serialize())

def getUserById(public_id):
    try:
        sql_string = "CALL find_InfoUserImage ('{params}')".format(params=public_id)
        user = db.session.execute(sql_string)
        output = infoUserImageToArray(user)

        return jsonify(Response(ResponseType.SUCCESS,200,'Usuario retornado',output).serialize())
    except Exception as ex:
        return jsonify(Response(ResponseType.ERROR,404,str(ex),None).serialize())


def getDirectorBySchool(school_id):
    try:
        sql_string = "CALL find_InfoDirectorbySchool ('{params}')".format(params=school_id)
        user = db.session.execute(sql_string)
        output = infoDirectorToArray(user)

        return jsonify(Response(ResponseType.SUCCESS,200,'Datos del director de la escuela enviada',output).serialize())
    except Exception as ex:
        return jsonify(Response(ResponseType.ERROR,404,str(ex),None).serialize())

def getUserByUserCode(user_code, id_type):
    try:
        sql_string = "CALL find_InfoUserCode ('{params}')".format(params=user_code)
        user = db.session.execute(sql_string)
        output = InfoUserCode(user)

        return jsonify(Response(ResponseType.SUCCESS,200,'Usuario retornado',output).serialize())
    except Exception as ex:
        return jsonify(Response(ResponseType.ERROR,404,str(ex),None).serialize())


def getLoggedUser(logged_users):
    try:
        loggusr = toLoggedUser(logged_users)
        logged_users = db.session.query(LoggedUser).filter((LoggedUser.user_name == loggusr.user_name) & (LoggedUser.password == loggusr.password) & (LoggedUser.id_type == loggusr.id_type) & (LoggedUser.status == 1))
        output = loggeduserToArray(logged_users)
        if (output == []):
            return jsonify(Response(ResponseType.ERROR,300,'Usuario no encontrado',None).serialize())
        else:
            return jsonify(Response(ResponseType.SUCCESS,200,'Usuario logueado',output).serialize())
    except Exception as ex:
        return jsonify(Response(ResponseType.ERROR,404,str(ex),None).serialize())

def getAllLoggedUser():
    try:
        loggusr = db.session.query(LoggedUser).all()
        output = loggeduserToArray(loggusr)

        return jsonify(Response(ResponseType.SUCCESS,200,'Usuario retornado',output).serialize())
    except Exception as ex:
        return jsonify(Response(ResponseType.ERROR,404,str(ex),"").serialize())

#METODO CREADO PARA CREAR USUARIOS, DE CUALQUIER TIPO
def createUser(user):
    try :
        usr = toUser(user)

        schoo = db.session.query(School).filter(School.public_id_school == user['public_id_school'])
        output2 = schoolToArray(schoo)

        if (user['id_type'] != 5):
            users = db.session.query(User).filter(User.email == user['email'])
            output = userToArray(users)

            if (output != []):
                return jsonify(Response(ResponseType.ERROR,300,'Usuario ya registrado con este correo',None).serialize())
            else:
                if (user['password'] != user['password2']):
                    return jsonify(Response(ResponseType.ERROR,300,'Las contrasenas no coinciden',None).serialize())
                else:
                    if (output2 != []):
                        db.session.add(usr)
                        db.session.commit()

                        schoolid =  output2[0]['school_id']
                        generateCodeUser(user)

                        if (user['id_type'] != 5):
                            loginUser(user)

                        if (user['id_type'] == 3):
                            schoolid =  output2[0]['school_id']
                            if (len(user['subject_array_id']) !=0 ):
                                createTeacherSubject(user,schoolid)

                        if (user['id_type'] != 1):
                           createUserSchool(user, schoolid)
                    else:
                        return jsonify(Response(ResponseType.ERROR,300,'El Centro Educativo digitado no existe en el sistema. Favor contactar al administrador.',None).serialize())
                return jsonify(Response(ResponseType.SUCCESS,201,'Usuario Insertado',None).serialize())
        else:
            db.session.add(usr)
            db.session.commit()

            generateCodeUser(user)

            schoolid =  output2[0]['school_id']

            createUserParent(user, schoolid)
            createStudentCourse(user)
        return jsonify(Response(ResponseType.SUCCESS,201,'Usuario Insertado',None).serialize())


    except Exception as ex:
        return jsonify(Response(ResponseType.ERROR,424,'Error insertando usuario: '+str(ex), user).serialize())

#METODO CREADO PARA CREAR LOS LOGIN DE LOS USUARIOS, EXCEPTUANDO LOS ESTUDIANTES
def loginUser(user):
    try :
        luser = LoggedUser()
        users = db.session.query(User).filter(User.email == user['email'])
        output = userToArray(users)

        luser.id_user = output[0]['user_id']
        luser.user_name = user['user_name']
        luser.id_type = user['id_type']
        luser.password = user['password']
        luser.status = 1

        db.session.add(luser)
        db.session.commit()

    except Exception as ex:
        print ('Error')

#METODO CREADO PARA GENERAR EL CODE DEL USUARIO CUANDO SE REGISTRA
def generateCodeUser(user):
    try :
        users = db.session.query(User).filter(User.email == user['email'])
        output = userToArray(users)
        userGenerateCode = str(output[0]['user_id'])

        while len(userGenerateCode) < 5:
            userGenerateCode = '0' + str(userGenerateCode)

        if (user['id_type'] == 1):
            userGenerateCode = 'ADM-' + userGenerateCode
        if (user['id_type'] == 2):
            userGenerateCode = 'D-' + userGenerateCode
        if (user['id_type'] == 3):
            userGenerateCode = 'P-' + userGenerateCode
        if (user['id_type'] == 4):
            userGenerateCode = 'T-' + userGenerateCode
        if (user['id_type'] == 5):
            userGenerateCode = 'E-' + userGenerateCode

        db.session.query(User).filter(User.email == user['email']).update({User.user_code: userGenerateCode })
        db.session.commit()


    except Exception as ex:
        print (ex)

#METODO CREADO PARA REALIZAR ACTUALIZACION DE LOS DATOS DE UN USUARIO YA REGISTRADO
def updateUser(user):
    try:
        db.session.query(User).filter(User.public_id == user['public_id']).update({User.first_name: user['first_name'],User.last_name: user['last_name'],User.phone: user['phone'],User.cell_phone: user['cell_phone'],User.status: user['status'],User.gender: user['gender'],User.email: user['email'] })
        db.session.commit()

        return jsonify(Response(ResponseType.SUCCESS,200,'Usuario retornado',user).serialize())
    except Exception as ex:
        return jsonify(Response(ResponseType.ERROR,404,str(ex),None).serialize())

#METODO CREADO PARA OBTENER EL LISTADO DE TODAS LAS ESCUELAS
def getAllSchool():
    try:
        school = db.session.query(School).all()
        output = schoolToArray(school)
        return jsonify(Response(ResponseType.SUCCESS,200,'Escuela retornada',output).serialize())
    except Exception as ex:
        return jsonify(Response(ResponseType.ERROR,404,str(ex),"").serialize())

#METODO PARA OBTENER LOS DATOS DE LA ESCUELA, POR EL PUBLIC ID DEL USUARIO DE CUALQUIER TIPO
def getSchoolByUserId(public_id):
    try:
        sql_string = "CALL find_SchoolInfobyUser ('{params1}')".format(params1=public_id)
        user = db.session.execute(sql_string)
        outputUser2 = schoolUserToArray(user)
        result = jsonify(Response(ResponseType.SUCCESS,200,'Escuela asociada al id del usuario',outputUser2).serialize())
        return result

    except Exception as ex:
        return jsonify(Response(ResponseType.ERROR,404,str(ex),None).serialize())


#METODO CREADO PARA CREAR EL CENTRO EDUCATIVO POR PRIMERA VEZ
def createSchool(school):
    try :
        sch = toSchool(school)

        sh = db.session.query(School).filter(School.document_id == school['document_id'])
        output = schoolToArray(sh)
        if (output != []):
            return jsonify(Response(ResponseType.ERROR,300,'Escuela con el RNC ya ha sido registrada',None).serialize())
        else:
            db.session.add(sch)
            db.session.commit()

            #generateCodeSchool(school)
            #loadUserDirector(school)

            result = jsonify(Response(ResponseType.SUCCESS,201,'Escuela Insertada',sch).serialize())
            return result
    except Exception as ex:
        result = jsonify(Response(ResponseType.ERROR,424,'Error insertando escuela: '+str(ex), sch).serialize())

#METODO CREADO PARA GENERAR EL CODE DEL CENTRO CUANDO SE REGISTRA
def generateCodeSchool(school):
    try :
        schoo = db.session.query(School).filter(School.document_id == school['document_id'])
        output = schoolToArray(schoo)

        schoolGenerateCode = str(output[0]['school_id'])

        while len(schoolGenerateCode) < 4:
            schoolGenerateCode = '0' + str(schoolGenerateCode)

        schoolGenerateCode = 'C-' + schoolGenerateCode

        db.session.query(School).filter(School.document_id == school['document_id']).update({School.school_code: schoolGenerateCode })
        db.session.commit()


    except Exception as ex:
        print (ex)

#METODO CREADO PARA CREAR LA ASOCIACION DE LOS PADRES CON LOS ESTUDIANTES
def createUserParent(user, schoolid):
    student = db.session.query(User).filter(User.document_id == user['document_id'])
    output = userToArray(student)

    uParen = UserParent()
    uParen.user_id = output[0]['user_id']
    uParen.parent_id = user['tutor_id']

    db.session.add(uParen)
    db.session.commit()

#METODO CREADO PARA CREAR LA ASOCIACION DE LOS DOCENTES CON LAS MATERIAS
def createTeacherSubject(user, schoolid):
    teacher = db.session.query(User).filter(User.document_id == user['document_id'])
    output = userToArray(teacher)

    subject_id = user['subject_array_id'].split(",")
    print(subject_id)

    for id_sub in subject_id:
        print(id_sub)
        uSubject = TeacherSubject()
        uSubject.id_usr_teacher = output[0]['user_id']
        uSubject.id_subject = id_sub
        uSubject.id_school = schoolid
        db.session.add(uSubject)
        db.session.commit()

#METODO CREADO PARA CREAR LA ASOCIACION DE LOS ESTUDIANTES CON EL CURSO
def createStudentCourse(user):
    student = db.session.query(User).filter(User.document_id == user['document_id'])
    output = userToArray(student)

    sCourse = StudentCourse()
    sCourse.id_course = user['course_id']
    sCourse.id_usr_student = output[0]['user_id']

    db.session.add(sCourse)
    db.session.commit()

#METODO CREADO PARA ASOCIAR LOS USUARIOS CREADOS A UN CENTRO EDUCATIVO (DIRECTOR, ASISTENTE, DOCENTE, TUTOR Y ESTUDIANTE)
def createUserSchool(user, schoolid):
    try :
        uSch = UserSchool()
        users = db.session.query(User).filter(User.email == user['email'])
        output = userToArray(users)

        uSch.user_id = output[0]['user_id']
        uSch.id_type = user['id_type']
        uSch.school_id = schoolid

        db.session.add(uSch)
        db.session.commit()

    except Exception as ex:
        print ('Error al crear asociacion de school con user')

def loadUserDirector(school):

    try :

        uSch = UserSchool()
        users = db.session.query(User).filter(User.public_id == school['public_id'])
        output = userToArray(users)

        schoo = db.session.query(School).filter(School.document_id == school['document_id'])
        output2 = schoolToArray(schoo)

        uSch.user_id = output[0]['user_id']
        uSch.id_type = 2
        uSch.school_id = output2[0]['school_id']

        db.session.add(uSch)
        db.session.commit()

    except Exception as ex:
        print ('Error')

def getSchoolByDirectorId(public_id):
    try:
        userschool = db.session.query(UserSchool).join(UserSchool.user).filter(User.public_id == public_id)
        output = userSchoolToArray(userschool)

        return jsonify(Response(ResponseType.SUCCESS,200,'Usuarios con escuela retornado',output).serialize())
    except Exception as ex:
        return jsonify(Response(ResponseType.ERROR,404,str(ex),None).serialize())

def getAllGrade():
    try:
        grade = db.session.query(Grade).all()
        output = gradeToArray(grade)
        return jsonify(Response(ResponseType.SUCCESS,200,'Aulas retornadas',output).serialize())
    except Exception as ex:
        return jsonify(Response(ResponseType.ERROR,404,str(ex),"").serialize())

def createGrade(grade):
    try :
        grad = toGrade(grade)
        db.session.add(grad)
        db.session.commit()

        result = jsonify(Response(ResponseType.SUCCESS,201,'Aula Insertada',None).serialize())
        return result
    except Exception as ex:
        result = jsonify(Response(ResponseType.ERROR,424,'Error insertando Aula: '+str(ex), None).serialize())

def createAssitance(assitance):
    try :
        assist = toAssitance(assitance)
        db.session.add(assist)
        db.session.commit()

        result = jsonify(Response(ResponseType.SUCCESS,201,'Asistencia agregada a estudiante',None).serialize())
        return result
    except Exception as ex:
        result = jsonify(Response(ResponseType.ERROR,424,'Error insertando asistencia: '+str(ex), None).serialize())

def createQualification(qualification):
    try :
        qual = toQualification(qualification)
        db.session.add(qual)
        db.session.commit()

        result = jsonify(Response(ResponseType.SUCCESS,201,'Calificacion agregada a estudiante',None).serialize())
        return result
    except Exception as ex:
        result = jsonify(Response(ResponseType.ERROR,424,'Error insertando calificacion: '+str(ex), None).serialize())


def getGradeByDirectorId(public_id, school_id):
    try:
        sql_string = "CALL find_GradeInfobyDirector ('{params1}','{params2}')".format(params1=public_id,params2=school_id)
        user = db.session.execute(sql_string)
        outputUser2 = gradeDirectorToArray(user)
        result = jsonify(Response(ResponseType.SUCCESS,200,'Grados asociados a la escuela del director',outputUser2).serialize())
        return result

    except Exception as ex:
        return jsonify(Response(ResponseType.ERROR,404,str(ex),None).serialize())

def getTeacherByDirectorId(public_id, school_id):
    try:
        sql_string = "CALL find_TeacherInfobyDirector ('{params1}','{params2}')".format(params1=public_id,params2=school_id)
        user = db.session.execute(sql_string)
        outputTeacher = teacherDirectorToArray(user)
        result = jsonify(Response(ResponseType.SUCCESS,200,'Docentes asociados a la escuela del director',outputTeacher).serialize())
        return result
    except Exception as ex:
        return jsonify(Response(ResponseType.ERROR,404,str(ex),None).serialize())

def getStudentByTeacherId(public_id,school_id,subject_id):
    try:
        sql_string = "CALL find_StudentbyTeacher ('{params1}','{params2}','{params3}')".format(params1=public_id,params2=school_id,params3=subject_id)
        user = db.session.execute(sql_string)
        outputUser2 = listStudentToArray(user)
        result = jsonify(Response(ResponseType.SUCCESS,200,'Lista de estudiantes asociados al docente',outputUser2).serialize())
        return result
    except Exception as ex:
        return jsonify(Response(ResponseType.ERROR,404,str(ex),None).serialize())

def getStudentBySubjectId(course_id,school_id,subject_id):
    try:
        sql_string = "CALL find_StudentbySubject ('{params1}','{params2}','{params3}')".format(params1=course_id,params2=school_id,params3=subject_id)
        user = db.session.execute(sql_string)
        outputUser2 = studentSubjectToArray(user)
        result = jsonify(Response(ResponseType.SUCCESS,200,'Lista de estudiantes por materia',outputUser2).serialize())
        return result
    except Exception as ex:
        return jsonify(Response(ResponseType.ERROR,404,str(ex),None).serialize())

def getStudentByCourseId(course_id,school_id):
    try:
        sql_string = "CALL find_StudentbyCourse ('{params1}','{params2}')".format(params1=course_id,params2=school_id)
        user = db.session.execute(sql_string)
        outputUser2 = studentbyCourseToArray(user)
        result = jsonify(Response(ResponseType.SUCCESS,200,'Lista de estudiantes por curso',outputUser2).serialize())
        return result
    except Exception as ex:
        return jsonify(Response(ResponseType.ERROR,404,str(ex),None).serialize())

def getTutorByStudentId(student_id):
    try:
        sql_string = "CALL find_TutorbyStudent ('{params1}')".format(params1=student_id)
        user = db.session.execute(sql_string)
        outputUser2 = tutorStudentToArray(user)
        result = jsonify(Response(ResponseType.SUCCESS,200,'Public id del Tutor',outputUser2).serialize())
        return result
    except Exception as ex:
        return jsonify(Response(ResponseType.ERROR,404,str(ex),None).serialize())

def getTeacherByStudentId(student_id):
    try:
        sql_string = "CALL find_TeacherbyStudent ('{params1}')".format(params1=student_id)
        user = db.session.execute(sql_string)
        outputUser2 = teacherStudentToArray(user)
        result = jsonify(Response(ResponseType.SUCCESS,200,'Lista de estudiantes por curso',outputUser2).serialize())
        return result
    except Exception as ex:
        return jsonify(Response(ResponseType.ERROR,404,str(ex),None).serialize())

def getQualificationByStudentId(course_id, student_id,subject_id):
    try:
        sql_string = "CALL find_QualificationByStudent ('{params1}','{params2}','{params3}')".format(params1=course_id,params2=student_id,params3=subject_id)
        user = db.session.execute(sql_string)
        outputUser2 = studentQualificationToArray(user)
        result = jsonify(Response(ResponseType.SUCCESS,200,'Calificacion de estudiantes por materia',outputUser2).serialize())
        return result
    except Exception as ex:
        return jsonify(Response(ResponseType.ERROR,404,str(ex),None).serialize())

def getQualificationBySubjectId(course_id,subject_id):
    try:
        sql_string = "CALL find_QualificationBySubject ('{params1}','{params2}')".format(params1=course_id,params2=subject_id)
        user = db.session.execute(sql_string)
        outputUser2 = studentQualificationToArray(user)
        result = jsonify(Response(ResponseType.SUCCESS,200,'Lista de calificacion de estudiantes por curso y materia',outputUser2).serialize())
        return result
    except Exception as ex:
        return jsonify(Response(ResponseType.ERROR,404,str(ex),None).serialize())

def getStudentsByTutorId(tutor_id, school_id):
    try:
        sql_string = "CALL find_StudentsbyTutor ('{params1}','{params2}')".format(params1=tutor_id,params2=school_id)
        user = db.session.execute(sql_string)
        outputUser2 = userToArrayStudentsbyTutor(user)
        result = jsonify(Response(ResponseType.SUCCESS,200,'Lista de estudiantes por tutor y escuela',outputUser2).serialize())
        return result
    except Exception as ex:
        return jsonify(Response(ResponseType.ERROR,404,str(ex),None).serialize())

#METODO CREADO PARA REALIZAR ACTUALIZACION DE LOS DATOS DE UN CURSO
def updateTeacherSubject(public_id, teacher_code, id_subject, status):
    try:
        if (status == '0'):
            sql_string = "CALL update_TeacherSubjectStatus ('{params1}','{params2}')".format(params1=id_subject,params2=teacher_code)
            user = db.session.execute(sql_string)
            db.session.commit()
            result = jsonify(Response(ResponseType.SUCCESS,200,'Materias actualizadas para el docente',None).serialize())
        if (status == '1'):
            sql_string = "CALL insert_TeacherSubjectStatus ('{params1}','{params2}','{params3}')".format(params1=id_subject,params2=teacher_code,params3=public_id)
            user = db.session.execute(sql_string)
            db.session.commit()
            #outputTeacher = teacherDirectorToArray(user)
            result = jsonify(Response(ResponseType.SUCCESS,200,'Materias creadas para el docente',None).serialize())

        return result

    except Exception as ex:
        return jsonify(Response(ResponseType.ERROR,404,str(ex),None).serialize())


#METODO PARA PERFIL DE PADRES Y DOCENTES
def getCountStudentsById(public_id, id_type):
    try:
        if (id_type == '4'):
            sql_string = "CALL find_StudentSchoolParent ('{params}')".format(params=public_id)
            user = db.session.execute(sql_string)
            outputUser2 = studentToArraySchool(user)
            result = jsonify(Response(ResponseType.SUCCESS,200,'Cantidad Estudiantes para tutor en escuelas',outputUser2).serialize())
            return result
        if (id_type == '3'):
            sql_string = "CALL find_TeacherSchool ('{params}')".format(params=public_id)
            user = db.session.execute(sql_string)
            outputUser2 = studentToArraySchool(user)
            result = jsonify(Response(ResponseType.SUCCESS,200,'Cantidad Estudiantes para docente en escuelas',outputUser2).serialize())
            return result
        else:
            print("en el else")

    except Exception as ex:
        return jsonify(Response(ResponseType.ERROR,404,str(ex),None).serialize())

#METODO PPARA OBTENER DATOS DE DETALLE DE ESTUDIANTES DE TUTOR Y DE DOCENTES
def getStudentsBySchoolId(public_id, id_type, school_id):
    try:
        if (id_type == '2'):#Listado de estudiantes de la escuela por director
            sql_string = "CALL find_ListStudentbySchool ('{params1}','{params2}')".format(params1=public_id,params2=school_id)
            user = db.session.execute(sql_string)
            outputUser = infoListStudentToArray(user)
            result = jsonify(Response(ResponseType.SUCCESS,200,'Informacion de estudiantes de escuela',outputUser).serialize())
            return result
        if (id_type == '10'):#Listado de tutores de la escuela por director
            sql_string = "CALL find_ListTutorbySchool ('{params1}','{params2}')".format(params1=public_id,params2=school_id)
            user = db.session.execute(sql_string)
            outputUser = infoListTutorToArray(user)
            result = jsonify(Response(ResponseType.SUCCESS,200,'Informacion de estudiantes de escuela',outputUser).serialize())
            return result
        if (id_type == '11'):#Listado de docentes de la escuela por director
            sql_string = "CALL find_ListTeacherbySchool ('{params1}','{params2}')".format(params1=public_id,params2=school_id)
            user = db.session.execute(sql_string)
            outputUser = infoListTeacherToArray(user)
            result = jsonify(Response(ResponseType.SUCCESS,200,'Informacion de docentes de escuela',outputUser).serialize())
            return result
        if (id_type == '12'):#Listado de cursos de la escuela por director
            sql_string = "CALL find_ListCoursebySchool ('{params1}','{params2}')".format(params1=public_id,params2=school_id)
            user = db.session.execute(sql_string)
            outputUser = infoListCourseToArray(user)
            result = jsonify(Response(ResponseType.SUCCESS,200,'Informacion de docentes de escuela',outputUser).serialize())
            return result
        if (id_type == '3'):#Listado de estudiantes de la escuela por docente
            sql_string = "CALL find_InfoTeacherbySchool ('{params1}','{params2}')".format(params1=public_id,params2=school_id)
            user = db.session.execute(sql_string)
            outputUser = infoTeacherToArraySchool(user)
            result = jsonify(Response(ResponseType.SUCCESS,200,'Informacion de docentes de escuela',outputUser).serialize())
            return result
        if (id_type == '4'):#Listado de estudiantes de la escuela por tutor
            sql_string = "CALL find_InfoStudentbySchool ('{params1}','{params2}')".format(params1=public_id,params2=school_id)
            user = db.session.execute(sql_string)
            outputUser = infoStudentToArraySchool(user)
            result = jsonify(Response(ResponseType.SUCCESS,200,'Informacion de estudiantes de escuela',outputUser).serialize())
            return result

    except Exception as ex:
        return jsonify(Response(ResponseType.ERROR,404,str(ex),None).serialize())

def getCourseByIdType(public_id, id_type):
    try:
        if (id_type == '2'):
            sql_string = "CALL find_CourseInfobyDirector ('{params}')".format(params=public_id)
            user = db.session.execute(sql_string)
            outputUser2 = courseToArray(user)
            result = jsonify(Response(ResponseType.SUCCESS,200,'Cursos asociados a la escuela del director',outputUser2).serialize())
            return result
        if (id_type == '3'):
            sql_string = "CALL find_StudentParent ('{params}')".format(params=public_id)
            user = db.session.execute(sql_string)
            outputUser = userToArrayStudents(user)
            result = jsonify(Response(ResponseType.SUCCESS,200,'Tutores con estudiantes en escuelas retornado',outputUser).serialize())
            return result
        else:
            print("en el else")

    except Exception as ex:
        return jsonify(Response(ResponseType.ERROR,404,str(ex),None).serialize())

def getAllCourse():
    try:
        course = db.session.query(Course).all()
        output = courseToArrayModel(course)
        return jsonify(Response(ResponseType.SUCCESS,200,'Aulas retornadas',output).serialize())
    except Exception as ex:
        return jsonify(Response(ResponseType.ERROR,404,str(ex),"").serialize())

def createCourse(course):
    try :
        cour = toCourse(course)
        db.session.add(cour)
        db.session.commit()
        result = jsonify(Response(ResponseType.SUCCESS,201,'Clase Insertada',None).serialize())
        return result
    except Exception as ex:
        result = jsonify(Response(ResponseType.ERROR,424,'Error insertando Clase: '+str(ex), None).serialize())

#METODO CREADO PARA REALIZAR ACTUALIZACION DE LOS DATOS DE UN CURSO
def updateCourse(course):
    try:
        if (course['status'] == 0):
            db.session.query(Course).filter(Course.course_id == course['id_course']).update({Course.status: course['status']})
            db.session.commit()
        if   (course['status'] == 1):
            db.session.query(Course).filter(Course.course_id == course['id_course']).update({Course.name: course['name'],Course.status: course['status']})
            db.session.commit()

        return jsonify(Response(ResponseType.SUCCESS,200,'Curso actualizado',None).serialize())
    except Exception as ex:
        return jsonify(Response(ResponseType.ERROR,404,str(ex),None).serialize())


def getAssistantByStudentId(public_id,subject_id):
    try:
        sql_string = "CALL find_AssistantByStudents ('{params1}','{params2}')".format(params1=public_id,params2=subject_id)
        subject = db.session.execute(sql_string)
        outputUser2 = assistantStudentToArray(subject)
        result = jsonify(Response(ResponseType.SUCCESS,200,'Asistencia correspondiente a estudiante',outputUser2).serialize())
        return result

    except Exception as ex:
        return jsonify(Response(ResponseType.ERROR,404,str(ex),None).serialize())


def getAllSubject():
    try:
        subject = db.session.query(Subject).all()
        output = subjectToArray(subject)
        return jsonify(Response(ResponseType.SUCCESS,200,'Materias retornadas',output).serialize())
    except Exception as ex:
        return jsonify(Response(ResponseType.ERROR,404,str(ex),"").serialize())

def getSubjectByDirectorId(public_id):
    try:
        sql_string = "CALL find_SubjectByUser ('{params1}')".format(params1=public_id)
        subject = db.session.execute(sql_string)
        outputUser2 = subjectStudentToArray(subject)
        result = jsonify(Response(ResponseType.SUCCESS,200,'Materias asociadas al usuario enviado',outputUser2).serialize())
        return result

    except Exception as ex:
        return jsonify(Response(ResponseType.ERROR,404,str(ex),None).serialize())

def createSubject(subject):
    try :
        subj = toSubject(subject)
        db.session.add(subj)
        db.session.commit()
        result = jsonify(Response(ResponseType.SUCCESS,201,'Materia Insertada',None).serialize())
        return result
    except Exception as ex:
        result = jsonify(Response(ResponseType.ERROR,424,'Error insertando Materia: '+str(ex), None).serialize())


#METODO CREADO PARA REALIZAR ACTUALIZACION DE LOS DATOS DE UN CURSO
def updateSubject(subject):
    try:
        if (subject['status'] == 0):
            db.session.query(Subject).filter(Subject.subject_id == subject['subject_id']).update({Subject.status: subject['status']})
            db.session.commit()
        if   (subject['status'] == 1):
            db.session.query(Subject).filter(Subject.subject_id == subject['subject_id']).update({Subject.name: subject['name'],Subject.status: subject['status'],Subject.time_from: subject['time_from'],Subject.time_to: subject['time_to']})
            db.session.commit()

        return jsonify(Response(ResponseType.SUCCESS,200,'Materia actualizado',None).serialize())
    except Exception as ex:
        return jsonify(Response(ResponseType.ERROR,404,str(ex),None).serialize())

def getAllMemo():
    try:
        memo = db.session.query(Memo).all()
        output = memoToArray(memo)
        return jsonify(Response(ResponseType.SUCCESS,200,'Boletines retornados',output).serialize())
    except Exception as ex:
        return jsonify(Response(ResponseType.ERROR,404,str(ex),"").serialize())

def createMemo(memo):
    try :
        mem = Memo()

        users = db.session.query(User).filter(User.public_id == memo['public_id_creator'])
        output = userToArray(users)

        mem.user_id = output[0]['user_id']
        mem.school_id = memo['school_id']
        mem.id_memo_type = memo['id_memo_type']
        mem.title = memo['title']
        mem.description = memo['description']

        db.session.add(mem)
        db.session.commit()

        result = jsonify(Response(ResponseType.SUCCESS,201,'Boletin Insertado',None).serialize())
        return result
    except Exception as ex:
        result = jsonify(Response(ResponseType.ERROR,424,'Error insertando Boletin: '+str(ex), None).serialize())

def createCity(city):
    try :
        cit = toCity(city)
        print(city)
        db.session.add(cit)
        db.session.commit()
        result = jsonify(Response(ResponseType.SUCCESS,201,'Ciudad Insertada',None).serialize())
        return result
    except Exception as ex:
        result = jsonify(Response(ResponseType.ERROR,424,'Error insertando ciudad: '+str(ex), None).serialize())

def getAllProvince():
    try:
        province = db.session.query(Province).all()
        output = provinceToArray(province)
        return jsonify(Response(ResponseType.SUCCESS,200,'Provincias retornadas',output).serialize())
    except Exception as ex:
        return jsonify(Response(ResponseType.ERROR,404,str(ex),"").serialize())

def createProvince(province):
    try :
        prov = toProvince(province)
        db.session.add(prov)
        db.session.commit()
        result = jsonify(Response(ResponseType.SUCCESS,201,'Provincia Insertada',None).serialize())
        return result
    except Exception as ex:
        result = jsonify(Response(ResponseType.ERROR,424,'Error insertando provincia: '+str(ex), None).serialize())

def getAllNeighborhood():
    try:
        neighborhood = db.session.query(Neighborhood).all()
        output = neighborhoodToArray(neighborhood)
        return jsonify(Response(ResponseType.SUCCESS,200,'Neighborhood retornadas',output).serialize())
    except Exception as ex:
        return jsonify(Response(ResponseType.ERROR,404,str(ex),"").serialize())

def createNeighborhood(neighborhood):
    try :
        neig = toNeighborhood(neighborhood)
        db.session.add(neig)
        db.session.commit()
        result = jsonify(Response(ResponseType.SUCCESS,201,'Neighborhood Insertada',None).serialize())
        return result
    except Exception as ex:
        result = jsonify(Response(ResponseType.ERROR,424,'Error insertando neighborhood: '+str(ex), None).serialize())


def getAllUserImage():
    try:
        uImage = db.session.query(UserImage).all()
        output = userimageToArray(uImage)
        return jsonify(Response(ResponseType.SUCCESS,200,'Imagenes retornadas',output).serialize())
    except Exception as ex:
        return jsonify(Response(ResponseType.ERROR,404,str(ex),"").serialize())

def createUserImage(userimage):
    try :
        sql_string = "CALL insert_UserImage ('{params1}','{params2}')".format(params1=userimage['public_user_id'],params2=userimage['url_image'])
        userimg = db.session.execute(sql_string)
        db.session.commit()
        outputUser2 = infoResponseUserToArray(userimg)
        result = jsonify(Response(ResponseType.SUCCESS,200,"Imagen agregada al usuario",outputUser2).serialize())
        return result
    except Exception as ex:
        result = jsonify(Response(ResponseType.ERROR,424,'Error insertando Imagen: '+str(ex), None).serialize())


def getUserImageByUserId(public_id):
    try:
            sql_string = "CALL find_UserImage ('{params1}')".format(params1=public_id)
            userimg = db.session.execute(sql_string)
            outputUser2 = userimageToArray(userimg)
            result = jsonify(Response(ResponseType.SUCCESS,200,'Imagen asociada al usuario',outputUser2).serialize())
            return result

    except Exception as ex:
        return jsonify(Response(ResponseType.ERROR,404,str(ex),None).serialize())

def createSchedule(schedule):
    try :
        schedule = toSchedule(schedule)
        print(schedule)
        db.session.add(schedule)
        db.session.commit()
        result = jsonify(Response(ResponseType.SUCCESS,201,'Schedule Insertada',None).serialize())
        return result
    except Exception as ex:
        result = jsonify(Response(ResponseType.ERROR,424,'Error insertando Schedule: '+str(ex), None).serialize())
