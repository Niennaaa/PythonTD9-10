# -*- coding: utf-8 -*-


## ON UTILISE STREAMLIT 

# to open the file : (windows)
#     1) open anaconda prompt and enter : cd "C:\Users\Jehanne\Desktop\ESILV\S6\Python\Projet"
#     2) enter : streamlit run myfile.py
#     3) activer 'settings'->'run on save' pour que l'app se relance à chaque sauvegarde
#           
#     si y'a des pb de memoire limite (c'est précisé 200mb) entrer ça plutot (changer les chiffres selon la taille necessaire)
#     streamlit run myfile.py --server.maxUploadSize 1000 --server.maxMessageSize 1000


import streamlit as st
import pandas as pd
import plotly.express as px


st.title('Plots sur les données en 2021')

# utiliser @st.cache avant les fonctions qui prennent du temps à reload, elles ne seront pas rechargées si elles sont non modifiées
# Chargement et nettoyage des données
@st.cache(allow_output_mutation=True)
def load_data(nrows=5,usecols=["Date mutation","Nature mutation","Valeur fonciere","Type de voie","Commune","Code departement","Nombre de lots","Type local","Surface reelle bati","Nombre pieces principales","Surface terrain"]): # FONCTION A NE PAS MODIFIER SOUS PEINE D'UN TEMPS DE CHARGEMENT DE MILLE ANS
    
    
    # Url des tables
    VF2021="https://static.data.gouv.fr/resources/demandes-de-valeurs-foncieres/20220408-143516/valeursfoncieres-2021.txt"

    df2021 = pd.read_csv(VF2021, sep="|", header=0, nrows=nrows, usecols=usecols)
    df2021 = df2021.dropna(axis=1, how="all", thresh=int(df2021.shape[0]*0.5)) #on drop toutes les colonnes vides à 50%
    df2021 = df2021.fillna(0) #on remplace les NaN par des 0 pour eviter les erreurs plus tard

    
    # Conversion de Valeur fonciere en float 
    conv_to_float = lambda x : float(str(x).replace(",","."))
    df2021["Valeur fonciere"]=df2021.loc[:,"Valeur fonciere"].apply(conv_to_float)
    
    # # Conversion des Dates mutation en dates 
    df2021["Date mutation"] = pd.to_datetime(df2021["Date mutation"])
    

    # # Conversion de certaines tables objet en string car sinon streamlit essaie de les convertir en int et leve une erreur
    # # mais y'a certaines années où les données passent jsp pk :l    

    
    #df2021["Type de voie"]=df2021["Type de voie"].astype(str)
    #df2021["Code voie"]=df2021["Code voie"].astype(str)
    #df2021["Voie"]=df2021["Voie"].astype(str)
    #df2021["Code departement"]=df2021["Code departement"].astype(str)
    #df2021["Section"]=df2021["Section"].astype(str)
    #df2021["Type local"]=df2021["Type local"].astype(str)
    #df2021["Nature culture"]=df2021["Nature culture"].astype(str)
    
    return df2021


#les autres années
@st.cache(allow_output_mutation=True)
def loadelse(nrows=5,usecols=["Valeur fonciere","Date mutation", "Surface terrain"]):
    VF2020="https://static.data.gouv.fr/resources/demandes-de-valeurs-foncieres/20220408-143240/valeursfoncieres-2020.txt"
    VF2019="https://static.data.gouv.fr/resources/demandes-de-valeurs-foncieres/20220408-142854/valeursfoncieres-2019.txt"
    VF2018="https://static.data.gouv.fr/resources/demandes-de-valeurs-foncieres/20220408-142623/valeursfoncieres-2018.txt"
    VF2017="https://static.data.gouv.fr/resources/demandes-de-valeurs-foncieres/20220408-141722/valeursfoncieres-2017.txt"
    
    df2017 = pd.read_csv(VF2017, sep="|", header=0, usecols=usecols, nrows=nrows)
    df2017 = df2017.dropna(axis=1, how="all", thresh=int(df2017.shape[0]*0.5)) #on drop toutes les colonnes vides à 50%
    df2017 = df2017.fillna(0) #on remplace les NaN par des 0 pour eviter les erreurs plus tard
    
    df2018 = pd.read_csv(VF2018, sep="|", header=0, usecols=usecols, nrows=nrows)
    df2018 = df2018.dropna(axis=1, how="all", thresh=int(df2018.shape[0]*0.5)) #on drop toutes les colonnes vides à 50%
    df2018 = df2018.fillna(0) #on remplace les NaN par des 0 pour eviter les erreurs plus tard
    
    df2019 = pd.read_csv(VF2019, sep="|", header=0, usecols=usecols, nrows=nrows)
    df2019 = df2019.dropna(axis=1, how="all", thresh=int(df2019.shape[0]*0.5)) #on drop toutes les colonnes vides à 50%
    df2019 = df2019.fillna(0) #on remplace les NaN par des 0 pour eviter les erreurs plus tard
    
    df2020 = pd.read_csv(VF2020, sep="|", header=0, usecols=usecols, nrows=nrows)
    df2020 = df2020.dropna(axis=1, how="all", thresh=int(df2020.shape[0]*0.5)) #on drop toutes les colonnes vides à 50%
    df2020 = df2020.fillna(0) #on remplace les NaN par des 0 pour eviter les erreurs plus tard
    
    # Conversion de Valeur fonciere en float 
    conv_to_float = lambda x : float(str(x).replace(",","."))
    df2017["Valeur fonciere"]=df2017.loc[:,"Valeur fonciere"].apply(conv_to_float)
    df2018["Valeur fonciere"]=df2018.loc[:,"Valeur fonciere"].apply(conv_to_float)
    df2019["Valeur fonciere"]=df2019.loc[:,"Valeur fonciere"].apply(conv_to_float)
    df2020["Valeur fonciere"]=df2020.loc[:,"Valeur fonciere"].apply(conv_to_float)            
    # Conversion des Dates mutation en dates 
    df2017["Date mutation"] = pd.to_datetime(df2017["Date mutation"])
    df2018["Date mutation"] = pd.to_datetime(df2018["Date mutation"])
    df2019["Date mutation"] = pd.to_datetime(df2019["Date mutation"])
    df2020["Date mutation"] = pd.to_datetime(df2020["Date mutation"])
    return df2020,df2019,df2018,df2017



