# Generated by Django 3.2.14 on 2024-04-24 15:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cc_courses', '0070_merge_20240424_1217'),
        ('coopolis', '0126_merge_20240424_1217'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='id_number_backup',
            field=models.CharField(editable=False, max_length=11, null=True, verbose_name='Còpia de seguretat id_number'),
        ),
        migrations.AlterField(
            model_name='createdentity',
            name='sub_service',
            field=models.SmallIntegerField(choices=[(None, 'Cap'), (101, "1 a  Taula territorial per l'articulació conjunta de l'economia social amb els diversos actors (ATENEU)"), (102, "1 b  Elaboració d'un catàleg bones pràctiques (ATENEU I CERCLES)."), (103, '1 c Organització de jornades per visibilitzar experiències, presència als mitjans de comunicació locals, assistència a fires, actes i premis, trobades sectorials, col·laboracions amb altres iniciatives (ATENEU)'), (199, '1 d Altres accions dins del servei de mapeig i diagnosi (ATENEU I CERCLES).'), (104, "1 e Identificar actes, jornades, fires, programes i publicacions que ja s'estan duent a terme al territori on sigui interessant i factible la participació o la col·laboració de l'ateneu cooperatiu. (ATENEU)"), (201, '2 a Campanya de comunicació i difusió a col·lectius especial atenció. Materials difusió fórmula cooperativa. (ATENEU)'), (202, '2 b Tallers dirigits a joves estudiants de cicles formatius. (ATENEU)'), (203, '2 c Accions per a la creació de diferents classes de cooperatives. (CERCLES)'), (204, '2 d Diagnosi sobre les mancances i oportunitats socioeconòmiques i identificació de les empreses participants (CERCLES)'), (205, "2 e Sessions col·lectives i d'acompanyament expert individual (CERCLES)"), (299, '2 f Altres accions dins del servei de divulgació, sensibilització i generació de coneixement.'), (206, '2 g Difusió materials (Ateneu)'), (207, '2 h Elaboració material específic sobre la fórmula cooperativa (ATENEU)'), (208, '2 i Accions de sensibilització (ATENEU I CERCLES)'), (301, '3 a Activitats formatives i informatives (ATENEU)'), (302, '3 b Tallers de formació bàsica a persones emprenedores interessades en la fòrmula cooperativa (ATENEU)'), (303, '3 c Sessions col·lectives (ATENEU)'), (304, '3 d Acompanyament expert (ATENEU)'), (305, '3 e Tallers de sensibilització o dinamització adreçada al teixit associatiu i a les empreses (ATENEU I CERCLES)'), (399, '3 f  Altres accions dins del servei de formació.'), (306, "3 g Tallers de sensibilització o dinamització adreçada a professionals que s'agrupen (ATENEU I CERCLES)"), (401, "4 a Assessorament a mida per a la creació de cooperatives i altres organitzacions d'ESS (ATENEU i CERCLES)"), (402, '4 b Acompanyament a la consolidació i creixement de cooperatives existents (ATENEU i CERCLES)'), (403, "4 c Acompanyament a la transformació d'empreses ( ATENEU I CERCLES)"), (404, '4 d Campanya de comunicació i difusió (CERCLES)'), (405, '4 e Accions de sensibilització o dinamització (CERCLES)'), (499, "4 f Altres accions dins del servei d'acompanyament."), (501, "5 a Generar espais d'intercooperació i treball en xarxa dins del territori, intercooperació local, creació d'espais i grups d'intercooperació (ATENEU)"), (502, "5 b Incorporació d'empreses a l'ateneu cooperatiu (ATENEU)"), (503, '5 c Treball en xarxa amb altres ateneus: assistir a reunions i col·laborar en iniciatives conjuntes (ATENEU)'), (599, '5 d Altres accions dins del servei de facilitació de la intercooperació.'), (504, '5 e Assemblea ateneu '), (505, '5 f Assemblea XAC'), (601, '6 a Espai físic per proporcionar informació sobre ESS a diferents públics (ATENEU I CERCLES)'), (602, "6 b Punt o punts d'informació (ATENEU I CERCLES)"), (701, '7 a Serveis Complementaris (ATENEU I CERCLES)')], null=True, verbose_name='(Obsolet) Sub-servei'),
        ),
        migrations.AlterField(
            model_name='employmentinsertion',
            name='activity',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='employment_insertions', to='cc_courses.activity', verbose_name='sessió'),
        ),
        migrations.AlterField(
            model_name='user',
            name='id_number',
            field=models.CharField(help_text="Si degut a la teva situació legal et suposa un inconvenient indicar el DNI, deixa'l en blanc.", max_length=11, null=True, verbose_name='DNI/NIE/Passaport'),
        ),
    ]
