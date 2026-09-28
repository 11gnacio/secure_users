from flask_app.config.mysqlconnection import connectToMySQL

class Usuario:
    BASE_DATOS = 'esquema_loginreg'

    def __init__(self, datos):
        self.id = datos['id']
        self.nombre = datos['nombre']
        self.apellido = datos['apellido']
        self.email = datos['email']
        self.password = datos['password']
        self.created_at = datos.get('created_at')
        self.updated_at = datos.get('updated_at')

    @classmethod
    def guardar(cls, datos):
        query = """
            INSERT INTO usuarios (nombre, apellido, email, password)
            VALUES (%(nombre)s, %(apellido)s, %(email)s, %(password)s);
        """
        return connectToMySQL(cls.BASE_DATOS).query_db(query, datos)

    @classmethod
    def buscar_por_email(cls, datos):
        query = "SELECT * FROM usuarios WHERE email = %(email)s;"
        resultados = connectToMySQL(cls.BASE_DATOS).query_db(query, datos)

        if len(resultados) < 1:
            return False
        return cls(resultados[0])

    @classmethod
    def buscar_por_id(cls, datos):
        query = "SELECT * FROM usuarios WHERE id = %(id)s;"
        resultados = connectToMySQL(cls.BASE_DATOS).query_db(query, datos)

        if len(resultados) < 1:
            return False
        return cls(resultados[0])
