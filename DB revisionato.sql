DROP SCHEMA public CASCADE;
CREATE SCHEMA public;


create table utente (
    id varchar(7) primary key,
    nome varchar(20),
    cognome varchar(20),
    mail text,
    dataN date,
    --tipo varchar(1) --è ricavabile da id percheè abbiamo p.... r.... 
    hash_psw text,
    fatt_risc text,
    id_med_ref varchar(7) references utente(id)
);
 
insert into utente (id, nome, cognome, mail, dataN, hash_psw, fatt_risc, id_med_ref)
values
('M000001', 'Gino', 'Montanari', 'g.montanari@gmail.com', '1985-07-01', '$2b$12$NZDgaHyPhgZ9pd0OfpiwyenoN/1v9Dh1m0BJgxb7GAvrqupir3ZSG', null, null),
('M000002', 'Valerio', 'Rossi', 'v.rossi@gmail.com', '1987-05-05', '$2b$12$4XuKXCYQCEFoiCNFGUeqvOd4bb7QYESwItg97qFKtwiauIZPP1Zka', null, null),
('P000001', 'Mario', 'Rossi', 'm.rossi@gmail.com', '1984-06-06', '$2b$12$34DhHK/7EIQCwxm9rSFAQeHw8g9x5/0khcwViwJ28j/NX2KiVGTsm', 'obeso, fumatore','M000001'),
('P000002', 'Luigi', 'Verdi', 'l.verdi@gmail.com', '1985-03-09', '$2b$12$rFw0BfQJe8FDLPzppTWkbO34FIEJPzH2PKr2fiEwc8k3bzDBJG/fi', 'alcolizzato', 'M000002'),
('R000001', 'Lino', 'Gialli', 'r.responsabiliApp@gmail.com', '1960-04-05', '$2b$12$NngwdDihiPgZmIAYPr/.1OzuQFBjMgegIbRh.JcEr/SscLutFXG1u', null, null);

create table dati_gior (
	giorno date,
    id_paz varchar(7) references utente(id),
	ora time,
    pmin integer,
	pmax integer,
	primary key(id_paz, giorno, ora)
);

insert into dati_gior (giorno, id_paz, ora, pmin, pmax)
values
( '2023-05-01', 'P000001', '09:00:00', 80, 129), --prima misurazione che mario fa nel giorno 05-01
( '2023-05-01', 'P000001', '20:00:00', 85, 120), --seconda misurazione che  amrio fa
( '2023-05-02', 'P000001', '09:00:00', 87, 130),
( '2023-05-02', 'P000001', '21:00:00', 83, 128),
( '2023-05-01', 'P000002', '10:00:00', 90, 160),
( '2023-05-02', 'P000002', '22:00:00', 110, 180),
--qui Mario non si è loggato fini al 6 maggio, maledetto, si è logato solo Luigi e ha inserito le misurazioni
--3/05
( '2023-05-03', 'P000002', '10:00:00', 90, 160),
--4/05
( '2023-05-04', 'P000002', '10:00:00', 110, 160),
( '2023-05-04', 'P000002', '19:00:00', 111, 170),
--5/05
( '2023-05-05', 'P000002', '10:00:00', 90, 160),

( '2023-05-19', 'P000001', '10:00:00', 90, 160),
( '2023-05-21', 'P000001', '10:00:00', 90, 180),
( '2023-05-21', 'P000001', '11:00:00', 110, 160),
( '2023-05-21', 'P000001', '12:00:00', 70, 100),
( '2023-05-22', 'P000001', '10:00:00', 90, 160),
( '2023-05-23', 'P000001', '09:00:00', 80, 170),
( '2023-05-23', 'P000001', '10:00:00', 90, 160);


create table sintomo(
    nome text primary key
);

