from flask_restplus import fields

def getMySQLConn():

    #return 'mysql+pymysql://youtop:YouToP8472@localhost/tutor_db'
    return 'mysql+pymysql://tutor_db:password@localhost/tutor_db'

def getUserParam(us):
	return us.model('User', {
		'user_id' : fields.Integer(readOnly=False, description='The unique identifier'),
		'id_type' : fields.Integer(required=True, description='Id Tipo'),
		'first_name' : fields.String(required=True, description='Nombres'),
		'last_name' : fields.String(required=True, description='Apellidos'),
		'phone' : fields.String(required=False, description='Telefono'),
		'cell_phone' : fields.String(required=False, description='Celular'),
		'status' : fields.String(required=False, description='Estado'),
        'user_name' : fields.String(required=True, description='Usuario'),
        'password' : fields.String(required=True, description='Contrasena'),
        'password2' : fields.String(required=True, description='Contrasena2'),
        'date_birth' : fields.String(required=False, description='Fecha Cumpleanos'),
        'document_id' : fields.String(required=False, description='document_id'),
        'age' : fields.String(required=False, description='Edad'),
        'gender' : fields.String(required=False, description='Genero'),
        'tutor_id' : fields.Integer(required=False, description='Id del Tutor'),
        'email' : fields.String(required=True, description='Correo Electronico'),
        'public_id' : fields.String(required=False, description='Token del Usuario'),
        'public_id_school' : fields.String(required=True, description='Token del Centro'),
        'course_id' : fields.Integer(required=False, description='Id del Curso del Estudiante'),
        'subject_array_id' : fields.String(required=False, description='Datos de materias del docente')
	})

def getUserPutParam(us):
	return us.model('User', {
		#'user_id' : fields.Integer(readOnly=False, description='The unique identifier'),
		#'id_type' : fields.Integer(required=True, description='Id Tipo'),
		'first_name' : fields.String(required=True, description='Nombres'),
		'last_name' : fields.String(required=True, description='Apellidos'),
		'phone' : fields.String(required=False, description='Telefono'),
		'cell_phone' : fields.String(required=False, description='Celular'),
		'status' : fields.String(required=False, description='Estado'),
        #'password' : fields.String(required=True, description='Contrasena'),
        #'password2' : fields.String(required=True, description='Contrasena2'),
        'date_birth' : fields.String(required=False, description='Fecha Cumpleanos'),
        #'document_id' : fields.String(required=False, description='document_id'),
        'age' : fields.String(required=False, description='Edad'),
        'gender' : fields.String(required=False, description='Genero'),
        #'email' : fields.String(required=True, description='Correo Electronico'),
        'public_id' : fields.String(required=True, description='public_id')
	})

def getLoggedUserParam(logged_us):
	return logged_us.model('LoggedUser', {
		'user_name' : fields.String(required=True, description='Usuario'),
		'password' : fields.String(required=True, description='Contrasena'),
        'id_type' : fields.String(required=True, description='Tipo Usuario')
	})

def getSchoolParam(school):
	return school.model('School', {
		'name' : fields.String(required=True, description='Nombre Escuela'),
        'id_province' : fields.String(required=False, description='id_province'),
		'id_neighborhood' : fields.String(required=False, description='id_neighborhood'),
		'street' : fields.String(required=False, description='street'),
        'block' : fields.String(required=False, description='block'),
		'apartment' : fields.String(required=False, description='apartment'),
        'logo' : fields.String(required=False, description='logo'),
        'location' : fields.String(required=False, description='location'),
        #'public_id' : fields.String(required=True, description='No. Diretor'),
        'document_id' : fields.String(required=True, description='No. RNC')

	})

def getUserImageParam(img):
	return img.model('UserImage', {
		'public_user_id' : fields.String(required=True, description='PublicId del Usuario'),
		'url_image' : fields.String(required=True, description='URL de Imagen')
	})

def getGradeParam(grade):
	return grade.model('Grade', {
		'id_school' : fields.String(required=True, description='Id School'),
		'name' : fields.String(required=True, description='Nombre Aula')
	})

def getCourseParam(course):
	return course.model('Course', {
        'id_course' : fields.Integer(required=True, description='Id Course'),
		'name' : fields.String(required=False, description='Nombre Curso'),
        'status' : fields.Integer(required=True, description='Status Curso')
	})

def getSubjectParam(subject):
	return subject.model('Subject', {
        'subject_id' : fields.Integer(required=True, description='Id Subject'),
		'id_grade' : fields.String(required=True, description='Id Grade'),
		'name' : fields.String(required=True, description='Nombre Materia'),
        'time_from' : fields.String(required=True, description='Hora desde'),
        'time_to' : fields.String(required=True, description='Hora hasta'),
        'status' : fields.Integer(required=True, description='Status Materia')
	})

def getAssitanceParam(assitance):
	return assitance.model('Assitance', {
		'id_assitance_type' : fields.Integer(required=True, description='Id Tipo Asistencia'),
        'id_course' : fields.Integer(required=True, description='Id Curso'),
        'id_usr_student' : fields.Integer(required=True, description='Id Estudiante'),
        'id_subject' : fields.Integer(required=True, description='Id Materia'),
        'value' : fields.Integer(required=True, description='Valor Asistencia'),
        'comments' : fields.String(required=True, description='Comentarios docente')

	})

def getQualificationParam(qualification):
	return qualification.model('Qualification', {
		'id_qualification_type' : fields.Integer(required=True, description='Id Tipo Calificacion'),
        'id_course' : fields.Integer(required=True, description='Id Curso'),
        'id_usr_student' : fields.Integer(required=True, description='Id Estudiante'),
        'id_subject' : fields.Integer(required=True, description='Id Materia'),
        'value' : fields.Integer(required=True, description='Valor Calificacion'),
        'test_date' : fields.String(required=True, description='Fecha de Prueba'),
        'test_type' : fields.String(required=True, description='Tipo de Prueba')
	})

def getMemoParam(memo):
	return memo.model('Memo', {
		'id_memo_type' : fields.Integer(required=True, description='Id Tipo Memo'),
		'title' : fields.String(required=True, description='Titulo Memo'),
        'school_id' : fields.Integer(required=True, description='School ID'),
        'public_id_creator' : fields.String(required=True, description='Public Id Creador Memo'),
        'description' : fields.String(required=True, description='Descripcion Memo')
	})

def getProvinceParam(province):
	return province.model('Province', {
		'name' : fields.String(required=True, description='Nombre Provincia')
	})

def getNeighborhoodParam(neighborhood):
	return neighborhood.model('Neighborhood', {
		'id_province' : fields.String(required=True, description='Id Provincia'),
		'name' : fields.String(required=True, description='Nombre Neighborhood')
	})

def getScheduleParam(item):
	return item.model('Schedule', {
		'task' : fields.String(required=True, description='Task'),
		'datetime_todo' : fields.String(required=True, description='Fecha a ejecutar tarea')
	})
