CREATE TABLE IF NOT EXISTS continents (
     continent_id INTEGER PRIMARY KEY NOT NULL,
     continent TEXT UNIQUE NOT NULL,
     continent_guid TEXT UNIQUE NOT NULL
);
CREATE TABLE IF NOT EXISTS countries(
     country_id INTEGER PRIMARY KEY NOT NULL,
     country TEXT UNIQUE NOT NULL,
     continent_id INTEGER NOT NULL,
     country_guid TEXT UNIQUE NOT NULL,
     UNIQUE (country, continent_id),
     FOREIGN KEY (continent_id) REFERENCES continents (continent_id)
);
CREATE TABLE IF NOT EXISTS genders(
     gender_id INTEGER PRIMARY KEY NOT NULL,
     gender TEXT UNIQUE NOT NULL
);
CREATE TABLE IF NOT EXISTS genres(
     genre_id INTEGER PRIMARY KEY NOT NULL,
     genre TEXT UNIQUE NOT NULL,
     genre_guid TEXT UNIQUE NOT NULL
);
CREATE TABLE IF NOT EXISTS publishers(
     publisher_id INTEGER PRIMARY KEY NOT NULL,
     publisher TEXT UNIQUE NOT NULL,
     publisher_guid TEXT UNIQUE NOT NULL
);
CREATE TABLE IF NOT EXISTS themes(
     theme_id INTEGER PRIMARY KEY NOT NULL,
     theme TEXT UNIQUE NOT NULL,
     theme_guid TEXT UNIQUE NOT NULL
);
CREATE TABLE IF NOT EXISTS authors(
     author_id INTEGER PRIMARY KEY NOT NULL,
     full_name TEXT UNIQUE NOT NULL,
     birth_year INTEGER,
     death_year INTEGER,
     gender_id INTEGER,
     country_id INTEGER,
     author_guid TEXT UNIQUE NOT NULL,
     FOREIGN KEY (country_id) REFERENCES countries (country_id),
     FOREIGN KEY (gender_id) REFERENCES genders (gender_id)
);
CREATE TABLE IF NOT EXISTS ebooks(
     ebook_id INTEGER PRIMARY KEY NOT NULL,
     title TEXT NOT NULL,
     year_of_publication INTEGER,
     publisher_id INTEGER,
     ebook_guid TEXT UNIQUE NOT NULL,
     FOREIGN KEY (publisher_id) REFERENCES publishers (publisher_id)
);
CREATE TABLE IF NOT EXISTS ebooks_authors(
     ebook_id INTEGER NOT NULL,
     author_id INTEGER NOT NULL,
     PRIMARY KEY (ebook_id, author_id),
     FOREIGN KEY (ebook_id) REFERENCES ebooks (ebook_id),
     FOREIGN KEY (author_id) REFERENCES authors (author_id)
);
CREATE TABLE IF NOT EXISTS ebooks_genres(
     ebook_id INTEGER NOT NULL,
     genre_id INTEGER NOT NULL,
     PRIMARY KEY (ebook_id, genre_id),
     FOREIGN KEY (ebook_id) REFERENCES ebooks (ebook_id),
     FOREIGN KEY (genre_id) REFERENCES genres (genre_id)
);
CREATE TABLE IF NOT EXISTS ebooks_themes(
     ebook_id INTEGER NOT NULL,
     theme_id INTEGER NOT NULL,
     PRIMARY KEY (ebook_id, theme_id),
     FOREIGN KEY (ebook_id) REFERENCES ebooks (ebook_id),
     FOREIGN KEY (theme_id) REFERENCES themes (theme_id)
);
INSERT INTO continents (continent, continent_guid) VALUES ('Europe', '389c2a17-7dc5-4bd8-9a78-8fca72a65820');
INSERT INTO continents (continent, continent_guid) VALUES ('Asie', 'b283c589-94df-4e29-b2ae-9e0a74a1bb9d');
INSERT INTO continents (continent, continent_guid) VALUES ('Amérique du Nord', '105fc88d-cc27-49fd-b3cc-c12f03186516');
INSERT INTO continents (continent, continent_guid) VALUES ('Amérique du Sud', '3292db5f-a50f-4e1c-9400-52707a7bf55d');
INSERT INTO continents (continent, continent_guid) VALUES ('Océanie', '97d71399-55e2-45fa-a5b7-989b704a9167');
INSERT INTO continents (continent, continent_guid) VALUES ('Afrique', '8a2988fc-1b48-4e71-99c2-8b4d0af65183');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Algérie', 6, '171aae39-f023-4e0d-9a61-9c139b2f7d9d');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Angola', 6, '5d60361a-a509-4ebd-af4b-5b98924da5f9');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Bénin', 6, 'cf767f6b-5f2a-422e-8f60-a7918c643fc3');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Botswana', 6, 'e489a511-1859-4109-8426-c83e41d4c47e');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Burundi', 6, 'ce40c10f-1453-4c17-8850-3e253ad499a8');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Cameroun', 6, '7f498079-1063-4f33-aa8e-7d269efa5f8b');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('République centrafricaine', 6, '2e8806a7-4f7b-4fda-be18-9dcc28718dad');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Tchad', 6, 'a555843e-9036-4a49-a765-5e20eb9b1b54');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Comores', 6, 'c27316bf-8057-45d2-a29d-1099add37718');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Congo', 6, '4b834027-fa1c-4e8d-bf30-1326c34c3964');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('République Démocratique du Congo', 6, 'cb6de9ea-b8ce-4cc2-8b4a-fce1bb4ced22');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Djibouti', 6, '6362c82d-58e2-4ac5-8901-38b05f80ff57');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Egypte', 6, '563282d2-0841-4322-9abb-726bc74466bc');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Guinée-équatoriale', 6, '08b5709b-e0e1-463a-b8cd-a3a1d40b5a56');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Erythrée', 6, '52f81f35-e57d-4a49-9c5d-ccdb97f284ad');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Ethiopie', 6, 'ca23b8ca-15b7-4e22-a522-5e1013d4562d');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Gabon', 6, '59070045-25f9-4faa-bbfe-c3c6309109ee');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Gambie', 6, '4c0cde1c-303f-403d-8d31-02f7747269df');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Ghana', 6, '490569f6-805f-444c-8fbb-489a201f3c56');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Guinée', 6, '5290b5ac-1771-4d71-bd3c-7918e576bfa7');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Guinée-Bissau', 6, 'f81e82c5-6056-49a9-99e5-e4015a50a6a6');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Kenya', 6, 'df2c3737-ce8d-46a0-a265-5a14e27a356d');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Lesotho', 6, '1eb76c05-8298-4fc5-a57b-5d8e5f655aad');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Liberia', 6, '83f2a0ee-cd29-4888-b0cc-bf6a9050bd30');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Libye', 6, '0e220328-015c-47cc-9401-f61919a5dcaf');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Madagascar', 6, '251c6978-6be8-42e9-a6a8-4b73c5c2a012');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Malawi', 6, '901a821c-da3f-46ca-b04f-3687ffc8ee29');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Mali', 6, 'f34ec33d-fc31-43b7-86f2-baa8befc6820');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Mauritanie', 6, '2b874fbd-207c-4746-9041-055a163a2d28');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Ile Maurice', 6, '963ee8bf-7021-4753-b431-63f8a2d7feed');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Maroc', 6, '5e70cc70-8387-496b-ae9b-24226cee64c8');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Mozambique', 6, '6ac73319-8621-4fff-9d5c-b3e9327defb9');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Namibie', 6, 'ba5fdda1-2279-4204-872c-94f97882ed0d');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Niger', 6, '669b7cf9-f330-475a-ad2f-e5f857fee639');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Nigeria', 6, 'a1438e1e-6412-4b58-b08c-6cbaa4317808');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Rwanda', 6, '2a4da0cd-7590-4e4d-946c-47b26f946a9e');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Sao-Tomé-et-Principe', 6, '293cb53e-4c23-4ea4-aaab-6e11220227c2');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Sénégal', 6, '13effe90-4925-4e16-9566-272f73a09ea7');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Seychelles', 6, '92680175-3fb5-4a22-a3a2-26f6478c4105');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Sierra Leone', 6, 'af1514d4-ec24-40d2-b396-fb0f718a3d8f');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Somalie', 6, 'b42ea942-ac5f-4ada-acd9-e6e5cc33f7fd');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Afrique du Sud', 6, 'dd4a694f-f95f-4950-ae5e-98d3fee7fd17');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Soudan du Sud', 6, '98115d29-de1b-4111-b2f6-062e00b4a4df');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Soudan', 6, 'ead854a6-61b4-4284-8ab4-c40441f4948b');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Eswatini', 6, '9ef1254b-0895-4a30-9816-3f685f9d7db8');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Tanzanie', 6, '27205b17-8295-4834-b37c-73904bcb2c1f');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Togo', 6, '93bd6cac-221f-4fcf-8046-ec2a4f8f6541');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Tunisie', 6, 'd0fe1a6e-3642-499c-acd2-44dc818d2832');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Ouganda', 6, '8408a133-1824-44e0-a82e-47a34258bf08');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Zambie', 6, '0a221596-64a0-464d-a6d3-a75250752df4');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Zimbabwe', 6, '8a9d7853-8b3d-47df-8c83-f3e11a96b346');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Afghanistan', 2, '8149008a-6056-408d-9a80-1114679ae5f0');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Bahrein', 2, '6d571850-0158-4ff5-bcb0-1617037db300');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Bangladesh', 2, 'a277671c-098b-47ff-922c-cb6958461e63');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Bhoutan', 2, 'b5c298fd-d739-43ab-b4f0-dc2a6eee60c6');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Birmanie', 2, '7a3152a1-67aa-4f66-b8e7-ff504237de50');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Cambodge', 2, 'e5eb37ad-31ae-47a9-ac69-80683531e133');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Chine', 2, '3a19b4ef-264f-48ed-a4b8-abbce45e1a5d');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Hong Kong', 2, '015dcc5a-adaa-43bf-83ae-6087ba640bcb');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Inde', 2, '70a277e1-5032-4176-915c-84269b27455d');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Indonésie', 2, 'df83aa07-ad08-40a5-94cf-7eba569cb848');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Iran', 2, '519e2f77-bbc4-4ad9-bd09-38201972522c');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Irak', 2, 'f0951075-506c-4fc9-aee1-947820bb31af');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Israel', 2, '45b28abb-9414-4ba4-85eb-7aad2096298d');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Japon', 2, '5d57675d-1175-48bc-b25e-6e42d8b43d57');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Jordanie', 2, '8c56cdde-427f-477f-9816-f37431ac186e');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Kazakhstan', 2, '048290f2-e267-4ddd-920b-16e203e74485');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Corée du Nord', 2, '52dd538c-fbb7-47f7-8669-b0143c540ccb');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Corée du Sud', 2, '0c53cb3b-8bc6-4f2a-a7a6-9ac0009f25af');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Koweit', 2, '1ebef1b4-a4d0-474b-9605-885f1881e15d');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Kirghizistan', 2, 'cdab09ec-e7d3-4348-a415-865e72f5199b');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Laos', 2, '09525b60-a9ac-4a4f-a72d-fcfdb03ed02b');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Liban', 2, 'c81e7150-8218-4aca-ae00-45c60ac2e661');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Malaisie', 2, '771b96ac-7c9b-405e-96fd-95b382d15b2c');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Maldives', 2, '6943346b-29d5-4e20-9d64-2789ed1a7bfd');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Mongolie', 2, 'd673298e-981c-41c1-a584-0f79b77fefbd');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Népal', 2, '7a73e967-38d6-4887-a3d2-8cf65eae62b0');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Oman', 2, '44203fe6-44c1-4917-a27c-31c46e26eadc');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Pakistan', 2, 'd89a3f98-54de-4d05-b1bb-bc30829b7a40');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Philippines', 2, '19624ece-b15c-4d11-9385-ded628bc1646');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Qatar', 2, '998340a2-e98c-4dc8-b419-75cc0755cb49');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Arabie Saoudite', 2, 'c2c5875e-8503-4b36-ac88-1961f9a3669f');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Singapour', 2, '1d7c2d10-8171-4261-9203-1d93e8277d6c');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Sri Lanka', 2, '0c224287-7276-433e-97e1-01b9a8c1bd8d');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Taiwan', 2, 'a15c68c5-bc4c-4767-bb40-84d69b228a53');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Tadjikistan', 2, 'e55f7206-296e-47d4-9bdb-b6c300892050');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Thailande', 2, '25fafca7-73c4-4e0c-af1a-d7af2ae93843');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Turquie', 1, '633e4fb1-fc35-42e8-b0bf-b4827f73f475');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Turkménistan', 2, '6a584ca9-b537-4fe3-b35a-caaef682d1e2');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Emirats arabes unis', 2, '8b89ed60-7902-4e39-bdeb-1793b8f11748');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Ouzbékistan', 2, 'ab0fd460-7f40-45c9-8330-68401676b449');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Yémen', 2, 'b9688803-15c0-4dee-8542-f95f0439001a');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Albanie', 1, 'd8542eb8-319a-4414-bf2f-686f4dcdbc2c');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Andorre', 1, '680e3711-fafb-453c-8fec-72700c3b0bce');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Arménie', 1, '3ed9d751-84ef-4d97-907c-a4c09efcc710');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Autriche', 1, '841dec5e-c1a2-4a59-91ca-bdd6be2d929b');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Azerbaidjan', 1, '5d4fea2a-1f46-43e9-a3f4-41599e6f09f5');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Biélorussie', 1, '6e3f664c-ba71-4170-9e3d-ba68e02be02a');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Belgique', 1, '91862871-ed55-44ce-8dd5-8f55dde166bd');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Bosnie-Herzégovine', 1, 'a35f4fd3-3b06-4f90-8d20-a51c4a490be4');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Bulgarie', 1, 'fd7a8518-5f36-4bd7-92ef-475a6ca2f879');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Croatie', 1, 'bcbe5083-d983-4c27-a224-f810c290bcce');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Chypre', 1, '823fef4d-7cd5-44e3-acbe-3cef89309f69');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Danemark', 1, '54760fab-92bd-4978-a7b4-6053f11bceba');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Estonie', 1, '0ea9d58c-3f5c-4a27-af94-e8a31ca3919b');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Finlande', 1, 'ae62eaa9-1965-43d1-939c-c67f1472e8da');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('France', 1, 'e0ea4fbf-3ac3-4e4f-b443-d3f7fc749d7a');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Écosse', 1, 'bdb28f50-6a59-4554-8650-410c968a1ba9');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Pays de Galles', 1, 'd362411a-fd93-4026-9a4d-a5ae9826f188');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Angleterre', 1, 'dcd74ae6-0774-4352-ada3-6925a9e08295');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Géorgie', 1, '06bf1359-4284-48ef-937d-45666f9b5f5d');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Allemagne', 1, '2cd52f43-8ad7-45c2-99c0-372222e705b3');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Gréce', 1, '04502064-4b15-4dd6-b1c5-00f5d460fafb');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Hongrie', 1, 'a3f484a3-48ae-44f0-b85a-0c1b85ca0aa1');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Islande', 1, 'cc888f3b-4feb-45be-b325-98ad5860812e');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Irlande', 1, '6f02b676-721f-4f5c-a39c-f33307a5a4e9');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Irlande du Nord', 1, '8c45b957-4072-4648-b025-8ba1e71bd7fc');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Italie', 1, '95896757-31a8-4441-bd61-f4f5418fa0eb');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Lettonie', 1, 'bf849a75-e5ee-4a1c-83a1-6a9cf5619b58');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Liechtenstein', 1, '8a2f29e3-b598-4f8a-aba0-c20839d14037');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Lituanie', 1, '6bffb890-a0b5-44b4-b22c-6c604e2c1928');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Luxembourg', 1, '7111415b-d1ba-4d00-a8d9-a01ea0766695');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Macédoine', 1, '418d6c5e-debf-44e8-9a42-bd3c487fb549');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Malte', 1, '16b86ac7-163f-43a2-bd65-3eab961711e7');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Moldavie', 1, 'dabbd926-fbc1-4d3d-b4be-9f9085030d59');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Monaco', 1, '62356804-cdc3-4895-b7b8-8f6b360c4eb0');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Monténégro', 1, 'c67c84ca-4f50-4a4f-aa84-fba5069910d0');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Pays-Bas', 1, 'ad36ed9e-3b10-461a-8b94-c009e1775dd6');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Norvége', 1, '293328bc-1f2d-4cf4-9271-5f978f1a93b9');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Pologne', 1, 'c4ca1f06-b5c4-45f9-9a7e-7fbd56a2a0b8');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Portugal', 1, 'a6af49d0-29cf-4cfe-a456-4a9e998431ba');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Roumanie', 1, 'f452d562-ca4d-4921-879f-598542356d40');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Saint-Marin', 1, '2d20cb51-30fa-4cfa-80d6-e5a035b2732e');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Serbie', 1, 'b60c01ac-e225-4d41-ad2c-379e2d8fc9d4');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Slovaquie', 1, 'a6cb1da4-4bb7-43ab-a2a0-7add89aa0b98');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Slovénie', 1, 'e85a9ed9-2b05-46a5-83bb-4a8c52a87dde');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Espagne', 1, '8b73c19a-3c4a-4578-97ca-9652f9bda3ac');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Suéde', 1, '0814b508-dc35-4c0b-beb4-36808c8e0ce0');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Suisse', 1, 'bc24af20-9ec0-4fbd-8908-c8549b3ea9d1');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Ukraine', 1, 'be0fc93c-8f7e-4af5-bb59-875a6959686d');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Vatican', 1, '9dfb8098-ee2a-453c-ab00-49aafc68868f');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Antigua-et-Barbuda', 3, '438626d3-59d9-4216-85c2-acf7bda7d6a5');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Bahamas', 3, 'e01f92f7-5e6f-4830-bead-e001643ad971');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Barbade', 3, '5ba1db75-6ec6-4a2f-8469-ccc52f0e311e');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Belize', 3, '3715c4cc-09d2-451f-bb9f-c408a4d6c44e');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Canada', 3, 'aea67f60-1330-4441-b147-d7bab9f663d2');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Costa Rica', 3, '53703c14-284b-4a15-acfe-67ff9839e04c');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Cuba', 3, 'f3383ac6-f4d2-48ac-9d6b-12e57ebded70');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('République dominicaine', 3, '9b156ec8-8087-40d9-9e48-46614d0a30b5');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Salvador', 3, 'd2dfea53-af6d-4ddc-90cb-6415563d9129');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Grenade', 3, 'c1bfaaaf-618a-4557-9f00-3197eb2f222f');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Guatemala', 3, '7b97c41a-408e-4c86-afef-baa92f3c4797');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Haéti', 3, '77ccf1db-ab1d-4e4d-bd32-bbb691b22784');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Honduras', 3, 'fc47eb92-463a-4ced-a55d-e5f9f01d8240');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Jamaique', 3, '57de593d-6054-42b6-8f8e-a9ec8c422fb7');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Mexique', 3, '4487df31-ea41-40cd-a297-33c01a25c019');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Nicaragua', 3, '1a9f9c2e-45b0-42d1-b118-31dedef9830e');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Panama', 3, '5ee2c870-bc06-4dd4-b7ba-717b950ad678');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Saint-Christophe-et-Niévès', 3, 'd06bc458-6b5d-49da-895f-9637f2d0c362');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Sainte-Lucie', 3, 'd83d3d40-402d-4884-87b9-aea941585788');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Saint-Vincent-et-les-Grenadines', 3, '6971645b-014e-4274-8a1a-8562369eead4');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Trinité et Tobago', 3, '50a2db00-bbec-4dbe-bd69-1ba7a97089fd');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Australie', 5, 'db4e4a63-f7a8-4def-9e58-3d7b80500903');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Fidji', 5, '760c1fdf-a60e-4a70-af2c-95404f6da9f9');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Kiribati', 5, '5f8e56ce-5b22-481d-8113-8f0bde96b22b');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Iles Marshall', 5, 'a75bda32-abd4-4e51-be98-081e42060b51');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Micronésie', 5, '0545f8ff-f275-44f1-8348-d6f2c46ae806');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Nauru', 5, '5f0f1717-dfd5-4218-a5a6-c313ded15114');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Nouvelle-Zélande', 5, 'd132bdad-d6d9-416c-ac52-e99a597c4e1c');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Palaos', 5, '7acbd809-0bf3-4a49-bbfc-1a67d1fdf760');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Papouasie-Nouvelle-Guinée', 5, '5971f2e0-e701-4b60-ba37-681fb653c1b1');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Samoa', 5, '3e2915fb-22f7-4c5a-95ce-1255c848ef1e');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Iles Salomon', 5, '9bbeeae8-7a94-43a6-996f-53ac5adad950');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Tonga', 5, 'bffd25f8-0019-4e17-b8d4-f8cf17b6b7c1');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Tuvalu', 5, 'a620a113-0574-41f6-9d44-c3157bdd6117');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Vanuatu', 5, '2f33b035-1d9e-4a1a-9225-2c004c598104');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Argentine', 4, 'faf4b5a4-d4a7-4fdb-803d-08b0a9f47777');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Bolivie', 4, 'a8952061-0163-477e-b59c-22581395262c');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Brésil', 4, '5c304100-0feb-4af6-bb91-7c9056b677c7');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Chili', 4, 'c17a84a4-3c02-4c93-80ca-b4af0c88db9d');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Colombie', 4, '8fc9f9da-79f3-4097-84df-ac749ab10a39');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Equateur', 4, '15d23f03-d7d6-4b84-b65d-36407ad45538');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Guyana', 4, '0fdafbd9-b9a5-4b04-bb6f-d95bef2f4e60');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Paraguay', 4, 'ec18c847-612e-4cd7-962a-e394b9ff4549');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Pérou', 4, 'b1cbc776-e247-47d5-b624-cde065d9dc66');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Suriname', 4, 'f294379b-08d0-4442-be6b-db03c4259b12');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Uruguay', 4, '0fb83300-60c8-4dd9-a2cc-6513f68f035a');
INSERT INTO countries (country, continent_id, country_guid) VALUES ('Venezuela', 4, '7952d9dc-6546-4aaf-993c-8354a80c1595');
INSERT INTO genders VALUES (1, 'Homme');
INSERT INTO genders VALUES (2, 'Femme');
INSERT INTO reading_status (reading_status) VALUES ('Reading', 'Finished', 'Partially read', 'On Hold', 'Dropped')