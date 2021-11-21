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

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: auth_group; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_group (
    id integer NOT NULL,
    name character varying(150) NOT NULL
);


ALTER TABLE public.auth_group OWNER TO postgres;

--
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.auth_group_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_id_seq OWNER TO postgres;

--
-- Name: auth_group_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.auth_group_id_seq OWNED BY public.auth_group.id;


--
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_group_permissions (
    id bigint NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_group_permissions OWNER TO postgres;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.auth_group_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_permissions_id_seq OWNER TO postgres;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.auth_group_permissions_id_seq OWNED BY public.auth_group_permissions.id;


--
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


ALTER TABLE public.auth_permission OWNER TO postgres;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.auth_permission_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_permission_id_seq OWNER TO postgres;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.auth_permission_id_seq OWNED BY public.auth_permission.id;


--
-- Name: auth_user; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_user (
    id integer NOT NULL,
    password character varying(128) NOT NULL,
    last_login timestamp with time zone,
    is_superuser boolean NOT NULL,
    username character varying(150) NOT NULL,
    first_name character varying(150) NOT NULL,
    last_name character varying(150) NOT NULL,
    email character varying(254) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    date_joined timestamp with time zone NOT NULL
);


ALTER TABLE public.auth_user OWNER TO postgres;

--
-- Name: auth_user_groups; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_user_groups (
    id bigint NOT NULL,
    user_id integer NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE public.auth_user_groups OWNER TO postgres;

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.auth_user_groups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_groups_id_seq OWNER TO postgres;

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.auth_user_groups_id_seq OWNED BY public.auth_user_groups.id;


--
-- Name: auth_user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.auth_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_id_seq OWNER TO postgres;

--
-- Name: auth_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.auth_user_id_seq OWNED BY public.auth_user.id;


--
-- Name: auth_user_user_permissions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_user_user_permissions (
    id bigint NOT NULL,
    user_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_user_user_permissions OWNER TO postgres;

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.auth_user_user_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_user_permissions_id_seq OWNER TO postgres;

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.auth_user_user_permissions_id_seq OWNED BY public.auth_user_user_permissions.id;


--
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id integer NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);


ALTER TABLE public.django_admin_log OWNER TO postgres;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.django_admin_log_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_admin_log_id_seq OWNER TO postgres;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.django_admin_log_id_seq OWNED BY public.django_admin_log.id;


--
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


ALTER TABLE public.django_content_type OWNER TO postgres;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.django_content_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_content_type_id_seq OWNER TO postgres;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.django_content_type_id_seq OWNED BY public.django_content_type.id;


--
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_migrations (
    id bigint NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


ALTER TABLE public.django_migrations OWNER TO postgres;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.django_migrations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_migrations_id_seq OWNER TO postgres;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.django_migrations_id_seq OWNED BY public.django_migrations.id;


--
-- Name: django_session; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


ALTER TABLE public.django_session OWNER TO postgres;

--
-- Name: game_answer; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.game_answer (
    id bigint NOT NULL,
    answer integer NOT NULL,
    user_id integer NOT NULL,
    quiz_question_id bigint NOT NULL,
    CONSTRAINT game_answer_answer_check CHECK ((answer >= 0))
);


ALTER TABLE public.game_answer OWNER TO postgres;

--
-- Name: game_answer_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.game_answer_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.game_answer_id_seq OWNER TO postgres;

--
-- Name: game_answer_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.game_answer_id_seq OWNED BY public.game_answer.id;


--
-- Name: game_match; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.game_match (
    id bigint NOT NULL,
    matched_at timestamp with time zone NOT NULL,
    matched_user_id integer,
    quiz_id bigint NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE public.game_match OWNER TO postgres;

--
-- Name: game_match_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.game_match_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.game_match_id_seq OWNER TO postgres;

--
-- Name: game_match_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.game_match_id_seq OWNED BY public.game_match.id;


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
-- Name: game_quiz; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.game_quiz (
    id bigint NOT NULL,
    year integer NOT NULL,
    week integer NOT NULL,
    CONSTRAINT game_quiz2_week_check CHECK ((week >= 0)),
    CONSTRAINT game_quiz2_year_check CHECK ((year >= 0))
);


ALTER TABLE public.game_quiz OWNER TO postgres;

--
-- Name: game_quiz2_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.game_quiz2_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.game_quiz2_id_seq OWNER TO postgres;

--
-- Name: game_quiz2_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.game_quiz2_id_seq OWNED BY public.game_quiz.id;


--
-- Name: game_quizquestion; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.game_quizquestion (
    id bigint NOT NULL,
    question_index integer NOT NULL,
    question_id bigint NOT NULL,
    quiz_id bigint NOT NULL,
    CONSTRAINT game_quizquestion_question_index_ee186f8c_check CHECK ((question_index >= 0))
);


ALTER TABLE public.game_quizquestion OWNER TO postgres;

--
-- Name: game_quizquestionset_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.game_quizquestionset_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.game_quizquestionset_id_seq OWNER TO postgres;

--
-- Name: game_quizquestionset_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.game_quizquestionset_id_seq OWNED BY public.game_quizquestion.id;


--
-- Name: game_suggestion; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.game_suggestion (
    id bigint NOT NULL,
    question character varying(256) NOT NULL,
    option1 character varying(256) NOT NULL,
    option2 character varying(256) NOT NULL,
    option3 character varying(256) NOT NULL,
    option4 character varying(256) NOT NULL,
    suggested_at timestamp with time zone NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE public.game_suggestion OWNER TO postgres;

--
-- Name: game_suggestion_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.game_suggestion_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.game_suggestion_id_seq OWNER TO postgres;

--
-- Name: game_suggestion_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.game_suggestion_id_seq OWNED BY public.game_suggestion.id;


--
-- Name: auth_group id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group ALTER COLUMN id SET DEFAULT nextval('public.auth_group_id_seq'::regclass);


--
-- Name: auth_group_permissions id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions ALTER COLUMN id SET DEFAULT nextval('public.auth_group_permissions_id_seq'::regclass);


--
-- Name: auth_permission id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission ALTER COLUMN id SET DEFAULT nextval('public.auth_permission_id_seq'::regclass);


--
-- Name: auth_user id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user ALTER COLUMN id SET DEFAULT nextval('public.auth_user_id_seq'::regclass);


--
-- Name: auth_user_groups id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_groups ALTER COLUMN id SET DEFAULT nextval('public.auth_user_groups_id_seq'::regclass);


--
-- Name: auth_user_user_permissions id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_user_permissions ALTER COLUMN id SET DEFAULT nextval('public.auth_user_user_permissions_id_seq'::regclass);


--
-- Name: django_admin_log id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log ALTER COLUMN id SET DEFAULT nextval('public.django_admin_log_id_seq'::regclass);


--
-- Name: django_content_type id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_content_type ALTER COLUMN id SET DEFAULT nextval('public.django_content_type_id_seq'::regclass);


--
-- Name: django_migrations id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_migrations ALTER COLUMN id SET DEFAULT nextval('public.django_migrations_id_seq'::regclass);


--
-- Name: game_answer id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.game_answer ALTER COLUMN id SET DEFAULT nextval('public.game_answer_id_seq'::regclass);


--
-- Name: game_match id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.game_match ALTER COLUMN id SET DEFAULT nextval('public.game_match_id_seq'::regclass);


--
-- Name: game_question id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.game_question ALTER COLUMN id SET DEFAULT nextval('public.game_questionset_id_seq'::regclass);


--
-- Name: game_quiz id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.game_quiz ALTER COLUMN id SET DEFAULT nextval('public.game_quiz2_id_seq'::regclass);


--
-- Name: game_quizquestion id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.game_quizquestion ALTER COLUMN id SET DEFAULT nextval('public.game_quizquestionset_id_seq'::regclass);


--
-- Name: game_suggestion id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.game_suggestion ALTER COLUMN id SET DEFAULT nextval('public.game_suggestion_id_seq'::regclass);


--
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_group (id, name) FROM stdin;
\.


--
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_group_permissions (id, group_id, permission_id) FROM stdin;
\.


--
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_permission (id, name, content_type_id, codename) FROM stdin;
1	Can add log entry	1	add_logentry
2	Can change log entry	1	change_logentry
3	Can delete log entry	1	delete_logentry
4	Can view log entry	1	view_logentry
5	Can add permission	2	add_permission
6	Can change permission	2	change_permission
7	Can delete permission	2	delete_permission
8	Can view permission	2	view_permission
9	Can add group	3	add_group
10	Can change group	3	change_group
11	Can delete group	3	delete_group
12	Can view group	3	view_group
13	Can add user	4	add_user
14	Can change user	4	change_user
15	Can delete user	4	delete_user
16	Can view user	4	view_user
17	Can add content type	5	add_contenttype
18	Can change content type	5	change_contenttype
19	Can delete content type	5	delete_contenttype
20	Can view content type	5	view_contenttype
21	Can add session	6	add_session
22	Can change session	6	change_session
23	Can delete session	6	delete_session
24	Can view session	6	view_session
25	Can add question set	7	add_questionset
26	Can change question set	7	change_questionset
27	Can delete question set	7	delete_questionset
28	Can view question set	7	view_questionset
29	Can add quiz	8	add_quiz
30	Can change quiz	8	change_quiz
31	Can delete quiz	8	delete_quiz
32	Can view quiz	8	view_quiz
33	Can add answer set	9	add_answerset
34	Can change answer set	9	change_answerset
35	Can delete answer set	9	delete_answerset
36	Can view answer set	9	view_answerset
37	Can add user	10	add_user
38	Can change user	10	change_user
39	Can delete user	10	delete_user
40	Can view user	10	view_user
41	Can add match	11	add_match
42	Can change match	11	change_match
43	Can delete match	11	delete_match
44	Can view match	11	view_match
45	Can add question set long	12	add_questionsetlong
46	Can change question set long	12	change_questionsetlong
47	Can delete question set long	12	delete_questionsetlong
48	Can view question set long	12	view_questionsetlong
49	Can add answer set long	13	add_answersetlong
50	Can change answer set long	13	change_answersetlong
51	Can delete answer set long	13	delete_answersetlong
52	Can view answer set long	13	view_answersetlong
53	Can add quiz long	14	add_quizlong
54	Can change quiz long	14	change_quizlong
55	Can delete quiz long	14	delete_quizlong
56	Can view quiz long	14	view_quizlong
57	Can add quiz item	15	add_quizitem
58	Can change quiz item	15	change_quizitem
59	Can delete quiz item	15	delete_quizitem
60	Can view quiz item	15	view_quizitem
61	Can add answer	16	add_answer
62	Can change answer	16	change_answer
63	Can delete answer	16	delete_answer
64	Can view answer	16	view_answer
65	Can add quiz2	17	add_quiz2
66	Can change quiz2	17	change_quiz2
67	Can delete quiz2	17	delete_quiz2
68	Can view quiz2	17	view_quiz2
69	Can add suggestion	18	add_suggestion
70	Can change suggestion	18	change_suggestion
71	Can delete suggestion	18	delete_suggestion
72	Can view suggestion	18	view_suggestion
73	Can add quiz question set	19	add_quizquestionset
74	Can change quiz question set	19	change_quizquestionset
75	Can delete quiz question set	19	delete_quizquestionset
76	Can view quiz question set	19	view_quizquestionset
77	Can add question	7	add_question
78	Can change question	7	change_question
79	Can delete question	7	delete_question
80	Can view question	7	view_question
81	Can add quiz question	19	add_quizquestion
82	Can change quiz question	19	change_quizquestion
83	Can delete quiz question	19	delete_quizquestion
84	Can view quiz question	19	view_quizquestion
\.


--
-- Data for Name: auth_user; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) FROM stdin;
24	pbkdf2_sha256$260000$amuuo2mApagjKAydFeqslh$2kPG+PsylPGUB679CN1MHSCofkemK9peq02Hc6ncxi8=	2021-11-20 15:10:48.649887+01	f	qqq				f	t	2021-11-20 15:10:48.421554+01
25	pbkdf2_sha256$260000$BN8CT98aCbwPBPWqGg3Ysv$yNOBE2DGSn2vV+czDSJZj0ZRouU9HaUwhuJxsl9LGlU=	\N	f	ryszardjedrys				f	t	2021-11-20 18:03:25.230562+01
26	pbkdf2_sha256$260000$ElSU3cHggnxf5iFnp82KX9$PekCFjEPwmA3prwIkgP8O41WmblTyILzkqDCx6i+Hro=	\N	f	karoljedrak				f	t	2021-11-20 18:07:39.311467+01
1	pbkdf2_sha256$260000$ZGq2MWrS3Vt7y13GptNh9e$ZdOMsHKepPvxKjTP7d6PLnWZg977KHl78p2WU9oz21k=	2021-11-20 18:23:55.708788+01	t	zuzanna				t	t	2021-10-17 20:50:56.128315+02
9	pbkdf2_sha256$260000$GjsGJwGL2ue7H0gtFgkpMr$YNx5mUoiqhXnibu+VZvmVGL2/VHom3XsvEi9QKiz/sA=	2021-11-20 18:24:27.010665+01	f	zuzanna2				f	t	2021-11-08 20:15:25.434391+01
10	pbkdf2_sha256$260000$Rap1oQh54Ayn7QlxgC2ayj$oSWAcSJ9VytF11lVtCD3CWR2YI7k8MKX8NsCAK+w/Hs=	2021-11-20 18:24:40.53203+01	f	zuzanna3				f	t	2021-11-09 08:14:18.380455+01
12	pbkdf2_sha256$260000$kAKTHmggWfjF8PWXRdNqSt$ohRhMfZblDnHGLOOgs29QH64xU4wPwycV6rACgpBkRY=	\N	f	twoszczyna				f	t	2021-11-19 09:47:02.51437+01
13	pbkdf2_sha256$260000$yVQIuKfkwTmh9O6z6id8hU$kLjYRaVept6BN0NRvN/IKT5WM752jVBRdgGMw5jzGho=	\N	f	fsoroko				f	t	2021-11-19 11:05:49.972659+01
14	pbkdf2_sha256$260000$RxIaF7fLywZui3LudBy9iA$eJOpksHe/kAxbIYXDqRnUjyk7dojoLf6bnyJAELK4LY=	\N	f	gnypkarol				f	t	2021-11-19 11:06:12.285149+01
15	pbkdf2_sha256$260000$KfhlevnjrJ5qrXTXyww5i0$iZrcSku3sqJSR+pHm0uKmsPRDwN97fs0aydSWO916wA=	\N	f	bandykjacek				f	t	2021-11-19 11:06:54.17288+01
16	pbkdf2_sha256$260000$5AKHouxJ9mH9dDZlodMWv5$vDP9BSBYVmNrLzXCOT2MDudEvs2dDq+b9bj7nvoVewA=	\N	f	jakub02				f	t	2021-11-19 11:09:02.934202+01
17	pbkdf2_sha256$260000$E0bTpSIHWhyMyI8sRfqiAS$pwWEz2WvZ8yH8ZCaLvEIoEIIJdDd4vbsbnv7Qu91VoQ=	\N	f	kozlakarkadiusz				f	t	2021-11-19 11:09:15.67288+01
18	pbkdf2_sha256$260000$CW0kBVCYznbmjSgee1IWe0$HxtCNwnPD1AZUf4SE46WZpe1gwlFakgBdWURS05acDU=	\N	f	plichmaks				f	t	2021-11-19 11:09:29.237269+01
19	pbkdf2_sha256$260000$MmeksYuIffxZeURsMHdiVf$bxY1fATfdIjtqa/qMUFXcTgjP20t/Zaz2k2Dc66yJt4=	\N	f	gaja49				f	t	2021-11-19 11:10:06.045029+01
20	pbkdf2_sha256$260000$H3lbzJ80NJnUfIY8MaR1Vk$be45+ucanqxKm6md7JMioy2i6j1km9rrwSr5RQYrShU=	\N	f	iwo39				f	t	2021-11-19 11:11:15.330202+01
21	pbkdf2_sha256$260000$eRytWYQQ0titWIM3uwnyxv$GkUvv3u3A/4Q+DHxs2xVWB8BdS3wWdPt/wzx7COufHM=	\N	f	lewiczkornel				f	t	2021-11-19 11:17:24.974431+01
22	pbkdf2_sha256$260000$iYVGUuijfWx7cFXDXD9ETe$Mzj/x3IHceWo0HCi1p5Bad9SapLAC8we2LJ+wD18IVY=	2021-11-19 13:08:10.719854+01	f	lukasz				f	t	2021-11-19 13:08:10.500051+01
23	pbkdf2_sha256$260000$DRVgNfsldUdRw89xdGvf4m$tg1031s7WwckN29NjVtsQzgR/k0rJt8QU44ymGYAcY8=	2021-11-20 09:06:47.378482+01	f	test				f	t	2021-11-20 09:06:47.051313+01
\.


--
-- Data for Name: auth_user_groups; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_user_groups (id, user_id, group_id) FROM stdin;
\.


--
-- Data for Name: auth_user_user_permissions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_user_user_permissions (id, user_id, permission_id) FROM stdin;
\.


--
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) FROM stdin;
\.


--
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_content_type (id, app_label, model) FROM stdin;
1	admin	logentry
2	auth	permission
3	auth	group
4	auth	user
5	contenttypes	contenttype
6	sessions	session
8	game	quiz
9	game	answerset
10	game	user
11	game	match
12	game	questionsetlong
13	game	answersetlong
14	game	quizlong
15	game	quizitem
16	game	answer
17	game	quiz2
18	game	suggestion
7	game	question
19	game	quizquestion
\.


--
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_migrations (id, app, name, applied) FROM stdin;
1	contenttypes	0001_initial	2021-10-16 18:25:53.613383+02
2	auth	0001_initial	2021-10-16 18:25:53.871735+02
3	admin	0001_initial	2021-10-16 18:25:53.942583+02
4	admin	0002_logentry_remove_auto_add	2021-10-16 18:25:53.968332+02
5	admin	0003_logentry_add_action_flag_choices	2021-10-16 18:25:53.987783+02
6	contenttypes	0002_remove_content_type_name	2021-10-16 18:25:54.017284+02
7	auth	0002_alter_permission_name_max_length	2021-10-16 18:25:54.03398+02
8	auth	0003_alter_user_email_max_length	2021-10-16 18:25:54.051803+02
9	auth	0004_alter_user_username_opts	2021-10-16 18:25:54.06974+02
10	auth	0005_alter_user_last_login_null	2021-10-16 18:25:54.091616+02
11	auth	0006_require_contenttypes_0002	2021-10-16 18:25:54.097533+02
12	auth	0007_alter_validators_add_error_messages	2021-10-16 18:25:54.112209+02
13	auth	0008_alter_user_username_max_length	2021-10-16 18:25:54.142506+02
14	auth	0009_alter_user_last_name_max_length	2021-10-16 18:25:54.158611+02
15	auth	0010_alter_group_name_max_length	2021-10-16 18:25:54.179411+02
16	auth	0011_update_proxy_permissions	2021-10-16 18:25:54.197339+02
17	auth	0012_alter_user_first_name_max_length	2021-10-16 18:25:54.217185+02
18	game	0001_initial	2021-10-16 18:25:54.250339+02
19	game	0002_quiz	2021-10-16 18:25:54.311002+02
20	game	0003_auto_20211016_1436	2021-10-16 18:25:54.388876+02
21	sessions	0001_initial	2021-10-16 18:25:54.450851+02
22	game	0004_auto_20211016_1827	2021-10-16 18:27:57.467609+02
23	game	0005_auto_20211016_1842	2021-10-16 18:42:36.452515+02
24	game	0006_delete_quiz	2021-10-16 18:44:54.270628+02
25	game	0007_quiz	2021-10-16 18:45:06.164694+02
26	game	0008_auto_20211017_2021	2021-10-17 20:22:23.261955+02
27	game	0009_auto_20211017_2022	2021-10-17 20:22:24.048843+02
28	game	0010_auto_20211017_2055	2021-10-17 20:55:28.140788+02
29	game	0011_auto_20211017_2104	2021-10-17 21:04:12.620065+02
30	game	0012_auto_20211017_2113	2021-10-17 21:14:06.955289+02
31	game	0013_match	2021-10-22 22:12:07.454409+02
32	game	0014_alter_quiz_unique_together	2021-10-25 20:37:27.620227+02
33	game	0015_alter_answerset_unique_together	2021-10-26 22:12:07.315274+02
34	game	0016_answersetlong_questionsetlong_quizlong	2021-10-28 22:00:40.742182+02
35	game	0017_auto_20211028_2204	2021-10-28 22:04:58.910513+02
36	game	0018_alter_answersetlong_quiz	2021-10-28 22:06:08.758297+02
37	game	0019_auto_20211028_2207	2021-10-28 22:08:10.091067+02
38	game	0020_auto_20211029_0724	2021-10-29 07:24:49.987355+02
39	game	0021_auto_20211029_0733	2021-10-29 07:33:20.369335+02
40	game	0022_auto_20211029_0754	2021-10-29 07:55:39.659819+02
41	game	0023_delete_answerset	2021-10-29 07:56:17.089298+02
42	game	0024_auto_20211029_0759	2021-10-29 07:59:26.653846+02
43	game	0025_rename_option0_questionset_option4	2021-10-29 08:09:23.274642+02
44	game	0026_alter_answer_unique_together	2021-10-29 18:52:30.233808+02
45	game	0027_alter_match_matched_at	2021-11-01 09:49:09.671772+01
46	game	0028_suggestion	2021-11-02 21:04:50.683804+01
47	game	0029_auto_20211108_1925	2021-11-08 19:27:22.98161+01
48	game	0030_auto_20211120_1501	2021-11-20 15:01:35.435314+01
49	game	0031_rename_question_set_quiz_question_sets	2021-11-20 16:42:15.275761+01
50	game	0032_auto_20211120_1642	2021-11-20 16:42:15.646383+01
\.


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_session (session_key, session_data, expire_date) FROM stdin;
tp44smdnandmelu0wnejt6c6l7jyc5ol	.eJxVjE0OwiAYBe_C2hAQgeLSvWcg3w9I1UBS2pXx7krShW7fzLyXiLCtJW49LXFmcRZaHH43BHqkOgDfod6apFbXZUY5FLnTLq-N0_Oyu38HBXr51kig0AXIGimzc6DzyWCazKSC8s7mhBQssSEDWntLPmdgVDwah0fx_gAXiDlJ:1mcBFZ:ruxKqQKYllEoZZvnds5dciA590ASZ_lBE-P06FmAh4M	2021-10-31 19:51:13.145672+01
3nxp6lo0roidoelf64m29itt1vrmc490	.eJxVjEEOwiAQRe_C2hBAoMWl-56BDDODVA1NSrsy3l1JutDte-__l4iwbyXujdc4k7gIrcTpFybAB9du6A71tkhc6rbOSfZEHrbJaSF-Xo_276BAK9-1pWyDY-9d8JZG9OCSNqB4NC5DoHPyWnUweAsZgULObLQNGhUPmMT7AwNdOF4:1moU6S:grJY2RXg3sxzn-qfArMiLYQ1PcAs9KItOHjCKjNNBG8	2021-12-04 18:24:40.538661+01
7bbnkv0p29tfl2ad6345en4ea0mbxaes	.eJxVjEEOwiAQRe_C2hBAoMWl-56BDDODVA1NSrsy3l1JutDte-__l4iwbyXujdc4k7gIrcTpFybAB9du6A71tkhc6rbOSfZEHrbJaSF-Xo_276BAK9-1pWyDY-9d8JZG9OCSNqB4NC5DoHPyWnUweAsZgULObLQNGhUPmMT7AwNdOF4:1mkLKk:XNIDMWNWOPsYdXaNtpTyV3VJrrlZ4rsPUH87i92fSRE	2021-11-23 08:14:18.585147+01
1q20oivro4889d1b0mdoheh1xq1po7ar	.eJxVjE0OwiAYRO_C2hBayp9L9z0DmcKHVA1NSrsy3t2SdKGrSd68mTfz2Lfs90qrnyO7Mscuv2xCeFJpRXyg3BcelrKt88Sbws-28nGJ9Lqd7t9BRs3H2prBCgzpSG2FkR2gLYAORAEUEnrrZOhDhBLUoHVJKCeN1tKpyD5f84c4dA:1mkrbH:1a3NP7GaPxH2HkKIWdA6ZhH3qFar-stqsw77EwjSsWI	2021-11-24 18:41:31.771459+01
4iq91nalo24otktvd0fppvc1hhruu1ne	.eJxVjEEOwiAQRe_C2hBAoMWl-56BDDODVA1NSrsy3l1JutDte-__l4iwbyXujdc4k7gIrcTpFybAB9du6A71tkhc6rbOSfZEHrbJaSF-Xo_276BAK9-1pWyDY-9d8JZG9OCSNqB4NC5DoHPyWnUweAsZgULObLQNGhUPmMT7AwNdOF4:1mo3sI:ngTiWS2F6pGSOQdJRWycM2-zAdojVdPXlMI0oomyyPo	2021-12-03 14:24:18.947484+01
\.


--
-- Data for Name: game_answer; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.game_answer (id, answer, user_id, quiz_question_id) FROM stdin;
877	4	1	11
878	1	1	12
879	4	1	13
880	1	1	14
881	2	1	15
882	1	1	16
883	1	1	17
884	1	1	18
885	4	1	19
886	2	1	20
887	2	9	11
888	3	9	12
889	4	9	13
890	3	9	14
891	4	9	15
892	1	9	16
893	1	9	17
894	3	9	18
895	4	9	19
896	2	9	20
917	1	24	11
918	1	24	12
919	1	24	13
920	1	24	14
921	3	24	15
922	3	24	16
923	1	24	17
924	3	24	18
925	1	24	19
926	3	24	20
928	4	20	11
929	1	20	12
930	2	20	13
931	2	20	14
932	1	20	15
933	1	20	16
934	3	20	17
935	3	20	18
936	3	20	19
937	4	20	20
938	4	25	11
939	3	25	12
940	4	25	13
941	2	25	14
942	2	25	15
943	1	25	16
944	4	25	17
945	2	25	18
946	1	25	19
947	1	25	20
948	3	10	11
949	3	10	12
950	3	10	13
951	1	10	14
952	3	10	15
953	2	10	16
954	1	10	17
955	2	10	18
956	2	10	19
957	3	10	20
958	3	17	11
959	2	17	12
960	4	17	13
961	1	17	14
962	1	17	15
963	1	17	16
964	2	17	17
965	3	17	18
966	2	17	19
967	4	17	20
968	3	14	11
969	4	14	12
970	4	14	13
971	1	14	14
972	1	14	15
973	3	14	16
974	1	14	17
975	4	14	18
976	3	14	19
977	4	14	20
978	4	18	11
979	4	18	12
980	3	18	13
981	1	18	14
982	2	18	15
983	3	18	16
984	4	18	17
985	2	18	18
986	3	18	19
987	1	18	20
988	1	19	11
989	3	19	12
990	3	19	13
991	1	19	14
992	2	19	15
993	1	19	16
994	4	19	17
995	1	19	18
996	3	19	19
997	3	19	20
998	2	21	11
999	2	21	12
1000	4	21	13
1001	2	21	14
1002	4	21	15
1003	3	21	16
1004	4	21	17
1005	2	21	18
1006	3	21	19
1007	3	21	20
1008	2	22	11
1009	4	22	12
1010	4	22	13
1011	2	22	14
1012	1	22	15
1013	4	22	16
1014	4	22	17
1015	3	22	18
1016	4	22	19
1017	4	22	20
1018	1	15	11
1019	4	15	12
1020	4	15	13
1021	1	15	14
1022	4	15	15
1023	1	15	16
1024	4	15	17
1025	4	15	18
1026	1	15	19
1027	2	15	20
1028	4	23	11
1029	4	23	12
1030	1	23	13
1031	1	23	14
1032	3	23	15
1033	4	23	16
1034	3	23	17
1035	1	23	18
1036	4	23	19
1037	3	23	20
1038	1	16	11
1039	1	16	12
1040	3	16	13
1041	1	16	14
1042	2	16	15
1043	3	16	16
1044	4	16	17
1045	2	16	18
1046	4	16	19
1047	2	16	20
1048	3	26	11
1049	4	26	12
1050	1	26	13
1051	1	26	14
1052	2	26	15
1053	2	26	16
1054	1	26	17
1055	4	26	18
1056	2	26	19
1057	1	26	20
1058	3	13	11
1059	4	13	12
1060	1	13	13
1061	4	13	14
1062	4	13	15
1063	4	13	16
1064	3	13	17
1065	1	13	18
1066	1	13	19
1067	2	13	20
1068	4	12	11
1069	4	12	12
1070	3	12	13
1071	3	12	14
1072	2	12	15
1073	2	12	16
1074	1	12	17
1075	3	12	18
1076	1	12	19
1077	4	12	20
1078	1	12	21
1079	1	12	22
1080	2	12	23
1081	3	12	24
1082	2	12	25
1083	3	12	26
1084	4	12	27
1085	1	12	28
1086	4	12	29
1087	2	12	30
1088	2	10	21
1089	4	10	22
1090	3	10	23
1091	3	10	24
1092	4	10	25
1093	3	10	26
1094	4	10	27
1095	3	10	28
1096	2	10	29
1097	2	10	30
1098	1	17	21
1099	4	17	22
1100	3	17	23
1101	2	17	24
1102	2	17	25
1103	1	17	26
1104	3	17	27
1105	1	17	28
1106	1	17	29
1107	3	17	30
1108	4	9	21
1109	2	9	22
1110	3	9	23
1111	1	9	24
1112	1	9	25
1113	2	9	26
1114	3	9	27
1115	4	9	28
1116	2	9	29
1117	3	9	30
1118	1	1	21
1119	3	1	22
1120	1	1	23
1121	4	1	24
1122	3	1	25
1123	3	1	26
1124	4	1	27
1125	1	1	28
1126	3	1	29
1127	4	1	30
1128	4	21	21
1129	3	21	22
1130	3	21	23
1131	3	21	24
1132	1	21	25
1133	2	21	26
1134	3	21	27
1135	3	21	28
1136	3	21	29
1137	2	21	30
1138	4	16	21
1139	3	16	22
1140	4	16	23
1141	2	16	24
1142	4	16	25
1143	4	16	26
1144	3	16	27
1145	2	16	28
1146	1	16	29
1147	2	16	30
1148	3	25	21
1149	1	25	22
1150	1	25	23
1151	4	25	24
1152	1	25	25
1153	1	25	26
1154	3	25	27
1155	1	25	28
1156	3	25	29
1157	3	25	30
1158	4	20	21
1159	4	20	22
1160	3	20	23
1161	3	20	24
1162	1	20	25
1163	2	20	26
1164	4	20	27
1165	3	20	28
1166	4	20	29
1167	3	20	30
1168	3	26	21
1169	4	26	22
1170	2	26	23
1171	2	26	24
1172	4	26	25
1173	4	26	26
1174	2	26	27
1175	3	26	28
1176	2	26	29
1177	1	26	30
1178	2	17	31
1179	4	17	32
1180	3	17	33
1181	1	17	34
1182	4	17	35
1183	1	17	36
1184	2	17	37
1185	1	17	38
1186	2	17	39
1187	2	17	40
1188	1	1	31
1189	1	1	32
1190	2	1	33
1191	3	1	34
1192	4	1	35
1193	1	1	36
1194	2	1	37
1195	4	1	38
1196	1	1	39
1197	3	1	40
1198	2	15	21
1199	3	15	22
1200	3	15	23
1201	3	15	24
1202	2	15	25
1203	1	15	26
1204	1	15	27
1205	2	15	28
1206	1	15	29
1207	4	15	30
1208	4	15	31
1209	2	15	32
1210	3	15	33
1211	2	15	34
1212	4	15	35
1213	3	15	36
1214	3	15	37
1215	1	15	38
1216	4	15	39
1217	3	15	40
1218	3	14	31
1219	2	14	32
1220	2	14	33
1221	2	14	34
1222	2	14	35
1223	1	14	36
1224	4	14	37
1225	2	14	38
1226	4	14	39
1227	3	14	40
1228	1	12	31
1229	2	12	32
1230	4	12	33
1231	3	12	34
1232	1	12	35
1233	1	12	36
1234	1	12	37
1235	1	12	38
1236	1	12	39
1237	4	12	40
1238	3	26	31
1239	2	26	32
1240	1	26	33
1241	1	26	34
1242	2	26	35
1243	4	26	36
1244	1	26	37
1245	4	26	38
1246	4	26	39
1247	1	26	40
1248	3	13	31
1249	4	13	32
1250	1	13	33
1251	3	13	34
1252	1	13	35
1253	1	13	36
1254	4	13	37
1255	3	13	38
1256	2	13	39
1257	4	13	40
1258	1	18	21
1259	1	18	22
1260	1	18	23
1261	3	18	24
1262	3	18	25
1263	2	18	26
1264	1	18	27
1265	2	18	28
1266	1	18	29
1267	3	18	30
1268	3	20	31
1269	4	20	32
1270	4	20	33
1271	2	20	34
1272	1	20	35
1273	1	20	36
1274	4	20	37
1275	1	20	38
1276	1	20	39
1277	4	20	40
1278	4	12	51
1279	4	12	52
1280	3	12	53
1281	1	12	54
1282	3	12	55
1283	4	12	56
1284	3	12	57
1285	1	12	58
1286	1	12	59
1287	1	12	60
1288	3	26	51
1289	2	26	52
1290	3	26	53
1291	2	26	54
1292	3	26	55
1293	1	26	56
1294	4	26	57
1295	3	26	58
1296	3	26	59
1297	4	26	60
1298	4	1	41
1299	4	1	42
1300	3	1	43
1301	1	1	44
1302	2	1	45
1303	3	1	46
1304	2	1	47
1305	2	1	48
1306	1	1	49
1307	2	1	50
1308	4	14	41
1309	1	14	42
1310	1	14	43
1311	1	14	44
1312	1	14	45
1313	2	14	46
1314	4	14	47
1315	1	14	48
1316	2	14	49
1317	4	14	50
1318	3	26	41
1319	1	26	42
1320	3	26	43
1321	1	26	44
1322	4	26	45
1323	3	26	46
1324	1	26	47
1325	3	26	48
1326	4	26	49
1327	1	26	50
1328	1	9	51
1329	1	9	52
1330	3	9	53
1331	1	9	54
1332	1	9	55
1333	3	9	56
1334	2	9	57
1335	3	9	58
1336	1	9	59
1337	1	9	60
1338	3	23	51
1339	1	23	52
1340	3	23	53
1341	1	23	54
1342	1	23	55
1343	3	23	56
1344	1	23	57
1345	3	23	58
1346	1	23	59
1347	2	23	60
1348	2	22	51
1349	3	22	52
1350	1	22	53
1351	4	22	54
1352	4	22	55
1353	4	22	56
1354	4	22	57
1355	1	22	58
1356	4	22	59
1357	1	22	60
1358	1	24	41
1359	1	24	42
1360	1	24	43
1361	3	24	44
1362	1	24	45
1363	2	24	46
1364	1	24	47
1365	4	24	48
1366	4	24	49
1367	3	24	50
1368	2	10	51
1369	3	10	52
1370	3	10	53
1371	2	10	54
1372	2	10	55
1373	1	10	56
1374	3	10	57
1375	3	10	58
1376	4	10	59
1377	4	10	60
1378	3	15	51
1379	2	15	52
1380	1	15	53
1381	3	15	54
1382	2	15	55
1383	3	15	56
1384	1	15	57
1385	3	15	58
1386	4	15	59
1387	1	15	60
1388	3	14	21
1389	2	14	22
1390	3	14	23
1391	4	14	24
1392	4	14	25
1393	3	14	26
1394	4	14	27
1395	4	14	28
1396	3	14	29
1397	2	14	30
1398	2	13	21
1399	4	13	22
1400	3	13	23
1401	1	13	24
1402	2	13	25
1403	2	13	26
1404	2	13	27
1405	1	13	28
1406	3	13	29
1407	4	13	30
1408	3	12	41
1409	4	12	42
1410	3	12	43
1411	3	12	44
1412	1	12	45
1413	3	12	46
1414	2	12	47
1415	3	12	48
1416	1	12	49
1417	1	12	50
1418	1	21	31
1419	4	21	32
1420	1	21	33
1421	3	21	34
1422	2	21	35
1423	3	21	36
1424	3	21	37
1425	3	21	38
1426	3	21	39
1427	1	21	40
1428	4	16	41
1429	3	16	42
1430	3	16	43
1431	4	16	44
1432	3	16	45
1433	2	16	46
1434	1	16	47
1435	2	16	48
1436	2	16	49
1437	2	16	50
1438	3	16	51
1439	3	16	52
1440	1	16	53
1441	4	16	54
1442	4	16	55
1443	3	16	56
1444	3	16	57
1445	2	16	58
1446	1	16	59
1447	4	16	60
1448	2	23	41
1449	2	23	42
1450	1	23	43
1451	3	23	44
1452	4	23	45
1453	1	23	46
1454	4	23	47
1455	4	23	48
1456	1	23	49
1457	1	23	50
1458	2	1	51
1459	4	1	52
1460	3	1	53
1461	2	1	54
1462	3	1	55
1463	3	1	56
1464	3	1	57
1465	4	1	58
1466	2	1	59
1467	2	1	60
1468	1	18	51
1469	4	18	52
1470	2	18	53
1471	1	18	54
1472	3	18	55
1473	4	18	56
1474	3	18	57
1475	2	18	58
1476	1	18	59
1477	4	18	60
1478	2	10	31
1479	1	10	32
1480	1	10	33
1481	4	10	34
1482	1	10	35
1483	4	10	36
1484	2	10	37
1485	3	10	38
1486	2	10	39
1487	1	10	40
1488	2	17	51
1489	2	17	52
1490	4	17	53
1491	2	17	54
1492	1	17	55
1493	3	17	56
1494	2	17	57
1495	3	17	58
1496	1	17	59
1497	1	17	60
1498	2	25	51
1499	2	25	52
1500	3	25	53
1501	1	25	54
1502	1	25	55
1503	4	25	56
1504	3	25	57
1505	4	25	58
1506	4	25	59
1507	1	25	60
1508	1	19	21
1509	2	19	22
1510	4	19	23
1511	3	19	24
1512	2	19	25
1513	3	19	26
1514	3	19	27
1515	4	19	28
1516	3	19	29
1517	4	19	30
1518	3	21	51
1519	4	21	52
1520	4	21	53
1521	3	21	54
1522	3	21	55
1523	2	21	56
1524	1	21	57
1525	1	21	58
1526	1	21	59
1527	3	21	60
1528	4	24	21
1529	4	24	22
1530	3	24	23
1531	2	24	24
1532	3	24	25
1533	3	24	26
1534	3	24	27
1535	2	24	28
1536	2	24	29
1537	3	24	30
1538	4	10	41
1539	1	10	42
1540	1	10	43
1541	4	10	44
1542	3	10	45
1543	2	10	46
1544	4	10	47
1545	3	10	48
1546	4	10	49
1547	3	10	50
1548	1	14	51
1549	3	14	52
1550	4	14	53
1551	4	14	54
1552	3	14	55
1553	1	14	56
1554	3	14	57
1555	1	14	58
1556	3	14	59
1557	3	14	60
1558	3	25	41
1559	3	25	42
1560	1	25	43
1561	4	25	44
1562	1	25	45
1563	1	25	46
1564	2	25	47
1565	4	25	48
1566	2	25	49
1567	1	25	50
1568	2	23	21
1569	1	23	22
1570	3	23	23
1571	4	23	24
1572	4	23	25
1573	2	23	26
1574	4	23	27
1575	2	23	28
1576	3	23	29
1577	2	23	30
\.


--
-- Data for Name: game_match; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.game_match (id, matched_at, matched_user_id, quiz_id, user_id) FROM stdin;
325	2021-11-20 17:42:57.148544+01	9	27	1
326	2021-11-20 17:42:57.151524+01	1	27	9
327	2021-11-20 17:42:57.153362+01	\N	27	24
328	2021-11-20 18:03:25.58531+01	9	27	1
329	2021-11-20 18:03:25.590831+01	1	27	9
330	2021-11-20 18:03:25.595802+01	24	27	20
331	2021-11-20 18:03:25.600765+01	20	27	24
332	2021-11-20 18:03:25.75846+01	9	27	1
333	2021-11-20 18:03:25.763802+01	1	27	9
334	2021-11-20 18:03:25.768521+01	25	27	20
335	2021-11-20 18:03:25.778446+01	\N	27	24
336	2021-11-20 18:03:25.783773+01	20	27	25
337	2021-11-20 18:03:25.946345+01	9	27	1
338	2021-11-20 18:03:25.955647+01	1	27	9
339	2021-11-20 18:03:25.960671+01	24	27	10
340	2021-11-20 18:03:25.966278+01	25	27	20
341	2021-11-20 18:03:25.97154+01	10	27	24
342	2021-11-20 18:03:25.97781+01	20	27	25
343	2021-11-20 18:03:26.180145+01	9	27	1
344	2021-11-20 18:03:26.189452+01	1	27	9
345	2021-11-20 18:03:26.195187+01	24	27	10
346	2021-11-20 18:03:26.200621+01	20	27	17
347	2021-11-20 18:03:26.205597+01	17	27	20
348	2021-11-20 18:03:26.210289+01	10	27	24
349	2021-11-20 18:03:26.215384+01	\N	27	25
350	2021-11-20 18:03:26.413553+01	9	27	1
351	2021-11-20 18:03:26.423844+01	1	27	9
352	2021-11-20 18:03:26.428431+01	24	27	10
353	2021-11-20 18:03:26.433402+01	17	27	14
354	2021-11-20 18:03:26.438652+01	14	27	17
355	2021-11-20 18:03:26.443744+01	25	27	20
356	2021-11-20 18:03:26.451437+01	10	27	24
357	2021-11-20 18:03:26.45988+01	20	27	25
358	2021-11-20 18:03:26.678561+01	9	27	1
359	2021-11-20 18:03:26.685387+01	1	27	9
360	2021-11-20 18:03:26.690462+01	24	27	10
361	2021-11-20 18:03:26.69556+01	17	27	14
362	2021-11-20 18:03:26.700715+01	14	27	17
363	2021-11-20 18:03:26.705729+01	25	27	18
364	2021-11-20 18:03:26.710873+01	\N	27	20
365	2021-11-20 18:03:26.71599+01	10	27	24
366	2021-11-20 18:03:26.721525+01	18	27	25
367	2021-11-20 18:03:26.94994+01	9	27	1
368	2021-11-20 18:03:26.957107+01	1	27	9
369	2021-11-20 18:03:26.964075+01	24	27	10
370	2021-11-20 18:03:26.969035+01	17	27	14
371	2021-11-20 18:03:26.97388+01	14	27	17
372	2021-11-20 18:03:26.987046+01	19	27	18
373	2021-11-20 18:03:26.997618+01	18	27	19
374	2021-11-20 18:03:27.005727+01	25	27	20
375	2021-11-20 18:03:27.01783+01	10	27	24
376	2021-11-20 18:03:27.023007+01	20	27	25
377	2021-11-20 18:03:27.269298+01	9	27	1
378	2021-11-20 18:03:27.276565+01	1	27	9
379	2021-11-20 18:03:27.281312+01	24	27	10
380	2021-11-20 18:03:27.286728+01	17	27	14
381	2021-11-20 18:03:27.291836+01	14	27	17
382	2021-11-20 18:03:27.297078+01	19	27	18
383	2021-11-20 18:03:27.302498+01	18	27	19
384	2021-11-20 18:03:27.309553+01	\N	27	20
385	2021-11-20 18:03:27.315094+01	25	27	21
386	2021-11-20 18:03:27.320523+01	10	27	24
387	2021-11-20 18:03:27.326502+01	21	27	25
388	2021-11-20 18:03:27.570961+01	9	27	1
389	2021-11-20 18:03:27.575787+01	1	27	9
390	2021-11-20 18:03:27.580529+01	24	27	10
391	2021-11-20 18:03:27.585606+01	17	27	14
392	2021-11-20 18:03:27.590814+01	14	27	17
393	2021-11-20 18:03:27.595694+01	19	27	18
394	2021-11-20 18:03:27.600561+01	18	27	19
395	2021-11-20 18:03:27.606532+01	22	27	20
396	2021-11-20 18:03:27.61213+01	25	27	21
397	2021-11-20 18:03:27.617607+01	20	27	22
398	2021-11-20 18:03:27.623764+01	10	27	24
399	2021-11-20 18:03:27.62819+01	21	27	25
400	2021-11-20 18:03:27.9533+01	9	27	1
401	2021-11-20 18:03:27.960522+01	1	27	9
402	2021-11-20 18:03:27.965088+01	24	27	10
403	2021-11-20 18:03:27.970094+01	17	27	14
404	2021-11-20 18:03:27.975068+01	19	27	15
405	2021-11-20 18:03:27.98183+01	14	27	17
406	2021-11-20 18:03:27.994456+01	25	27	18
407	2021-11-20 18:03:28.003436+01	15	27	19
408	2021-11-20 18:03:28.010949+01	22	27	20
409	2021-11-20 18:03:28.020048+01	\N	27	21
410	2021-11-20 18:03:28.02506+01	20	27	22
411	2021-11-20 18:03:28.03761+01	10	27	24
412	2021-11-20 18:03:28.046722+01	18	27	25
413	2021-11-20 18:03:28.357203+01	9	27	1
414	2021-11-20 18:03:28.364376+01	1	27	9
415	2021-11-20 18:03:28.374108+01	19	27	10
416	2021-11-20 18:03:28.378864+01	17	27	14
417	2021-11-20 18:03:28.383763+01	25	27	15
418	2021-11-20 18:03:28.388614+01	14	27	17
419	2021-11-20 18:03:28.393349+01	21	27	18
420	2021-11-20 18:03:28.399117+01	10	27	19
421	2021-11-20 18:03:28.406886+01	22	27	20
422	2021-11-20 18:03:28.413589+01	18	27	21
423	2021-11-20 18:03:28.419784+01	20	27	22
424	2021-11-20 18:03:28.425942+01	24	27	23
425	2021-11-20 18:03:28.431635+01	23	27	24
426	2021-11-20 18:03:28.437103+01	15	27	25
427	2021-11-20 18:09:33.773132+01	9	27	1
428	2021-11-20 18:09:33.780801+01	1	27	9
429	2021-11-20 18:09:33.78503+01	19	27	10
430	2021-11-20 18:09:33.790101+01	17	27	14
431	2021-11-20 18:09:33.795431+01	25	27	15
432	2021-11-20 18:09:33.80051+01	18	27	16
433	2021-11-20 18:09:33.805613+01	14	27	17
434	2021-11-20 18:09:33.811163+01	16	27	18
435	2021-11-20 18:09:33.816519+01	10	27	19
436	2021-11-20 18:09:33.821174+01	\N	27	20
437	2021-11-20 18:09:33.825758+01	22	27	21
438	2021-11-20 18:09:33.830519+01	21	27	22
439	2021-11-20 18:09:33.836052+01	24	27	23
440	2021-11-20 18:09:33.841524+01	23	27	24
441	2021-11-20 18:09:33.846874+01	15	27	25
442	2021-11-20 18:09:34.187941+01	9	27	1
443	2021-11-20 18:09:34.192336+01	1	27	9
444	2021-11-20 18:09:34.196669+01	26	27	10
445	2021-11-20 18:09:34.20102+01	17	27	14
446	2021-11-20 18:09:34.20877+01	19	27	15
447	2021-11-20 18:09:34.213707+01	18	27	16
448	2021-11-20 18:09:34.223846+01	14	27	17
449	2021-11-20 18:09:34.229406+01	16	27	18
450	2021-11-20 18:09:34.234754+01	15	27	19
451	2021-11-20 18:09:34.239732+01	22	27	20
452	2021-11-20 18:09:34.244711+01	25	27	21
453	2021-11-20 18:09:34.249758+01	20	27	22
454	2021-11-20 18:09:34.254936+01	24	27	23
455	2021-11-20 18:09:34.26108+01	23	27	24
456	2021-11-20 18:09:34.266253+01	21	27	25
457	2021-11-20 18:09:34.271536+01	10	27	26
458	2021-11-20 18:09:34.660182+01	9	27	1
459	2021-11-20 18:09:34.667126+01	1	27	9
460	2021-11-20 18:09:34.673572+01	26	27	10
461	2021-11-20 18:09:34.679428+01	23	27	13
462	2021-11-20 18:09:34.6857+01	17	27	14
463	2021-11-20 18:09:34.704089+01	19	27	15
464	2021-11-20 18:09:34.710691+01	18	27	16
465	2021-11-20 18:09:34.716166+01	14	27	17
466	2021-11-20 18:09:34.721347+01	16	27	18
467	2021-11-20 18:09:34.726706+01	15	27	19
468	2021-11-20 18:09:34.73349+01	22	27	20
469	2021-11-20 18:09:34.739169+01	25	27	21
470	2021-11-20 18:09:34.744697+01	20	27	22
471	2021-11-20 18:09:34.749828+01	13	27	23
472	2021-11-20 18:09:34.754673+01	\N	27	24
473	2021-11-20 18:09:34.760022+01	21	27	25
474	2021-11-20 18:09:34.766059+01	10	27	26
475	2021-11-20 18:09:35.277689+01	9	27	1
476	2021-11-20 18:09:35.284965+01	1	27	9
477	2021-11-20 18:09:35.29454+01	24	27	10
478	2021-11-20 18:09:35.29926+01	26	27	12
479	2021-11-20 18:09:35.304104+01	23	27	13
480	2021-11-20 18:09:35.30915+01	17	27	14
481	2021-11-20 18:09:35.314354+01	19	27	15
482	2021-11-20 18:09:35.319596+01	18	27	16
483	2021-11-20 18:09:35.325053+01	14	27	17
484	2021-11-20 18:09:35.330262+01	16	27	18
485	2021-11-20 18:09:35.336415+01	15	27	19
486	2021-11-20 18:09:35.341915+01	22	27	20
487	2021-11-20 18:09:35.347564+01	25	27	21
488	2021-11-20 18:09:35.352896+01	20	27	22
489	2021-11-20 18:09:35.35817+01	13	27	23
490	2021-11-20 18:09:35.363638+01	10	27	24
491	2021-11-20 18:09:35.368977+01	21	27	25
492	2021-11-20 18:09:35.375269+01	12	27	26
493	2021-11-20 18:23:08.734302+01	\N	32	12
494	2021-11-20 18:23:08.89245+01	12	32	10
495	2021-11-20 18:23:08.899764+01	10	32	12
496	2021-11-20 18:23:09.045873+01	12	32	10
497	2021-11-20 18:23:09.053226+01	10	32	12
498	2021-11-20 18:23:09.057723+01	\N	32	17
499	2021-11-20 18:23:09.211665+01	17	32	9
500	2021-11-20 18:23:09.218163+01	12	32	10
501	2021-11-20 18:23:09.229926+01	10	32	12
502	2021-11-20 18:23:09.243504+01	9	32	17
503	2021-11-20 18:23:09.415407+01	\N	32	1
504	2021-11-20 18:23:09.422333+01	17	32	9
505	2021-11-20 18:23:09.427365+01	12	32	10
506	2021-11-20 18:23:09.432631+01	10	32	12
507	2021-11-20 18:23:09.437456+01	9	32	17
508	2021-11-20 18:23:09.60366+01	17	32	1
509	2021-11-20 18:23:09.613127+01	21	32	9
510	2021-11-20 18:23:09.617316+01	12	32	10
511	2021-11-20 18:23:09.622061+01	10	32	12
512	2021-11-20 18:23:09.626904+01	1	32	17
513	2021-11-20 18:23:09.631947+01	9	32	21
514	2021-11-20 18:23:09.816459+01	\N	32	1
515	2021-11-20 18:23:09.823211+01	21	32	9
516	2021-11-20 18:23:09.827891+01	12	32	10
517	2021-11-20 18:23:09.833182+01	10	32	12
518	2021-11-20 18:23:09.838187+01	17	32	16
519	2021-11-20 18:23:09.843063+01	16	32	17
520	2021-11-20 18:23:09.848031+01	9	32	21
521	2021-11-20 18:23:10.025208+01	25	32	1
522	2021-11-20 18:23:10.032147+01	21	32	9
523	2021-11-20 18:23:10.03913+01	12	32	10
524	2021-11-20 18:23:10.044081+01	10	32	12
525	2021-11-20 18:23:10.049117+01	17	32	16
526	2021-11-20 18:23:10.056283+01	16	32	17
527	2021-11-20 18:23:10.061209+01	9	32	21
528	2021-11-20 18:23:10.066988+01	1	32	25
529	2021-11-20 18:23:10.26397+01	12	32	1
530	2021-11-20 18:23:10.268306+01	21	32	9
531	2021-11-20 18:23:10.272877+01	20	32	10
532	2021-11-20 18:23:10.277563+01	1	32	12
533	2021-11-20 18:23:10.28203+01	\N	32	16
534	2021-11-20 18:23:10.286785+01	25	32	17
535	2021-11-20 18:23:10.292675+01	10	32	20
536	2021-11-20 18:23:10.298264+01	9	32	21
537	2021-11-20 18:23:10.308665+01	17	32	25
538	2021-11-20 18:23:10.519858+01	12	32	1
539	2021-11-20 18:23:10.524354+01	20	32	9
540	2021-11-20 18:23:10.528644+01	26	32	10
541	2021-11-20 18:23:10.53392+01	1	32	12
542	2021-11-20 18:23:10.538545+01	21	32	16
543	2021-11-20 18:23:10.543879+01	25	32	17
544	2021-11-20 18:23:10.548601+01	9	32	20
545	2021-11-20 18:23:10.553486+01	16	32	21
546	2021-11-20 18:23:10.558562+01	17	32	25
547	2021-11-20 18:23:10.564218+01	10	32	26
548	2021-11-20 18:23:21.804903+01	\N	33	17
549	2021-11-20 18:23:21.971749+01	17	33	1
550	2021-11-20 18:23:21.97944+01	1	33	17
551	2021-11-20 18:23:22.192134+01	12	32	1
552	2021-11-20 18:23:22.19915+01	\N	32	9
553	2021-11-20 18:23:22.203494+01	26	32	10
554	2021-11-20 18:23:22.208609+01	1	32	12
555	2021-11-20 18:23:22.213479+01	16	32	15
556	2021-11-20 18:23:22.218823+01	15	32	16
557	2021-11-20 18:23:22.224182+01	25	32	17
558	2021-11-20 18:23:22.229803+01	21	32	20
559	2021-11-20 18:23:22.23534+01	20	32	21
560	2021-11-20 18:23:22.240517+01	17	32	25
561	2021-11-20 18:23:22.24563+01	10	32	26
562	2021-11-20 18:23:22.414918+01	17	33	1
563	2021-11-20 18:23:22.419355+01	\N	33	15
564	2021-11-20 18:23:22.423606+01	1	33	17
565	2021-11-20 18:23:22.57759+01	17	33	1
566	2021-11-20 18:23:22.582793+01	15	33	14
567	2021-11-20 18:23:22.587311+01	14	33	15
568	2021-11-20 18:23:22.591698+01	1	33	17
569	2021-11-20 18:23:22.746262+01	12	33	1
570	2021-11-20 18:23:22.753572+01	1	33	12
571	2021-11-20 18:23:22.7579+01	15	33	14
572	2021-11-20 18:23:22.763275+01	14	33	15
573	2021-11-20 18:23:22.768188+01	\N	33	17
574	2021-11-20 18:23:22.936062+01	12	33	1
575	2021-11-20 18:23:22.940616+01	1	33	12
576	2021-11-20 18:23:22.944818+01	26	33	14
577	2021-11-20 18:23:22.949063+01	17	33	15
578	2021-11-20 18:23:22.953492+01	15	33	17
579	2021-11-20 18:23:22.958185+01	14	33	26
580	2021-11-20 18:23:23.128142+01	17	33	1
581	2021-11-20 18:23:23.134895+01	13	33	12
582	2021-11-20 18:23:23.13922+01	12	33	13
583	2021-11-20 18:23:23.1435+01	15	33	14
584	2021-11-20 18:23:23.148142+01	14	33	15
585	2021-11-20 18:23:23.152729+01	1	33	17
586	2021-11-20 18:23:23.157679+01	\N	33	26
587	2021-11-20 18:23:23.397019+01	12	32	1
588	2021-11-20 18:23:23.401604+01	20	32	9
589	2021-11-20 18:23:23.406103+01	26	32	10
590	2021-11-20 18:23:23.410404+01	1	32	12
591	2021-11-20 18:23:23.41513+01	18	32	15
592	2021-11-20 18:23:23.420015+01	21	32	16
593	2021-11-20 18:23:23.428669+01	25	32	17
594	2021-11-20 18:23:23.433811+01	15	32	18
595	2021-11-20 18:23:23.43898+01	9	32	20
596	2021-11-20 18:23:23.448751+01	16	32	21
597	2021-11-20 18:23:23.454118+01	17	32	25
598	2021-11-20 18:23:23.460187+01	10	32	26
599	2021-11-20 18:23:23.638243+01	12	33	1
600	2021-11-20 18:23:23.645532+01	1	33	12
601	2021-11-20 18:23:23.651717+01	20	33	13
602	2021-11-20 18:23:23.656603+01	26	33	14
603	2021-11-20 18:23:23.66415+01	17	33	15
604	2021-11-20 18:23:23.668843+01	15	33	17
605	2021-11-20 18:23:23.673567+01	13	33	20
606	2021-11-20 18:23:23.67841+01	14	33	26
607	2021-11-20 18:23:34.965941+01	\N	35	12
608	2021-11-20 18:23:35.12456+01	26	35	12
609	2021-11-20 18:23:35.132377+01	12	35	26
610	2021-11-20 18:23:35.33894+01	\N	34	1
611	2021-11-20 18:23:35.488297+01	14	34	1
612	2021-11-20 18:23:35.495519+01	1	34	14
613	2021-11-20 18:23:35.638432+01	26	34	1
614	2021-11-20 18:23:35.647835+01	\N	34	14
615	2021-11-20 18:23:35.65381+01	1	34	26
616	2021-11-20 18:23:35.804009+01	12	35	9
617	2021-11-20 18:23:35.810951+01	9	35	12
618	2021-11-20 18:23:35.815867+01	\N	35	26
619	2021-11-20 18:23:35.964384+01	23	35	9
620	2021-11-20 18:23:35.971196+01	26	35	12
621	2021-11-20 18:23:35.975554+01	9	35	23
622	2021-11-20 18:23:35.980166+01	12	35	26
623	2021-11-20 18:23:36.15864+01	23	35	9
624	2021-11-20 18:23:36.167598+01	22	35	12
625	2021-11-20 18:23:36.174433+01	12	35	22
626	2021-11-20 18:23:36.182747+01	9	35	23
627	2021-11-20 18:23:36.191468+01	\N	35	26
628	2021-11-20 18:23:36.344069+01	26	34	1
629	2021-11-20 18:23:36.351083+01	24	34	14
630	2021-11-20 18:23:36.356028+01	14	34	24
631	2021-11-20 18:23:36.360429+01	1	34	26
632	2021-11-20 18:23:36.52359+01	23	35	9
633	2021-11-20 18:23:36.530752+01	26	35	10
634	2021-11-20 18:23:36.536132+01	22	35	12
635	2021-11-20 18:23:36.54061+01	12	35	22
636	2021-11-20 18:23:36.545054+01	9	35	23
637	2021-11-20 18:23:36.549678+01	10	35	26
638	2021-11-20 18:23:36.743564+01	23	35	9
639	2021-11-20 18:23:36.747966+01	26	35	10
640	2021-11-20 18:23:36.752596+01	22	35	12
641	2021-11-20 18:23:36.757904+01	\N	35	15
642	2021-11-20 18:23:36.765141+01	12	35	22
643	2021-11-20 18:23:36.771118+01	9	35	23
644	2021-11-20 18:23:36.776438+01	10	35	26
645	2021-11-20 18:23:37.028781+01	12	32	1
646	2021-11-20 18:23:37.036099+01	\N	32	9
647	2021-11-20 18:23:37.040702+01	14	32	10
648	2021-11-20 18:23:37.045958+01	1	32	12
649	2021-11-20 18:23:37.050564+01	10	32	14
650	2021-11-20 18:23:37.055681+01	18	32	15
651	2021-11-20 18:23:37.06103+01	26	32	16
652	2021-11-20 18:23:37.066415+01	25	32	17
653	2021-11-20 18:23:37.071654+01	15	32	18
654	2021-11-20 18:23:37.077057+01	21	32	20
655	2021-11-20 18:23:37.082702+01	20	32	21
656	2021-11-20 18:23:37.088321+01	17	32	25
657	2021-11-20 18:23:37.094038+01	16	32	26
658	2021-11-20 18:23:37.415157+01	12	32	1
659	2021-11-20 18:23:37.420343+01	25	32	9
660	2021-11-20 18:23:37.424992+01	14	32	10
661	2021-11-20 18:23:37.429553+01	1	32	12
662	2021-11-20 18:23:37.433922+01	17	32	13
663	2021-11-20 18:23:37.438458+01	10	32	14
664	2021-11-20 18:23:37.442765+01	18	32	15
665	2021-11-20 18:23:37.447005+01	26	32	16
666	2021-11-20 18:23:37.453655+01	13	32	17
667	2021-11-20 18:23:37.458054+01	15	32	18
668	2021-11-20 18:23:37.462436+01	21	32	20
669	2021-11-20 18:23:37.467058+01	20	32	21
670	2021-11-20 18:23:37.471551+01	9	32	25
671	2021-11-20 18:23:37.475999+01	16	32	26
672	2021-11-20 18:23:37.619512+01	\N	34	1
673	2021-11-20 18:23:37.626842+01	26	34	12
674	2021-11-20 18:23:37.631441+01	24	34	14
675	2021-11-20 18:23:37.64361+01	14	34	24
676	2021-11-20 18:23:37.650403+01	12	34	26
677	2021-11-20 18:23:37.858558+01	17	33	1
678	2021-11-20 18:23:37.865844+01	20	33	12
679	2021-11-20 18:23:37.870656+01	21	33	13
680	2021-11-20 18:23:37.87511+01	15	33	14
681	2021-11-20 18:23:37.880007+01	14	33	15
682	2021-11-20 18:23:37.890398+01	1	33	17
683	2021-11-20 18:23:37.900624+01	12	33	20
684	2021-11-20 18:23:37.9067+01	13	33	21
685	2021-11-20 18:23:37.912387+01	\N	33	26
686	2021-11-20 18:23:38.081869+01	16	34	1
687	2021-11-20 18:23:38.089828+01	26	34	12
688	2021-11-20 18:23:38.097586+01	24	34	14
689	2021-11-20 18:23:38.102482+01	1	34	16
690	2021-11-20 18:23:38.107527+01	14	34	24
691	2021-11-20 18:23:38.112759+01	12	34	26
692	2021-11-20 18:23:38.330175+01	23	35	9
693	2021-11-20 18:23:38.337451+01	26	35	10
694	2021-11-20 18:23:38.342761+01	22	35	12
695	2021-11-20 18:23:38.348391+01	16	35	15
696	2021-11-20 18:23:38.353744+01	15	35	16
697	2021-11-20 18:23:38.359119+01	12	35	22
698	2021-11-20 18:23:38.364255+01	9	35	23
699	2021-11-20 18:23:38.372237+01	10	35	26
700	2021-11-20 18:23:38.553759+01	16	34	1
701	2021-11-20 18:23:38.561024+01	26	34	12
702	2021-11-20 18:23:38.570297+01	24	34	14
703	2021-11-20 18:23:38.575471+01	1	34	16
704	2021-11-20 18:23:38.580598+01	\N	34	23
705	2021-11-20 18:23:38.586362+01	14	34	24
706	2021-11-20 18:23:38.595142+01	12	34	26
707	2021-11-20 18:23:38.855579+01	12	35	1
708	2021-11-20 18:23:38.862558+01	23	35	9
709	2021-11-20 18:23:38.867134+01	26	35	10
710	2021-11-20 18:23:38.872134+01	1	35	12
711	2021-11-20 18:23:38.876941+01	\N	35	15
712	2021-11-20 18:23:38.881926+01	22	35	16
713	2021-11-20 18:23:38.887037+01	16	35	22
714	2021-11-20 18:23:38.894603+01	9	35	23
715	2021-11-20 18:23:38.899983+01	10	35	26
716	2021-11-20 18:23:39.118414+01	10	35	1
717	2021-11-20 18:23:39.125707+01	23	35	9
718	2021-11-20 18:23:39.133246+01	1	35	10
719	2021-11-20 18:23:39.149102+01	18	35	12
720	2021-11-20 18:23:39.160321+01	26	35	15
721	2021-11-20 18:23:39.168815+01	22	35	16
722	2021-11-20 18:23:39.18415+01	12	35	18
723	2021-11-20 18:23:39.196898+01	16	35	22
724	2021-11-20 18:23:39.205507+01	9	35	23
725	2021-11-20 18:23:39.215216+01	15	35	26
726	2021-11-20 18:23:39.429551+01	12	33	1
727	2021-11-20 18:23:39.436666+01	17	33	10
728	2021-11-20 18:23:39.441119+01	1	33	12
729	2021-11-20 18:23:39.445561+01	20	33	13
730	2021-11-20 18:23:39.450398+01	15	33	14
731	2021-11-20 18:23:39.455409+01	14	33	15
732	2021-11-20 18:23:39.460614+01	10	33	17
733	2021-11-20 18:23:39.466915+01	13	33	20
734	2021-11-20 18:23:39.474792+01	26	33	21
735	2021-11-20 18:23:39.480247+01	21	33	26
736	2021-11-20 18:23:39.712837+01	\N	35	1
737	2021-11-20 18:23:39.717125+01	23	35	9
738	2021-11-20 18:23:39.72156+01	26	35	10
739	2021-11-20 18:23:39.72599+01	18	35	12
740	2021-11-20 18:23:39.731044+01	17	35	15
741	2021-11-20 18:23:39.73839+01	22	35	16
742	2021-11-20 18:23:39.74346+01	15	35	17
743	2021-11-20 18:23:39.749117+01	12	35	18
744	2021-11-20 18:23:39.754894+01	16	35	22
745	2021-11-20 18:23:39.76035+01	9	35	23
746	2021-11-20 18:23:39.768186+01	10	35	26
747	2021-11-20 18:23:40.027583+01	25	35	1
748	2021-11-20 18:23:40.034825+01	23	35	9
749	2021-11-20 18:23:40.039497+01	26	35	10
750	2021-11-20 18:23:40.044186+01	18	35	12
751	2021-11-20 18:23:40.051313+01	17	35	15
752	2021-11-20 18:23:40.05623+01	22	35	16
753	2021-11-20 18:23:40.061453+01	15	35	17
754	2021-11-20 18:23:40.066569+01	12	35	18
755	2021-11-20 18:23:40.07414+01	16	35	22
756	2021-11-20 18:23:40.079653+01	9	35	23
757	2021-11-20 18:23:40.085174+01	1	35	25
758	2021-11-20 18:23:40.090674+01	10	35	26
759	2021-11-20 18:23:40.399244+01	25	32	1
760	2021-11-20 18:23:40.40646+01	\N	32	9
761	2021-11-20 18:23:40.410685+01	14	32	10
762	2021-11-20 18:23:40.415079+01	19	32	12
763	2021-11-20 18:23:40.421858+01	17	32	13
764	2021-11-20 18:23:40.42681+01	10	32	14
765	2021-11-20 18:23:40.431908+01	18	32	15
766	2021-11-20 18:23:40.437586+01	26	32	16
767	2021-11-20 18:23:40.443493+01	13	32	17
768	2021-11-20 18:23:40.448745+01	15	32	18
769	2021-11-20 18:23:40.453898+01	12	32	19
770	2021-11-20 18:23:40.459706+01	21	32	20
771	2021-11-20 18:23:40.465556+01	20	32	21
772	2021-11-20 18:23:40.471243+01	1	32	25
773	2021-11-20 18:23:40.479745+01	16	32	26
774	2021-11-20 18:23:40.737709+01	25	35	1
775	2021-11-20 18:23:40.74218+01	23	35	9
776	2021-11-20 18:23:40.74674+01	26	35	10
777	2021-11-20 18:23:40.751166+01	18	35	12
778	2021-11-20 18:23:40.756149+01	17	35	15
779	2021-11-20 18:23:40.760784+01	22	35	16
780	2021-11-20 18:23:40.765768+01	15	35	17
781	2021-11-20 18:23:40.771021+01	12	35	18
782	2021-11-20 18:23:40.775586+01	\N	35	21
783	2021-11-20 18:23:40.779619+01	16	35	22
784	2021-11-20 18:23:40.783954+01	9	35	23
785	2021-11-20 18:23:40.788672+01	1	35	25
786	2021-11-20 18:23:40.793894+01	10	35	26
787	2021-11-20 18:23:41.11879+01	25	32	1
788	2021-11-20 18:23:41.126227+01	24	32	9
789	2021-11-20 18:23:41.13133+01	14	32	10
790	2021-11-20 18:23:41.136169+01	19	32	12
791	2021-11-20 18:23:41.146662+01	17	32	13
792	2021-11-20 18:23:41.157688+01	10	32	14
793	2021-11-20 18:23:41.167106+01	18	32	15
794	2021-11-20 18:23:41.175083+01	26	32	16
795	2021-11-20 18:23:41.180981+01	13	32	17
796	2021-11-20 18:23:41.189815+01	15	32	18
797	2021-11-20 18:23:41.20118+01	12	32	19
798	2021-11-20 18:23:41.209337+01	21	32	20
799	2021-11-20 18:23:41.218381+01	20	32	21
800	2021-11-20 18:23:41.225569+01	9	32	24
801	2021-11-20 18:23:41.231567+01	1	32	25
802	2021-11-20 18:23:41.236293+01	16	32	26
803	2021-11-20 18:23:41.408511+01	16	34	1
804	2021-11-20 18:23:41.41582+01	14	34	10
805	2021-11-20 18:23:41.422492+01	26	34	12
806	2021-11-20 18:23:41.427026+01	10	34	14
807	2021-11-20 18:23:41.432316+01	1	34	16
808	2021-11-20 18:23:41.439999+01	24	34	23
809	2021-11-20 18:23:41.446036+01	23	34	24
810	2021-11-20 18:23:41.452188+01	12	34	26
811	2021-11-20 18:23:41.729618+01	25	35	1
812	2021-11-20 18:23:41.734189+01	23	35	9
813	2021-11-20 18:23:41.738554+01	26	35	10
814	2021-11-20 18:23:41.743297+01	18	35	12
815	2021-11-20 18:23:41.748306+01	21	35	14
816	2021-11-20 18:23:41.755478+01	17	35	15
817	2021-11-20 18:23:41.760583+01	22	35	16
818	2021-11-20 18:23:41.766032+01	15	35	17
819	2021-11-20 18:23:41.77406+01	12	35	18
820	2021-11-20 18:23:41.7791+01	14	35	21
821	2021-11-20 18:23:41.784852+01	16	35	22
822	2021-11-20 18:23:41.790081+01	9	35	23
823	2021-11-20 18:23:41.795542+01	1	35	25
824	2021-11-20 18:23:41.800994+01	10	35	26
825	2021-11-20 18:23:42.040619+01	16	34	1
826	2021-11-20 18:23:42.047562+01	14	34	10
827	2021-11-20 18:23:42.054365+01	26	34	12
828	2021-11-20 18:23:42.059333+01	10	34	14
829	2021-11-20 18:23:42.064149+01	1	34	16
830	2021-11-20 18:23:42.069028+01	25	34	23
831	2021-11-20 18:23:42.076744+01	\N	34	24
832	2021-11-20 18:23:42.081624+01	23	34	25
833	2021-11-20 18:23:42.087608+01	12	34	26
834	2021-11-20 18:23:42.476095+01	25	32	1
835	2021-11-20 18:23:42.483079+01	24	32	9
836	2021-11-20 18:23:42.490696+01	26	32	10
837	2021-11-20 18:23:42.495305+01	19	32	12
838	2021-11-20 18:23:42.500123+01	17	32	13
839	2021-11-20 18:23:42.505175+01	23	32	14
840	2021-11-20 18:23:42.51039+01	18	32	15
841	2021-11-20 18:23:42.517763+01	\N	32	16
842	2021-11-20 18:23:42.523323+01	13	32	17
843	2021-11-20 18:23:42.52973+01	15	32	18
844	2021-11-20 18:23:42.535472+01	12	32	19
845	2021-11-20 18:23:42.541324+01	21	32	20
846	2021-11-20 18:23:42.546498+01	20	32	21
847	2021-11-20 18:23:42.551652+01	14	32	23
848	2021-11-20 18:23:42.55714+01	9	32	24
849	2021-11-20 18:23:42.562873+01	1	32	25
850	2021-11-20 18:23:42.568848+01	10	32	26
\.


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
-- Data for Name: game_quiz; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.game_quiz (id, year, week) FROM stdin;
27	2021	46
32	2021	45
33	2021	44
34	2021	43
35	2021	42
\.


--
-- Data for Name: game_quizquestion; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.game_quizquestion (id, question_index, question_id, quiz_id) FROM stdin;
11	1	10	27
12	2	7	27
13	3	5	27
14	4	8	27
15	5	3	27
16	6	2	27
17	7	4	27
18	8	6	27
19	9	1	27
20	10	9	27
21	1	11	32
22	2	2	32
23	3	8	32
24	4	10	32
25	5	9	32
26	6	4	32
27	7	3	32
28	8	7	32
29	9	6	32
30	10	1	32
31	1	9	33
32	2	11	33
33	3	7	33
34	4	2	33
35	5	4	33
36	6	1	33
37	7	6	33
38	8	5	33
39	9	3	33
40	10	8	33
41	1	10	34
42	2	9	34
43	3	8	34
44	4	4	34
45	5	11	34
46	6	7	34
47	7	1	34
48	8	3	34
49	9	6	34
50	10	5	34
51	1	9	35
52	2	8	35
53	3	11	35
54	4	7	35
55	5	4	35
56	6	3	35
57	7	1	35
58	8	5	35
59	9	10	35
60	10	6	35
\.


--
-- Data for Name: game_suggestion; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.game_suggestion (id, question, option1, option2, option3, option4, suggested_at, user_id) FROM stdin;
3	Twoje ulubione drzewo?	sosna	dąb	wierzba	brzoza	2021-11-02 21:37:03.518421+01	1
6	Jaki lubisz kolor oczu?	niebieski	brązowy	zielony	mieszany	2021-11-04 08:07:28.069832+01	1
8	Jaka jest twoj ulubiony kolor skóry?	Biały	Czarny	Azjata	Afroamerykanin	2021-11-07 09:22:36.38379+01	1
7	Którą żeńską postać z Przyjaciół lubisz najbardziej?	Phoebe	Rachel	Monica	Nie znam serialu Przyjaciele	2021-11-06 22:03:17.045817+01	1
9	Preferowany alkohol?	piwo	wino	wódka	nie piję alkoholu	2021-11-19 09:27:55.130365+01	9
10	Śniadanie na codzień to?	płatki z mlekiem	jajka i kanapki	kawa	nie jem śniadań	2021-11-19 10:04:51.458304+01	10
4	Najchętniej zakupy robię w?	galerii handlowej	małym sklepiku	targu	przez internet	2021-11-03 08:20:00.070321+01	1
5	Jaki lubisz kolor włosów?	blond	brunet(ka)	rudy	nie mam preferencji	2021-11-04 08:06:43.022807+01	1
13	Którą męską postać z Przyjaciół lubisz najbardziej?	Chandler	Ross	Joey	Nie znam serialu Przyjaciele	2021-11-19 11:49:08.476+01	1
14	Najfaniejsza rasa psa dla mnie to?	golden retriever	oczwarek niemiecki	buldog francuski	jamnik	2021-11-19 11:50:11.308+01	1
\.


--
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_group_id_seq', 1, false);


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_group_permissions_id_seq', 1, false);


--
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_permission_id_seq', 84, true);


--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_user_groups_id_seq', 1, false);


--
-- Name: auth_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_user_id_seq', 26, true);


--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_user_user_permissions_id_seq', 1, false);


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_admin_log_id_seq', 1, false);


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_content_type_id_seq', 19, true);


--
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_migrations_id_seq', 50, true);


--
-- Name: game_answer_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.game_answer_id_seq', 1577, true);


--
-- Name: game_match_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.game_match_id_seq', 850, true);


--
-- Name: game_questionset_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.game_questionset_id_seq', 11, true);


--
-- Name: game_quiz2_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.game_quiz2_id_seq', 35, true);


--
-- Name: game_quizquestionset_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.game_quizquestionset_id_seq', 60, true);


--
-- Name: game_suggestion_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.game_suggestion_id_seq', 14, true);


--
-- Name: auth_group auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- Name: auth_group_permissions auth_group_permissions_group_id_permission_id_0cd325b0_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq UNIQUE (group_id, permission_id);


--
-- Name: auth_group_permissions auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_group auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- Name: auth_permission auth_permission_content_type_id_codename_01ab375a_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq UNIQUE (content_type_id, codename);


--
-- Name: auth_permission auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups auth_user_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups auth_user_groups_user_id_group_id_94350c0c_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_group_id_94350c0c_uniq UNIQUE (user_id, group_id);


--
-- Name: auth_user auth_user_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions auth_user_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions auth_user_user_permissions_user_id_permission_id_14a6b632_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_permission_id_14a6b632_uniq UNIQUE (user_id, permission_id);


--
-- Name: auth_user auth_user_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_username_key UNIQUE (username);


--
-- Name: django_admin_log django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- Name: django_content_type django_content_type_app_label_model_76bd3d3b_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq UNIQUE (app_label, model);


--
-- Name: django_content_type django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- Name: django_migrations django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- Name: django_session django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- Name: game_answer game_answer_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.game_answer
    ADD CONSTRAINT game_answer_pkey PRIMARY KEY (id);


--
-- Name: game_answer game_answer_user_id_quiz_question_id_239f8f2b_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.game_answer
    ADD CONSTRAINT game_answer_user_id_quiz_question_id_239f8f2b_uniq UNIQUE (user_id, quiz_question_id);


--
-- Name: game_match game_match_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.game_match
    ADD CONSTRAINT game_match_pkey PRIMARY KEY (id);


--
-- Name: game_question game_questionset_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.game_question
    ADD CONSTRAINT game_questionset_pkey PRIMARY KEY (id);


--
-- Name: game_quiz game_quiz2_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.game_quiz
    ADD CONSTRAINT game_quiz2_pkey PRIMARY KEY (id);


--
-- Name: game_quiz game_quiz2_year_week_7ceb8ed9_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.game_quiz
    ADD CONSTRAINT game_quiz2_year_week_7ceb8ed9_uniq UNIQUE (year, week);


--
-- Name: game_quizquestion game_quizquestion_quiz_id_question_index_88b80ecc_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.game_quizquestion
    ADD CONSTRAINT game_quizquestion_quiz_id_question_index_88b80ecc_uniq UNIQUE (quiz_id, question_index);


--
-- Name: game_quizquestion game_quizquestionset_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.game_quizquestion
    ADD CONSTRAINT game_quizquestionset_pkey PRIMARY KEY (id);


--
-- Name: game_suggestion game_suggestion_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.game_suggestion
    ADD CONSTRAINT game_suggestion_pkey PRIMARY KEY (id);


--
-- Name: auth_group_name_a6ea08ec_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_group_name_a6ea08ec_like ON public.auth_group USING btree (name varchar_pattern_ops);


--
-- Name: auth_group_permissions_group_id_b120cbf9; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_group_permissions_group_id_b120cbf9 ON public.auth_group_permissions USING btree (group_id);


--
-- Name: auth_group_permissions_permission_id_84c5c92e; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_group_permissions_permission_id_84c5c92e ON public.auth_group_permissions USING btree (permission_id);


--
-- Name: auth_permission_content_type_id_2f476e4b; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_permission_content_type_id_2f476e4b ON public.auth_permission USING btree (content_type_id);


--
-- Name: auth_user_groups_group_id_97559544; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_user_groups_group_id_97559544 ON public.auth_user_groups USING btree (group_id);


--
-- Name: auth_user_groups_user_id_6a12ed8b; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_user_groups_user_id_6a12ed8b ON public.auth_user_groups USING btree (user_id);


--
-- Name: auth_user_user_permissions_permission_id_1fbb5f2c; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_user_user_permissions_permission_id_1fbb5f2c ON public.auth_user_user_permissions USING btree (permission_id);


--
-- Name: auth_user_user_permissions_user_id_a95ead1b; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_user_user_permissions_user_id_a95ead1b ON public.auth_user_user_permissions USING btree (user_id);


--
-- Name: auth_user_username_6821ab7c_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_user_username_6821ab7c_like ON public.auth_user USING btree (username varchar_pattern_ops);


--
-- Name: django_admin_log_content_type_id_c4bce8eb; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_admin_log_content_type_id_c4bce8eb ON public.django_admin_log USING btree (content_type_id);


--
-- Name: django_admin_log_user_id_c564eba6; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_admin_log_user_id_c564eba6 ON public.django_admin_log USING btree (user_id);


--
-- Name: django_session_expire_date_a5c62663; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_session_expire_date_a5c62663 ON public.django_session USING btree (expire_date);


--
-- Name: django_session_session_key_c0390e0f_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_session_session_key_c0390e0f_like ON public.django_session USING btree (session_key varchar_pattern_ops);


--
-- Name: game_answer_quiz_question_id_c91f74df; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX game_answer_quiz_question_id_c91f74df ON public.game_answer USING btree (quiz_question_id);


--
-- Name: game_answer_user_id_aee23c95; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX game_answer_user_id_aee23c95 ON public.game_answer USING btree (user_id);


--
-- Name: game_match_matched_user_id_024f2abb; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX game_match_matched_user_id_024f2abb ON public.game_match USING btree (matched_user_id);


--
-- Name: game_match_quiz_id_8ac06bcf; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX game_match_quiz_id_8ac06bcf ON public.game_match USING btree (quiz_id);


--
-- Name: game_match_user_id_1c2a2ef8; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX game_match_user_id_1c2a2ef8 ON public.game_match USING btree (user_id);


--
-- Name: game_quizquestionset_question_set_id_d2849d6f; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX game_quizquestionset_question_set_id_d2849d6f ON public.game_quizquestion USING btree (question_id);


--
-- Name: game_quizquestionset_quiz_id_350cf194; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX game_quizquestionset_quiz_id_350cf194 ON public.game_quizquestion USING btree (quiz_id);


--
-- Name: game_suggestion_user_id_f0aec064; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX game_suggestion_user_id_f0aec064 ON public.game_suggestion USING btree (user_id);


--
-- Name: auth_group_permissions auth_group_permissio_permission_id_84c5c92e_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions auth_group_permissions_group_id_b120cbf9_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_permission auth_permission_content_type_id_2f476e4b_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups auth_user_groups_group_id_97559544_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_group_id_97559544_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups auth_user_groups_user_id_6a12ed8b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_6a12ed8b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_content_type_id_c4bce8eb_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_user_id_c564eba6_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: game_answer game_answer_quiz_question_id_c91f74df_fk_game_quizquestion_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.game_answer
    ADD CONSTRAINT game_answer_quiz_question_id_c91f74df_fk_game_quizquestion_id FOREIGN KEY (quiz_question_id) REFERENCES public.game_quizquestion(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: game_answer game_answer_user_id_aee23c95_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.game_answer
    ADD CONSTRAINT game_answer_user_id_aee23c95_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: game_match game_match_matched_user_id_024f2abb_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.game_match
    ADD CONSTRAINT game_match_matched_user_id_024f2abb_fk_auth_user_id FOREIGN KEY (matched_user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: game_match game_match_quiz_id_8ac06bcf_fk_game_quiz_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.game_match
    ADD CONSTRAINT game_match_quiz_id_8ac06bcf_fk_game_quiz_id FOREIGN KEY (quiz_id) REFERENCES public.game_quiz(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: game_match game_match_user_id_1c2a2ef8_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.game_match
    ADD CONSTRAINT game_match_user_id_1c2a2ef8_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: game_quizquestion game_quizquestion_question_id_1b857850_fk_game_question_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.game_quizquestion
    ADD CONSTRAINT game_quizquestion_question_id_1b857850_fk_game_question_id FOREIGN KEY (question_id) REFERENCES public.game_question(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: game_quizquestion game_quizquestionset_quiz_id_350cf194_fk_game_quiz_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.game_quizquestion
    ADD CONSTRAINT game_quizquestionset_quiz_id_350cf194_fk_game_quiz_id FOREIGN KEY (quiz_id) REFERENCES public.game_quiz(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: game_suggestion game_suggestion_user_id_f0aec064_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.game_suggestion
    ADD CONSTRAINT game_suggestion_user_id_f0aec064_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- PostgreSQL database dump complete
--