insert into sintomo(nome) values
('AFFATICAMENTO'),
('ALTERAZIONI DEL SONNO'),
('ANGINA'),
('ANSIA'),
('ARROSSAMENTO DEL VISO'),
('BATTITO CARDIACO IRREGOLARE'),
('CAMBIAMENTI NELLE FECI O NELL''URINA'),
('CEFALEA'),
('CONFUSIONE MENTALE'),
('DIFFICOLTÀ A DORMIRE'),
('DISTURBI GASTROINTESTINALI'),
('DISTURBI VISIVI'),
('DOLORE'),
('DOLORE AL PETTO O SENSATIONE DI OPPRESSIONE'),
('DOLORE TORACICO'),
('FATICA'),
('FATICA O DEBOLEZZA'),
('FEBBRE'),
('FLUSSO URINARIO RIDOTTO'),
('GONFIORE ALLE CAVIGLIE, AI PIEDI O ALLE GAMBE'),
('INSUFFICIENZA RENALE'),
('IRRITABILITÀ'),
('MAL DI TESTA'),
('NAUSEA'),
('PALPITAZIONI'),
('PERDITA DI APPETITO'),
('PERDITA DI PESO INVOLONTARIA'),
('PRESENZA DI SANGUE NELLE URINE'),
('PROBLEMI DI VISIONE'),
('PROBLEMI RESPIRATORI'),
('RUMORI ALL''ORECCHIO'),
('SANGUINAMENTO DAL NASO'),
('STANCHEZZA'),
('VERTIGINI'),
('VISIONE OFFUSCATA'),
('VOMITO');

create table occ_sintomo(
    nome_sint text references sintomo(nome), 
    id_paz varchar(7) references utente(id),
    inizio date,
    tipo text,       -- conc, preg
    fine date,
    primary key(nome_sint, id_paz, inizio)
);

insert into occ_sintomo(nome_sint, id_paz, inizio, tipo, fine)
values ('MAL DI TESTA', 'P000001', '2023-05-01', 'conc', null),
('NAUSEA', 'P000001', '2023-04-28', 'preg', '2023-04-29'),
('FEBBRE', 'P000002', '2023-05-02', 'preg', '2023-05-07'),
('VOMITO', 'P000002', '2023-05-03', 'preg', '2023-05-06');


create table patologia(
    nome text primary key
);

insert into patologia(nome) values 
--('Ipertensione'), ????????????
('ANSIA'),
('ARTRITE'),
('ASMA'),
('CANCRO'),
('DEPRESSIONE'),
('DIABETE'),
('DISTURBI CARDIOVASCOLARI'),
('DISTURBI ENDOCRINI'),
('DISTURBI EMATOLOGICI'),
('DISTURBI GASTROINTESTINALI'),
('DISTURBI METABOLICI'),
('DISTURBI MUSCOLOSCHLETRICI'),
('DISTURBI NEUROLOGICI'),
('DISTURBI OCULARI'),
('DISTURBI ORMONALI'),
('DISTURBI PSICHIATRICI'),
('DISTURBI UROLOGICI'),
('DISTURBI RESPIRATORI'),
('EPILESSIA'),
('HIV/AIDS'),
('IPERTENSIONE'),
('MALATTIE CARDIACHE'),
('MALATTIE EPATICHE'),
('MALATTIE NEUROLOGICHE'),
('MALATTIE OCULARI'),
('MALATTIE RENALI'),
('MALATTIE RESPIRATORIE'),
('OBESITÀ');

create table occ_patologia(
    nome_pat text references patologia(nome), 
    id_paz varchar(7) references utente(id),
    inizio date,
    tipo text,      --conc, preg, segn_pat_conc
    fine date,
    primary key(nome_pat, id_paz, inizio)
);

insert into occ_patologia(nome_pat, id_paz, inizio, tipo, fine)
values ('DIABETE', 'P000001', '2016-05-01', 'conc', null),
('CANCRO', 'P000001', '2022-04-28', 'conc', null),
('CANCRO', 'P000001', '2016-04-28', 'preg', '2017-09-07'),
('ASMA', 'P000002', '2002-01-02', 'preg', '2023-05-07'),
('ARTRITE', 'P000001', '2023-04-23', 'segn_pat_conc', null)
;

create table farmaco(
    nome text primary key,
    tipo text --iper, altro
);

