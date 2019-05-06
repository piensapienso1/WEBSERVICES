from flask import Flask, request, jsonify
from flask_restplus import Api, Resource, Namespace, reqparse, fields
from flask_sqlalchemy import SQLAlchemy
from tutor_model import Base, User
import tutor_services
import tutor_param
from flask_cors import CORS


app = Flask(__name__)
api = Api(app)
service = tutor_services
CORS(app)

us = Namespace('user', description='Operaciones de usuario')
logged_us = Namespace('loggeduser', description='Login de Usuario')
sch = Namespace('school', description='Operaciones de Escuelas')
helper = Namespace('helper', description='Cantidad de estudiantes por tipo de usuario')
direct = Namespace('director', description='Operaciones del director')
stud = Namespace('student', description='Operaciones del estudiante')
tutor = Namespace('tutor', description='Operaciones del tutor')
teach = Namespace('teacher', description='Operaciones del docente')
grad = Namespace('grade', description='Operaciones de Aulas')
cour = Namespace('course', description='Operaciones de Cursos')
subj = Namespace('subject', description='Operaciones de Materias')
img = Namespace('image', description='Mantenimiento de Imagenes')
assit = Namespace('assitance', description='Mantenimiento de asistencia')
qual = Namespace('qualification', description='Mantenimiento de Calificaciones')
schedule = Namespace('schedule', description='Mantenimiento de schedule')
memo = Namespace('memo', description='Mantenimiento de boletines o memorandum')
province = Namespace('province', description='Mantenimiento de Provincias')
neighborhood = Namespace('neighborhood', description='Mantenimiento de Neighborhood')


api.add_namespace(us)
api.add_namespace(logged_us)
api.add_namespace(sch)
api.add_namespace(direct)
api.add_namespace(teach)
api.add_namespace(tutor)
api.add_namespace(stud)
api.add_namespace(helper)
api.add_namespace(grad)
api.add_namespace(cour)
api.add_namespace(subj)
api.add_namespace(img)
api.add_namespace(assit)
api.add_namespace(qual)
#api.add_namespace(schedule)
api.add_namespace(memo)
api.add_namespace(province)
api.add_namespace(neighborhood)


app.config['SECRET_KEY'] = 'lopezthelma'
app.config['SQLALCHEMY_DATABASE_URI'] = tutor_param.getMySQLConn()

db = SQLAlchemy(app)
service.db = db

@us.route('')
class user(Resource):
    def get(self):
        return service.getAllUser()

    @us.expect(tutor_param.getUserParam(us))
    def post(self,*args, **kwargs):
        data = request.get_json()
        return service.createUser(data)

    @us.expect(tutor_param.getUserParam(us))
    def put(self,*args, **kwargs):
        data = request.get_json()
        return service.updateUser(data)

@us.route('/<string:public_id>')
class getUserById(Resource):
    def get(self,public_id):
        return service.getUserById(public_id)

#@us.route('/<string:user_code>/<string:id_type>')
#class getUserByUserCode(Resource):
#    def get(self,user_code, id_type):
#        return service.getUserByUserCode(user_code, id_type)

@logged_us.route('')
class LoggedUser(Resource):
    #def get(self):
    #    return service.getAllLoggedUser()

    @logged_us.expect(tutor_param.getLoggedUserParam(logged_us))
    def post(self,*args, **kwargs):
        data = request.get_json()
        return service.getLoggedUser(data)

@sch.route('')
class school(Resource):
    def get(self):
        return service.getAllSchool()

    @sch.expect(tutor_param.getSchoolParam(sch))
    def post(self,*args, **kwargs):
        data = request.get_json()
        return service.createSchool(data)

@sch.route('/<string:public_id>')
class getSchoolByUserId(Resource):
    def get(self,public_id):
        return service.getSchoolByUserId(public_id)

@sch.route('/<string:public_id>/<string:id_type>')
class getSchoolByDirectorId(Resource):
    def get(self,public_id, id_type):
        return service.getSchoolByDirectorId(public_id)

@sch.route('/<string:public_id>/<string:id_type>/<string:school_id>')
class getStudentsBySchoolId(Resource):
    def get(self,public_id,id_type, school_id):
        return service.getStudentsBySchoolId(public_id,id_type, school_id)

@direct.route('/<string:school_id>')
class getDirectorBySchool(Resource):
    def get(self, school_id):
        return service.getDirectorBySchool(school_id)

@direct.route('/<string:public_id>/<string:teacher_code>/<string:id_subject>/<string:status>')
class updateTeacherByDirectorId(Resource):
    def get(self, public_id, teacher_code, id_subject, status):
        return service.updateTeacherSubject(public_id, teacher_code,id_subject, status)

@tutor.route('/<string:student_id>')
class getTutorByStudentId(Resource):
    def get(self,student_id):
        return service.getTutorByStudentId(student_id)

@tutor.route('/<string:tutor_id>/<string:school_id>')
class getStudentsByTutorId(Resource):
    def get(self,tutor_id, school_id):
        return service.getStudentsByTutorId(tutor_id, school_id)

@stud.route('/<string:student_id>')
class getTeacherByStudentId(Resource):
    def get(self,student_id):
        return service.getTeacherByStudentId(student_id)

#@stud.route('/<string:course_id>/<string:school_id>')
#class getStudentByCourseId(Resource):
#    def get(self,course_id, school_id):
#        return service.getStudentByCourseId(course_id,school_id)

