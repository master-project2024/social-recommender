import streamlit as st
import pickle
import pandas as pd
import numpy as np
import cv2
import os
import matplotlib.pyplot as plt
from PIL import Image
from sklearn.preprocessing import MinMaxScaler
from streamlit_option_menu import option_menu

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


def contour( pic ): 
    contours2 = np.zeros( pic.shape )
    
    for j in range( pic.shape[1] ) :
        color = 'black'
        for i in range( pic.shape[0] ) :
            if( pic[i][j] == 255 and color=='black' ) :
                contours2[i][j] = 255
                color = 'white'
            elif( pic[i][j] == 0 and color=='white' ) :
                contours2[i-1][j] = 255
                color = 'black'
                
    for i in range( pic.shape[0] ) :
        color = 'black'
        for j in range( pic.shape[1] ) :
            if( pic[i][j] == 255 and color == 'black' ) :
                contours2[i][j] = 255
                color = 'white'
            elif( pic[i][j] == 0 and color == 'white' ) :
                contours2[i][j-1] = 255
                color = 'black'
    contours2 = contours2.astype(np.uint8) 
    return contours2

from PIL import Image
def fenetrage(image,Nb_fenetres,Chevauchement):

    #le fenetrage consiste a diviser l'image en blocs
    # ici on divise l'image a 4 fenetres 
    # le largeur de la fenetre est le 1er entier superieur au largeur/4
    Fenetres = []
    [x , y]=image.shape

    if(x>0 and y>12):
        while((y+Chevauchement*(Nb_fenetres-1)) % Nb_fenetres) != 0 :
            y=y+1
        image  = np.array(Image.fromarray(image).resize((y, x), Image.NEAREST))

        Largeur_fenetre=(y+Chevauchement*(Nb_fenetres-1))//Nb_fenetres; 
        
        Fin = y;
        a= Fin-Largeur_fenetre
        Fenetres=[image[0:x,a:Fin]];
        for k in range (Nb_fenetres-1):
            Fin=Fin-Largeur_fenetre+Chevauchement
            a= Fin-Largeur_fenetre
            Fenetres.append(image[0:x,a:Fin])       
    else:
        #Erreur en fichier !!!!!!!!!!!!!!!!!!!!
        print('Erreur image trop petite !');
    return Fenetres

def upperContour( pic ) : 
    contour_up = np.zeros( pic.shape )
    for j in range (pic.shape[1]) :
        for i in range (pic.shape[0]) :
            if( pic[i][j] == 255 ) :
                contour_up[i][j] = 255
                break
    return contour_up

def lowerContour( pic ) : 
    contour_low = np.zeros( pic.shape )
    for j in range (pic.shape[1]) :
        index = 256
        for i in range ( pic.shape[0]) :
            if( pic[i][j] == 255 ) :
                index = i
        if( index != 256 ) :
            contour_low[index][j] = 255
    return contour_low

#labels = ['المنزه 9','المرناقية 20 مارس','سيدي إبراهيم الزهار','المنزه 6','زنوش','شتاوة صحراوي','رأس الذراع','سبعة آبار','شعّال','الخليج','تطاوين 7 نوفمبر','أكّودة','شمّاخ','نقة','المحارزة 18','نحّال','مارث','الدخّانية','تلّ الغزلان','سيدي الظاهر','الفايض','الرضاع']
#labels = ['المنزه','المرناقية 20 مارس','سيدي إبراهيم الزهار','المنزه','زنوش','شتاوة صحراوي','رأس الذراع','سبعة آبار','شعّال','الخليج','تطاوين 7 نوفمبر','أكّودة','شمّاخ','نقة','المحارزة','نحّال','مارث','الدخّانية','تلّ الغزلان','سيدي الظاهر','الفايض','الرضاع']
labels = ['المنزه','المرناقية 20 مارس','سيدي ابراهيم الزهار','المنزه','زنوش','شتاوة صحراوي','راس الذراع','سبعة ابار','شعال','الخليج','تطاوين 7 نوفمبر','أكودة','شماخ','نقة','المحارزة','نحال','مارث','الدخانية','تل الغزلان','سيدي الظاهر','الفايض','الرضاع']
classes_df = pd.DataFrame( {'labels':labels} )


