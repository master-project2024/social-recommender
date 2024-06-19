import streamlit as st
from streamlit_option_menu import option_menu
#import pickle
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt

with st.sidebar :
    choose = option_menu("Menu", ["Accueil", "Prétraitement", "Extraction des caractéristiques", "Classification", "Contact", "Aide"],
                         icons=['house', 'gear-wide', 'table', 'stars','person lines fill'],
                         menu_icon="menu-app",
                         styles={
        "container": {"padding": "5!important", "background-color": "#fafafa"},
        "icon": {"color": "orange", "font-size": "25px"}, 
        "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "#02ab21"},
    }
    )

if choose == "Accueil" :
    st.title( "Reconnaissance des mots arabes manuscrits pris de la base de données IFN/ENIT" )
    st.write( "### Après avoir choisi un jeu de données et un fenêtrage, vous pouvez tester une image de la base de données et observer le prétraitement utilisé, l'extraction de ses caractéristiques et sa classification." )

elif choose == "Prétraitement" :
    st.write( "### Nous sommes toujours ravis de votre contact!" )
    
elif choose == "Classification" : 
    st.write( "### Nous sommes toujours ravis de votre contact!" )
    
elif choose == "Contact" :
    st.write( "### Nous sommes toujours ravis de votre contact!" )
    st.write( "### Envoyez-nous un e-mail et dites-nous comment nous pouvons vous aider via cet mail : reconnaissance.manu.arb@gmail.com " )
    
elif choose == "Aide" :
    st.write( "### - CSS : Caractéristiques statistiques et structurelles" )
    st.write( "### - Codage de Freeman avec chaîne normalisée : Caractéristiques extraites de la chaîne de code avec chaîne normalisée" )
    st.write( "### - Codage de Freeman avec fréquences cumulées : Caracteristiques extraites de la chaine de code avec fréquences cumulées" )
    
