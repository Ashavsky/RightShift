drop table if exists jobs;

create table jobs 
(
	id integer primary key autoincrement,
	total_payment decimal(10,2) not null,
	location text not null,
	hospital text not null
);