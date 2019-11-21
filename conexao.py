import psycopg2
from usuario import Usuario
class Conexao:
	def __init__(self):
		self.__con = psycopg2.connect(host='localhost', database='apptrade',user='postgres', password='admin')
		self.__cur = self.__con.cursor()
	def usuarios(self):
		lista = []
		sql = "SELECT * FROM USUARIO"
		self.__cur.execute(sql)
		rec = self.__cur.fetchall()
		for r in rec:
			u = Usuario(r[0],r[1],r[3],r[2])
			lista.append(u)
		return lista
	def cadastrar(self,u):
		sql = "INSERT INTO USUARIO	(nome,email,senha)VALUES(%s,%s,%s);"
		self.__cur.execute(sql, (u.getNome(),u.getEmail(),u.getSenha()))
		self.__con.commit()
	def getUsuario(self, id):
		list = self.usuarios()
		for x in list:
			if int(x.getId()) == int(id):
				return x