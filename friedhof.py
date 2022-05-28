import tkinter as tk
import datetime as dt
import sqlite3
import pandas as pd
from PIL import ImageTk, Image
from tkinter.ttk import *
import gc
from tkinter.messagebox import showinfo, showwarning, askyesno
# from memory_profiler import profile


### CREATE TABLE IF NOT EXISTS KÍVÜLRE DEF!!
def create_table_if_not_exists():
    conn = sqlite3.connect("friedhof.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS "temeto" (
	"id"	INTEGER NOT NULL,
	"graveyard_name"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("id" AUTOINCREMENT)
    )""")
    c.execute("""
    CREATE TABLE IF NOT EXISTS "grave" (
	"id"	INTEGER NOT NULL,
	"parcella"	TEXT NOT NULL,
	"sor"	INTEGER NOT NULL,
	"oszlop"	INTEGER NOT NULL,
	"temetoId"	INTEGER NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("temetoId") REFERENCES "temeto"("id") ON UPDATE CASCADE ON DELETE CASCADE)
    """)
    c.execute("""
    CREATE TABLE IF NOT EXISTS "berlo" (
	"id"	INTEGER NOT NULL,
	"berlo_nev"	TEXT,
	"berlo_cim"	TEXT,
	"megvaltas_ok"	TEXT DEFAULT 'temetés',
	"siremlek_tipus"	TEXT,
	"lejarat_eve"	INTEGER,
	"egyeb_megjegyzes"  TEXT,
	"graveId"	INTEGER NOT NULL UNIQUE,
	FOREIGN KEY("graveId") REFERENCES "grave"("id") ON UPDATE CASCADE ON DELETE CASCADE,
	PRIMARY KEY("id" AUTOINCREMENT)
)
    """)
    c.execute("""
    CREATE TABLE IF NOT EXISTS "deadPersons" (
	"id"	INTEGER NOT NULL,
	"vezeteknev"	TEXT,
	"keresztnev"	TEXT,
	"temetesi_ev"	INTEGER,
	"berloId"	INTEGER NOT NULL,
	FOREIGN KEY("berloId") REFERENCES "berlo"("id") ON DELETE CASCADE ON UPDATE CASCADE,
	PRIMARY KEY("id" AUTOINCREMENT)
)
    """)
    c.execute("""
        INSERT OR IGNORE INTO temeto (graveyard_name) VALUES("Felső");
    """)
    c.execute("""
        INSERT OR IGNORE INTO temeto (graveyard_name) VALUES("Alsó");
    """)


    ### TEST ---INSERT IGNORE INTO grave (parcella, sor, oszlop, temetoId) VALUES("A", 2, 4, 1);
    '''
    insert_stmt = ("""
        INSERT INTO grave (parcella, sor, oszlop, temetoId)
        SELECT ?, ?, ?, ?
        WHERE NOT EXISTS (SELECT 1 FROM grave WHERE parcella = ? and sor = ? and oszlop = ? and temetoId = ?)
        """)
    c.execute(insert_stmt, ("A", 2, 4, 1) * 2)

    insert_stmt = ("""
            INSERT INTO grave (parcella, sor, oszlop, temetoId)
            SELECT ?, ?, ?, ?
            WHERE NOT EXISTS (SELECT 1 FROM grave WHERE parcella = ? and sor = ? and oszlop = ? and temetoId = ?)
            """)
    c.execute(insert_stmt, ("A", 2, 5, 1) * 2)
    '''
    ### END TEST

    conn.commit()
    conn.close()


create_table_if_not_exists()

## DEFs
def excelbe_rendez():
    global lejarati_adatok
    year = dt.date.today().year
    print(year)
    lejartak = []
    for elem in lejarati_adatok:
        if int(elem['lejarat']) < year and int(elem['lejarat'] != 1):
            lejart = {
                "sirkod": elem['parcella'],
                "halott_nev": elem['halott_nev'],
            }
            lejartak.append(lejart)
        elif elem['lejarat'] == 1:
            if year-int(elem['utolso_temetes']) >= 26:
                lejart = {
                    "sirkod": elem['parcella'],
                    "halott_nev": elem['halott_nev'],
                }
                lejartak.append(lejart)
        elif elem['lejarat'] == 1 and elem['utolso_temetes'] == 2:
            lejart = {
                "sirkod": elem['parcella'],
                "halott_nev": elem['halott_nev'],
            }
            lejartak.append(lejart)

    print(lejartak)

    if len(lejartak) >= 1:
        temeto = lejarati_adatok[0]['temeto']
        parcella_for_excel = lejarati_adatok[0]['parcella_for_excel']

        dict_for_excel = {
            "Sírkód": [],
            "Sírban lévők": [],
        }

        for elem in lejartak:
            dict_for_excel["Sírkód"].append(elem['sirkod'])
            dict_for_excel["Sírban lévők"].append(elem['halott_nev'])

        df = pd.DataFrame(dict_for_excel)
        df.to_excel(f'../Excelek/{temeto}_temeto_{parcella_for_excel}_parcella_lejart_sirok.xlsx')
        showinfo(title='Info', message=f"A táblázat elkészült.")
        gc.collect()


def raise_frame(frame):
    frame.tkraise()
    af_temeto.set("Temetők")
    search_temeto.set("Temetők")
    search_parc_temeto.set("Temetők")
    parcells_upper_optionmenu.set("Parcellák")
    parcells_lower_optionmenu.set("Percellák")
    var_megvaltas.set("Ok")
    var_sirhely.set("Síremlék")
    parc.delete(0, 'end')
    sor.delete(0, 'end')
    oszlop.delete(0, 'end')
    berlo_nev.delete(0, 'end')
    berlo_cim.delete(0, 'end')
    # next.place(anchor="center", relx=.7, rely=.75)
    b_nev_label.place_forget()
    berlo_nev.place_forget()
    b_cim_label.place_forget()
    berlo_cim.place_forget()
    megvaltas_label.place_forget()
    sirvaltas_oka.place_forget()
    sec_next.place_forget()
    sirhely_label.place_forget()
    shely_type.place_forget()
    lejarat_eve.place_forget()
    lejarat_year.place_forget()
    lejarat_year.delete(0, 'end')
    vezeteknev.delete(0, 'end')
    keresztnev.delete(0, 'end')
    meghalt_ev.delete(0, 'end')
    add_button.place_forget()
    # alert_label.place_forget()
    egyb_megj.place_forget()
    egyeb_megjegyzes.place_forget()
    egyeb_megjegyzes.delete(0, 'end')
    save_button.place_forget()
    search_vezeteknev.delete(0, 'end')
    search_keresztnev.delete(0, 'end')
    search_meghalt_ev.delete(0, 'end')
    search_vezeteknev.delete(0, 'end')
    search_keresztnev.delete(0, 'end')
    search_meghalt_ev.delete(0, 'end')
    search_parc.delete(0, 'end')
    search_sor.delete(0, 'end')
    search_oszlop.delete(0, 'end')
    global temeto_id
    temeto_id = 0
    global grave_id
    grave_id = None
    global membercount
    membercount = 0
    treeview.delete(*treeview.get_children())
    treeview_namelist.delete(*treeview_namelist.get_children())
    parcells_treeview.delete(*parcells_treeview.get_children())
    gc.collect()

    ### SAFEMETHOD: IF SOMEBODY SWITCHES FRAME, THE DEAD_PERSONS ARRAY WILL BE DELETED
    global sirban_levo_szemelyek_adatai
    sirban_levo_szemely_adatok = {
        "vezeteknev": vezeteknev.get(),
        "keresztnev": keresztnev.get(),
        "meghalt_ev": 1,
    }
    sirban_levo_szemelyek_adatai = []
    sirban_levo_szemelyek_adatai.append(sirban_levo_szemely_adatok)


def nextframe_raise(frame):
    frame.tkraise()
    back_button.place(anchor=tk.NW, x=50, y=30)
    vezeteknev_lab.place(anchor="center", relx=0.05, rely=0.25, width=200)
    vezeteknev.place(anchor="center", relx=0.22, rely=0.25, width=180)
    keresztnev_label.place(anchor="center", relx=0.32, rely=0.25, width=200)
    keresztnev.place(anchor="center", relx=0.5, rely=0.25, width=200)
    meghalt_ev_label.place(anchor="center", relx=0.62, rely=0.25, width=200)
    meghalt_ev.place(anchor="center", relx=0.725, rely=0.25, width=60)
    add_button.place(relx=.8, rely=.23)
    delete_button.place(relx=.88, rely=.23)
    save_button.place(anchor="center", relx=.8, rely=.85)


def switch_search_frames(frame):
    frame.tkraise()
    search_temeto.set("Temetők")
    search_vezeteknev.delete(0, 'end')
    search_keresztnev.delete(0, 'end')
    search_meghalt_ev.delete(0, 'end')

    search_parc_temeto.set("Temetők")
    search_parc.delete(0, 'end')
    search_sor.delete(0, 'end')
    search_oszlop.delete(0, 'end')


def parcells_frame_switch(frame):
    frame.tkraise()
    upper_grave_backbutton.place(relx=.03, rely=.03)
    lower_grave_backbutton.place(relx=.03, rely=.03)
    parcells_upper_optionmenu.set("Parcellák")
    parcells_lower_optionmenu.set("Percellák")


def frame_raise_without_forget(frame):
    frame.tkraise()


def missing_or_bad_argument(missings, badargs, nameproblem, expireproblem, empty_entry, name_empty, search_problem, parcell_empty):
    misses = ""
    badstr = ""
    emptystr = ""
    problem = ""
    is_missing = False
    is_bads = False
    is_empty_name = False
    is_problem = False

    if len(missings) > 0:
        is_missing = True
        for elem in missings:
            misses = misses + f"{elem}, "

    if len(badargs) > 0:
        is_bads = True
        for elem in badargs:
            badstr = badstr + f"{elem}, "

    if len(name_empty) > 0:
        is_empty_name = True
        for elem in name_empty:
            emptystr = emptystr + f"{elem}, "

    if len(search_problem) > 0:
        is_problem = True
        for elem in search_problem:
            problem = problem + f"{elem}, "

    if is_missing and not is_bads and not nameproblem and not expireproblem and not is_empty_name and not is_problem and not parcell_empty:
        showwarning(title='Figyelem!', message=f"  Nem töltötte ki a(z) '{misses}' menü(ke)t!")
    elif is_bads and not is_missing and not nameproblem and not expireproblem and not is_empty_name and not is_problem and not parcell_empty:
        showwarning(title='Figyelem!', message=f"  Hibásan töltötte ki a(z) '{badstr}' menü(ke)t!")
    elif is_bads and is_missing and not nameproblem and not expireproblem and not is_empty_name and not is_problem and not parcell_empty:
        showwarning(title='Figyelem!', message=f"  Nem töltötte ki a(z) '{misses}' menü(ke)t!\n  Hibásan töltötte ki a(z) '{badstr}' menü(ke)t!")
    elif nameproblem and not is_bads and not is_missing and not expireproblem and not is_empty_name and not is_problem and not parcell_empty:
        showwarning(title='Figyelem!', message=f"  Hibásan töltötte ki a 'bérlő neve' menüt!")
    elif nameproblem and not is_bads and is_missing and not expireproblem and not is_empty_name and not is_problem and not parcell_empty:
        showwarning(title='Figyelem!', message=f"  Hibásan töltötte ki a 'bérlő neve' menüt!\n  Nem töltötte ki a(z) '{misses}' menü(ke)t!")
    elif nameproblem and not is_missing and is_bads and not expireproblem and not is_empty_name and not is_problem and not parcell_empty:
        showwarning(title='Figyelem!', message=f"  Hibásan töltötte ki a 'bérlő neve' menüt!\n  Hibásan töltötte ki a(z) '{badstr}' menü(ke)t!")
    elif nameproblem and is_missing and is_bads and not expireproblem and not is_empty_name and not is_problem and not parcell_empty:
        showwarning(title='Figyelem!', message=f"  Hibásan töltötte ki a 'bérlő neve' menüt!\n  Nem töltötte ki a(z) '{misses}' menü(ke)t!\n  Hibásan töltötte ki a(z) '{badstr}' menü(ke)t!")
    elif expireproblem and not nameproblem and not is_missing and not is_bads and not is_empty_name and not is_problem and not parcell_empty:
        showwarning(title='Figyelem!', message=f"  Hibásan töltötte ki a 'lejárat éve' menüt!")
    elif expireproblem and nameproblem and not is_missing and not is_bads and not is_empty_name and not is_problem and not parcell_empty:
        showwarning(title='Figyelem!', message=f"  Hibásan töltötte ki a 'lejárat éve' menüt!\n  Hibásan töltötte ki a 'bérlő neve' menüt!")
    elif expireproblem and not nameproblem and is_missing and not is_bads and not is_empty_name and not is_problem and not parcell_empty:
        showwarning(title='Figyelem!', message=f"  Hibásan töltötte ki a 'lejárat éve' menüt!\n  Nem töltötte ki a(z) '{misses}' menü(ke)t!")
    elif expireproblem and not nameproblem and not is_missing and is_bads and not is_empty_name and not is_problem and not parcell_empty:
        showwarning(title='Figyelem!', message=f"  Hibásan töltötte ki a 'lejárat éve' menüt!\n  Hibásan töltötte ki a(z) '{badstr}' menü(ke)t!")
    elif expireproblem and nameproblem and is_missing and not is_bads and not is_empty_names and not is_problem and not parcell_empty:
        showwarning(title='Figyelem!', message=f"  Hibásan töltötte ki a 'lejárat éve' menüt!\n  Hibásan töltötte ki a 'bérlő neve' menüt!\n  Nem töltötte ki a(z) '{misses}' menü(ke)t!")
    elif expireproblem and not nameproblem and is_missing and is_bads and not is_empty_name and not is_problem and not parcell_empty:
        showwarning(title='Figyelem!', message=f"  Hibásan töltötte ki a 'lejárat éve' menüt!\n  Hibásan töltötte ki a(z) '{badstr}' menü(ke)t!\n  Nem töltötte ki a(z) '{misses}' menü(ke)t!")
    elif expireproblem and nameproblem and not is_missing and is_bads and not is_empty_name and not is_problem and not parcell_empty:
        showwarning(title='Figyelem!', message=f"  Hibásan töltötte ki a 'lejárat éve' menüt!\n  Hibásan töltötte ki a 'bérlő neve' menüt!\n  Hibásan töltötte ki a(z) '{badstr}' menü(ke)t!")
    elif expireproblem and nameproblem and is_missing and is_bads and not is_empty_name and not is_problem and not parcell_empty:
        showwarning(title='Figyelem!', message=f"  Hibásan töltötte ki a 'lejárat éve' menüt!\n  Hibásan töltötte ki a 'bérlő neve' menüt!\n  Hibásan töltötte ki a(z) '{badstr}' menü(ke)t!\n  Nem töltötte ki a(z) '{misses}' menü(ke)t!")
    elif empty_entry and not expireproblem and not nameproblem and not is_missing and not is_bads and not is_empty_name and not is_problem and not parcell_empty:
        showwarning(title='Figyelem!', message=f"  Legalább egy mezőt töltsön ki!\nAz elhalálozás éve mező csak szám lehet.")
    elif is_empty_name and not empty_entry and not expireproblem and not nameproblem and not is_missing and not is_bads and not is_problem and not parcell_empty:
        showwarning(title='Figyelem!', message=f"  Kérem, az ideális keresés érdekében\ntöltse ki a(z) '{emptystr}' mező(ke)t!")
    elif is_problem and not is_empty_name and not empty_entry and not expireproblem and not nameproblem and not is_missing and not is_bads and not parcell_empty:
        showwarning(title='Figyelem!', message=f"  Ellenőrizze a(z) '{problem}' menü(ke)t!")
    elif parcell_empty and not is_empty_name and not empty_entry and not expireproblem and not nameproblem and not is_missing and not is_bads and not is_problem:
        showwarning(title='Figyelem!', message=f"  Töltse ki a  'parcella' menüt!")

membercount = 0
def add_member():
    if vezeteknev.get() == "" and keresztnev.get() == "" and meghalt_ev.get() == "":
        missing_or_bad_argument("", "", False, False, True, "", "", False)
    elif meghalt_ev.get() != "" and not meghalt_ev.get().strip().isnumeric():
        missing_or_bad_argument("", "", False, False, True, "", "", False)

    else:
        ### HA SEMMI ADAT NEM ISMERT, AKKOR ÍRJON 1-EST AZ ÉVHEZ
        if meghalt_ev.get().strip() != "" and meghalt_ev.get().strip().isnumeric():
            meghalt_ev_var = int(meghalt_ev.get().strip())
        if meghalt_ev.get().strip() == "":
            meghalt_ev_var = 1

        sirban_levo_szemely_adatok = {
            "vezeteknev": vezeteknev.get(),
            "keresztnev": keresztnev.get(),
            "meghalt_ev": meghalt_ev_var,
        }

        global membercount

        treeview.insert(parent="", index="end", iid=membercount, text="",
                        values=(sirban_levo_szemely_adatok['vezeteknev'],
                                sirban_levo_szemely_adatok['keresztnev'], sirban_levo_szemely_adatok['meghalt_ev']))

        vezeteknev.delete(0, 'end')
        keresztnev.delete(0, 'end')
        meghalt_ev.delete(0, 'end')
        membercount+=1


def del_member(treeview):
    selected_items = treeview.selection()
    for item in selected_items:
        treeview.delete(item)


def checkforok(temeto, parc, sor, oszlop, second):
    ### NOTE: Ha nem ír be semmit a felhasználó, ne tűnjön el KÉSZ
    # print(temeto, parc, sor, oszlop, second)
    # print(f"Lejárat éve: {lejarat_year.get()}")
    missings = []
    badargument = []
    bads = False
    miss = False
    not_correct_name = False
    not_correct_expire = False
    correct_expire = False
    can_continue = False
    if temeto == "Temetők":
        missings.append("temető")
        miss = True
    if parc == "":
        missings.append("parcella")
        miss = True
    if sor == "":
        missings.append("sor")
        miss = True
    if oszlop == "":
        missings.append("oszlop")
        miss = True

    ### ISNUMERIC
    if parc != "" and parc.strip().isnumeric():
        badargument.append("parcella")
        bads = True
    if sor != "" and not sor.strip().isnumeric():
        badargument.append("sor")
        bads = True
    if oszlop != "" and not oszlop.strip().isnumeric():
        badargument.append("oszlop")
        bads = True

    ### SECOND CHECK
    if second:
        if berlo_nev.get().strip() != "":
            berlo = berlo_nev.get()
            berlo = berlo.strip().split()
            if len(berlo) <= 1:
                not_correct_name = True
            elif len(berlo) > 1:
                can_continue = True
        elif berlo_nev.get() == "":
            can_continue = True
        if lejarat_year.get().strip() != "":
            lejarat = lejarat_year.get().strip().split()
            if len(lejarat) != 1 or not lejarat_year.get().strip().isnumeric():
                not_correct_expire = True
            elif len(lejarat) == 1:
                correct_expire = True
        elif lejarat_year.get() == "":
            correct_expire = True



    if miss or bads or not_correct_name or not_correct_expire:
        missing_or_bad_argument(missings, badargument, not_correct_name, not_correct_expire, False, "", "", False)


    if not miss and not bads and not not_correct_name and not second:
        ### NOTE: BÉRLŐ ADATOK FELVÉTELE .PLACE
        ### CHECK IF ALREADY EXIST
        already_exist = False

        b_nev_label.place(anchor="center", relx=0.377, rely=0.25, width=300)
        berlo_nev.place(anchor="center", relx=0.638, rely=0.25, width=250)
        b_cim_label.place(anchor="center", relx=0.377, rely=0.35, width=300)
        berlo_cim.place(anchor="center", relx=0.6957, rely=0.35, width=400)
        megvaltas_label.place(anchor="center", relx=0.313, rely=0.45, width=300)
        sirvaltas_oka.place(anchor="center", relx=0.6, rely=0.45, width=150)
        sirhely_label.place(anchor="center", relx=0.309, rely=0.55, width=300)
        shely_type.place(anchor="center", relx=0.6, rely=0.55, width=150)
        lejarat_eve.place(anchor="center", relx=0.378, rely=0.65, width=300)
        lejarat_year.place(anchor="center", relx=0.5799, rely=0.65, width=100)
        egyb_megj.place(anchor="center", relx=0.348, rely=0.75, width=200)
        egyeb_megjegyzes.place(anchor="center", relx=0.657, rely=0.75, width=300)
        sec_next.place(anchor="center", relx=.7, rely=.85)

        berlo_nev.delete(0, 'end')
        berlo_cim.delete(0, 'end')
        var_megvaltas.set("Ok")
        var_sirhely.set("Síremlék")
        lejarat_year.delete(0, 'end')
        egyeb_megjegyzes.delete(0, 'end')

        treeview.delete(*treeview.get_children())

        conn = sqlite3.connect("friedhof.db")
        c = conn.cursor()

        ### INSERT
        def search_for_exist():
            row = c.execute("""
            SELECT rowid FROM temeto
            WHERE graveyard_name = ?""", (temeto,)).fetchone()

            if row is not None:
                global temeto_id
                temeto_id = row[0]
                print(temeto_id)
            else:
                pass # NINCS AZ ADATBÁZISBAN ILYEN ADAT


            row = c.execute("""
            SELECT rowid FROM grave
            WHERE temetoId = ?
            AND parcella = ?
            AND sor = ?
            AND oszlop = ?
            """, (temeto_id, parc.upper(), sor, oszlop)).fetchone()

            ### LEKÉRTÜK A KAPOTT ADATOKBÓL, HOGY LÉTEZIK-E A CUCC, HA NEM LÉTEZIK, None-t AD VISSZA
            if row is not None: ## HA LÉTEZIK
                global grave_id
                grave_id = row[0]
                already_exist = True
                print(grave_id)
                showinfo(title='Info', message=f"\tA megadott sír már létezik az adatbázisban.\n\tAz adatok be lesznek töltve.")

                c.execute("""
                            SELECT berlo_nev, berlo_cim, megvaltas_ok, siremlek_tipus, lejarat_eve, egyeb_megjegyzes, rowid FROM berlo
                            WHERE graveId = ?
                            """, (grave_id,))
                berloAdatok = c.fetchone()
                print(berloAdatok)
                ### SECOND PAGE DATAS LOAD
                berlo_nev.insert('end', berloAdatok[0])
                berlo_cim.insert('end', berloAdatok[1])
                var_megvaltas.set(berloAdatok[2])
                var_sirhely.set(berloAdatok[3])
                lejarat_year.insert('end', berloAdatok[4])
                egyeb_megjegyzes.insert('end', berloAdatok[5])

                ### HALOTTAK BETÖLTÉSE
                c.execute("""
                            SELECT vezeteknev, keresztnev, temetesi_ev FROM deadPersons
                            WHERE berloId = ?
                                            """, (berloAdatok[-1],))
                deadPersons = c.fetchall()
                global membercount
                for line in deadPersons:
                    treeview.insert(parent="", index="end", iid=membercount, text="",
                                    values=(line[0], line[1], line[2]))
                    membercount+=1

                c.close()
                conn.close()
                frame_raise_without_forget(secondframe)

            else: ## HA NEM LÉTEZIK
                showinfo(title='Info', message=f"\tÚj adat lesz felvéve az adatbázisba.\n\tTemető: {temeto}; Parcella: {parc}; Sor: {sor}; Oszlop: {oszlop}")
                print(f"Nincs ilyen adat; Row: {row}")
                grave_id = None

                c.close()
                conn.close()
                frame_raise_without_forget(secondframe)


        search_for_exist()

    if second and not miss and not bads and not not_correct_name and can_continue and correct_expire:
        nextframe_raise(nextframe)


def name_query():
    ### CHECK DATAS
    missed_things = []
    missed = False
    if search_vezeteknev.get().strip() == "":
        missed_things.append("vezetéknév")
        missed = True
    if search_keresztnev.get().strip() == "":
        missed_things.append("keresztnév")
        missed = True
    if search_temeto.get() == "Temetők":
        missed_things.append("temető")
        missed = True
    if search_meghalt_ev.get().strip() != "" and not search_meghalt_ev.get().strip().isnumeric():
        missed_things.append("elhalálozás éve")
        missed = True
    if missed:
        missing_or_bad_argument("", "", False, False, False, missed_things, "", False)
    else:
        if search_meghalt_ev.get().strip() == "":
            search_meghalt_ev_var = 1
        else:
            search_meghalt_ev_var = int(search_meghalt_ev.get().strip())

        keresesi_ertekek = {
            "vezeteknev": search_vezeteknev.get().strip(),
            "keresztnev": search_keresztnev.get().strip(),
            "meghalt_ev": search_meghalt_ev_var,
            "temeto": search_temeto.get()
        }
        print(keresesi_ertekek)

        ### ADATBÁZISBÓL LEKÉRÉS
        conn = sqlite3.connect("friedhof.db")
        c = conn.cursor()

        row = c.execute("""
                            SELECT rowid FROM temeto
                            WHERE graveyard_name = ?
                            """, (keresesi_ertekek['temeto'],)).fetchone()

        temeto_id = row[0]
        print(temeto_id)

        if keresesi_ertekek['meghalt_ev'] == 1:
            halott_adatok = c.execute("""
                                SELECT berloId, vezeteknev, keresztnev, temetesi_ev FROM deadPersons
                                WHERE vezeteknev = ? COLLATE NOCASE AND keresztnev = ? COLLATE NOCASE
                                """, (keresesi_ertekek['vezeteknev'],keresesi_ertekek['keresztnev'])).fetchall()

        else:
            halott_adatok = c.execute("""
                                SELECT berloId, vezeteknev, keresztnev, temetesi_ev FROM deadPersons
                                WHERE UPPER(vezeteknev) = ? AND UPPER(keresztnev) = ? AND temetesi_ev = ?
                                """, (keresesi_ertekek['vezeteknev'].upper(),keresesi_ertekek['keresztnev'].upper(), keresesi_ertekek['meghalt_ev'])).fetchall()

        print(halott_adatok)
        if len(halott_adatok) == 0:
            showinfo(title='Info', message=f"A keresett sír nincs az adatbázisban.")
            c.close()
            conn.close()
        else:
            grave_ids = []
            for elem in halott_adatok:
                row = c.execute("""
                                SELECT graveId FROM berlo
                                WHERE rowid = ?
                                """, (elem[0],)).fetchone()[0]
                grave_ids.append(row)
            print(grave_ids)

            sir_adatok = []
            for elem in grave_ids:
                sir_adat = c.execute("""
                                        SELECT parcella, sor, oszlop FROM grave
                                        WHERE temetoId = ? and id = ?""", (temeto_id, elem)).fetchone()
                sir_adatok.append(sir_adat)
            print(sir_adatok)

            ### LISTÁBA ÍRÁS
            vegleges_lista = []
            for i in range(0, len(halott_adatok)):
                elem = {
                    'vezeteknev': halott_adatok[i][1],
                    'keresztnev': halott_adatok[i][2],
                    'meghalt_ev': halott_adatok[i][3],
                    'temeto': keresesi_ertekek['temeto'],
                    'parcella': sir_adatok[i][0],
                    'sor': sir_adatok[i][1],
                    'oszlop': sir_adatok[i][2],
                }
                vegleges_lista.append(elem)

            print(vegleges_lista)
            counteer = 0
            for line in vegleges_lista:
                treeview_namelist.insert(parent="", index="end", iid=counteer, text="",
                                         values=(line['vezeteknev'], line['keresztnev'], line['meghalt_ev'],
                                                 line['temeto'], line['parcella'], line['sor'], line['oszlop']))
                counteer += 1

            c.close()
            conn.close()
            frame_raise_without_forget(namelist)


def delete_item():
    answer = askyesno(title='Megerősítés',
                      message='Biztosan végleg törölni akarja a sírt az adatbázisból?')
    if answer:
        selected_items = treeview_namelist.selection()
        conn = sqlite3.connect("friedhof.db")
        c = conn.cursor()

        for item in selected_items:
            adat = treeview_namelist.item(item)["values"]

            torlendo_adat= {
                "vezeteknev": adat[0],
                "keresztnev": adat[1],
                "meghalt_ev": adat[2],
                "temeto": adat[3],
                "parcella": adat[4],
                "sor": adat[5],
                "oszlop": adat[6]
            }
            treeview_namelist.delete(item)

            if torlendo_adat['temeto'] == "Felső":
                temeto_id = 1
            elif torlendo_adat['temeto'] == "Alsó":
                temeto_id = 2

            row = c.execute("""
                                SELECT rowid FROM grave
                                WHERE parcella = ? AND sor = ? AND oszlop = ? AND temetoId = ?
                                """, (torlendo_adat['parcella'], torlendo_adat['sor'], torlendo_adat['oszlop'], temeto_id)).fetchone()

            grave_id = row[0]

            c.execute("""
                        DELETE FROM grave
                        WHERE id = ?""", (grave_id,))
            conn.commit()

            row = c.execute("""
                                SELECT rowid FROM berlo
                                WHERE graveId = ?
                                """,(grave_id,)).fetchone()

            berlo_id = row[0]

            c.execute("""
                                DELETE FROM berlo
                                WHERE graveId = ?""", (grave_id,))
            conn.commit()

            c.execute("""
                                DELETE FROM deadPersons
                                WHERE berloId = ?""", (berlo_id,))
            conn.commit()

        c.close()
        conn.close()


def gravekod_search_check(parcell, sor, oszlop, temeto):
    is_problem = False
    problem_list = []
    if parcell.strip() == "" or parcell.strip().isnumeric():
        is_problem = True
        problem_list.append("parcella")
    if sor.strip() == "" or not sor.strip().isnumeric():
        is_problem = True
        problem_list.append("sor")
    if oszlop.strip() == "" or not oszlop.strip().isnumeric():
        is_problem = True
        problem_list.append("oszlop")
    if temeto == "Temetők":
        is_problem = True
        problem_list.append("temető")

    if is_problem:
        missing_or_bad_argument("", "", False, False, False, "", problem_list, False)
    else:
        ### KERESÉS IDE
        conn = sqlite3.connect("friedhof.db")
        c = conn.cursor()

        if temeto == "Felső":
            temeto_id = 1
        elif temeto == "Alsó":
            temeto_id = 2

        grave_adatok = c.execute("""
                            SELECT rowid, parcella, sor, oszlop FROM grave
                            WHERE parcella = ? AND sor = ? AND oszlop = ? AND temetoId = ?
                            """, (parcell.upper(), sor, oszlop, temeto_id)).fetchone()

        print(grave_adatok)
        if grave_adatok is None:
            showinfo(title='Info', message=f"A keresett sír nincs az adatbázisban.")
            c.close()
            conn.close()
        else:
            berlo_id = c.execute("""
                                SELECT rowid FROM berlo
                                WHERE graveId = ?""", (grave_adatok[0],)).fetchone()[0]
            print(berlo_id)

            halott_adatok = c.execute("""
                                SELECT vezeteknev, keresztnev, temetesi_ev FROM deadPersons
                                WHERE berloId = ?
                                """, (berlo_id,)).fetchone()

            print(halott_adatok)
            c.close()
            conn.close()

            treeview_namelist.insert(parent="", index="end",
                                     iid=0, text="", values=(halott_adatok[0],
                                                             halott_adatok[1], halott_adatok[2],
                                                             temeto, grave_adatok[1], grave_adatok[2], grave_adatok[3]))

            frame_raise_without_forget(namelist)


def parcells_check(parcell, temeto_id):
    if parcell == "Parcellák":
        missing_or_bad_argument("", "", False, False, False, "", "", True)
    else:
        ### KERESÉS, LISTÁZÁS
        conn = sqlite3.connect("friedhof.db")
        c = conn.cursor()

        temeto_adatok = c.execute("""
                        SELECT rowid, sor, oszlop FROM grave
                        WHERE  parcella = ? AND temetoId = ?""",
                                  (parcell, temeto_id)).fetchall()

        if temeto_id == 1:
            temeto = "felso"
        elif temeto_id == 2:
            temeto = "also"

        count = 0
        i = 0
        global lejarati_adatok
        lejarati_adatok = []
        for elem in temeto_adatok:
            berlo_adat = c.execute("""
                        SELECT rowid, berlo_nev, lejarat_eve FROM berlo
                        WHERE graveId = ?""",
                                     (elem[0],)).fetchone()

            if berlo_adat is not None:
                halottak = c.execute("""
                            SELECT vezeteknev, keresztnev, temetesi_ev FROM deadPersons
                            WHERE berloId = ?""", (berlo_adat[0],)).fetchall()

                parcells_treeview.insert(parent='', index="end",
                                         iid=count, values=(temeto_adatok[i][1], temeto_adatok[i][2], berlo_adat[1], berlo_adat[2]))

                not_modified_count = count
                latest_burry = 2
                print(halottak)
                for halott in halottak:
                    parcells_treeview.insert(parent=f'{not_modified_count}', index="end", iid=count+1, values=("", "", f"{halott[0]} {halott[1]}", halott[2]))
                    if latest_burry < int(halott[2]):
                        latest_burry = int(halott[2])
                    count += 1

                if halottak[0][0] == "" and halottak[0][1] == "":
                    halott_nev = "nincs név megadva"
                else:
                    halott_nev = f"{halottak[0][0]} {halottak[0][1]}"

                if berlo_adat[2] == "":
                    expiration_year = 1
                else:
                    expiration_year = int(berlo_adat[2])

                lejarati_adat = {
                    "parcella": f"{parcell}-{elem[1]}-{elem[2]}",
                    "lejarat": expiration_year,
                    "halott_nev": halott_nev,
                    "utolso_temetes": latest_burry,
                    "temeto": temeto,
                    "parcella_for_excel": parcell
                }
                lejarati_adatok.append(lejarati_adat)

            count+=1
            i+=1

        c.close()
        conn.close()
        print(lejarati_adatok)
        frame_raise_without_forget(parcells_list)


def save_datas():
    if meghalt_ev.get() != "" and not meghalt_ev.get().strip().isnumeric():
        missing_or_bad_argument("", "", False, False, True, "", "", False)

    for line in treeview.get_children():
        lista = treeview.item(line)['values']
        sirban_levo_szemely_adatok = {
            "vezeteknev": lista[0].strip(),
            "keresztnev": lista[1].strip(),
            "meghalt_ev": lista[2],
        }
        sirban_levo_szemelyek_adatai.append(sirban_levo_szemely_adatok)

    ### IF THE LATEST ENTRY.GET() != THE LATES ELEMENTS OF THE LIST: LIST.APPEND(THE LATEST GET())
    if sirban_levo_szemelyek_adatai[-1]['vezeteknev'] != vezeteknev.get() or sirban_levo_szemelyek_adatai[-1]['keresztnev'] != keresztnev.get() or sirban_levo_szemelyek_adatai[-1]['meghalt_ev'] != meghalt_ev.get():
        if meghalt_ev.get().strip() != "":
            sirban_levo_szemely_adatok = {
                "vezeteknev": vezeteknev.get().strip(),
                "keresztnev": keresztnev.get().strip(),
                "meghalt_ev": meghalt_ev.get().strip(),
            }
            sirban_levo_szemelyek_adatai.append(sirban_levo_szemely_adatok)
        else:
            sirban_levo_szemely_adatok = {
                "vezeteknev": vezeteknev.get().strip(),
                "keresztnev": keresztnev.get().strip(),
                "meghalt_ev": 1,
            }
            sirban_levo_szemelyek_adatai.append(sirban_levo_szemely_adatok)

    if len(sirban_levo_szemelyek_adatai) != 1 and sirban_levo_szemelyek_adatai[0]['vezeteknev'] == "" and sirban_levo_szemelyek_adatai[0]['keresztnev'] == "" and sirban_levo_szemelyek_adatai[0]['meghalt_ev'] == 1:
        sirban_levo_szemelyek_adatai.pop(0)
    if len(sirban_levo_szemelyek_adatai) > 1 and sirban_levo_szemelyek_adatai[-1]['vezeteknev'] == "" and sirban_levo_szemelyek_adatai[-1]['keresztnev'] == "" and sirban_levo_szemelyek_adatai[-1]['meghalt_ev'] == 1:
        sirban_levo_szemelyek_adatai.pop(-1)
    if len(sirban_levo_szemelyek_adatai) > 1 and sirban_levo_szemelyek_adatai[-1]['vezeteknev'] == "" and sirban_levo_szemelyek_adatai[-1]['keresztnev'] == "" and sirban_levo_szemelyek_adatai[-1]['meghalt_ev'] == "":
        sirban_levo_szemelyek_adatai.pop(-1)

    ### MENTÉS KÉSZ POP-UP
    showinfo(title='Info', message="Mentés kész.")

    new_datas = {
        "temeto": af_temeto.get(),
        "parcell": parc.get().strip().upper(),
        "sor": sor.get().strip(),
        "oszlop": oszlop.get().strip(),
        "berlo_nev": berlo_nev.get().strip().title(),
        "berlo_cim": berlo_cim.get().strip(),
        "megvaltas_oka": var_megvaltas.get(),
        "siremlek": var_sirhely.get(),
        "lejarat_eve": lejarat_year.get().strip(),
        "egyeb_megjegyzes": egyeb_megjegyzes.get().strip()
    }

    if len(sirban_levo_szemelyek_adatai) > 1:
        if sirban_levo_szemelyek_adatai[0]["vezeteknev"] == "" and sirban_levo_szemelyek_adatai[0]["keresztnev"] == "" and sirban_levo_szemelyek_adatai[0]["meghalt_ev"] == 1:
            sirban_levo_szemelyek_adatai.pop(0)

        for elem in sirban_levo_szemelyek_adatai:
            if elem["vezeteknev"] != "":
                elem["vezeteknev"] = elem["vezeteknev"].title()
            if elem["keresztnev"] != "":
                elem["keresztnev"] = elem["keresztnev"].title()

    # print(new_datas)
    print(sirban_levo_szemelyek_adatai)

    conn = sqlite3.connect("friedhof.db")
    c = conn.cursor()

    print(new_datas['parcell'], new_datas['sor'], new_datas['oszlop'], temeto_id)
    global grave_id
    if grave_id is not None:
        # UPDATE RECORD
        # BIZTOS VÁLTOZTATNI AKAR? ELLENŐRZÉS, HOGY VÁLTOZOTT-E

        row = c.execute("""
                            SELECT rowid FROM berlo
                            WHERE graveId = ?
                            """, (grave_id,)).fetchone()

        berlo_id = row[0]
        print(berlo_id)
        c.execute("""
                    UPDATE berlo
                    SET berlo_nev=?, berlo_cim=?, megvaltas_ok=?, siremlek_tipus=?, lejarat_eve=?, egyeb_megjegyzes=?
                    WHERE graveId = ?
                    """, (new_datas['berlo_nev'], new_datas['berlo_cim'],
                          new_datas['megvaltas_oka'], new_datas['siremlek'],
                          new_datas['lejarat_eve'], new_datas['egyeb_megjegyzes'], grave_id))
        conn.commit()
        ### HALOTTAK BEÍRÁSA
        c.execute("""
                    DELETE FROM deadPersons
                    WHERE berloId = ?
                    """, (berlo_id,))
        conn.commit()

        for elem in sirban_levo_szemelyek_adatai:
            c.execute("""
                    INSERT INTO deadPersons (vezeteknev, keresztnev, temetesi_ev, berloId)
                    VALUES(?, ?, ?, ?)
            """, (elem['vezeteknev'], elem['keresztnev'], elem['meghalt_ev'], berlo_id))
        conn.commit()


    elif grave_id is None:
        # NEW RECORD
        c.execute("""
            INSERT INTO grave (parcella, sor, oszlop, temetoId)
            VALUES(?, ?, ?, ?)""", (new_datas['parcell'], new_datas['sor'], new_datas['oszlop'], temeto_id))

        conn.commit()

        row = c.execute("""
                    SELECT rowid FROM grave
                    WHERE temetoId = ?
                    AND parcella = ?
                    AND sor = ?
                    AND oszlop = ?
                    """, (temeto_id, new_datas['parcell'], new_datas['sor'], new_datas['oszlop'])).fetchone()

        grave_id = int(row[0])

        c.execute("""
                    INSERT INTO berlo (berlo_nev, berlo_cim, megvaltas_ok, siremlek_tipus, lejarat_eve, egyeb_megjegyzes, graveId)
                    VALUES(?, ?, ?, ?, ?, ?, ?)""", (new_datas['berlo_nev'], new_datas['berlo_cim'],
                                                  new_datas['megvaltas_oka'], new_datas['siremlek'], new_datas['lejarat_eve'], new_datas['egyeb_megjegyzes'], grave_id))
        conn.commit()

        row = c.execute("""
                            SELECT rowid FROM berlo
                            WHERE graveId = ?
                            """, (grave_id,)).fetchone()

        berlo_id = int(row[0])
        # print(grave_id, berlo_id)
        i = 0
        for elem in range(0, len(sirban_levo_szemelyek_adatai)):
            c.execute("""
                            INSERT INTO deadPersons (vezeteknev, keresztnev, temetesi_ev, berloId)
                            VALUES(?, ?, ?, ?)""", (sirban_levo_szemelyek_adatai[i]['vezeteknev'],
                                                    sirban_levo_szemelyek_adatai[i]['keresztnev'],
                                                    sirban_levo_szemelyek_adatai[i]['meghalt_ev'],
                                                    berlo_id))
            conn.commit()
            i+=1

    c.close()
    conn.close()
    raise_frame(mainframe)


root = tk.Tk()

root.geometry("1300x750")
root.configure(background='#565656', height='900', width='1300')
root.title("Friedhof 1.6")
root.resizable(0, 0)

navimg = Image.open('navbaricon.png')
navimg = navimg.resize((50, 50), Image.ANTIALIAS)
navimg = ImageTk.PhotoImage(navimg)

backbutton = Image.open('close.png')
backbutton = backbutton.resize((50, 50), Image.ANTIALIAS)
backbutton = ImageTk.PhotoImage(backbutton)

addbutton = Image.open('addbutton.png')
addbutton = addbutton.resize((40, 40), Image.ANTIALIAS)
addbutton = ImageTk.PhotoImage(addbutton)

searchbutton = Image.open('searchicon.png')
searchbutton = searchbutton.resize((45, 45), Image.ANTIALIAS)
searchbutton = ImageTk.PhotoImage(searchbutton)

deletebutton = Image.open('deletebutton.png')
deletebutton = deletebutton.resize((40, 40), Image.ANTIALIAS)
deletebutton = ImageTk.PhotoImage(deletebutton)

seebutton = Image.open('seebutton.png')
seebutton = seebutton.resize((40, 40), Image.ANTIALIAS)
seebutton = ImageTk.PhotoImage(seebutton)

### FRAMES
navframe = tk.Frame(root, background='#FADA5E').place(anchor=tk.NW, relwidth=1, height=70)

mainframe = tk.Frame(root, background="#565656")
newgrave = tk.Frame(root, background="#565656")
search = tk.Frame(root, background="#565656")
search_parcells = tk.Frame(root, background="#565656")
search_name = tk.Frame(root, background="#565656")
parcells = tk.Frame(root, background="#565656")
parcells_upper = tk.Frame(root, background="#565656")
parcells_lower = tk.Frame(root, background="#565656")
parcells_list = tk.Frame(root, background="#565656")
nextframe = tk.Frame(root, background="#565656")
secondframe = tk.Frame(root, background="#565656")
namelist = tk.Frame(root, background="#565656")


for frame in (mainframe, newgrave, search, parcells, nextframe, search_parcells, search_name, parcells_upper, parcells_lower, secondframe, namelist, parcells_list):
    frame.place(anchor=tk.NW, y=70, relwidth=1, height=680)

### NAVBAR BUTTONS
tk.Button(navframe, image=navimg, background='#FADA5E',
          activebackground='#FADA5E', bd=0, command=lambda: raise_frame(mainframe)).place(anchor=tk.NW, x=10, y=10)

tk.Button(navframe, background='#FADA5E', bd=0, relief="groove", compound=tk.CENTER, fg="black",
          activeforeground="#818589", activebackground="#FADB5F",
          font="Raleway 20", text="Új adat", command=lambda: raise_frame(newgrave)).place(anchor="center",
                                                                                         relx=.38, rely=.045)

tk.Button(navframe, background='#FADA5E', bd=0, relief="groove", compound=tk.CENTER, fg="black",
          activeforeground="#818589", activebackground="#FADB5F",
          font="Raleway 20", text="Keresés", command=lambda: raise_frame(search)).place(anchor="center", relx=.5, rely=.045)

tk.Button(navframe, background='#FADA5E', bd=0, compound=tk.CENTER, fg="black",
          activeforeground="#71797E", activebackground="#FADB5F",
          font="Raleway 20", text="Parcellák", command=lambda: raise_frame(parcells)).place(anchor="center", relx=.625, rely=.045)

### CONTENT
tk.Label(mainframe, text="Friedhof 1.6", font="Raleway 60", background="#565656").place(anchor="center",
                                                                                        relx=0.5, rely=0.5)

### NEW GRAVE SCREEN
tk.Label(newgrave, text="Új adat felvétele", font="Raleway 60", background="#565656").place(anchor="center",
                                                                                 relx=0.5, rely=0.1)

tk.Label(newgrave, text="Válasszon temetőt:* ", font="Raleway 16", justify=tk.LEFT, anchor='nw', background="#565656").place(anchor="center",
                                                                                 relx=0.35, rely=0.3, width=200)
### VARIABLES
var_megvaltas = tk.StringVar(root)
var_sirhely = tk.StringVar(root)
search_temeto = tk.StringVar(root)
search_parc_temeto = tk.StringVar(root)
parcells_upper_optionmenu = tk.StringVar(root)
parcells_lower_optionmenu = tk.StringVar(root)

### DROPDOWN MENU
af_temeto = tk.StringVar(root)
temetok = ('Felső', 'Alsó')
s = Style()
s.configure("TMenubutton", background="#8c99aa", font="Raleway 12", foreground="#111111")
s.configure('TEntry', background="#8c99aa", font="Raleway 12", foreground="#111111")
opmenu = OptionMenu(newgrave, af_temeto, "Temetők", *temetok)
opmenu.place(anchor="center", relx=0.58, rely=0.3, width=100)

### BEFORE THE FIRST NEXT BUTTON
tk.Label(newgrave, text="Írja be a parcella betűjét:* ", font="Raleway 16", justify=tk.RIGHT, anchor='nw', background="#565656").place(anchor="center",
                                                                                 relx=0.34797, rely=0.4, width=300)

parc = Entry(newgrave, justify=tk.CENTER, font=("Raleway", 13, "bold"))
parc.place(anchor="center", relx=0.5569, rely=0.4, width=40)

tk.Label(newgrave, text="Írja be a sír sorszámát:* ", font="Raleway 16", justify=tk.RIGHT, anchor='nw', background="#565656").place(anchor="center",
                                                                                 relx=0.36, rely=0.5, width=300)

sor = Entry(newgrave, justify=tk.CENTER, font=("Raleway", 13, "bold"))
sor.place(anchor="center", relx=0.5569, rely=0.5, width=40)

tk.Label(newgrave, text="Írja be a sír oszlopát:* ", font="Raleway 16", justify=tk.RIGHT, anchor='nw', background="#565656").place(anchor="center",
                                                                                 relx=0.374, rely=0.6, width=300)

oszlop = Entry(newgrave, justify=tk.CENTER, font=("Raleway", 13, "bold"))
oszlop.place(anchor="center", relx=0.5569, rely=0.6, width=40)


### FIRST NEXT BUTTON
def helper_def_for_next_button(*args):
    checkforok(af_temeto.get(), parc.get(), sor.get(), oszlop.get(), False)


next = tk.Button(newgrave, background='#FADA5E', bd=1, relief="groove", compound=tk.CENTER, fg="black",
          activeforeground="#71797E", activebackground="#FADB5F",
          font="Raleway 16", text="Tovább", command=lambda: checkforok(af_temeto.get(), parc.get(), sor.get(), oszlop.get(), False))
next.bind('<Return>', helper_def_for_next_button)
next.place(anchor="center", relx=.7, rely=.77)


### AFTER FIRST NEXT BUTTON
tk.Label(secondframe, text="Egyéb adatok", font="Raleway 60", background="#565656").place(anchor="center", relx=0.5, rely=0.1)
back_button_second = tk.Button(secondframe, relief = "groove", image=backbutton, background='#565656',
          activebackground='#565656', bd=0, command=lambda: nextframe_raise(newgrave))
back_button_second.place(relx=.03, rely=.03)

b_nev_label = tk.Label(secondframe, text="Írja be a bérlő nevét: ", font="Raleway 16", justify=tk.RIGHT, anchor='nw', background="#565656")

berlo_nev = Entry(secondframe, justify=tk.LEFT, font=("Raleway", 13, "bold"))

b_cim_label = tk.Label(secondframe, text="Írja be a bérlő címét: ", font="Raleway 16", justify=tk.RIGHT, anchor='nw', background="#565656")

berlo_cim = Entry(secondframe, justify=tk.LEFT, font=("Raleway", 13, "bold"))

megvaltas_label = tk.Label(secondframe, text="Válassza ki a megváltás okát: ", font="Raleway 16", justify=tk.RIGHT, anchor='nw', background="#565656")

megvaltas_okok = ("temetés", "előreváltás", "újraváltás")
sirvaltas_oka = OptionMenu(secondframe, var_megvaltas, "Ok", *megvaltas_okok)

sirhely_label = tk.Label(secondframe, text="Válassza ki a síremlék típusát: ", font="Raleway 16", justify=tk.RIGHT, anchor='nw', background="#565656")

sirhely_tipusok = ("műkő", "gránit", "márvány", "síremlék nélküli", "földhantos", "fakereszt", "műkő sírjel")
shely_type = OptionMenu(secondframe, var_sirhely, "Síremlék", *sirhely_tipusok)

lejarat_eve = tk.Label(secondframe, text="Írja be a lejárat évét: ", font="Raleway 16", justify=tk.RIGHT, anchor='nw', background="#565656")
lejarat_year = Entry(secondframe, justify=tk.LEFT, font=("Raleway", 13, "bold"))

egyb_megj = tk.Label(secondframe, text="Egyéb megjegyzés: ", font="Raleway 16", justify=tk.RIGHT, anchor='nw', background="#565656")
egyeb_megjegyzes = Entry(secondframe, justify=tk.LEFT, font=("Raleway", 13, "bold"))

### SECOND NEXT BUTTON
def helper_def_for_sec_next_button(*args):
    checkforok(af_temeto.get(), parc.get(), sor.get(), oszlop.get(), True)

sec_next = tk.Button(secondframe, background='#FADA5E', bd=1, relief="groove", compound=tk.CENTER, fg="black",
          activeforeground="#71797E", activebackground="#FADB5F",
          font="Raleway 16", text="Tovább", command=lambda: checkforok(af_temeto.get(), parc.get(), sor.get(), oszlop.get(), True))

sec_next.bind('<Return>', helper_def_for_sec_next_button)

### AFTER THE SECOND NEXT BUTTON ***NEXTFRAME***
back_button = tk.Button(nextframe, relief = "groove", image=backbutton, background='#565656',
          activebackground='#565656', bd=0, command=lambda: nextframe_raise(secondframe))
back_button.place(relx=.03, rely=.03)

tk.Label(nextframe, text="Sírban lévők felvétele", font="Raleway 60", background="#565656").place(anchor="center",
                                                                                 relx=0.5, rely=0.1)

tk.Label(nextframe, text="Sírban fekvő személy(ek) ", font="Raleway 16", background="#565656", anchor='nw').place(anchor="center", relx=0.3, rely=0.2)

vezeteknev_lab = tk.Label(nextframe, text="Vezetékneve: ", font="Raleway 16", background="#565656", anchor='e')
vezeteknev = Entry(nextframe, justify=tk.LEFT, font=("Raleway", 13, "bold"))
keresztnev_label = tk.Label(nextframe, text="Keresztneve(i): ", font="Raleway 16", background="#565656", anchor='e')
keresztnev = Entry(nextframe, justify=tk.LEFT, font=("Raleway", 13, "bold"))
meghalt_ev_label = tk.Label(nextframe, text="Elhalálozás éve: ", font="Raleway 16", background="#565656", anchor='e')
meghalt_ev = Entry(nextframe, justify=tk.LEFT, font=("Raleway", 13, "bold"))


sirban_levo_szemely_adatok = {
    "vezeteknev": vezeteknev.get(),
    "keresztnev": keresztnev.get(),
    "meghalt_ev": meghalt_ev.get(),
}
sirban_levo_szemelyek_adatai = []
sirban_levo_szemelyek_adatai.append(sirban_levo_szemely_adatok)

### TREEVIEW
s.theme_use("clam")
s.configure("Treeview",
            background="#D3D3D3",
            foreground="black",
            rowheight=25,
            fieldbackground="#D3D3D3"
            )
s.map('Treeview', background=[('selected', '#ffffa1')], foreground=[('selected', 'black')])

tree_frame = tk.Canvas(nextframe)
tree_frame.place(relx=.3, rely=.4)

tree_scroll = Scrollbar(tree_frame)
tree_scroll.pack(side="right", fill="y")

treeview = Treeview(tree_frame, yscrollcommand=tree_scroll.set)
treeview['columns'] = ("Vezetéknév", "Keresztnév", "Elhalálozás éve")
treeview.column("#0", width=0, stretch="NO")
treeview.column("Vezetéknév", anchor="c", width=170)
treeview.column("Keresztnév", anchor="c", width=170)
treeview.column("Elhalálozás éve", anchor="c", width=140)

treeview.heading("#0", anchor="w")
treeview.heading("Vezetéknév", text="Vezetéknév", anchor="c")
treeview.heading("Keresztnév", text="Keresztnév", anchor="c")
treeview.heading("Elhalálozás éve", text="Elhalálozás éve", anchor="c")

treeview.pack()
tree_scroll.configure(command=treeview.yview)


add_button = tk.Button(nextframe, relief = "groove", image=addbutton, background='#565656', activebackground='#565656', bd=0, command= add_member)
delete_button = tk.Button(nextframe, relief = "groove", image=deletebutton, background='#565656', activebackground='#565656', bd=0, command= lambda:del_member(treeview))
save_button = tk.Button(nextframe, background='#FADA5E', bd=1, relief="groove", compound=tk.CENTER, fg="black",
          activeforeground="#71797E", activebackground="#FADB5F",
          font="Raleway 16", text="Mentés", command=save_datas)

### SEARCH SCREEN
tk.Label(search, text="Válasszon keresési formát!", font="Raleway 60", background="#565656").place(anchor="center",
                                                                                 relx=0.5, rely=0.1)

s_with_name_button = tk.Button(search, background='#FADA5E', bd=1, relief="groove", compound=tk.CENTER, fg="black",
          activeforeground="#71797E", activebackground="#FADB5F",
          font="Raleway 16", text="Név/év szerinti keresés", command=lambda: switch_search_frames(search_name))
s_with_name_button.place(anchor="center", relx=0.35, rely=0.3)

s_with_grave_button = tk.Button(search, background='#FADA5E', bd=1, relief="groove", compound=tk.CENTER, fg="black",
          activeforeground="#71797E", activebackground="#FADB5F",
          font="Raleway 16", text="Sír szerinti keresés", command=lambda: switch_search_frames(search_parcells))
s_with_grave_button.place(anchor="center", relx=0.65, rely=0.3)

### SEARCH WITH NAME AND YEAR OF DEATH
search_name_back_button = tk.Button(search_name, relief = "groove", image=backbutton, background='#565656',
          activebackground='#565656', bd=0, command=lambda: raise_frame(search))
search_name_back_button.place(relx=.03, rely=.03)

name_bevezeto = tk.Label(search_name, text="Töltse ki a mezőket!", font="Raleway 22", background="#565656", anchor="center")
search_vezeteknev_lab = tk.Label(search_name, text="Vezetékneve:* ", font="Raleway 16", background="#565656", anchor='e')
search_vezeteknev = Entry(search_name, justify=tk.LEFT, font=("Raleway", 13, "bold"))
search_keresztnev_label = tk.Label(search_name, text="Keresztneve(i):* ", font="Raleway 16", background="#565656", anchor='e')
search_keresztnev = Entry(search_name, justify=tk.LEFT, font=("Raleway", 13, "bold"))
search_meghalt_ev_label = tk.Label(search_name, text="Elhalálozás éve: ", font="Raleway 16", background="#565656", anchor='e')
search_meghalt_ev = Entry(search_name, justify=tk.LEFT, font=("Raleway", 13, "bold"))
search_temeto_label = tk.Label(search_name, text="Temető:* ", font="Raleway 16", background="#565656", anchor='e')
name_alert = tk.Label(search_name, text="Figyelem!\nAz 'Elhalálozás éve' mező kitöltése nem kötelező,\nde csak számot írhat be!", font="Raleway 22", background="#565656", anchor="center", fg="red")

searchmenu = OptionMenu(search_name, search_temeto, "Temetők", *temetok)

search_button = tk.Button(search_name, relief = "groove", image=searchbutton,
                          background='#565656', activebackground='#565656', bd=0, command=name_query)

name_bevezeto.place(anchor="center", relx=0.5, rely=0.07)
search_vezeteknev_lab.place(anchor="center", relx=0.1, rely=0.15, width=200)
search_vezeteknev.place(anchor="center", relx=0.24, rely=0.15, width=150)
search_keresztnev_label.place(anchor="center", relx=0.34, rely=0.15, width=200)
search_keresztnev.place(anchor="center", relx=0.5, rely=0.15, width=200)
search_meghalt_ev_label.place(anchor="center", relx=0.62, rely=0.15, width=200)
search_meghalt_ev.place(anchor="center", relx=0.725, rely=0.15, width=60)
search_temeto_label.place(anchor="center", relx=0.8, rely=0.15, width=100)
searchmenu.place(anchor="center", relx=0.879, rely=0.15, width=100)
search_button.place(anchor="center", relx=.5, rely=.27)
name_alert.place(anchor="center", relx=0.5, rely=0.55)

### SEARCH WITH GRAVE CODES
search_parcell_back_button = tk.Button(search_parcells, relief = "groove", image=backbutton, background='#565656',
          activebackground='#565656', bd=0, command=lambda: raise_frame(search))
search_parcell_back_button.place(relx=.03, rely=.03)

parcells_bevezeto = tk.Label(search_parcells, text="Töltse ki a mezőket!", font="Raleway 22", background="#565656", anchor="center")
search_parcell_lab = tk.Label(search_parcells, text="Parcella:* ", font="Raleway 16", background="#565656", anchor='e')
search_parc = Entry(search_parcells, justify=tk.LEFT, font=("Raleway", 13, "bold"))
search_sor_label = tk.Label(search_parcells, text="Sor:* ", font="Raleway 16", background="#565656", anchor='e')
search_sor = Entry(search_parcells, justify=tk.LEFT, font=("Raleway", 13, "bold"))
search_oszlop_label = tk.Label(search_parcells, text="Oszlop:* ", font="Raleway 16", background="#565656", anchor='e')
search_oszlop = Entry(search_parcells, justify=tk.LEFT, font=("Raleway", 13, "bold"))
search_temeto_label_parcell = tk.Label(search_parcells, text="Temető:* ", font="Raleway 16", background="#565656", anchor='e')

searchmenu_parc = OptionMenu(search_parcells, search_parc_temeto, "Temetők", *temetok)

search_parc_button = tk.Button(search_parcells,
                               relief = "groove", image=searchbutton,
                               background='#565656', activebackground='#565656', bd=0, command=lambda: gravekod_search_check(search_parc.get(), search_sor.get(), search_oszlop.get(), search_parc_temeto.get()))

parcells_bevezeto.place(anchor="center", relx=0.5, rely=0.07)
search_parcell_lab.place(anchor="center", relx=0.3, rely=0.15, width=100)
search_parc.place(anchor="center", relx=0.36, rely=0.15, width=40)
search_sor_label.place(anchor="center", relx=0.42, rely=0.15, width=100)
search_sor.place(anchor="center", relx=0.48, rely=0.15, width=40)
search_oszlop_label.place(anchor="center", relx=0.57, rely=0.15, width=100)
search_oszlop.place(anchor="center", relx=0.63, rely=0.15, width=40)
search_temeto_label_parcell.place(anchor="center", relx=0.7, rely=0.15, width=100)
searchmenu_parc.place(anchor="center", relx=0.78, rely=0.15, width=100)
search_parc_button.place(anchor="center", relx=.5, rely=.27)

### SHARED PROPERTYS THE TWO LIST FRAME
tk.Label(namelist, text="Keresési eredmények", font="Raleway 60", background="#565656").place(anchor="center",
                                                                                                  relx=0.5, rely=0.1)
namelist_tree_frame = tk.Canvas(namelist)
namelist_tree_frame.place(relx=.055, rely=.2)

scrollbar = Scrollbar(namelist_tree_frame)
scrollbar.pack(side="right", fill="y")

treeview_namelist = Treeview(namelist_tree_frame, yscrollcommand=scrollbar.set, height=15)
treeview_namelist['columns'] = ("Vezetéknév", "Keresztnév", "Elhalálozás éve", "Temető", "Parcella", "Sor", "Oszlop")
treeview_namelist.column("#0", width=0, stretch="NO")
treeview_namelist.column("Vezetéknév", anchor="c", width=200)
treeview_namelist.column("Keresztnév", anchor="c", width=200)
treeview_namelist.column("Elhalálozás éve", anchor="c", width=150)
treeview_namelist.column("Temető", anchor="c", width=150)
treeview_namelist.column("Parcella", anchor="c", width=150)
treeview_namelist.column("Sor", anchor="c", width=150)
treeview_namelist.column("Oszlop", anchor="c", width=150)

treeview_namelist.heading("#0", anchor="w")
treeview_namelist.heading("Vezetéknév", text="Vezetéknév", anchor="c")
treeview_namelist.heading("Keresztnév", text="Keresztnév", anchor="c")
treeview_namelist.heading("Elhalálozás éve", text="Elhalálozás éve", anchor="c")
treeview_namelist.heading("Temető", text="Temető", anchor="c")
treeview_namelist.heading("Parcella", text="Parcella", anchor="c")
treeview_namelist.heading("Sor", text="Sor", anchor="c")
treeview_namelist.heading("Oszlop", text="Oszlop", anchor="c")

treeview_namelist.pack()
scrollbar.configure(command=treeview_namelist.yview)

# see_button = tk.Button(namelist, relief = "groove", image=seebutton,
#                           background='#565656', activebackground='#565656', bd=0, command="None")
# see_button.place(anchor="center", relx=.45, rely=.9)
deleterow_button = tk.Button(namelist, relief = "groove", image=deletebutton,
                          background='#565656', activebackground='#565656', bd=0, command=delete_item)
deleterow_button.place(anchor="center", relx=.55, rely=.9)

back_button_for_lists = tk.Button(namelist, relief = "groove", image=backbutton, background='#565656',
          activebackground='#565656', bd=0, command=lambda: raise_frame(search))
back_button_for_lists.place(relx=.03, rely=.03)

### PARCELLS SCREEN
tk.Label(parcells, text="Válasszon temetőt!", font="Raleway 60", background="#565656").place(anchor="center", relx=0.5, rely=0.1)

parcells_choose_grave_felso = tk.Button(parcells, background='#FADA5E', bd=1, relief="groove", compound=tk.CENTER, fg="black",
          activeforeground="#71797E", activebackground="#FADB5F",
          font="Raleway 16", text="Felső temető", command=lambda: parcells_frame_switch(parcells_upper))
parcells_choose_grave_felso.place(anchor="center", relx=0.35, rely=0.3)

parcells_choose_grave_also = tk.Button(parcells, background='#FADA5E', bd=1, relief="groove", compound=tk.CENTER, fg="black",
          activeforeground="#71797E", activebackground="#FADB5F",
          font="Raleway 16", text="Alsó temető", command=lambda: parcells_frame_switch(parcells_lower))
parcells_choose_grave_also.place(anchor="center", relx=0.65, rely=0.3)

### PARCELLÁK
felso_parcells = ('A','Aa', 'B', 'C', 'D', 'E',
                  'F', 'G', 'H', 'I', 'J-1', 'J-2',
                  'J-3', 'J-4', 'J-5', 'K-1', 'K-2',
                  'K-3', 'L-1', 'L-2', 'L-3', 'L-4',
                  'L-5', 'L-6', 'M-1', 'M-2', 'N', 'N-1',
                  'O-1', 'O-2', 'O-3', 'O-4', 'O-5', 'O-6', 'O-7',
                  'N-2', 'N-3', 'P-1', 'P-2', 'P-3', 'P-4', 'P-5',
                  'R-1', 'R-2', 'R-3', 'R-4', 'R-5', 'R-6', 'R-7',
                  'S-1', 'S-2', 'S-3', 'S-4', 'UP1', 'UP2')

also_parcells = ('A', 'B', 'C', 'D', 'D-1', 'E', 'F', 'G', 'H', 'I', 'J', 'K-1', 'K-2', 'L-1', 'L-2', 'M', 'N', 'O')

### PARCELLS_UPPER GRAVE
upper_grave_backbutton = tk.Button(parcells_upper, relief = "groove", image=backbutton, background='#565656',
          activebackground='#565656', bd=0, command=lambda: raise_frame(parcells))

parcell_choose_lab = tk.Label(parcells_upper, text="Válasszon parcellát:*", font="Raleway 16", background="#565656", anchor='e')
parcell_choose_lab.place(anchor="center", relx=0.35, rely=0.15, width=200)

upper_optionmenu = Combobox(parcells_upper, textvariable=parcells_upper_optionmenu, values=felso_parcells, state='readonly')
upper_optionmenu.place(anchor="center", relx=0.5, rely=0.15, width=100)
upper_parc_searchbutton = tk.Button(parcells_upper,
                               relief = "groove", image=searchbutton,
                               background='#565656', activebackground='#565656', bd=0, command=lambda: parcells_check(parcells_upper_optionmenu.get(), 1))
upper_parc_searchbutton.place(anchor="center", relx=.65, rely=.15)


### PARCELLS_LOWER GRAVE
lower_grave_backbutton = tk.Button(parcells_lower, relief = "groove", image=backbutton, background='#565656',
          activebackground='#565656', bd=0, command=lambda: raise_frame(parcells))

lower_parcell_choose_lab = tk.Label(parcells_lower, text="Válasszon parcellát:*", font="Raleway 16", background="#565656", anchor='e')
lower_parcell_choose_lab.place(anchor="center", relx=0.35, rely=0.15, width=200)

lower_optionmenu = Combobox(parcells_lower, textvariable=parcells_lower_optionmenu, values=also_parcells, state='readonly')
lower_optionmenu.place(anchor="center", relx=0.5, rely=0.15, width=100)
lower_parc_searchbutton = tk.Button(parcells_lower,
                               relief = "groove", image=searchbutton,
                               background='#565656', activebackground='#565656', bd=0, command=lambda: parcells_check(parcells_lower_optionmenu.get(), 2))
lower_parc_searchbutton.place(anchor="center", relx=.65, rely=.15)


### PARCELLS LIST
expire_button = tk.Button(parcells_list, background='#FADA5E', bd=1, relief="groove", compound=tk.CENTER, fg="black",
          activeforeground="#71797E", activebackground="#FADB5F",
          font="Raleway 16", text="Lejártak Excelbe listázása", command= excelbe_rendez)
expire_button.place(anchor="center", relx=.5, rely=.9)

back_button_for_parcells = tk.Button(parcells_list, relief = "groove", image=backbutton, background='#565656',
          activebackground='#565656', bd=0, command=lambda: raise_frame(parcells))
back_button_for_parcells.place(relx=.03, rely=.03)

tk.Label(parcells_list, text="Sírok listája", font="Raleway 60", background="#565656").place(anchor="center", relx=0.5, rely=0.1)
parcells_list_frame= tk.Canvas(parcells_list)
parcells_list_frame.place(relx=.21, rely=.2)

parcells_scrollbar = Scrollbar(parcells_list_frame)
parcells_scrollbar.pack(side="right", fill="y")

parcells_treeview = Treeview(parcells_list_frame, yscrollcommand=parcells_scrollbar.set, height=15)
parcells_treeview['columns'] = ("Sor", "Oszlop", "Bérlő", "Lejárat")
parcells_treeview.column("#0", width=0)
parcells_treeview.column("Sor", anchor="c", width=100)
parcells_treeview.column("Oszlop", anchor="c", width=100)
parcells_treeview.column("Bérlő", anchor="c", width=300)
parcells_treeview.column("Lejárat", anchor="c", width=300)

parcells_treeview.heading("#0", anchor="w")
parcells_treeview.heading("Sor", text="Sor", anchor="c")
parcells_treeview.heading("Oszlop", text="Oszlop", anchor="c")
parcells_treeview.heading("Bérlő", text="Bérlő", anchor="c")
parcells_treeview.heading("Lejárat", text="Lejárat", anchor="c")

parcells_treeview.pack()
parcells_scrollbar.configure(command=parcells_treeview.yview)


### END CODES
raise_frame(mainframe)
root.mainloop()
