create table usuario(
	id serial primary key,
	nome varchar(50) not null,
	senha text not null,
	email varchar(100) not null
);
insert into usuario("nome","senha","email") values('Luis Santos Reis','123456','luissantosreis@gmail.com');