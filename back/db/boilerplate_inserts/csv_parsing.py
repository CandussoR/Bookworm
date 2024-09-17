import sqlite3


def get_line(l) -> list:
    return l.split(';')

def parse_continents(header : list) :
    europe_index = [i for (i,c) in enumerate(header) if "europe" in c]
    america_index = [i for (i,c) in enumerate(header) if "america" in c]
    africa_index = [i for (i,c) in enumerate(header) if "africa" in c]
    asia_index = [i for (i,c) in enumerate(header) if "asia" in c]
    oceania_index = [i for (i,c) in enumerate(header) if "oceania" in c]
    return {
        "europe": europe_index,
        "america": america_index,
        "africa": africa_index,
        "asia": asia_index,
        "oceania": oceania_index,
    }

# fw = open('pays-continents-clean.csv', 'w')
# continent_country_en = open('back/db/boilerplate_inserts/countries_by_continents.csv', 'r', newline="\r\n").readlines()[1:]
# new_continent_country = []
# fw = open('countries_continents_fr_en.csv', 'w')
# country_continents_content = []

# with open('back/db/boilerplate_inserts/pays_en_fr.csv', 'r', newline="\n", encoding="utf-8") as fr:
#     header = get_line(fr.readline()[:-2])
#     index_name_fr = header.index("name_fr")
#     index_name_en = header.index("name_en")
#     # index_continent = parse_continents(header)
#     # continent_header_part = [header[i] for k in index_continent.keys() for i in index_continent[k]]
#     # new_header = [header[index_name_fr], header[index_name_en]] + continent_header_part
#     # fw.write(";".join(new_header) + "\n")

#     # indexes = [index_name_fr, index_name_en] + [i for k in index_continent.keys() for i in index_continent[k]]
#     # indexes = [index_name_fr, index_name_en] 
#     for l in fr:
#         line = get_line(l[:-2])
#     #     clean_line = [line[i] for i in indexes]
#     #     fw.write(";".join(clean_line) + "\n")
#         country_continents_content.append({"fr" : line[index_name_fr], "en": line[index_name_en]})

#         new_continent_country = []
#         for l in continent_country_en:
#             for d in country_continents_content:
#                 if d["en"] in l:
#                     new_continent_country.append(l[:-2] + f",{d['fr']}" + "\n")
#                     break;

#     fw.write('continent,country_en,countr_fr\r\n')
#     for d in new_continent_country:
#         fw.write(d)

# fw.close()

# with open('back/db/boilerplate_inserts/pays-continents-clean.csv', 'r', encoding="ISO-8859-1", newline="\n") as fr:
#     header = get_line(fr.readline())
#     continent_indexes = parse_continents(header)
#     continents = {"europe" : [], "africa" : [], "asia" : [], "america" : [], "oceania" : []}
#     for l in fr:
#         line = get_line(l)
#         if "True" in [line[i] for i in continent_indexes["europe"]]:
#             continents["europe"].append(line[0])
#         elif "True" in [line[i] for i in continent_indexes["africa"]]:
#             continents["africa"].append(line[0])
#         elif "True" in [line[i] for i in continent_indexes["oceania"]]:
#             continents["oceania"].append(line[0])
#         elif "True" in [line[i] for i in continent_indexes["asia"]]:
#             continents["asia"].append(line[0])
#         elif "True" in [line[i] for i in continent_indexes["america"]]:
#             continents["america"].append(line[0])
#     with open('back/db/boilerplate_inserts/pays_continents.txt', 'w', encoding="ISO-8859-1") as fw:
#         for k in continents.keys():
#             fw.write(k.upper() + f" ({str(len(continents[k]))} pays) : \n")
#             for v in continents[k]:
#                 fw.write(f"\t{v} ; \n")

with sqlite3.connect(':memory:') as conn:
    conn.execute('PRAGMA foreign_keys = on;')
    stmt = '''CREATE TABLE IF NOT EXISTS continents (
     continent_id INTEGER PRIMARY KEY NOT NULL,
     continent TEXT UNIQUE NOT NULL
);
CREATE TABLE IF NOT EXISTS countries(
     country_id INTEGER PRIMARY KEY NOT NULL,
     country TEXT UNIQUE NOT NULL,
     continent_id INTERGER NOT NULL,
     UNIQUE (country, continent_id),
     FOREIGN KEY (continent_id) REFERENCES continents (continent_id)
);'''
    conn.executescript(stmt)
    with open('back/db/boilerplate_inserts/continent_country_inserts_fr.sql', 'r', encoding="utf-8") as fr:
        conn.executescript(fr.read())

    # conn.execute('CREATE TABLE continent_country (continent TEXT NOT NULL, country TEXT UNIQUE NOT NULL, PRIMARY KEY (continent, country));')
    # with open('back/db/boilerplate_inserts/continent_country_inserts_fr.sql', 'r', encoding="cp1252") as fr:
    #     fr.readline()
    #     for l in fr:
    #         [continent, c_en, continent_fr, c_fr] = get_line(l[:-1])
    #         conn.execute('INSERT INTO continent_country (continent, country) VALUES (?, ?)', [continent_fr, c_fr])
    all = conn.execute('SELECT * FROM countries').fetchall()
    print(1)

# def add_french_continent(line, header=False) -> str:
#     d = {"Oceania" : "Océanie",
#         "Europe" : "Europe",
#         "Asia" : "Asie",
#         "North America" : "Amérique du Nord",
#         "South America" : "Amérique du Sud",
#         "Africa" : "Afrique"}
#     if line == '':
#         return ''
#     [continent_en, c_en, c_fr] = get_line(line[:-1])
#     new_line = [continent_en, c_en, "continent_fr" if header else d[continent_en], c_fr]
#     return ";".join(new_line) + "\n"


# with open('back/db/boilerplate_inserts/continent_country.csv', 'r', encoding="cp1252") as fr:
#     new_file = []
#     new_file.append(add_french_continent(fr.readline(), True))
#     for i,l in enumerate(fr):
#         new_file.append(add_french_continent(l))
#     with open('continent_country_full.csv', 'w') as fw:
#         for l in new_file:
#             fw.write(l)
    
# fw = open('back/db/boilerplate_inserts/continent_country_inserts_fr.sql', 'w')
# d = {"Europe" : 1, "Asie" : 2, "Amérique du Nord" : 3, "Amérique du Sud" : 4, "Océanie" : 5, "Afrique" : 6}
# for c in ["Europe", "Asie", "Amérique du Nord", "Amérique du Sud", "Océanie", "Afrique"]:
#     fw.write(f"INSERT INTO continents (continent) VALUES (\'{c}\');\n")
# with open('back/db/boilerplate_inserts/continent_country_full.csv', 'r', encoding="utf-8") as fr:
#     fr.readline()
#     for l in fr:
#         [continent, c_en, continent_fr, c_fr] = get_line(l[:-1])
#         fw.write(f"INSERT INTO countries (country, continent_id) VALUES (\'{c_fr}\', {d[continent_fr]});\n")
# fw.close()

        