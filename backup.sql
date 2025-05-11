--
-- PostgreSQL database dump
--

-- Dumped from database version 17.3
-- Dumped by pg_dump version 17.3

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
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
-- Name: ai_technology; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ai_technology (
    id integer NOT NULL,
    name character varying NOT NULL
);


ALTER TABLE public.ai_technology OWNER TO postgres;

--
-- Name: ai_technology_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.ai_technology_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.ai_technology_id_seq OWNER TO postgres;

--
-- Name: ai_technology_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.ai_technology_id_seq OWNED BY public.ai_technology.id;


--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO postgres;

--
-- Name: institutions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.institutions (
    id integer NOT NULL,
    name character varying NOT NULL,
    country character varying DEFAULT 'Unknown'::character varying NOT NULL,
    city character varying DEFAULT 'Unknown'::character varying NOT NULL,
    state character varying DEFAULT 'Unknown'::character varying NOT NULL,
    latitude double precision DEFAULT '0'::double precision NOT NULL,
    longitude double precision DEFAULT '0'::double precision NOT NULL
);


ALTER TABLE public.institutions OWNER TO postgres;

--
-- Name: institutions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.institutions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.institutions_id_seq OWNER TO postgres;

--
-- Name: institutions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.institutions_id_seq OWNED BY public.institutions.id;


--
-- Name: project_ai_technology; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.project_ai_technology (
    project_id integer NOT NULL,
    ai_technology_id integer NOT NULL
);


ALTER TABLE public.project_ai_technology OWNER TO postgres;

--
-- Name: projects; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.projects (
    id integer NOT NULL,
    title character varying NOT NULL,
    short_description character varying NOT NULL,
    full_description json NOT NULL,
    contact character varying,
    url character varying,
    logo_filename character varying,
    status character varying DEFAULT 'pending'::character varying NOT NULL,
    date_created timestamp without time zone DEFAULT CURRENT_DATE,
    project_initiation_date date,
    institution_id integer NOT NULL,
    submitted_by integer NOT NULL
);


ALTER TABLE public.projects OWNER TO postgres;

--
-- Name: use_cases_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.use_cases_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.use_cases_id_seq OWNER TO postgres;

--
-- Name: use_cases_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.use_cases_id_seq OWNED BY public.projects.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id integer NOT NULL,
    username character varying NOT NULL,
    email character varying NOT NULL,
    hashed_password character varying NOT NULL,
    role character varying NOT NULL
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_id_seq OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: ai_technology id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ai_technology ALTER COLUMN id SET DEFAULT nextval('public.ai_technology_id_seq'::regclass);


--
-- Name: institutions id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.institutions ALTER COLUMN id SET DEFAULT nextval('public.institutions_id_seq'::regclass);


