BEGIN;
CREATE DATABASE downloads;
\c downloads;
create table downloads_datas( uid integer primary key,value json);
END;