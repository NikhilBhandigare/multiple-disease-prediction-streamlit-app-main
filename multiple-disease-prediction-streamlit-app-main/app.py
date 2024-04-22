import os
import pickle
import streamlit as st
from streamlit_option_menu import option_menu

# Set page configuration
st.set_page_config(page_title="Health Assistant",
                   layout="wide",
                   page_icon="🧑‍⚕️")

    
# getting the working directory of the main.py
working_dir = os.path.dirname(os.path.abspath(__file__))

# loading the saved models

diabetes_model = pickle.load(open(f'{working_dir}/saved_models/diabetes_model.sav', 'rb'))

heart_disease_model = pickle.load(open(f'{working_dir}/saved_models/heart_disease_model.sav', 'rb'))

parkinsons_model = pickle.load(open(f'{working_dir}/saved_models/parkinsons_model.sav', 'rb'))

# sidebar for navigation
with st.sidebar:
    selected = option_menu('Multiple Disease Prediction System',

                           ['Diabetes Prediction',
                            'Heart Disease Prediction',
                            'Parkinsons Prediction'],
                           menu_icon='hospital-fill',
                           icons=['activity', 'heart', 'person'],
                           default_index=0)


# Diabetes Prediction Page

    # Diabetes Prediction Page
if selected == 'Diabetes Prediction':

     # page title
    st.title('Diabetes Prediction using ML')

    # getting the input data from the user
    col1, col2, col3 = st.columns(3)

    with col1:
        Pregnancies = st.text_input('Number of Pregnancies')

    with col2:
        Glucose = st.text_input('Glucose Level (Median Range 117.0)')

    with col3:
        BloodPressure = st.text_input('Blood Pressure value (min=90, max=120)')

    with col1:
        SkinThickness = st.text_input('Skin Thickness value (Median Range  23.0)')

    with col2:
        Insulin = st.text_input('Insulin Level (Median Range 30.5)')

    with col3:
        BMI = st.text_input('BMI value (Median Range 32.0)')

    # with col1:
    #     DiabetesPedigreeFunction = st.text_input('Diabetes Pedigree Function value (0-1-2-3)')

    # with col2:
    #     Age = st.text_input('Age of the Person')

    # code for Prediction
    diab_diagnosis = ''

    # creating a button for Prediction
    if st.button('Diabetes Test Result'):

        user_input = [Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin,
                      BMI]

        user_input = [float(x) for x in user_input]

        diab_prediction = diabetes_model.predict([user_input])

        if diab_prediction[0] == 1:
            diab_diagnosis = 'The person is diabetic'

            # Medicine Recommendation
            st.subheader('Medicine Recommendation:')
            st.write('Based on the prediction, it is recommended to consult with a healthcare professional for appropriate medication.')
            st.write("1. Metformin: Metformin is usually the first-line medication for type 2 diabetes. It works by decreasing the amount of glucose produced by the liver and improving insulin sensitivity in the body's cells.")
            st.write('2. Sulfonylureas: These medications stimulate the pancreas to release more insulin. Examples include glipizide, glyburide, and glimepiride.')
            st.write('3. DPP-4 inhibitors: Dipeptidyl peptidase-4 (DPP-4) inhibitors help lower blood sugar levels by increasing insulin secretion and reducing glucose production. Examples include sitagliptin, saxagliptin, and linagliptin.')
            st.write('4. Insulin: For individuals with type 1 diabetes or advanced type 2 diabetes, insulin therapy may be necessary to control blood sugar levels. There are various types of insulin, including rapid-acting, short-acting, intermediate-acting, and long-acting, which can be used alone or in combination.')

            # Exercise Recommendation
            st.subheader('Exercise Recommendation:')
            st.write('In addition to medication, regular physical activity is beneficial for managing diabetes.')
            st.write('1. Aerobic Exercise: Engage in moderate-intensity aerobic exercises such as brisk walking, cycling, swimming, or dancing. Aim for at least 150 minutes of aerobic activity per week, spread across most days of the week.')
            st.write('2. Strength Training: Incorporate strength training exercises using resistance bands, free weights, or weight machines. Focus on major muscle groups such as legs, arms, back, and abdomen. Perform strength training exercises at least two days per week, allowing a day of rest in between sessions.')
            st.write('3. Monitor Blood Sugar Levels: Check your blood sugar levels before, during, and after exercise, especially if you are taking medications that can lower blood sugar levels. Adjust your exercise intensity or duration accordingly to maintain safe blood sugar levels.')
            st.write('4. Stay Hydrated: Drink plenty of water before, during, and after exercise to stay hydrated.')

            #Diet recommendation
            st.subheader('Diet Recommendation:')
            st.write('A well-balanced diet plays a crucial role in managing diabetes by helping to control blood sugar levels, manage weight, and reduce the risk of complications ')
            st.write('1. Emphasize Whole Foods: Base your meals around whole, minimally processed foods such as fruits, vegetables, whole grains, lean proteins, and healthy fats. These foods are rich in nutrients and fiber, which can help regulate blood sugar levels.')
            st.write('2. Choose Healthy Fats: Incorporate sources of healthy fats into your diet, such as avocados, nuts, seeds, olive oil, and fatty fish (e.g., salmon, mackerel, sardines). Healthy fats can help improve insulin sensitivity and reduce the risk of heart disease, a common complication of diabetes.')
            st.write('3. Include Lean Proteins: Opt for lean sources of protein, such as poultry (without skin), fish, tofu, tempeh, legumes, and low-fat dairy products. Protein can help stabilize blood sugar levels and promote satiety, aiding in weight management.')
            st.write('4. Control Carbohydrate Intake: Carbohydrates have the most significant impact on blood sugar levels. Aim for complex carbohydrates with a low glycemic index (GI), such as whole grains (e.g., oats, quinoa, brown rice), legumes, and non-starchy vegetables. Monitor portion sizes and consider carbohydrate counting to manage blood sugar levels effectively.')


        else:
            diab_diagnosis = 'The person is not diabetic'

            # No Recommendation for Non-Diabetic
            st.subheader('No Specific Recommendation:')
            st.write('As the prediction indicates that the person is not diabetic, no specific medication or exercise recommendation is provided. It is still advisable to maintain a healthy lifestyle with a balanced diet and regular physical activity.')

            # Additional Recommendations for Non-Diabetic
            st.subheader('Additional Recommendations:')
            st.write('Although the prediction suggests the person is not diabetic, it is important to maintain a healthy lifestyle. Consider adopting a balanced diet, staying hydrated, and participating in regular physical activities to promote overall well-being.')

    st.success(diab_diagnosis)