insert into farmaco(nome, tipo) values 
('AMLODIPINA', 'iper'),
('BENAZAPRIL', 'iper'),
('BISOPROLOLO', 'iper'),
('CANDERSARTAN', 'iper'),
('CAPTOPRIL', 'iper'),
('CLORTALIDONE', 'iper'),
('DOXAZOSINA', 'iper'),
('ENALAPRIL', 'iper'),
('FOSINOPRIL', 'iper'),
('IDROCLOROTIAZIDE', 'iper'),
('LABETALOLO', 'iper'),
('LOSARTAN', 'iper'),
('METILDOPA', 'iper'),
('NEBIVOLOLO', 'iper'),
('OLMESARTAN', 'iper'),
('RAMIPRIL', 'iper'),
('TELMISARTAN', 'iper'),
('VALSARTAN', 'iper'),
('ACETAMINOFENE', 'altro'),
('ALPRAZOLAM', 'altro'),
('AMOXICILLINA', 'altro'),
('ASPIRINA', 'altro'),
('ATORVASTATINA', 'altro'),
('BROMAZEPAM', 'altro'),
('CETIRIZINA', 'altro'),
('CIPROFLOXACINA', 'altro'),
('CITALOPRAM', 'altro'),
('DEXAMETASONE', 'altro'),
('DIAZEPAM', 'altro'),
('DOMPERIDONE', 'altro'),
('ESOMEPRAZOLO', 'altro'),
('FLUOXETINA', 'altro'),
('GABAPENTIN', 'altro'),
('IBUPROFENE', 'altro'),
('LEVOFLOXACINA', 'altro'),
('LISINOPRIL', 'altro'),
('METFORMINA', 'altro'),
('METOCLOPRAMIDE', 'altro'),
('OMEPRAZOLO', 'altro'),
('ONDANSETRONE', 'altro'),
('PANTOPRAZOLO', 'altro'),
('PARACETAMOLO', 'altro'),
('PREDNISONE', 'altro'),
('QUETIAPINA', 'altro'),
('RANITIDINA', 'altro'),
('RINAZINA', 'altro'),
('SILDENAFIL', 'altro'),
('TRAMADOLO', 'altro'),
('VENLAFAXINA', 'altro');

create table terapia(
    nome_farm text references farmaco(nome), 
    id_paz varchar(7) references utente(id),
    inizio date,
    qtaxdose text,
	ndosi integer,
	ind text,
    tipo varchar(20),        --preg, conc, iper, segn_ter_conc
    fine date,
    primary key(nome_farm, id_paz, inizio)
);

insert into terapia(nome_farm, id_paz, inizio, qtaxdose, ndosi, ind, tipo, fine)
values
('BENAZAPRIL','P000001', '2020-09-08','1 pastiglia', '2', 'bere molta acqua dopo l''assunzione', 'iper', null),
('PARACETAMOLO','P000001', '2022-11-08', '1 pastiglia', '1', 'dopo pranzo', 'conc', null),
('CAPTOPRIL', 'P000001', '2019-10-14', '1/4 pastiglia', '2', '', 'iper', null),
('RINAZINA', 'P000001', '2012-01-01','3 spruzzi', '4', 'Non inalare', 'segn_ter_conc', null),
('BENAZAPRIL','P000001', '2010-09-08','1 pastiglia', '2', 'bere molta acqua dopo l''assunzione', 'preg', '2015-09-08'),

('BENAZAPRIL', 'P000002', '2020-09-08','2 pastiglie', '1', 'mattina e sera', 'iper', null);

create table assunzione (
    nome_farm text, 
    id_paz varchar(7),
    inizio_ter date,
    giorno date,
    dose integer,
    ora time,
    corretta boolean,
    primary key(nome_farm, id_paz, inizio_ter, giorno, dose),
    foreign key (nome_farm, id_paz, inizio_ter) references terapia(nome_farm, id_paz, inizio) ON UPDATE CASCADE
);

insert into assunzione(nome_farm, id_paz, inizio_ter, giorno, dose, ora, corretta)
values
--ricorda che la DB registra solamente l'assunzione dei farmaci relative alle terapie iper dei pazienti presenti all'interno della DB
--p000001 mario
--prima dose 
('BENAZAPRIL', 'P000001', '2020-09-08', '2023-05-01', 1, '09:00:00', TRUE),
('BENAZAPRIL', 'P000001', '2020-09-08', '2023-05-01',2, '20:00:00', FALSE),
('CAPTOPRIL', 'P000001', '2019-10-14', '2023-05-01', 1,'09:00:00', FALSE),
('CAPTOPRIL', 'P000001', '2019-10-14', '2023-05-01', 2,'20:00:00', TRUE),
('BENAZAPRIL', 'P000002', '2020-09-08', '2023-05-01',1, '08:00:00', FALSE),

