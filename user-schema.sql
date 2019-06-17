-- sqlite3 user.db < user-schema.sql

drop table if exists users;
create table users (
  id integer primary key autoincrement,
  user text not null,
  dob text not null
);