if choose == "Accueil" :
    st.title( "Reconnaissance des mots arabes manuscrits pris de la base de données IFN/ENIT" )
    st.write( "### Après avoir choisi un jeu de données et un fenêtrage, vous pouvez tester une image de la base de données et observer le prétraitement utilisé, l'extraction de ses caractéristiques et sa classification." )

elif choose == "Prétraitement" :
    image = cv2.imread( "ae09_011.bmp", 0 )
    st.write( " ### Choisissez une image de la base de données :" )
    image_uploaded = st.file_uploader( "", type=['bmp'] )
    if( image_uploaded is not None ) :
        #image_uploaded_show = cv2.imread( os.path.join( "bdh/", image_uploaded.name ), 0 )
        image_uploaded_show = Image.open( image_uploaded )
        image_uploaded_show = image_uploaded_show.convert( "L" )
        image_uploaded_show_array = np.asarray( image_uploaded_show )
        image = image_uploaded_show_array
    st.write( "### Une image de la base de données : ")
    st.image( image )
    button1 = button2 = button3 = button4 = button5 = False
    
    col1, col2, col3 = st.columns(3)
    with col1 :
        button1 = st.button( "Contour", key="contour" )
    with col2 :
        button4 = st.button( "ContourSupérieur", key="contour_sup" ) 
    with col3 :
        button5 = st.button( "ContourInférieur", key="contour_inf" )       
    
    #col4, col5 = st.columns(2)
    #with col4 :
     #   button2 = st.button( "Fenêtrage : 5Fenêtres, 3PixelsChevauchement", key="fenetrage5" )
    #with col5 :
     #   button3 = st.button( "Fenêtrage : 4Fenêtres, 4PixelsChevauchement", key="fenetrage4" )'''

    if( button1 ) :
        image_contour = contour( image )
        st.image( image_contour, caption="Image avec contour" )
        
    if( button2 ) :
        list_images_contour_fenetrage  = fenetrage( image, 5, 3 )
        column1, column2, column3, column4, column5 = st.columns(5)
        with column1 :
            st.image( list_images_contour_fenetrage[4], caption="Fenêtre1")
        with column2 :
            st.image( list_images_contour_fenetrage[3], caption="Fenêtre2")
        with column3 :
            st.image( list_images_contour_fenetrage[2], caption="Fenêtre3")
        with column4 :
            st.image( list_images_contour_fenetrage[1], caption="Fenêtre4")
        with column5 :
            st.image( list_images_contour_fenetrage[0], caption="Fenêtre5")
    
    if( button3 ) :
        list_images_contour_fenetrage  = fenetrage( image, 4, 4 )
        column1, column2, column3, column4 = st.columns(4)
        with column1 :
            st.image( list_images_contour_fenetrage[3], caption="Fenêtre1")
        with column2 :
            st.image( list_images_contour_fenetrage[2], caption="Fenêtre2")
        with column3 :
            st.image( list_images_contour_fenetrage[1], caption="Fenêtre3")
        with column4 :
            st.image( list_images_contour_fenetrage[0], caption="Fenêtre4")
    
    if( button4 ) :
        image_contour_sup = upperContour( image )
        st.image( image_contour_sup, caption="Image avec contour superieur", clamp=True )
        
    if( button5 ) :
        image_contour_inf = lowerContour( image )
        st.image( image_contour_inf, caption="Image avec contour inferieur", clamp=True )
        
    st.write("#### Fenêtrage" )
    col4, col5, col6 = st.columns(3)
    with col4 :
        optionI = st.selectbox( "Choisissez l'image à traiter : ", ('-', 'Image originale', 'Image avec contour') )
    with col5 :
        optionF = st.selectbox( "Choisissez le fenêtrage: ", ('-', '3 fenêtres', '4 fenêtres', '5 fenêtres', '6 fenêtres', '7 fenêtres', '8 fenêtres', '9 fenêtres') )
    with col6 :
        optionC = st.selectbox( "Choisissez le chevauchement : ", ('-', '2 pixels', '3 pixels', '4 pixels', '5 pixels', '6 pixels', '7 pixels', '8 pixels', '9 pixels') )    
        
    if( optionI != "-" and optionF != "-" and optionC != "-" ) :
        f = int(optionF[0])
        c = int(optionC[0])
        if( optionI == "Image originale" ) :
            list_images_contour_fenetrage  = fenetrage( image, f, 5 )
        elif( optionI == "Image avec contour" ) :
             list_images_contour_fenetrage  = fenetrage( contour(image), f, 5 )
        columns = st.columns(f)
        for i in range( f ) :
            with columns[i] :
                cap = "Fenêtre"+str(i+1)
                st.image( list_images_contour_fenetrage[f-1-i], caption=cap )
                