--il 02/05 mario non ha preso la seconda dose di benazapril, quindi la'assunzione di quell'ora non c'è
('BENAZAPRIL', 'P000001', '2020-09-08', '2023-05-02',1,'09:00:00', TRUE),
('BENAZAPRIL', 'P000001', '2020-09-08', '2023-05-02', 2,'20:00:00', TRUE),
('CAPTOPRIL', 'P000001', '2019-10-14', '2023-05-02',1, '09:00:00', TRUE),
('CAPTOPRIL', 'P000001', '2019-10-14', '2023-05-02', 2,'20:00:00', TRUE),
('BENAZAPRIL', 'P000002', '2020-09-08', '2023-05-02',1, '08:00:00', TRUE),

--il 03/05, Mario non si è loggato e quindi non ha comoilato le terapie, luigi inevece si e ha compilato
('BENAZAPRIL', 'P000001', '2020-09-08', '2023-05-03',1, '09:00:00', FALSE),
('BENAZAPRIL', 'P000001', '2020-09-08', '2023-05-03',2, '20:00:00', FALSE),
('CAPTOPRIL', 'P000001', '2019-10-14', '2023-05-03', 1,'09:00:00', FALSE),
('CAPTOPRIL', 'P000001', '2019-10-14', '2023-05-03',2, '20:00:00', FALSE),
('BENAZAPRIL', 'P000002', '2020-09-08', '2023-05-03', 1,'08:00:00', TRUE),

-- il 04/05 mario non si è loggato e luigi non ha compilato le terapie
('BENAZAPRIL', 'P000001', '2020-09-08', '2023-05-04',1, '09:00:00', FALSE),
('BENAZAPRIL', 'P000001', '2020-09-08', '2023-05-04',2, '20:00:00', FALSE),
('CAPTOPRIL', 'P000001', '2019-10-14', '2023-05-04',1, '09:00:00', FALSE),
('CAPTOPRIL', 'P000001', '2019-10-14', '2023-05-04',2, '20:00:00', FALSE),
('BENAZAPRIL', 'P000002', '2020-09-08', '2023-05-04',1, '08:00:00', FALSE),

-- -- 05/05 NON si è loggato
('BENAZAPRIL', 'P000001', '2020-09-08', '2023-05-05',1, '09:00:00', FALSE),
('BENAZAPRIL', 'P000001', '2020-09-08', '2023-05-05',2, '20:00:00', FALSE),
('CAPTOPRIL', 'P000001', '2019-10-14', '2023-05-05', 1,'09:00:00', FALSE),
('CAPTOPRIL', 'P000001', '2019-10-14', '2023-05-05', 2,'20:00:00', FALSE),
('BENAZAPRIL', 'P000002', '2020-09-08', '2023-05-05',1, '08:00:00', TRUE),


('BENAZAPRIL', 'P000001', '2020-09-08', '2023-05-19',1, '09:00:00', FALSE),
('BENAZAPRIL', 'P000001', '2020-09-08', '2023-05-19',2, '20:00:00', FALSE),
('CAPTOPRIL', 'P000001', '2019-10-14', '2023-05-19', 1,'09:00:00', FALSE),
('CAPTOPRIL', 'P000001', '2019-10-14', '2023-05-19',2, '20:00:00', FALSE),

-- il 20-05 non si è loggatto

('BENAZAPRIL', 'P000001', '2020-09-08', '2023-05-21',1, '09:00:00', FALSE),
('BENAZAPRIL', 'P000001', '2020-09-08', '2023-05-21',2, '20:00:00', FALSE),
('CAPTOPRIL', 'P000001', '2019-10-14', '2023-05-21', 1,'09:00:00', FALSE),
('CAPTOPRIL', 'P000001', '2019-10-14', '2023-05-21',2, '20:00:00', FALSE),

('BENAZAPRIL', 'P000001', '2020-09-08', '2023-05-22',1, '09:00:00', FALSE),
('BENAZAPRIL', 'P000001', '2020-09-08', '2023-05-22',2, '20:00:00', TRUE),
('CAPTOPRIL', 'P000001', '2019-10-14', '2023-05-22', 1,'09:00:00', FALSE),
('CAPTOPRIL', 'P000001', '2019-10-14', '2023-05-22',2, '20:00:00', TRUE),

