import streamlit as st
import pandas as pd
from langchain_ollama import ChatOllama

llm = ChatOllama(model="tinyllama")

students = pd.read_csv("data/students.csv")
academic = pd.read_csv("data/academic.csv")
fees = pd.read_csv("data/fees.csv")
attendance_percentage = pd.read_csv("data/attendance_percentage.csv")
attendance_daily = pd.read_csv("data/attendance.csv")

st.title("AI CHATBOT")

if "messages" not in st.session_state:
    st.session_state.messages = []

user_input = st.chat_input("Ask anything...")

if user_input:

    st.session_state.messages.append(("You", user_input))

    query = user_input.lower()

    response = None
    found = False

    # Search by Name or Registration ID
    for _, student in students.iterrows():

        reg_id = str(student["reg_id"]).lower()
        name = str(student["name"]).lower()

        if reg_id in query or name in query:

            found = True

            academic_row = academic[
                academic["reg_id"] == student["reg_id"]
            ].iloc[0]

            fee_row = fees[
                fees["reg_id"] == student["reg_id"]
            ].iloc[0]

            attendance_row = attendance_percentage[
                attendance_percentage["reg_id"] == student["reg_id"]
            ].iloc[0]

            if (
                "details" in query
                or "everything" in query
                or query == reg_id
                or query == name
            ):

                response = f"""
Name: {student['name']}
Registration ID: {student['reg_id']}
Branch: {student['branch']}
Email: {student['email']}
Phone: {student['phone']}

CGPA: {academic_row['cgpa']}
Marks: {academic_row['marks']}

Total Fee: ₹{fee_row['total_fee']}
Paid Fee: ₹{fee_row['paid_fee']}
Balance Fee: ₹{fee_row['balance_fee']}

Present Days: {attendance_row['present_days']}
Absent Days: {attendance_row['absent_days']}
Attendance Percentage: {attendance_row['attendance_percentage']}%
"""

            elif "cgpa" in query:

                response = f"""
Name: {student['name']}
cgpa: {academic_row['cgpa']}
"""

            elif "marks" in query:

                response = f"""
Name: {student['name']}
Marks: {academic_row['marks']}
"""

            elif "fee" in query:

                response = f"""
Name: {student['name']}

Total Fee: ₹{fee_row['total_fee']}
Paid Fee: ₹{fee_row['paid_fee']}
Balance Fee: ₹{fee_row['balance_fee']}
"""

            elif "daily attendance" in query:

                daily = attendance_daily[
                    attendance_daily["reg_id"] == student["reg_id"]
                ]

                attendance_text = ""

                for _, row in daily.iterrows():
                    attendance_text += (
                        f"{row['date']} : {row['status']}\n"
                    )

                response = f"""
Name: {student['name']}

Daily Attendance:

{attendance_text}
"""

            elif "attendance" in query:

                response = f"""
Name: {student['name']}

Present Days: {attendance_row['present_days']}
Absent Days: {attendance_row['absent_days']}
Attendance Percentage: {attendance_row['attendance_percentage']}%
"""

            elif "email" in query:

                response = f"""
Name: {student['name']}
Email: {student['email']}
"""

            elif "phone" in query:

                response = f"""
Name: {student['name']}
Phone: {student['phone']}
"""

            else:

                response = f"""
Name: {student['name']}
Registration ID: {student['reg_id']}
Branch: {student['branch']}
"""

            break

    if not found:

        ai_response = llm.invoke(user_input)
        response = ai_response.content

    st.session_state.messages.append(("AI", response))

for role, message in st.session_state.messages:
    st.write(f"**{role}:** {message}")