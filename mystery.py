from sqlalchemy import create_engine
import psycopg2
import logging

logging.basicConfig(filename='mystery.log',
        filemode='w',
        level=logging.INFO)


try:
    database = 'postgresql+psycopg2://usrname:pwd@host:port/dbname'

    engine = create_engine(database)
    con = engine.raw_connection()
    cursor = con.cursor()
    logging.info('db setup completed')
except:
    logging.error('error in setting up db',exc_info=True)

try:
    query='''
    create table income (
        ssn int primary key,
        income money
    );

    create table drivers_license(
        id int primary key,
        age int,
        height float,
        eye_color varchar (10),
        hair_color varchar(10),
        gender varchar(10),
        plate_number text,
        car_make text,
        car_model text
    );

    create table person(
        id int primary key,
        name varchar(50),
        license_id int,
        address_number int,
        address_street_name text,
        ssn int,
        foreign key (ssn) REFERENCES income(ssn) ON DELETE CASCADE,
        foreign key(license_id) REFERENCES drivers_license(id) ON DELETE CASCADE
    );

    create table get_fit_now_member(
        id int primary key,
        person_id int,
        name text,
        membership_start_date date,
        membership_status text,
        foreign key (person_id) REFERENCES person(id) ON DELETE CASCADE
    );

    create table get_fit_now_check_in(
        membership_id int,
        check_in_date date,
        check_in_time time,
        check_out_time time,
        foreign key (membership_id) references get_fit_now_member(id) ON DELETE CASCADE
    );

    create table facebook_event_checkin(
        person_id int not null,
        event_id int,
        event_name text,
        date date,
        foreign key(person_id) references person(id) ON DELETE CASCADE
    );

    create table interview (
        person_id int not null,
        transcript text,
        foreign key(person_id) REFERENCES person(id) ON DELETE CASCADE
    );

    create table crime_scene_report(
        date date,
        type text,
        description text,
        city text
    );

    '''
    cursor.execute(query)
    con.commit()
    cursor.close()
    logging.info('created tables succesfully')

except:
    logging.error('issue in query',exc_info=True)
