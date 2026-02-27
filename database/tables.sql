create database lesson_planner;
use lesson_planner;

create table lesson_plans (
    id int auto_increment primary key,
    subject varchar(50) not null,
    topic varchar(100) not null,
    grade varchar(10) not null,
    duration varchar(20) not null,
    lesson_text longtext not null,
    created_at timestamp default current_timestamp
);
select * from lesson_plans;