# Heart Disease Prediction Page
if selected == 'Heart Disease Prediction':

    # page title
    st.title('Heart Disease Prediction using ML')

    col1, col2, col3 = st.columns(3)

    # with col1:
    #     age = st.text_input('Age')

    with col1:
        sex = st.text_input('Sex (1 = male; 0 = female)')

    with col2:
        cp = st.text_input('Chest Pain types 0 =Non-anginal Pain , 1 = Atypical Angina, 2 =Typical Angina , 3 = Asymptomatic')

    with col3:
        trestbps = st.text_input('Resting Blood Pressure (,min= 90,Median=141.5,max=190)')

    with col1:
        chol = st.text_input('Serum Cholestoral in mg/dl(min=100,Median=258.5,max=399 )')

    with col2:
        fbs = st.text_input('Fasting Blood Sugar > 120 mg/dl (1 = true; 0 = false)')

    with col3:
        restecg = st.text_input('Resting Electrocardiographic results (0: Normal, 1:having ST-T wave abnormality, 2:showing probable)')

    with col1:
        thalach = st.text_input('Maximum Heart Rate achieved (min=60,Median=138.0,max=219 )')

    with col2:
        exang = st.text_input('Exercise Induced Angina (1 = yes; 0 = no)')

    with col3:
        oldpeak = st.text_input('ST depression induced by exercise (0=no ST depression,0.5=mild ST depression,1.0=moderate ST depression,1.5=moderately severe ST depression,2.0= severe ST depression,2.5 and above=extremely severe ST depression   )')

    with col1:
        slope = st.text_input('Slope of the peak exercise ST segment [0: upsloping, 1: flat, 2: downsloping]')

    with col2:
        ca = st.text_input('Major vessels colored by flourosopy (0=four major coronary vessels colored, 1= three major coronary vessels colored,2=two major coronary vessels colored,3=one major coronary vessel colored,4=No major coronary vessels colored)')

    with col1:
        thal = st.text_input('thal: 0 =fixed defect ;1 =normal ')
    # code for Prediction
    heart_diagnosis = ''

    # creating a button for Prediction

    



    if st.button('Diabetes Test Result'):

        user_input = [ sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]

        user_input = [float(x) for x in user_input]

        heart_prediction = heart_disease_model.predict([user_input])

        if heart_prediction[0] == 1:
            heart_diagnosis = 'The person is having heart disease'

            # Medicine Recommendation
            st.subheader('Medicine Recommendation:')
            st.write('Based on the prediction, it is recommended to consult with a healthcare professional for appropriate medication.')
            st.write("1. Aspirin: Often recommended for its blood-thinning properties to prevent blood clots and reduce the risk of heart attack or stroke.")
            st.write('2. Statins: These medications help lower cholesterol levels in the blood, thereby reducing the risk of coronary artery disease and heart attacks.')
            st.write('3. Beta-blockers: These drugs help lower blood pressure and reduce the workload on the heart by blocking the effects of adrenaline. They are often prescribed for conditions like high blood pressure, heart failure, and angina.')
            st.write('4. Angiotensin-converting enzyme (ACE) inhibitors: ACE inhibitors help relax blood vessels, lower blood pressure, and improve blood flow. They are commonly prescribed for heart failure and hypertension.')
            st.write('5. Diuretics: These medications help reduce fluid buildup in the body by increasing urine production, thereby reducing blood pressure and the workload on the heart. They are often used to treat conditions such as heart failure and hypertension.')

            # Exercise Recommendation
            st.subheader('Exercise Recommendation:')
            st.write('In addition to medication, regular physical activity is beneficial for managing heart disease.')
            st.write("1. Consult with a healthcare provider: Before starting any exercise program, it's crucial to consult with a healthcare provider or cardiac rehabilitation specialist. They can assess your individual condition, provide personalized recommendations, and ensure that your exercise plan is safe and appropriate for you.")
            st.write('2. Focus on aerobic exercises: Aerobic exercises, also known as cardiovascular or endurance exercises, are particularly beneficial for heart health. These include activities that increase your heart rate and breathing, such as walking, jogging, cycling, swimming, or dancing.')
            st.write('3. Start slowly and progress gradually: Begin with low-intensity activities such as walking, cycling on a stationary bike, or swimming, and gradually increase the duration and intensity of your workouts over time. Aim for at least 30 minutes of moderate-intensity aerobic exercise on most days of the week.')
            st.write('4. Stay Hydrated: Drink plenty of water before, during, and after exercise to stay hydrated.')

            #Diet recommendation
            st.subheader('Diet Recommendation:')
            st.write("For individuals with heart disease, a heart-healthy diet is crucial for managing the condition and reducing the risk of complications.")
            st.write('1. Emphasize Fruits and Vegetables: Aim to include a variety of colorful fruits and vegetables in your diet. These are rich in vitamins, minerals, antioxidants, and fiber, which can help lower blood pressure and reduce the risk of heart disease.')
            st.write('2. Choose Whole Grains: Opt for whole grains such as brown rice, quinoa, oats, barley, and whole wheat bread instead of refined grains. Whole grains are high in fiber, which can help lower cholesterol levels and improve heart health.')
            st.write('3. Include Lean Protein Sources: Incorporate lean protein sources such as skinless poultry, fish (especially fatty fish like salmon, mackerel, and trout rich in omega-3 fatty acids), legumes (beans, lentils, chickpeas), tofu, and nuts. Limit intake of red meat and processed meats, which are high in saturated fats and sodium.')
            st.write('4. Reduce Sodium Intake: Limit the amount of salt in your diet by avoiding processed and packaged foods, which are often high in sodium. Flavor foods with herbs, spices, lemon juice, and vinegar instead of salt. Aim to consume less than 2,300 milligrams of sodium per day, and even less if advised by your healthcare provider.')


        else:
            heart_diagnosis = 'The person does not have any heart disease'

            # No Recommendation for Non-Diabetic
            st.subheader('No Specific Recommendation:')
            st.write('As the prediction indicates that the person have heart disease, no specific medication or exercise recommendation is provided. It is still advisable to maintain a healthy lifestyle with a balanced diet and regular physical activity.')

            # Additional Recommendations for Non-Diabetic
            st.subheader('Additional Recommendations:')
            st.write('Although the prediction suggests The person does not have any heart disease, it is important to maintain a healthy lifestyle. Consider adopting a balanced diet, staying hydrated, and participating in regular physical activities to promote overall well-being.')

    st.success(heart_diagnosis)


    



    # Parkinson's Prediction Page
