-- public.livres definition

-- Drop table

-- DROP TABLE public.livres;

CREATE TABLE public.livres (
	titre varchar NOT NULL,
	auteur varchar NOT NULL,
	genre varchar NOT NULL,
	isbn varchar NOT NULL,
	livre_id int4 NOT NULL DEFAULT nextval('books_book_id_seq'::regclass),
	CONSTRAINT livres_pk PRIMARY KEY (livre_id)
);


-- public.utilisateurs definition

-- Drop table

-- DROP TABLE public.utilisateurs;

CREATE TABLE public.utilisateurs (
	nom varchar NOT NULL,
	prenom varchar NOT NULL,
	categorie varchar NOT NULL,
	utilisateur_id int4 NOT NULL DEFAULT nextval('users_user_id_seq'::regclass),
	CONSTRAINT utilisateurs_pk PRIMARY KEY (utilisateur_id)
);


-- public.emprunts definition

-- Drop table

-- DROP TABLE public.emprunts;

CREATE TABLE public.emprunts (
	debut timestamp NULL,
	fin timestamp NULL,
	utilisateur_id int4 NOT NULL,
	livre_id int4 NOT NULL,
	emprunt_id int4 NOT NULL DEFAULT nextval('borrows_borrow_id_seq'::regclass),
	CONSTRAINT emprunts_pk PRIMARY KEY (emprunt_id),
	CONSTRAINT emprunt_fk FOREIGN KEY (livre_id) REFERENCES public.livres(livre_id),
	CONSTRAINT emprunts_fk_1 FOREIGN KEY (utilisateur_id) REFERENCES public.utilisateurs(user_id)
);