elif choose == "Extraction des caractéristiques" : 
    image = cv2.imread( "ae09_011.bmp", 0 )
    i = 14
    st.write( " ### Choisissez une image de la base de données :" )
    image_uploaded = st.file_uploader( "", type=['bmp'] )
    df = pd.read_csv( "df.csv" )
    if( image_uploaded is not None ) :
        #image_uploaded_show = cv2.imread( os.path.join( "bdh/", image_uploaded.name ), 0 )
        image_uploaded_show = Image.open( image_uploaded )
        image_uploaded_show = image_uploaded_show.convert( "L" )
        image_uploaded_show_array = np.asarray( image_uploaded_show )
        image = image_uploaded_show_array
        i = df[df['0']==image_uploaded.name].iloc[:,0:2].values[0][0]
    st.write( "### Une image de la base de données : ")
    st.image( image )
    
    col1_e, col2_e = st.columns(2)
    with col1_e :
        button1_e = st.button( "Fenêtrage : 5Fenêtres, 3PixelsChevauchement", key="fenetrage5_e"  )
    with col2_e :
        button2_e = st.button( "Fenêtrage : 4Fenêtres, 4PixelsChevauchement", key="fenetrage4_e"  )
        
    if( button1_e ) :
        df1_5w = pd.read_csv( "cn_5w/df1_5W.csv" )
        df2_5w = pd.read_csv( "fc_5w/df2_5W.csv" )
        df1_5w = df1_5w.iloc[i,:-1]
        df2_5w = df2_5w.iloc[i,:-1]
        
        fen1 = pd.concat( [ df1_5w.iloc[0:6], df1_5w.iloc[24:26], df1_5w.iloc[130:133], df1_5w.iloc[134:150], df2_5w.iloc[134:142] ], axis = 0, ignore_index = True ).values
        fen2 = pd.concat( [ df1_5w.iloc[26:32], df1_5w.iloc[50:52], df1_5w.iloc[150:153], df1_5w.iloc[154:170], df2_5w.iloc[146:154] ], axis = 0, ignore_index = True ).values
        fen3 = pd.concat( [ df1_5w.iloc[52:58], df1_5w.iloc[76:78], df1_5w.iloc[170:173], df1_5w.iloc[174:190], df2_5w.iloc[158:166] ], axis = 0, ignore_index = True ).values
        fen4 = pd.concat( [ df1_5w.iloc[78:84], df1_5w.iloc[102:104], df1_5w.iloc[190:193], df1_5w.iloc[194:210], df2_5w.iloc[170:178] ], axis = 0, ignore_index = True ).values
        fen5 = pd.concat( [ df1_5w.iloc[104:110], df1_5w.iloc[128:130], df1_5w.iloc[210:213], df1_5w.iloc[214:230], df2_5w.iloc[182:190] ], axis = 0, ignore_index = True ).values
        
        fenetres = np.array( [fen1, fen2, fen3, fen4, fen5] )
        fenetres_df = pd.DataFrame( fenetres, index = ['Fenêtre1', 'Fenêtre2', 'Fenêtre3','Fenêtre4','Fenêtre5'], columns = ['Contour supérieur', 'Contour inférieur', 'Densité', 'Densité pixels', 'Transitions horizontales','Transitions verticales', 'Centre de gravité X', 'Centre de gravité Y', 'P1', 'P2', 'P3', 'Code1', 'Code2', 'Code3', 'Code4', 'Code5', 'Code6', 'Code7', 'Code8', 'Code9', 'Code10', 'Code11', 'Code12', 'Code13', 'Code14', 'Code15', 'Code16', 'Fréquence cumulée du code0', 'Fréquence cumulée du code1', 'Fréquence cumulée du code2', 'Fréquence cumulée du code3', 'Fréquence cumulée du code4', 'Fréquence cumulée du code5', 'Fréquence cumulée du code6', 'Fréquence cumulée du code7'])
        
        st.dataframe( fenetres_df )
        
    if( button2_e ) :
        df1_4w = pd.read_csv( "cn_4w/df1_4W.csv" )
        df2_4w = pd.read_csv( "fc_4w/df2_4W.csv" )
        df1_4w = df1_4w.iloc[i,:-1]
        df2_4w = df2_4w.iloc[i,:-1]
        
        fen11 = pd.concat( [ df1_4w.iloc[0:6], df1_4w.iloc[24:26], df1_4w.iloc[104:107], df1_4w.iloc[108:124], df2_4w.iloc[108:116] ], axis = 0, ignore_index = True ).values
        fen21 = pd.concat( [ df1_4w.iloc[26:32], df1_4w.iloc[50:52], df1_4w.iloc[124:127], df1_4w.iloc[128:144], df2_4w.iloc[120:128] ], axis = 0, ignore_index = True ).values
        fen31 = pd.concat( [ df1_4w.iloc[52:58], df1_4w.iloc[76:78], df1_4w.iloc[144:147], df1_4w.iloc[148:164], df2_4w.iloc[132:140] ], axis = 0, ignore_index = True ).values
        fen41 = pd.concat( [ df1_4w.iloc[78:84], df1_4w.iloc[102:104], df1_4w.iloc[164:167], df1_4w.iloc[168:184], df2_4w.iloc[144:152] ], axis = 0, ignore_index = True ).values
        
        fenetres1 = np.array( [fen11, fen21, fen31, fen41] )
        fenetres_df1 = pd.DataFrame( fenetres1, index = ['Fenêtre1', 'Fenêtre2', 'Fenêtre3','Fenêtre4'], columns = ['Contour supérieur', 'Contour inférieur', 'Densité', 'Densité pixels', 'Transitions horizontales','Transitions verticales', 'Centre de gravité X', 'Centre de gravité Y', 'P1', 'P2', 'P3', 'Code1', 'Code2', 'Code3', 'Code4', 'Code5', 'Code6', 'Code7', 'Code8', 'Code9', 'Code10', 'Code11', 'Code12', 'Code13', 'Code14', 'Code15', 'Code16', 'Fréquence cumulée du code0', 'Fréquence cumulée du code1', 'Fréquence cumulée du code2', 'Fréquence cumulée du code3', 'Fréquence cumulée du code4', 'Fréquence cumulée du code5', 'Fréquence cumulée du code6', 'Fréquence cumulée du code7'])
        
        st.dataframe( fenetres_df1 )
    