# Chargement des tables (histoire de voir où ça tourne)
data_load_state = st.text('Loading 2021...')

df2021= load_data(nrows=100,
                  usecols=["Date mutation","Nature mutation","Valeur fonciere","Type de voie","Commune","Code departement","Nombre de lots","Type local","Surface reelle bati","Nombre pieces principales","Surface terrain","No disposition","Code postal","Nombre de lots"])#mettre un entier pour load ce nb de ligne. None load tout.


dataelse=[k for k in loadelse(nrows=100, usecols=["Valeur fonciere","Date mutation", "Surface terrain","Nature mutation","Type de voie","Surface reelle bati","Nombre pieces principales"])]

liste_annee=["2020","2019","2018","2017"]
liste_data=dataelse
df2017=dataelse[3]
df2018=dataelse[2]
df2019=dataelse[1]
df2020=dataelse[0]
df2021["Annee"]=2021
df2020["Annee"]=2020
df2019["Annee"]=2019
df2018["Annee"]=2018
df2017["Annee"]=2017

# when you change the amount of nrows, some columns stops working. 
# add/remove those lines accordingly to what doesn't work
df2021["Code departement"]=df2021["Code departement"].astype(str)
df2021["Type local"]=df2021["Type local"].astype(str)
df2021["Type de voie"]=df2021["Type de voie"].astype(str)

df2019["Type de voie"]=df2019["Type de voie"].astype(str)
df2017["Type de voie"]=df2017["Type de voie"].astype(str)

df2017["Nombre pieces principales"]=df2017["Nombre pieces principales"].astype(str)
df2019["Nombre pieces principales"]=df2019["Nombre pieces principales"].astype(str)
df2020["Nombre pieces principales"]=df2020["Nombre pieces principales"].astype(str)
df2021["Nombre pieces principales"]=df2021["Nombre pieces principales"].astype(str)

df2017["Surface terrain"]=df2017["Surface terrain"].astype(float)
df2018["Surface terrain"]=df2018["Surface terrain"].astype(float)
df2019["Surface terrain"]=df2019["Surface terrain"].astype(float)
df2020["Surface terrain"]=df2020["Surface terrain"].astype(float)
df2021["Surface terrain"]=df2021["Surface terrain"].astype(float)


dataelse=[df2017, df2018, df2019, df2020]

data_load_state.text("All data loaded")


#### Ne pas toucher ce qu'il y a au dessus, risque de temps de chargement terribles





## Now lets get into plotting

st.header("Un aperçu du tableau de 2021..")
st.write(df2021)

if st.checkbox("Voir les autres années ?"):
    a = st.selectbox("Choisir une année", liste_annee)
    st.write(liste_data[liste_annee.index(a)])


####

st.header("Valeur fonciere en fonction du temps")
st.subheader("Par commune en 2021 : ")
commune = st.selectbox("Choisir une commune", df2021["Commune"].unique(), key=1)

fig1 = px.scatter(df2021.loc[df2021["Commune"]==commune],"Date mutation","Valeur fonciere")
st.plotly_chart(fig1)

#####

st.header("Nombre de lots par date de mutation")
st.write("La taille correspond à la valeur foncière")
typ = st.select_slider("Par type de local : ", df2021["Type local"].unique())
figa=px.scatter(df2021.loc[df2021["Type local"]==typ],x="Date mutation",y="Nombre de lots",size="Valeur fonciere", color="Valeur fonciere")
st.plotly_chart(figa)


####

