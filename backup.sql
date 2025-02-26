--
-- PostgreSQL database dump
--

-- Dumped from database version 17.3
-- Dumped by pg_dump version 17.3

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
-- SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: use_cases; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.use_cases (
    id integer NOT NULL,
    title character varying NOT NULL,
    short_description character varying NOT NULL,
    full_description character varying,
    institution character varying NOT NULL,
    ai_technologies character varying[],
    contact character varying,
    url character varying
);


--
-- Name: use_cases_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.use_cases_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: use_cases_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.use_cases_id_seq OWNED BY public.use_cases.id;


--
-- Name: use_cases id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.use_cases ALTER COLUMN id SET DEFAULT nextval('public.use_cases_id_seq'::regclass);


--
-- Data for Name: use_cases; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.use_cases (id, title, short_description, full_description, institution, ai_technologies, contact, url) FROM stdin;
1	Enhancing blended learning through AI-driven strategies	Coleg Gwent, Cardiff and Vale College, and Coleg y Cymoedd have collaborated to develop a toolkit for AI-driven blended learning, supported by the Welsh Government. This project enhances teaching and learning experiences by promoting activity-based curricula and innovative pedagogical strategies.	A Toolkit for AI-Driven Blended Learning\nThe Project\nColeg Gwent, Cardiff and Vale College, and Coleg y Cymoedd have worked together to produce a toolkit for AI-driven blended learning, as part of a wider project supported by the Welsh Government. Rooted in the principles of blended learning, the project aims to enhance teaching and learning experiences by promoting activity-based curricula and innovative pedagogical strategies.\n\nDevelopment and Approach\nThe AI Toolkit aligns with Diana Laurillard’s six learning types—acquisition, inquiry, practice, production, discussion, and collaboration—which emphasise the benefits of activity-based curricular.\nTo facilitate the use of GenAI, the toolkit introduces prompt frameworks such as:\n\nSAFE: Setup, Action, Format, Examples\nRTF: Role, Task, Format\nAPE: Action, Purpose, Expectations\nThese frameworks guide educators in crafting prompts that leverage AI’s capabilities effectively while maintaining clarity and purpose in its application.\n\nBlended Learning Expert Bot\nAs part of the project, Coleg Gwent has created their own bot – Blended Learning Expert – by customising their own GPT.\n\nThe bot can be accessed via ChatGPT (on ChatGPT Plus accounts you can explore customised GPTs, whose functionality is tailored towards specific tasks). It is used by teachers to guide them in how to utilise AI purposively in order to achieve engaging blended learning environments.\n\nJisc’s AI team used Blended Learning Expert to create a blended learning plan for a specific unit of a Level 3 Business studies course. It responded by giving me a comprehensive six-week plan that was aligned with Universal Design for Learning (UDL) principles and Diana Laurillard’s six learning types (Acquisition, Collaboration, Discussion, Investigation, Practice, and Production).\n\nThe plan detailed session-by-session activities that blended in-person and digital tools, including Canva and Excel. Each session mapped to the unit’s objectives, progressively guiding students through understanding event management concepts, planning and executing a small-scale event, and evaluating its success. It also incorporated formative and summative assessment opportunities at appropriate junctures.	Coleg Gwent, Cardiff and Vale College, and Coleg y Cymoedd	{LLM}	info@coleggwent.ac.uk	https://hwb.gov.wales/repository/resource/a242f4d1-2008-4724-8677-9810e09f85a1/overview
2	string	string	string	string	{string,string2,string3}	string	string
4	string	string	string	string	{string}	string	string
\.


--
-- Name: use_cases_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.use_cases_id_seq', 4, true);


--
-- Name: use_cases use_cases_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.use_cases
    ADD CONSTRAINT use_cases_pkey PRIMARY KEY (id);


--
-- Name: ix_use_cases_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_use_cases_id ON public.use_cases USING btree (id);


--
-- PostgreSQL database dump complete
--