elif choose == "Classification" : 
    df = pd.read_csv( "df.csv" )
    st.title( "Reconnaissance du manuscrit" )
    
    
    option = st.selectbox( "Choisissez le jeu de données utilisé lors de l'entrainement du modèle : ", ('-', 'Jeu de données 1 (CSS + codage de Freeman avec chaîne normalisée)', 'Jeu de données 2 (CSS + codage de Freeman avec fréquences cumulées)', 'Jeu de données 3 (CSS)') )
    
    option1 = st.selectbox( "Choisissez le fenêtrage : ", ('-', 'Fenêtrage 5, 3', 'Fenêtrage 4, 4') )
    st.write("")
    st.write("")
    st.write("")
    if( option == "Jeu de données 1 (CSS + codage de Freeman avec chaîne normalisée)" and option1 == "Fenêtrage 5, 3" ) :
        model = pickle.load(open("cn_5w/cn_5w.pkl",'rb'))
        fv = pd.read_csv("cn_5w/df1_5W.csv")
        #a,b,c=st.columns([0.5,4,0.5])
        #with b:
            #st.write( "### Taux de reconnaissance du modèle : 96.89%" )
        
    if( option == "Jeu de données 1 (CSS + codage de Freeman avec chaîne normalisée)" and option1 == "Fenêtrage 4, 4" ) :
        model = pickle.load(open("cn_4w/cn_4w.pkl",'rb'))
        fv = pd.read_csv("cn_4w/df1_4W.csv")
        l = []
        for i in range( 184 ) :
            if( max( fv[str(i)] ) > 1 ) :
                l.append( str(i) )
        for column in l :
            fv[ column ] = MinMaxScaler().fit_transform( np.array(fv[ column ]).reshape(-1, 1) )
        #a,b,c=st.columns([0.5,4,0.5])
        #with b:
            #st.write( "### Taux de reconnaissance du modèle : 95.43%" )
        
    if( option == "Jeu de données 2 (CSS + codage de Freeman avec fréquences cumulées)" and option1 == "Fenêtrage 5, 3" ) :
        model = pickle.load(open("fc_5w/fc_5w.pkl",'rb'))
        fv = pd.read_csv("fc_5w/df2_5W.csv")
        #a,b,c=st.columns([0.5,4,0.5])
        #with b:
            #st.write( "### Taux de reconnaissance du modèle : 98.01%" )
            
    if( option == "Jeu de données 2 (CSS + codage de Freeman avec fréquences cumulées)" and option1 == "Fenêtrage 4, 4" ) :
        model = pickle.load(open("fc_4w/fc_4w.pkl",'rb'))
        fv = pd.read_csv("fc_4w/df2_4W.csv")
        #a,b,c=st.columns([0.5,4,0.5])
        #with b:
            #st.write( "### Taux de reconnaissance du modèle : 98.08%" )
            
    if( option == "Jeu de données 3 (CSS)" and option1 == "Fenêtrage 5, 3" ) :
        model = pickle.load(open("ss_5w/ss_5w.pkl",'rb'))
        fv = pd.read_csv("ss_5w/df3_5W.csv")
        l = []
        for i in range( 130 ) :
            if( max( fv[str(i)] ) > 1 ) :
                l.append( str(i) )
        for column in l :
            fv[ column ] = MinMaxScaler().fit_transform( np.array(fv[ column ]).reshape(-1, 1) )
        #a,b,c=st.columns([0.5,4,0.5])
        #with b:
            #st.write( "### Taux de reconnaissance du modèle : 96.56%" )
    
    if( option == "Jeu de données 3 (CSS)" and option1 == "Fenêtrage 4, 4" ) :
        model = pickle.load(open("ss_4w/ss_4w.pkl",'rb'))
        fv = pd.read_csv("ss_4w/df3_4W.csv")
        l = []
        for i in range( 104 ) :
            if( max( fv[str(i)] ) > 1 ) :
                l.append( str(i) )
        for column in l :
            fv[ column ] = MinMaxScaler().fit_transform( np.array(fv[ column ]).reshape(-1, 1) )
        #a,b,c=st.columns([0.5,4,0.5])
        #with b:
            #st.write( "### Taux de reconnaissance du modèle : 95.30%" )
    
    if( option != "-" and option1 != "-" ) :
        st.write( "#### Choisissez une image de la base de données :" )
        image_uploaded_c = st.file_uploader( "", type=['bmp'], key="c" )
        if( image_uploaded_c is not None ) :
            #image_uploaded_show_c = cv2.imread( os.path.join( "bdh/", image_uploaded_c.name ), 0 )
            image_uploaded_show_c = Image.open( image_uploaded_c )
            image_uploaded_show_c = image_uploaded_show_c.convert( "L" )
            image_uploaded_show_c_array = np.asarray( image_uploaded_show_c )
            st.image( image_uploaded_show_c )
            i = df[df['0']==image_uploaded_c.name].iloc[:,0:2].values[0][0]
            x = fv.iloc[i,:-1].values.reshape(1,-1)
            y = int(model.predict( x )[0])
            #st.write( "i = ", i, "y = ", y )
            st.write("")
            st.write("")
            st.write("")
            
            st.write( "#### Classe de l'image :  ", int(y) )
            aa,bb=st.columns([3,3])
            with aa :
                st.write( "#### Reconnaissance du manuscrit : " )
            with bb :
                st.write( "## ", classes_df.iloc[y-1][0] )
                

elif choose == "Contact" :
    st.write( "### Nous sommes toujours ravis de votre contact!" )
    st.write( "### Envoyez-nous un e-mail et dites-nous comment nous pouvons vous aider via cet mail : reconnaissance.manu.arb@gmail.com " )
    
elif choose == "Aide" :
    st.write( "### - CSS : Caractéristiques statistiques et structurelles" )
    st.write( "### - Codage de Freeman avec chaîne normalisée : Caractéristiques extraites de la chaîne de code avec chaîne normalisée" )
    st.write( "### - Codage de Freeman avec fréquences cumulées : Caracteristiques extraites de la chaine de code avec fréquences cumulées" )
    