--
-- Name: projects id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.projects ALTER COLUMN id SET DEFAULT nextval('public.use_cases_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: ai_technology; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ai_technology (id, name) FROM stdin;
3	Large Language Model
4	Generative AI
5	Audio Analysis
6	Neural voice
7	Computer Vision
8	Natural Language Processing (NLP)
9	Machine Learning
10	Predictive Analytics
11	Speech-to-Text
12	Real-Time Video Analytics
13	Anomaly Detection
14	Conversational AI
15	Chatbot Frameworks
16	Recommender Systems
17	Knowledge Graphs
18	Time-Series Forecasting
19	Reinforcement Learning
20	IoT Integration
21	Deep Learning
22	Semantic Analysis
23	Natural Language Understanding
24	Sentiment Analysis
25	Adaptive Learning Algorithms
26	Information Retrieval
27	Semantic Matching
28	IoT (Internet of Things)
29	Predictive Maintenance
30	Natural Language Generation
31	Adaptive Learning Systems
32	Accessibility AI
33	Text-to-Speech
34	Image Recognition
35	Natural Language Search
36	Psychometric Analysis
\.


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.alembic_version (version_num) FROM stdin;
1d88edab9c4c
\.


--
-- Data for Name: institutions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.institutions (id, name, country, city, state, latitude, longitude) FROM stdin;
1	Default Institution	Unknown	Unknown	Unknown	0	0
3	Coleg Gwent	United Kingdom	Newport	Wales	51.573534337629496	-2.9531758687782506
4	Northumbria University	United Kingdom		Newcastle upon Tyne	54.97657238038968	-1.6070451357301043
5	The Open University	United Kingdom		Buckinghamshire	52.025039581766116	-0.7082056246838564
6	Windsor Forest College Group	United Kingdom	Maidenhead	England	51.50529326436991	-0.5448821515170119
7	The MarTech Laboratory: AI in marketing education	United Kingdom		Belfast district	54.60498510720302	-5.929093607717569
8	Arden University	United Kingdom	Coventry	England	52.369910739104036	-1.4678679833046537
9	Ayrshire College	United Kingdom	Ayr	Scotland	55.620501882985664	-4.50017958642574
10	Basingstoke College of Technology	United Kingdom		Hampshire	51.264249365675546	-1.0961284549570551
\.


--
-- Data for Name: project_ai_technology; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.project_ai_technology (project_id, ai_technology_id) FROM stdin;
15	3
15	8
16	14
16	8
16	15
17	16
17	17
17	8
18	9
18	18
18	10
19	19
19	20
19	10
20	21
20	22
20	8
21	4
21	23
22	9
22	35
22	10
23	24
23	8
23	13
24	14
24	6
24	25
25	3
25	26
25	27
26	28
26	29
26	13
27	4
27	31
27	30
28	16
28	8
28	36
29	23
29	24
30	7
30	32
30	33
30	34
31	10
31	9
6	4
32	3
7	4
7	3
8	4
9	4
10	4
11	7
11	4
5	4
5	6
12	8
12	9
12	10
47	3
48	3
49	3
1	3
1	4
13	6
13	11
13	4
14	7
14	12
14	13
\.


--
-- Data for Name: projects; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.projects (id, title, short_description, full_description, contact, url, logo_filename, status, date_created, project_initiation_date, institution_id, submitted_by) FROM stdin;
7	Has developed and launched a private version of Chat GPT	The college group’s AI platform (known as Winnie) allows students and staff to benefit from ChatGPT’s functionality, whilst maintaining peace of mind that inputted data and content is not being used to train the model. Popular uses include threading lessons together, moderating marking, modelling prompts with students, and translating for admissions. Winnie is also able to provide college-specific insights, due to its access to a large repository of institutional information (securely stored in the UK). And under development is a new feature that will plug it into databases of achievement and retention data – which will enable automation of reports and emails. 	{"value": "Windsor Forest Colleges Group\\u00a0has developed an AI platform called\\u00a0Winnie AI, designed to support students and staff by leveraging the functionality of ChatGPT within a secure, private environment. The platform was created to maintain the privacy of inputted data, ensuring that content shared by users is not utilized for further training of the AI model. The system is housed in UK-based data centers, addressing concerns around data privacy and security.\\nThe main purpose of Winnie is to save people time: in and out of the classroom. Every day, it is helping teachers and admin staff conquer their to-do lists. It's proved popular for threading lessons together, helping educators create a more integrated learning experience. Additionally, it is used for moderating, grading, translating materials for admissions, and providing insights based on a comprehensive repository of institutional documents.\\nDevelopment\\nWinnie AI was built primarily on GPT-3.5, with the capability to integrate GPT-4.0 and other models like LLaMA as needed. This flexibility allows the college to adjust the AI\\u2019s capabilities in response to specific institutional needs.\\nOne of the major challenges during development was balancing the AI\\u2019s contextual awareness with its ability to provide accurate, reliable information. To address this, the development team has fine-tuned the AI to ensure the right balance of responses being contextually relevant and factually sound.\\nValue for money\\nWinnie AI has proven to be a cost-effective solution for Windsor Forest Colleges Group. The college has adopted a usage-based pricing model, which has allowed them to manage costs effectively. For example, 10,000 conversations with Winnie AI \\u2013 from across the whole college group \\u2013 cost approximately \\u00a3136. The system was developed by a small team of three people using various AI tools, demonstrating that such an initiative can be undertaken with relatively modest resources.\\nCurrent Use and Future Plans\\nCurrently, Winnie AI is used to support a variety of functions within the college, including lesson integration and grading moderation. Plans are underway to expand its capabilities by integrating achievement and retention data, which would allow for automated reporting and email communication. The institution is also exploring the potential integration of other models like LLaMA to enhance the platform further.\\nOne outstanding use of Winnie has been in ESOL, where a typically tech-averse teacher has been using it as an extra language coach. Their students have used it to read aloud, practice job interviews, mark extra work, and have been sharing successful prompts in a Google Doc. Their feedback has revealed how they have gone from using it in more dubious ways, to mastering its function as a private tutor.\\nWindsor Forest Colleges Group has also established policies and a working group to oversee the ethical use of AI within the institution. This includes addressing issues such as bias, plagiarism, and digital safety, which are incorporated into student tutorials and demonstrations on AI usage."}	AI@jisc.ac.uk		\N	approved	2025-04-05 18:49:27.832936	2024-03-05	6	3
8	With artificial Intelligence being a key driver of innovation in marketing, the MarTech Laboratory is investigating a variety of practical ways in which their students can harness AI.	The college group’s AI platform (known as Winnie) allows students and staff to benefit from ChatGPT’s functionality, whilst maintaining peace of mind that inputted data and content is not being used to train the model. Popular uses include threading lessons together, moderating marking, modelling prompts with students, and translating for admissions. Winnie is also able to provide college-specific insights, due to its access to a large repository of institutional information (securely stored in the UK). And under development is a new feature that will plug it into databases of achievement and retention data – which will enable automation of reports and emails.	{"value": "The MarTech Laboratory: AI in marketing education\\nExploring the intersection of marketing and advanced technologies, the MarTech Laboratory is a joint project led by Ulster University and Liverpool John Moores University.\\nWith artificial intelligence being a key driver of innovation in marketing, the MarTech Laboratory is investigating a variety of practical ways in which their students can harness AI. The use cases of AI in this domain include:\\n* \\t\\tPersonalised marketing, where customers see messaging that is tailored to their interests\\n* \\t\\tPredictive analytics, which allows future trends to be forecasted based on past patterns\\n* \\t\\tChatbots and virtual assistants, to provide users with attentive, on-demand support\\n* \\t\\tReal-time social media analysis, to understand present trends and make decisions accordingly\\n* \\t\\tMarket research, where generative AI is used to conduct initial research into a particular market\\nMarTech Laboratory\\u2019s work centers around their\\u00a0#6SCommunity: Student-led, Specialist-supported, seeking to enable Startups, Social Enterprises, Sustainability-focused, and Social good projects. By working with a wide range of stakeholders, they are able to spread cutting-edge practices to a wider range of entrepreneurs, thus adding social, environmental, and commercial value.\\nIn one project, the laboratory explored how AI can be integrated into marketing within the tourism industry. This initiative involved a series of workshops designed to educate startup professionals and entrepreneurs in Africa on how to leverage AI to support a high-level, strategic approach. These workshops covered various aspects of AI, from basic concepts to advanced applications, emphasizing its potential to transform the tourism industry.\\nThe laboratory has also conducted work to understand younger generations\\u2019 perspectives on the ethical implications of AI. One such project included a detailed survey examining various dimensions of AI ethics, such as the influence of ethical practices on the willingness to use AI tools for education, and the importance of training students how to use AI ethically. The findings from this survey highlighted that a significant portion of respondents are concerned about the ethical implications of AI. Furthermore, there was a strong consensus among respondents on the importance of educational institutions providing training on the ethical use of AI tools.\\nContinuing their focus on AI use and its implications in Higher Education, the lab is in the process of conducting focus groups to inform the development of a new survey instrument to understand student perspectives in higher education contexts, and it aims to develop a practical toolset to support better pedagogic outcomes for students and educators alike."}	ncai@jisc.ac.uk	https://martech-laboratory.com/	\N	approved	2025-04-05 18:50:26.990652	2023-03-16	7	3
9	Is using AI as an additional way of providing careers information and advice	The Arden Careers Chatbot provides an effective way of offering free careers information and advice to the public, 24/7. It draws on a range of independent resources allowing users to explore different career options and understand next steps they might need to take to progress in their career journey.	{"value": ""}	ai@jisc.ac.uk		\N	approved	2025-04-05 18:51:41.841395	2023-03-05	8	3
10	Is using AI as part of Jisc’s Chatbot Pilot	Ayrshire College is one of the four FE colleges taking part in Jisc’s Chatbot Pilot, which launched in 2021. Working alongside Jisc’s AI team, they have tailored the chatbot so that it can answer queries that Ayrshire College students are likely to benefit from the most. They have also developed the chatbot so that it can respond to queries about student funding.	{"value": ""}	marketing@ayrshire.ac.uk		\N	approved	2025-04-05 18:52:20.27531	2021-09-05	9	3
11	Is using AI to personalise learning and reduce teacher workload (CENTURY Tech, adaptive learning platform)	Basingstoke College of Technology is spearheading a human-centric approach to innovation. By using adpative learning platform, CENTURY Tech, they are equipping teachers with more time and deeper insights with which to support students. And through VR platform, Bodyswaps, they are helping students to develop the strong interpersonal skills needed to flourish in later life.	{"value": ""}	bcotdigital@staff.bcot.ac.uk	https://www.century.tech/	\N	approved	2025-04-05 18:53:03.110975	2019-11-05	10	3
5	Revolutionising university support through AI-driven conversational assistance	For more than 18 years, Norman Managed Services (known simply as "Norman"), which is part of Northumbria University, has become a valued partner to over 40 universities in the UK and internationally. Operating 24/7/365, Norman provides critical support to an estimated one million service users plus worldwide, offering assistance for everything from technical troubleshooting to routine inquiries. This firm commitment to dependable, around-the-clock assistance has established Norman as an essential resource in the sector.	{"value": "Pioneering AI Support in Higher Education: Northumbria University\\u2019s Norman Service Ember Initiative\\nFor more than 18 years, Norman Managed Services (known simply as \\"Norman\\"), which is part of Northumbria University, has become a valued partner to over 40 universities in the UK and internationally. Operating 24/7/365, Norman provides critical support to an estimated one million service users plus worldwide, offering assistance for everything from technical troubleshooting to routine inquiries. This firm commitment to dependable, around-the-clock assistance has established Norman as an essential resource in the sector.\\nNow, Norman is taking its support capabilities to a new level with the introduction of Ember, an AI-driven service built using Microsoft technology. Ember builds on over 18 years of expertise in higher education support, combined with a bold vision to make assistance more accessible, personalised, and responsive. Using cutting-edge AI, Ember aims to transform how support is delivered by turning vast knowledge resources into intuitive, conversational responses that will engage users in real time.\\nMilestones and Road to Launch\\nNorman\\u2019s team is on track to launch Ember ahead of the 2025/26 academic year. The team has been making significant progress, securing agreement with Microsoft to integrate advanced neural voice technology and designing workflows to maximise user satisfaction and elevate the overall experience. Alongside this, they have been building Ember\\u2019s technical infrastructure - establishing essential capabilities such as greeting users, managing fallback responses, and implementing interruption controls to create a seamless, intuitive interaction.\\nAdditionally, Norman\\u2019s team has invested in specialised training through the Conversation Design Institute, equipping staff to create static content and pre-defined storylines within Ember, refining the conversational flow without depending solely on Generative AI. By merging innovative technology with thoughtful conversational design, Norman is aiming to carefully perfect the user experience.\\nCombining Conversational AI and Pre-Built Stories\\nWhile AI powers much of Ember\\u2019s conversational abilities, Norman\\u2019s design philosophy underscores the importance of curated, structured responses. By combining conversational AI with pre-built stories, Ember will offer users clear, structured guidance while allowing the AI to intuitively guide them to relevant content. This balanced approach brings together the adaptability of AI-driven interactions with the consistency of static, human-designed content - a valuable blend for delivering complex support, which might otherwise feel overwhelming in a purely AI-led conversation.\\nIncreasing Inclusivity Through Advanced Voice Recognition\\nA key focus for Ember is to build an inclusive support experience that overcomes the challenges of voice recognition across the UK\\u2019s rich diversity of dialects - a frequent pain point for users. One promising approach is exploring OpenAI\\u2019s Whisper model through Azure AI Speech to deliver a voice recognition experience that feels natural, accurate, and inclusive, fostering smooth interactions regardless of the user\\u2019s accent. This commitment to accessibility lies at the heart of Ember\\u2019s mission, as Norman aims to provide genuinely equitable support for all.\\nBuilding on Microsoft\\u2019s AI and Infrastructure\\nEmber\\u2019s architecture is powered by a robust suite of Microsoft technologies, designed to deliver agility and scalability. Norman leverages Copilot Studio alongside serverless components such as Azure Functions and Azure Cosmos DB to ensure a responsive, adaptable framework. At the heart of Ember\\u2019s AI capabilities is OpenAI\\u2019s GPT-4 model, accessed via Azure OpenAI Service, enabling real-time transformation of internal knowledge into dynamic, conversational responses.\\nFuture Plans for Avatars\\nAs part of its longer-term vision, Norman is exploring the integration of avatar-based support, with a rollout anticipated for 2026. This initiative aims to create a more engaging, recognisable interface for users, strengthening brand identity by modelling the avatar after a real-life university staff member. To balance familiarity with transparency, Norman plans to incorporate clear indicators that Ember\\u2019s avatar is a digital assistant, building trust and allowing users to opt out of the avatar experience if they prefer.\\nBalancing AI Efficiency with Human Support\\nNorman recognises that while AI is powerful, it cannot fully replicate the nuance and empathy of human agents, especially in sensitive scenarios. Ember\\u2019s design incorporates this understanding, featuring automated triggers and a carefully structured architecture that smoothly transitions users to human support when required. This approach aims to ensure that users receive the right balance of AI efficiency and human empathy."}	info@northumbria.ac.uk		\N	approved	2025-04-05 18:39:49.727124	2025-01-01	4	3
13	Automated Lecture Transcription and Summarization	Real-time transcription and summarization of lectures to enhance accessibility and study efficiency.	{"value": "This project uses neural voice recognition and generative AI to convert spoken lectures into accurate transcriptions and concise summaries. The system supports multilingual input and integrates with the university\\u2019s learning management system. It helps students with disabilities and those who miss classes due to illness. One challenge was ensuring transcription accuracy in noisy lecture environments, which was addressed through advanced acoustic models and directional microphones."}	alex.hughes@university.edu	https://www.university.edu/ai-lecture-transcription	\N	approved	2025-05-06 13:51:15.44903	2023-08-15	4	4
12	AI-Powered Academic Advising System	An intelligent system to provide students with personalized academic guidance and course planning.	{"value": "The AI-Powered Academic Advising System was developed to alleviate the strain on human advisors and offer 24/7 academic support. It uses machine learning algorithms and natural language processing to analyze a student's academic records, interests, and career goals to recommend courses, alert students about prerequisites, and identify at-risk students early. The project faced initial challenges in integrating legacy academic databases, but ultimately improved student engagement and reduced dropout rates by 12%."}	jane.william@university.edu	https://www.university.edu/ai-academic-advising	\N	approved	2025-05-06 13:49:15.391921	2023-09-01	3	4
1	Enhancing blended learning through AI-driven strategies	Coleg Gwent, Cardiff and Vale College, and Coleg y Cymoedd have collaborated to develop a toolkit for AI-driven blended learning, supported by the Welsh Government. This project enhances teaching and learning experiences by promoting activity-based curricula and innovative pedagogical strategies.	{"value": "A Toolkit for AI-Driven Blended Learning\\nThe Project\\nColeg Gwent, Cardiff and Vale College, and Coleg y Cymoedd have worked together to produce a toolkit for AI-driven blended learning, as part of a wider project supported by the Welsh Government. Rooted in the principles of blended learning, the project aims to enhance teaching and learning experiences by promoting activity-based curricula and innovative pedagogical strategies.\\n\\nDevelopment and Approach\\nThe AI Toolkit aligns with Diana Laurillard’s six learning types—acquisition, inquiry, practice, production, discussion, and collaboration—which emphasise the benefits of activity-based curricular.\\nTo facilitate the use of GenAI, the toolkit introduces prompt frameworks such as:\\n\\nSAFE: Setup, Action, Format, Examples\\nRTF: Role, Task, Format\\nAPE: Action, Purpose, Expectations\\nThese frameworks guide educators in crafting prompts that leverage AI’s capabilities effectively while maintaining clarity and purpose in its application.\\n\\nBlended Learning Expert Bot\\nAs part of the project, Coleg Gwent has created their own bot – Blended Learning Expert – by customising their own GPT.\\n\\nThe bot can be accessed via ChatGPT (on ChatGPT Plus accounts you can explore customised GPTs, whose functionality is tailored towards specific tasks). It is used by teachers to guide them in how to utilise AI purposively in order to achieve engaging blended learning environments.\\n\\nJisc’s AI team used Blended Learning Expert to create a blended learning plan for a specific unit of a Level 3 Business studies course. It responded by giving me a comprehensive six-week plan that was aligned with Universal Design for Learning (UDL) principles and Diana Laurillard’s six learning types (Acquisition, Collaboration, Discussion, Investigation, Practice, and Production).\\n\\nThe plan detailed session-by-session activities that blended in-person and digital tools, including Canva and Excel. Each session mapped to the unit’s objectives, progressively guiding students through understanding event management concepts, planning and executing a small-scale event, and evaluating its success. It also incorporated formative and summative assessment opportunities at appropriate junctures."}	info@coleggwent.ac.uk	https://hwb.gov.wales/repository/resource/a242f4d1-2008-4724-8677-9810e09f85a1/overview	\N	pending	2025-03-11 00:00:00	2023-01-01	3	1
14	AI-Driven Campus Safety Surveillance	An AI-enhanced video surveillance system for real-time detection of security threats on campus.	{"value": "This initiative uses computer vision and real-time video analytics to detect unusual behavior or emergencies such as fights, fires, or unauthorized access. The AI sends instant alerts to campus security, enabling faster response times. The system has increased safety perception among students and staff. Privacy concerns were addressed through anonymized video feeds and strict data retention policies."}	david.choi@university.edu	https://www.university.edu/ai-campus-safety	\N	approved	2025-05-06 13:55:17.163673	2023-07-01	5	4
15	Smart Grading Assistant	An AI tool to automate grading and feedback generation for essays and assignments.	{"value": "Developed to support faculty in managing high volumes of student submissions, the Smart Grading Assistant leverages large language models to assess written assignments for grammar, coherence, and content relevance. Instructors can review and edit AI-generated feedback before releasing it to students. The system saves hundreds of hours per semester, though faculty training and calibration were essential to maintain grading fairness."}	lisa.tan@university.edu	https://www.university.edu/ai-grading-assistant	\N	pending	2025-05-06 13:56:34.022169	2023-10-01	6	4
16	AI Chatbot for Student Services	A 24/7 AI chatbot that answers common student queries and assists with administrative tasks.	{"value": "The university deployed an AI chatbot to handle frequent inquiries about financial aid, course registration, campus events, and IT support. It uses conversational AI and connects to real-time data sources. The chatbot reduced the volume of emails to admin staff by 40% and has over 85% accuracy in resolving issues. Continuous training based on chat logs was needed to improve its responses."}	michael.lee@university.edu	https://www.university.edu/ai-student-chatbot	\N	pending	2025-05-06 13:58:31.814182	2023-09-10	7	4
26	AI-Enabled Lab Equipment Monitoring	Smart sensors and AI monitor lab equipment usage and maintenance needs in real-time.	{"value": "By equipping lab equipment with IoT sensors and AI analytics, this system tracks machine usage, predicts maintenance, and detects abnormalities that could indicate malfunctions. It has reduced lab downtime and repair costs by 30%. Integrating different equipment models and standards posed compatibility challenges, which were overcome using standardized APIs and modular sensor kits."}	zoe.anderson@university.edu	https://www.university.edu/ai-lab-monitoring	\N	pending	2025-05-06 14:20:43.611702	2023-08-01	9	4
17	AI-Enhanced Research Paper Recommender	A personalized AI engine that recommends academic papers based on research interests.	{"value": "This tool analyzes a researcher\\u2019s previous publications, saved papers, and abstract highlights to recommend relevant new research. Using embeddings and citation graphs, the system offers weekly suggestions tailored to ongoing projects. It increased research productivity and interdisciplinary discovery. The challenge was filtering out low-quality or irrelevant suggestions, tackled by adding peer-review status filters."}	emily.roberts@university.edu	https://www.university.edu/ai-research-recommender	\N	pending	2025-05-06 14:00:02.011018	2023-09-05	8	4
18	Predictive Enrollment Analytics	Forecasting course demand and enrollment trends using AI-driven models.	{"value": "To support academic planning and resource allocation, this system uses historical data, demographic trends, and student interest patterns to predict course enrollment. It helps departments manage capacity and faculty workloads. Implemented with machine learning models and time-series forecasting, it has improved scheduling efficiency and reduced class overflows. Accuracy depends heavily on data freshness and completeness."}	steven.khan@university.edu	https://www.university.edu/ai-enrollment-analytics	\N	pending	2025-05-06 14:02:20.754824	2023-08-20	9	4
19	AI for Campus Energy Optimization	Smart energy management system using AI to reduce electricity and heating usage.	{"value": "This project uses AI models to analyze real-time energy consumption, weather data, and occupancy rates to optimize HVAC and lighting systems. The system automatically adjusts settings across campus buildings and provides energy-saving recommendations. It led to a 15% reduction in energy costs. Key challenges included integrating with existing building infrastructure and ensuring occupant comfort."}	rachel.green@university.edu	https://www.university.edu/ai-energy-optimization	\N	pending	2025-05-06 14:04:05.400558	2023-06-01	10	4
20	Plagiarism Detection Using AI	An AI tool to detect academic dishonesty with semantic and structural analysis.	{"value": "Unlike traditional plagiarism detectors, this AI tool uses deep learning and semantic analysis to detect paraphrased or AI-generated content. It compares student submissions against internal and public databases. Results are flagged with detailed justifications for instructor review. The system has helped maintain academic integrity, although balancing detection sensitivity and false positives required fine-tuning."}	nina.morris@university.edu	https://www.university.edu/ai-plagiarism-detection	\N	pending	2025-05-06 14:07:09.152358	2023-09-01	3	4
21	AI-Generated Virtual Teaching Assistants	AI avatars assist instructors by answering routine questions and moderating forums.	{"value": "Virtual teaching assistants, powered by generative AI and natural language understanding, were introduced in large undergraduate courses to help manage discussion forums, respond to common student questions, and provide clarification on lectures. The assistants are trained on course materials and FAQs. This has reduced the burden on human TAs and improved response times. The main hurdle was ensuring the AI didn\\u2019t give incorrect or outdated answers, which was managed by regular updates."}	simon.keller@university.edu	https://www.university.edu/ai-virtual-ta	\N	pending	2025-05-06 14:10:12.866129	2023-09-10	4	4
22	AI-Optimized Library Management System	An intelligent system that automates cataloging, predicts book demand, and improves searchability in university libraries.	{"value": "This AI system enhances the traditional library experience by streamlining cataloging, digitizing rare documents, and optimizing book placement and inventory management. Machine learning algorithms predict peak demand for textbooks and automate restocking or digital acquisition. Natural language search interfaces allow students to ask complex questions like 'Find papers on renewable energy trends since 2020'. Implementation challenges included digitizing legacy collections and aligning AI suggestions with academic standards."}	olivia.ross@university.edu	https://www.university.edu/ai-library-management	\N	pending	2025-05-06 14:13:00.062124	2023-10-01	5	4
23	AI-Based Student Mental Health Support	An AI-driven platform offering mental health assessments and support recommendations for students.	{"value": "This project uses AI to detect early signs of mental health issues in students through sentiment analysis of text inputs, chat logs, and usage patterns on digital platforms. The system can recommend counseling sessions, stress management resources, or direct students to emergency support when needed. Developed in collaboration with health professionals, it emphasizes privacy and ethical data use. Challenges included avoiding false positives and ensuring student trust in the system."}	harper.young@university.edu	https://www.university.edu/ai-mental-health	\N	pending	2025-05-06 14:14:15.926357	2023-09-01	6	4
24	AI-Enhanced Foreign Language Tutoring	A conversational AI tutor that helps students practice speaking and writing in multiple languages.	{"value": "This AI tool serves as a virtual language partner, capable of simulating natural conversations in over 15 languages. It provides instant corrections, cultural context, and pronunciation feedback using neural voice technology. The system adapts to the user\\u2019s proficiency level and learning speed. It has significantly improved speaking confidence among students. One challenge was ensuring culturally appropriate and region-specific feedback, which required localization efforts."}	liam.patel@university.edu	https://www.university.edu/ai-language-tutor	\N	pending	2025-05-06 14:15:30.997744	2023-08-10	7	4
25	AI-Backed Research Grant Assistant	An AI tool that helps researchers find relevant funding opportunities and draft proposals.	{"value": "This system scans thousands of funding databases and uses AI to match researchers with suitable grant opportunities based on keywords, research history, and deadlines. It also suggests language and structural improvements for grant proposals. Researchers reported saving significant time during application season. Ensuring data accuracy across fast-changing funding portals was the main technical hurdle."}	ethan.ramos@university.edu	https://www.university.edu/ai-grant-assistant	\N	pending	2025-05-06 14:18:51.588689	2023-07-01	8	4
27	AI for Adaptive Exam Generation	A system that automatically generates personalized exams based on student progress and learning gaps.	{"value": "This tool analyzes each student\\u2019s coursework and performance to generate customized quizzes and exams that target their specific weak areas. Powered by generative AI and mastery models, it ensures students receive fair yet challenging assessments. Professors can also review and adjust generated content. Ensuring question diversity and alignment with learning outcomes was key to maintaining academic rigor."}	mia.bennett@university.edu	https://www.university.edu/ai-exam-generator	\N	pending	2025-05-06 14:22:05.27636	2023-09-01	10	4
28	AI Career Path Recommender	A personalized AI system that helps students explore career options based on their skills and preferences.	{"value": "Using psychometric analysis, academic records, and personality profiling, this AI system recommends career paths, internships, and certifications. It connects with labor market data to show job availability and trends. Students receive interactive dashboards and guidance on building relevant skills. Privacy and consent for data collection were addressed through opt-in systems and anonymized data usage."}	jacob.morris@university.edu	https://www.university.edu/ai-career-recommender	\N	pending	2025-05-06 14:31:28.098374	2023-09-05	3	4
29	AI-Facilitated Peer Review for Class Projects	An AI system that assists in managing and evaluating peer feedback in collaborative projects.	{"value": "Designed to improve the quality and fairness of peer feedback, this tool uses AI to analyze reviews for tone, relevance, and bias. It guides students to write constructive comments and can auto-score feedback quality. Professors gain insight into team dynamics and participation levels. The challenge was calibrating the AI to cultural differences in feedback tone."}	ava.singh@university.edu	https://www.university.edu/ai-peer-review	\N	pending	2025-05-06 14:33:02.522267	2023-10-01	4	4
30	AI Support for Inclusive Learning Design	AI helps faculty design accessible and inclusive course content for diverse learners.	{"value": "This project uses AI to assess course materials for accessibility compliance (e.g., font size, color contrast), generate captions for videos, and offer suggestions to make content more inclusive for neurodiverse and disabled students. It also simulates how content appears to individuals with visual or cognitive impairments. The initiative aligns with university inclusion goals and has received positive feedback from accessibility offices."}	noah.james@university.edu	https://www.university.edu/ai-inclusive-learning	\N	pending	2025-05-06 14:34:49.205489	2023-09-15	5	4
31	AI-Powered Student Retention Dashboard	A predictive analytics platform that identifies students at risk of dropping out.	{"value": "By analyzing attendance, grades, engagement metrics, and socioeconomic factors, this AI tool predicts student attrition risk and triggers alerts for early intervention. Advisors and faculty use the dashboard to offer timely academic or mental health support. The model has increased first-year retention by 9%. Ensuring equity in predictions was a key focus, with regular audits for algorithmic bias."}	charlotte.baker@university.edu	https://www.university.edu/ai-retention-dashboard	\N	pending	2025-05-06 14:36:10.416147	2023-08-01	6	4
6	Evaluated the robustness of various assessment types against generative AI disruptions	The Open University (OU) has conducted a pilot to evaluate the robustness of various assessment methods in the face of generative AI disruptions. The study examined 17 different types of assessments, including traditional and innovative formats like infographics and role-plays. The project, funded by the NCFE Assessment Innovation Fund, aimed to identify assessment methods that maintain academic integrity when AI is involved.	{"value": "Researching robust modes of assessment that maintain academic integrity in the era of AI\\nSpurred by the disruptive impacts generative AI is having on remote assessments, The Open University (The OU) has conducted a pilot to evaluate how robust different methods of assessment are to AI. As part of the project, The OU examined 17 assessment types, including traditional and innovative formats such as infographics and role-plays. Funded by the NCFE Assessment Innovation Fund, the project has now been completed and\\u00a0its findings\\u00a0have been published.\\nKey findings\\nThe two methods of assessment that were found to be most robust to generative AI were:\\n* \\t\\tRole play scenarios, that required learners to apply their learning in realistic situations\\n* \\t\\tReflective tasks, where learners had to draw upon concrete examples from a piece of work\\nFor these assessment types, generative AI performed less well in terms of grades achieved, human markers found it easier to detect AI-generated responses, and there were fewer false positives (cases where learner-created answers were mistaken for AI-generated responses).\\nMeanwhile, the researchers found that as the level of study rose, AI-generated responses achieved lower grades.\\nThat said, AI-generated responses still achieved passing marks in 58 out of 59 assessments. And while training for markers on how to detect AI written content did increase the rate at which AI generated responses were identified, it also increased the rate of false positives.\\nRecommendations\\nThe project team recommended that assessment redesign should be prioritised over increased training in detecting AI, that generative AI skills development for staff and students is put in place, and amendments to the academic conduct process are made when generative AI hallmarks are identified. For more details of these recommendations, please read\\u00a0the executive summary."}		https://web.archive.org/web/20241220004022/https://www.ncfe.org.uk/help-shape-the-future-of-learning-and-assessment/aif-pilots/the-open-university/	\N	approved	2025-04-05 18:48:20.808568	2025-03-03	5	3
32	test	test	{"value": "test"}			\N	rejected	2025-05-06 18:10:42.641349	2020-01-01	1	3
47	a	1	{"value": ""}			\N	rejected	2025-05-07 18:09:28.929599	1111-11-11	1	3
48	q	q	{"value": ""}			\N	rejected	2025-05-07 18:40:45.75167	0001-01-01	1	3
49	qa	qa	{"value": ""}			\N	rejected	2025-05-07 18:44:36.523891	0001-01-01	1	3
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, username, email, hashed_password, role) FROM stdin;
1	admin	admin@example.com	placeholder	admin
2	string	string@gmail.com	$2b$12$KQBsPH1p2OApOgJNRLtNPe7Ce1P/X..iXB1YEcmZI/fscki08aa4C	user
3	test	test@test.com	$2b$12$myX6saHqTTXdscYkPHkPd.lBTSW5Gt79r1dOuy4KDUCoK6r5Imed6	admin
4	user	user@user.com	$2b$12$1Yy5QCW2xVjYM17Dy3IKZurnvFRLBawnh0g2gqTEUrCn3bYJTkeeu	user
\.


