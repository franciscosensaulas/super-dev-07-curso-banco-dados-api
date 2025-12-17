drop database if exists mercado;
create database mercado;
use mercado; 

create table categorias(
	id int primary key auto_increment,
	nome varchar(100)
);

insert into categorias (nome) values ('Hortifruti'); -- id gerado 1
insert into categorias (nome) values ('Embutidos');	-- id gerado 2
select * from categorias;

-- PK -> Primary Key (Chave primária)
-- FK -> Foreign Key (Chave estrangeira) sempre está relacionada a outra Chave primária
-- FK tem que estar atrelada a um PK
create table produtos(
	id int primary key auto_increment,
	nome varchar(100),
	id_categoria int,
	
	foreign key (id_categoria) references categorias (id)
);

insert into produtos (nome, id_categoria) values ('Batatinha', 1);
insert into produtos (nome, id_categoria) values ('Calabresa', 2);
insert into produtos (nome, id_categoria) values ('Bacon', 2);
insert into produtos (nome, id_categoria) values ('Toddy', 3);


select * from produtos;



CREATE TABLE clientes(
	id INT PRIMARY KEY auto_increment,
	nome VARCHAR(50) NOT NULL,
	cpf VARCHAR(14) NOT NULL,
	data_nascimento DATE,
	limite DOUBLE
);