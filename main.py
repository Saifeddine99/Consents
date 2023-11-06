import pymongo as py
#-----------------------------------------------------------------------------
myclient=py.MongoClient("mongodb://localhost:27017")
#relating data to "demographic_database"
demographic_data_coll=myclient["Demographic_database"]["Demographic data"]
#Consents collection:
consents_coll=myclient["Consents"]["Consents Collection"]
#-----------------------------------------------------------------------------
import streamlit as st
st.set_page_config(page_title="Consents", page_icon=":bell:", layout="centered")
#-----------------------------------------------------------------------------
st.markdown(
    "<h1 style='font-size: 250%;text-align: center; color: #0B5345;'>Permissions platform</h1>", 
        unsafe_allow_html = True
)

st.write("#")
st.write("#")

#Use phone number for identification:
col1,col2,col3= st.columns([4,0.1,4])
with col1:
    st.header("Phone Number:")
with col3:
    phone_number=st.text_input("enter your phone number here:", )

if phone_number:
    demog_data=demographic_data_coll.find_one({"phone number":phone_number})
    if demog_data:
        uuid=demog_data["uuid"]
        phone_number_db=demog_data["phone number"]

        patient_name=demog_data["demographic data"]["identities"][0]["details"]["items"][0]["value"]["value"]
        patient_surname=demog_data["demographic data"]["identities"][0]["details"]["items"][1]["value"]["value"]
        gender="Mrs"
        patient_gender=demog_data["demographic data"]["details"]["items"][0]["items"][4]["value"]["value"]
        if patient_gender=="MALE":
            gender="Mr"

        st.write("#")
        st.success(f"Hello {gender} {patient_name} {patient_surname}!")

        st.write("#")
        
        a,b,c=st.columns([8,0.5,1.5])
        with a:
            st.write("Do you accept to use your demographic & clinical data for research purposes?")
        with c:
            decision=st.radio("s",
                              ["YES","NO"],
                              label_visibility="collapsed"
                              )
        
        st.write("#")
        st.write("#")

        #Adding a button to launch search engine once clicked.
        cola, colb, colc = st.columns([4,2,3])
        with colb:
            done = st.button('Submit')

        if done:    
            existance=consents_coll.find_one({"uuid":uuid})    
            if decision=="YES":
                if existance:
                    st.info("You're already existing in our database!")
                else:
                    consents_coll.insert_one({"uuid":uuid})
                    st.success(" : You're successfully added to our database!",icon="✅")
            else:
                if existance:
                    consents_coll.delete_many({"uuid":uuid})
                
                st.success(" : Your data will not be shared",icon="✅")


    else:
        st.write("#")
        st.warning(": Invalid phone number",icon="⛔")

else:
    st.write("#")
    st.warning(": You must enter your phone number",icon="⛔")