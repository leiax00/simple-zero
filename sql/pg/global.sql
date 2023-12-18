drop database if exists "simple-zero";
create database "simple-zero" with owner = postgres;

create schema novel;
alter schema novel owner to postgres;