('BENAZAPRIL', 'P000001', '2020-09-08', '2023-05-23',1, '09:00:00', FALSE),
('BENAZAPRIL', 'P000001', '2020-09-08', '2023-05-23',2, '20:00:00', FALSE),
('CAPTOPRIL', 'P000001', '2019-10-14', '2023-05-23', 1,'09:00:00', FALSE),
('CAPTOPRIL', 'P000001', '2019-10-14', '2023-05-23',2, '20:00:00', FALSE);

create table segnalazione (
	cod serial primary key,
    data date,
	id_paz varchar(7) references utente(id),
	tipo varchar(10), --no_segue, p_anomala
	gravita text
);

insert into segnalazione (data, id_paz, tipo, gravita)
values
( '2023-05-01', 'P000001', 'p_anomala', 'Ipertensione di Grado 3 grave'),
( '2023-05-06', 'P000001', 'no_segue', null);

create table controlli_fatti (
    giorno date primary key
);


















-- DB
-- MEDICO(ID, NOME, COGNOME, MAIL, AMBULATORIO, PSW)
-- PAZIENTE(ID, NOME, COGNOME, MAIL, FATT_RISC, ID_MED, PSW)
-- RESPONSABILE(ID, NOME, COGNOME, MAIL, UFFICIO, PSW)
-- DATI_GIOR(GIORNO, ID_PAZ, PMIN, PMAX, SINTOMI, ASS_CORR, ORA)
-- TER(FARMACO, ID_PAZ, QTAXDOSE, NDOSI, IND*, TIPO,  INIZIO, FINE)
-- ASSUNZIONE(ORA, ID_PAZ, GIORNO, FARMACO)
-- PATOLOGIA(NOME, ID_PAZ, TIPO, INIZIO, FINE*)
-- SEGNALAZIONE(COD, DATA, ID_PAZ, ID_MED, TIPO, GRAVITA*, NOME_PAT_CONC*, INZIO_PAT_CONC*, FARMACO_CONC*, QTAXDOSE*, NDOSI*, IND*)


-- QUERY DI RICERCA
-- select p.nome, m.nome
-- from paziente as p
--     join medico as m on(p.id_med = m.id);

-- select p.nome, dg.pmax, dg.pmin, dg.giorno
-- from paziente as p
-- 	join dati_giornalieri as dg on(p.id = dg.id_paz)
-- order by dg.giorno

-- select p.nome, t.farmaco
-- from Paziente as P
--     join terapia as t on(p.id = t.id_paz);
































-- DB
-- MEDICO(ID, NOME, COGNOME, MAIL, AMBULATORIO, PSW)
-- PAZIENTE(ID, NOME, COGNOME, MAIL, FATT_RISC, ID_MED, PSW)
-- RESPONSABILE(ID, NOME, COGNOME, MAIL, UFFICIO, PSW)
-- DATI_GIOR(GIORNO, ID_PAZ, PMIN, PMAX, SINTOMI, ASS_CORR, ORA)
-- TER(FARMACO, ID_PAZ, QTAXDOSE, NDOSI, IND*, TIPO,  INIZIO, FINE)
-- ASSUNZIONE(ORA, ID_PAZ, GIORNO, FARMACO)
-- PATOLOGIA(NOME, ID_PAZ, TIPO, INIZIO, FINE*)
-- SEGNALAZIONE(COD, DATA, ID_PAZ, ID_MED, TIPO, GRAVITA*, NOME_PAT_CONC*, INZIO_PAT_CONC*, FARMACO_CONC*, QTAXDOSE*, NDOSI*, IND*)


-- QUERY DI RICERCA
-- select p.nome, m.nome
-- from paziente as p
--     join medico as m on(p.id_med = m.id);

-- select p.nome, dg.pmax, dg.pmin, dg.giorno
-- from paziente as p
-- 	join dati_giornalieri as dg on(p.id = dg.id_paz)
-- order by dg.giorno

-- select p.nome, t.farmaco
-- from Paziente as P
--     join terapia as t on(p.id = t.id_paz);