if selected == "Parkinsons Prediction":

    # page title
    st.title("Parkinson's Disease Prediction using ML")

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        fo = st.text_input('MDVP:[Fo(Hz) (Midian Range 148.79)]')

    with col2:
        fhi = st.text_input('MDVP:[Fhi(Hz)(Midian Range 175.829)]')

    with col3:
        flo = st.text_input('MDVP:[Flo(Hz)(Midian Range 104.315)]')

    with col4:
        Jitter_percent = st.text_input('MDVP:[Jitter(%)(Midian Range 0.00494)]')

    with col5:
        Jitter_Abs = st.text_input('MDVP:[Jitter(Abs)(Midian Range 3e-05)]')

    with col1:
        RAP = st.text_input('MDVP:[RAP] (Midian Range 0.0025)')

    with col2:
        PPQ = st.text_input('MDVP:[PPQ] (Midian Range 0.00269)')

    with col3:
        DDP = st.text_input('Jitter:[DDP] (Midian Range 0.00749)')

    with col4:
        Shimmer = st.text_input('MDVP:[Shimmer] (Midian Range 0.02297)')

    with col5:
        Shimmer_dB = st.text_input('MDVP:[Shimmer(dB)] (Midian Range 0.221)')

    with col1:
        APQ3 = st.text_input('Shimmer:[APQ3](Midian Range 0.01279)')

    with col2:
        APQ5 = st.text_input('Shimmer:[APQ5] (Midian Range 0.01347)')

    with col3:
        APQ = st.text_input('MDVP:[APQ] (Midian Range 0.01826)')

    with col4:
        DDA = st.text_input('Shimmer:[DDA](Midian Range 0.03836)')

    with col5:
        NHR = st.text_input('NHR (Midian Range 0.01166)' )

    with col1:
        HNR = st.text_input('HNR (Midian Range 22.085)')

    with col2: 
        RPDE = st.text_input('RPDE (Midian Range 0.495954)')

    with col3:
        DFA = st.text_input('DFA (Midian Range 0.722254)')

    with col4:
        spread1 = st.text_input('spread1 (Midian Range  -5.720868)')

    with col5:
        spread2 = st.text_input('spread2 (Midian Range 0.218885)')

    with col1:
        D2 = st.text_input('D2 (Midian Range 2.361532)')

    with col2:
        PPE = st.text_input('PPE' '(Midian Range  0.194052)')

    # code for Prediction
    parkinsons_diagnosis = ''

    # code for Prediction
    parkinsons_diagnosis = ''

    # creating a button for Prediction    
    if st.button("Parkinson's Test Result"):

        user_input = [fo, fhi, flo, Jitter_percent, Jitter_Abs,
                      RAP, PPQ, DDP,Shimmer, Shimmer_dB, APQ3, APQ5,
                      APQ, DDA, NHR, HNR, RPDE, DFA, spread1, spread2, D2, PPE]

        user_input = [float(x) for x in user_input]

        parkinsons_prediction = parkinsons_model.predict([user_input])

        if parkinsons_prediction[0] == 1:
            parkinsons_diagnosis = "The person has Parkinson's disease"
            st.success(parkinsons_diagnosis)

            # Medicine Recommendation
            st.subheader("Medicine Recommendation:")
            st.write("Based on the prediction, it is recommended to consult with a neurologist for appropriate medication for Parkinson's disease.")
            st.write("1. Levodopa: Levodopa is the most effective medication for managing the motor symptoms of Parkinson's disease, such as tremors, stiffness, and slowness of movement. It is converted into dopamine in the brain, replenishing the brain's depleted dopamine levels. Levodopa is often combined with another medication called carbidopa to enhance its effectiveness and reduce side effects.")
            st.write("2. Dopamine Agonists: Dopamine agonists mimic the action of dopamine in the brain, helping to alleviate Parkinson's symptoms. They are often used as an initial treatment or in combination with levodopa. Examples of dopamine agonists include pramipexole, ropinirole, and rotigotine.")
            st.write('3. MAO-B Inhibitors: Monoamine oxidase-B (MAO-B) inhibitors help prevent the breakdown of dopamine in the brain, thereby increasing dopamine levels and improving motor symptoms. Examples of MAO-B inhibitors include selegiline and rasagiline.')
            st.write('4. COMT Inhibitors: Catechol-O-methyltransferase (COMT) inhibitors prolong the effects of levodopa by inhibiting its breakdown in the body. They are often used in combination with levodopa/carbidopa to reduce motor fluctuations. Entacapone and tolcapone are examples of COMT inhibitors.')
            # Exercise Recommendation
            st.subheader("Exercise Recommendation:")
            st.write("In addition to medication, regular physical activity can be beneficial for individuals with Parkinson's disease. Consider activities like walking, stretching, and balance exercises. However, it is crucial to consult with a healthcare professional or a physical therapist for personalized exercise recommendations.")
            st.write('1. Aerobic Exercise:Engage in aerobic activities such as walking, cycling, swimming, or dancing for at least 150 minutes per week, or as recommended by your healthcare provider.Choose activities that elevate your heart rate and breathing to improve cardiovascular health.Start slowly and gradually increase the intensity and duration of aerobic exercise sessions over time.')
            st.write('2. Strength Training:Incorporate strength training exercises using resistance bands, free weights, or weight machines to improve muscle strength and enduranceFocus on major muscle groups, including legs, arms, back, and corePerform strength training exercises 2-3 times per week, with a day of rest in between sessions.')
            st.write('3. Flexibility and Stretching:Include flexibility exercises and stretching to maintain or improve range of motion in your joints Perform stretching exercises for major muscle groups, including hamstrings, quadriceps, calves, shoulders, chest, and back.Hold each stretch for 15-30 seconds without bouncing, and repeat 2-4 times for each muscle group.')
            st.write('4. Balance and Stability Training:Practice balance exercises to reduce the risk of falls and improve stability.Examples of balance exercises include standing on one leg, heel-to-toe walking, standing on foam pads or balance boards, and practicing Tai Chi or yoga.Incorporate exercises that challenge your balance while seated or lying down if standing exercises are too challenging.')
            st.subheader("Diet Recommendation:")
            st.write("1. Emphasize Antioxidant-Rich Foods: Antioxidants help combat oxidative stress and inflammation, which are believed to play a role in Parkinson's disease progression. Include plenty of fruits and vegetables rich in antioxidants, such as berries, leafy greens, bell peppers, and cruciferous vegetables like broccoli and Brussels sprouts.")
            st.write('2. Consume Omega-3 Fatty Acids: Omega-3 fatty acids have anti-inflammatory properties and may help support brain health. Include sources of omega-3s in your diet, such as fatty fish (salmon, mackerel, sardines), flaxseeds, chia seeds, walnuts, and hemp seeds.')
            st.write("3. Maintain Adequate Protein Intake: While protein is important for muscle health and overall nutrition, some individuals with Parkinson's disease may experience difficulties with protein metabolism due to medications or motor symptoms. It's essential to consume adequate protein, but spacing it out throughout the day and avoiding excessive intake at any one meal may help manage motor fluctuations.")
            st.write("4. Fiber-Rich Foods: Constipation is a common issue in Parkinson's disease. Consuming plenty of fiber-rich foods such as whole grains, fruits, vegetables, legumes, and nuts can help promote regular bowel movements and alleviate constipation.")
            
        else:
            parkinsons_diagnosis = "The person does not have Parkinson's disease"
            st.success(parkinsons_diagnosis)

            # No Recommendation for Non-Parkinson's
            st.subheader("No Specific Recommendation:")
            st.write("As the prediction indicates that the person does not have Parkinson's disease, no specific medication or exercise recommendation is provided. It is still advisable to maintain a healthy lifestyle with regular physical activity.")


    st.success(parkinsons_diagnosis)
