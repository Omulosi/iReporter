
DROP TABLE IF EXISTS records;
DROP TABLE IF EXISTS blacklist;
DROP TABLE IF EXISTS users;

create table records (
      id serial primary key,
      type varchar(50) not null,
      comment varchar(140) not null,
      location varchar(30) not null,
      status varchar(50) not null,
      createdon timestamp with time zone not null default now(),
      images varchar(120)[] not null,
      videos varchar(120)[] not null,
      uri varchar(140),
      createdby integer not null,
      user_id integer references users(id) on delete cascade not null
);
            

create table users (
            id serial primary key,
            username varchar(80) not null,
            email varchar(100) not null,
            createdOn timestamp with time zone not null,
            firstname varchar(100) not null,
            lastname varchar(100) not null,
            othernames varchar(100) not null,
            phoneNumber varchar(100) not null,
            isAdmin boolean not null,
            password_hash varchar(100) not null
            );

create table blacklist (
            id serial primary key,
            jti varchar(140) not null
            );
            