--
-- Name: ai_technology_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.ai_technology_id_seq', 36, true);


--
-- Name: institutions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.institutions_id_seq', 10, true);


--
-- Name: use_cases_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.use_cases_id_seq', 49, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_seq', 4, true);


--
-- Name: ai_technology ai_technology_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ai_technology
    ADD CONSTRAINT ai_technology_name_key UNIQUE (name);


--
-- Name: ai_technology ai_technology_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ai_technology
    ADD CONSTRAINT ai_technology_pkey PRIMARY KEY (id);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: institutions institutions_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.institutions
    ADD CONSTRAINT institutions_name_key UNIQUE (name);


--
-- Name: institutions institutions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.institutions
    ADD CONSTRAINT institutions_pkey PRIMARY KEY (id);


--
-- Name: projects uq_use_cases_title; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.projects
    ADD CONSTRAINT uq_use_cases_title UNIQUE (title);


--
-- Name: project_ai_technology use_case_ai_technology_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.project_ai_technology
    ADD CONSTRAINT use_case_ai_technology_pkey PRIMARY KEY (project_id, ai_technology_id);


--
-- Name: projects use_cases_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.projects
    ADD CONSTRAINT use_cases_pkey PRIMARY KEY (id);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- Name: ix_ai_technology_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_ai_technology_id ON public.ai_technology USING btree (id);


--
-- Name: ix_institutions_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_institutions_id ON public.institutions USING btree (id);


--
-- Name: ix_use_cases_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_use_cases_id ON public.projects USING btree (id);


--
-- Name: ix_users_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_users_id ON public.users USING btree (id);


--
-- Name: project_ai_technology use_case_ai_technology_ai_technology_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.project_ai_technology
    ADD CONSTRAINT use_case_ai_technology_ai_technology_id_fkey FOREIGN KEY (ai_technology_id) REFERENCES public.ai_technology(id);


--
-- Name: project_ai_technology use_case_ai_technology_use_case_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.project_ai_technology
    ADD CONSTRAINT use_case_ai_technology_use_case_id_fkey FOREIGN KEY (project_id) REFERENCES public.projects(id);


--
-- Name: projects use_cases_institution_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.projects
    ADD CONSTRAINT use_cases_institution_id_fkey FOREIGN KEY (institution_id) REFERENCES public.institutions(id);


--
-- Name: projects use_cases_submitted_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.projects
    ADD CONSTRAINT use_cases_submitted_by_fkey FOREIGN KEY (submitted_by) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

