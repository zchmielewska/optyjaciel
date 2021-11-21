--
-- PostgreSQL database dump
--

-- Dumped from database version 10.19 (Ubuntu 10.19-0ubuntu0.18.04.1)
-- Dumped by pg_dump version 10.19 (Ubuntu 10.19-0ubuntu0.18.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: game_question; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.game_question (
    id bigint NOT NULL,
    question character varying(256) NOT NULL,
    option1 character varying(256) NOT NULL,
    option2 character varying(256) NOT NULL,
    option3 character varying(256) NOT NULL,
    option4 character varying(256) NOT NULL
);


ALTER TABLE public.game_question OWNER TO postgres;

--
-- Name: game_questionset_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.game_questionset_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.game_questionset_id_seq OWNER TO postgres;

--
-- Name: game_questionset_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.game_questionset_id_seq OWNED BY public.game_question.id;


--
-- Name: game_question id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.game_question ALTER COLUMN id SET DEFAULT nextval('public.game_questionset_id_seq'::regclass);


--
-- Data for Name: game_question; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.game_question (id, question, option1, option2, option3, option4) FROM stdin;
2	Ulubiony kolor?	czerwony	zielony	niebieski	żółty
3	Najsilniejszy superbohater?	Superman	Wonder Woman	Batman	Spider-man
5	Najbardziej wciągający serial?	przyjaciele	teoria wielkiego podrywu	gra o tron	głowa rodziny
6	Jakie masz lub chciał(a)byś mieć zwierzę?	kot	pies	rybki	papuga
7	Jaki sport uprawiasz albo oglądasz?	piłka nożna	tenis	pływanie	jazda na nartach
8	Ulubiony smak lodów?	czekoladowe	waniliowe	truskawkowe	pistacjowe
9	Gdzie najchętniej spędzasz czas?	plaża	las	miasto	góry
10	Ulubiona gra planszowa?	szachy	monopol	scrabble	jenga
1	Jaką porę roku lubisz najbardziej?	lato	jesień	zima	wiosna
4	Najsmaczniejsza potrawa?	pizza	sałatka	sushi	zupa pomidorowa
11	Jakim samochodem najchętniej byś jeździł(a)?	kabriolet	dżip	maluch	limuzyna
\.


--
-- Name: game_questionset_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.game_questionset_id_seq', 11, true);


--
-- Name: game_question game_questionset_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.game_question
    ADD CONSTRAINT game_questionset_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

