create database iss;

create table simulations (
    id int auto_increment primary key,
    created datetime,
    komentarz varchar(255)
);

create table results (
    sim_id integer,
    elapsed float,
    val float
);
