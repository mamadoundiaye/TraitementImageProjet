import psycopg2
from .ocrapi import *
from .models import *
import json
from django.core.mail import send_mail

candidats = Candidat.objects.all()

# person = Person(first_name="John", last_name="Deo")
# person.save()
# liste_git = Etudiant.objects.filter(departement=dep_num)


print("hello middleware")

# la partie bd distant
def bddistant():
    depots = []
    try:
        conn = psycopg2.connect(
            database="crplntnd",
            user="crplntnd",
            password="UCEnMwEkf9RsH8g1foq1Y-JAY5pu984N",
            host="hattie.db.elephantsql.com",
            port="5432",
        )
        # postgres://crplntnd:UCEnMwEkf9RsH8g1foq1Y-JAY5pu984N@hattie.db.elephantsql.com/crplntnd
        print("Opened database successfully")
        cur = conn.cursor()
        cur.execute("select * from eptconcours__r_ponses_reponses")
        depots = cur.fetchall()
        conn.close()
    except:
        print("connection a la base de donnees ehouee")
    return depots


def peuplerbdinitial(depots):
    if len(depots) != 0:
        for depot in depots:
            lienseconde = depot[8].split("=")[1]
            lienpremiere = depot[9].split("=")[1]
            lienterminale = depot[10].split("=")[1]
            lienreleve = depot[11].split("=")[1]

            print("trying THE OCR ********")
            moyseconde = ocr_space_url(
                url="https://drive.google.com/uc?export=view&id=" + lienseconde
            )
            moypremiere = ocr_space_url(
                url="https://drive.google.com/uc?export=view&id=" + lienpremiere
            )
            moyterminale = ocr_space_url(
                url="https://drive.google.com/uc?export=view&id=" + lienterminale
            )
            moyreleve = ocr_space_url(
                url="https://drive.google.com/uc?export=view&id=" + lienreleve
            )

            moysecondejson = json.loads(moyseconde)
            moypremierejson = json.loads(moypremiere)
            moyterminalejson = json.loads(moyterminale)
            moyrelevejson = json.loads(moyreleve)

            seconde = (
                moysecondejson["ParsedResults"][0]["ParsedText"]
                .split("MOYENNE :")[1]
                .split("\r")[0]
            )
            premiere = (
                moypremierejson["ParsedResults"][0]["ParsedText"]
                .split("MOYENNE :")[1]
                .split("\r")[0]
            )
            terminale = (
                moyterminalejson["ParsedResults"][0]["ParsedText"]
                .split("MOYENNE :")[1]
                .split("\r")[0]
            )
            releve = (
                moyrelevejson["ParsedResults"][0]["ParsedText"]
                .split("MOYENNE :")[1]
                .split("\r")[0]
            )

            print("saving to the database")
            candidat = Candidat(
                prenom=depot[1],
                nom=depot[2],
                lycee=depot[3],
                mail=depot[4],
                telephone=depot[5],
                genie=depot[7],
                centre=depot[6],
                moy_seconde=float(seconde),
                moy_premiere=float(premiere),
                moy_terminale=float(terminale),
                moy_bac=float(releve),
            )
            candidat.save()
            print("saving done")


depots = bddistant()
peuplerbdinitial(depots[len(candidats) :])
print(len(depots) == len(candidats))


class MyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        """
        on verifie s'il y'a de nouveaux enregistrements
        si oui on les parcour et on update notre base locale

        mise_a_jour = bddistant()
        actuel = Candidat.objects.all()
        if len(mise_a_jour) > len(actuel):
            newdonnees = mise_a_jour[len(actuel) :]
            peuplerbdinitial(newdonnees)
        """

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.
        # print("good bye")

        return response