@stud.route('/<string:course_id>/<string:school_id>/<string:subject_id>')
class getStudentBySubjectId(Resource):
    def get(self,course_id, school_id,subject_id):
        return service.getStudentBySubjectId(course_id,school_id,subject_id)

@helper.route('/<string:public_id>/<string:id_type>')
class getCountStudentsById(Resource):
    def get(self,public_id, id_type):
        return service.getCountStudentsById(public_id, id_type)


@teach.route('/<string:public_id>/<string:school_id>/<string:subject_id>')
class getStudentByTeacherId(Resource):
    def get(self,public_id, school_id,subject_id):
        return service.getStudentByTeacherId(public_id,school_id,subject_id)

@teach.route('/<string:public_id>/<string:school_id>/')
class getTeacherByDirectorId(Resource):
    def get(self,public_id, school_id):
        return service.getTeacherByDirectorId(public_id,school_id)

#@teach.route('/<string:public_id_student>')
#class getTeacherByDirectorId(Resource):
#    def get(self,public_id, school_id):
#        return service.getTeacherByDirectorId(public_id,school_id)


@grad.route('')
class Grade(Resource):
    def get(self):
        return service.getAllGrade()

    @grad.expect(tutor_param.getGradeParam(grad))
    def post(self,*args, **kwargs):
        data = request.get_json()
        return service.createGrade(data)

@grad.route('/<string:public_id>/<string:school_id>')
class getGradeByDirectorId(Resource):
    def get(self,public_id, school_id):
        return service.getGradeByDirectorId(public_id,school_id)

@subj.route('')
class Subject(Resource):
    def get(self):
        return service.getAllSubject()

    @subj.expect(tutor_param.getSubjectParam(subj))
    def post(self,*args, **kwargs):
        data = request.get_json()
        return service.createSubject(data)

    @subj.expect(tutor_param.getSubjectParam(subj))
    def put(self,*args, **kwargs):
        data = request.get_json()
        return service.updateSubject(data)

@subj.route('/<string:public_id>')
class getSubjectByDirectorId(Resource):
    def get(self,public_id):
        return service.getSubjectByDirectorId(public_id)

@img.route('')
class UserImage(Resource):
    def get(self):
        return service.getAllUserImage()

    @img.expect(tutor_param.getUserImageParam(img))
    def post(self,*args, **kwargs):
        data = request.get_json()
        return service.createUserImage(data)

@img.route('/<string:public_id>')
class getUserImageByUserId(Resource):
    def get(self,public_id):
        return service.getUserImageByUserId(public_id)

@assit.route('')
class Assitance(Resource):
    @assit.expect(tutor_param.getAssitanceParam(assit))
    def post(self,*args, **kwargs):
        data = request.get_json()
        return service.createAssitance(data)

@assit.route('/<string:public_id>/<string:subject_id>')
class getAssistantByStudentId(Resource):
    def get(self,public_id,subject_id):
        return service.getAssistantByStudentId(public_id,subject_id)

@qual.route('')
class Qualification(Resource):
    @qual.expect(tutor_param.getQualificationParam(qual))
    def post(self,*args, **kwargs):
        data = request.get_json()
        return service.createQualification(data)

@qual.route('/<string:course_id>/<string:student_id>/<string:subject_id>')
class getQualificationByStudentId(Resource):
    def get(self,course_id,student_id,subject_id):
        return service.getQualificationByStudentId(course_id,student_id,subject_id)

@qual.route('/<string:course_id>/<string:subject_id>')
class getQualificationBySubjectId(Resource):
    def get(self,course_id,subject_id):
        return service.getQualificationBySubjectId(course_id,subject_id)

@memo.route('')
class Memo(Resource):
    def get(self):
        return service.getAllMemo()

    @memo.expect(tutor_param.getMemoParam(memo))
    def post(self,*args, **kwargs):
        data = request.get_json()
        return service.createMemo(data)

@cour.route('')
class Course(Resource):
    def get(self):
        return service.getAllCourse()

    @cour.expect(tutor_param.getCourseParam(cour))
    def post(self,*args, **kwargs):
        data = request.get_json()
        return service.createCourse(data)

    @cour.expect(tutor_param.getCourseParam(cour))
    def put(self,*args, **kwargs):
        data = request.get_json()
        return service.updateCourse(data)

@cour.route('/<string:public_id>/<string:id_type>')
class getCourseByIdType(Resource):
    def get(self,public_id, id_type):
        return service.getCourseByIdType(public_id,id_type)


@province.route('')
class Province(Resource):
    def get(self):
        return service.getAllProvince()

    @province.expect(tutor_param.getProvinceParam(province))
    def post(self,*args, **kwargs):
        data = request.get_json()
        return service.createProvince(data)

@neighborhood.route('')
class Neighborhood(Resource):
    def get(self):
        return service.getAllNeighborhood()

    @neighborhood.expect(tutor_param.getNeighborhoodParam(neighborhood))
    def post(self,*args, **kwargs):
        data = request.get_json()
        return service.createNeighborhood(data)


@schedule.route('')
class Schedule(Resource):
    @schedule.expect(tutor_param.getScheduleParam(schedule))
    def post(self,*args, **kwargs):
        data = request.get_json()
        return service.createSchedule(data)

    @schedule.expect(tutor_param.getScheduleParam(schedule))
    def put(self,*args, **kwargs):
        data = request.get_json()
        return service.updateSchedule(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0')