st.header("Pourcentage du nombre de pieces")
local = st.checkbox("Voir pour un certain type de local ?")

if local:
    local2=st.selectbox("Choisir local : ", ["Appartement","Maison"])
    figb=px.pie(df2021.loc[df2021["Type local"]==local2],values="Nombre pieces principales", names="Nombre pieces principales")
else:
    figb=px.pie(df2021,values="Nombre pieces principales", names="Nombre pieces principales", color="Nombre pieces principales")
st.plotly_chart(figb) 


####


st.header("Valeur fonciere en fonction de la surface réelle bati")
st.subheader("Par commune en 2021 : ")

commune2 = st.selectbox("Choisir une commune", df2021["Commune"].unique(), key=2)


fig9 = px.line(df2021.loc[df2021["Commune"]==commune2],"Surface reelle bati","Valeur fonciere")
st.plotly_chart(fig9)


####

st.header("Nature des mutations au cours du temps")
val = st.slider("Valeur fonciere à inclure", 0, 1000000,1000000)
figc= px.scatter(df2021.loc[df2021["Valeur fonciere"]<val],x="Date mutation",y="Nature mutation", color="Valeur fonciere")
st.plotly_chart(figc)


#####

st.header("Surface des terrains au cours du temps")
st.write("La taille des bulles correpond à la valeur foncière")
val2 = st.slider("Surface terrains à inclure", 0, 55000,55000)
figc= px.scatter(df2021.loc[df2021["Surface terrain"]<val2],x="Date mutation",y="Surface terrain", size="Valeur fonciere", color="Type local")
st.plotly_chart(figc)



##### A PARTIR DE LA, COMPARAISON ENTRE LES ANN2ES


st.title("Comparaison avec les années precedentes")

st.subheader("De 2017 à 2021 : ")

allData=df2021.copy()
for k in dataelse:
    allData=allData.merge(k, how="outer")

fig2 = px.scatter(allData, x="Date mutation", y="Valeur fonciere",color="Annee", marginal_y="violin",
            trendline="ols", template="simple_white")
st.plotly_chart(fig2)


####


st.header("Comparaison du prix en fonction de la surface du terrain entre les années")

temp = allData.groupby('Surface terrain')["Valeur fonciere"].sum().reset_index()
temp = temp.melt(id_vars='Surface terrain', value_vars=["Valeur fonciere"],
                 var_name='Années', value_name='Valeur fonciere')
temp.head()
y_slider = st.slider('Valeur fonciere max : ', 0, 1000000,1000000)

fig3 = px.area(allData.loc[allData["Valeur fonciere"]!=0], x='Surface terrain', y="Valeur fonciere", color='Annee', height=600, width=700, range_y=[0,y_slider])
fig3.update_layout(xaxis_rangeslider_visible=True)
st.plotly_chart(fig3)


#####


st.header("Comparaison du nombre de types de voie entre années")
fig4 = px.bar(allData, x="Nature mutation", y="Annee",
              hover_data=['Nature mutation'], color='Annee', height=800)
st.plotly_chart(fig4)


####


st.header("Comparaison des valeurs fonciere totales entre les années")
mois = st.checkbox("Passer en années/somme sur tout les mois")
allData['Mois'] = pd.DatetimeIndex(allData['Date mutation']).month_name()
pris=""
if mois:
    pris="Mois" 
else:
    pris="Annee"
    
fig5 = px.pie(allData, values='Valeur fonciere', names=pris, color=pris)
st.plotly_chart(fig5)


####



st.header("Comparaison des valeurs fonciere en fonction de la surface réelle bati par année")
st.write("La taille des bulles correspond à la surface du terrain")

slidertaille = st.slider("Ajouter des années à inclure :", 2017,2021,2021)
fig6 = px.scatter(allData.loc[allData["Annee"]<=slidertaille], x="Surface reelle bati", y="Valeur fonciere",
	         size="Surface terrain", color="Annee",
                 hover_name="Annee", log_x=True, size_max=200, height=800, width=800)
st.plotly_chart(fig6)

liste_data=[df2017,df2018,df2019,df2020,df2021]
liste_annee=["2017","2018","2019","2020","2021"]

####



st.header("Nombre de pièces principales en fonction de la surface réelle bati")
allData["Nombre pieces principales"]=allData["Nombre pieces principales"].astype(float)

d2017=allData.loc[allData["Annee"]==2017]
d2018=allData.loc[allData["Annee"]==2018]
d2019=allData.loc[allData["Annee"]==2019]
d2020=allData.loc[allData["Annee"]==2020]
d2021=allData.loc[allData["Annee"]==2021]


ch = st.radio("Choisir les annee à visualiser (2018 n'a pas de data disponible et 2020 fait crash l'appli :confused_smiley:)", (2017,2019,2021))

fig7=px.scatter(allData.loc[allData["Annee"]==ch],x="Surface reelle bati", y="Nombre pieces principales",color="Type de voie")

st.plotly_chart(fig7)


