insert into usuarios (nome, cpf, email, senha) values ("Davi Brito", 123456, "db@", 123);

insert into pedidos (usuario_id, produtos);

ALTER TABLE produtos
RENAME COLUMN produtos TO combo;

select * from usuarios;
select * from pedidos;
select * from produtos;