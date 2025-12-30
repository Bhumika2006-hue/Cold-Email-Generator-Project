import streamlit as st

def main():
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")
    
    st.title("Welcome to the Cold Email Generator")
    st.write("Please select your mode:")
    
    mode = st.radio("Choose your interface:", ("Student Mode", "Placement Officer Mode"))
    
    if mode == "Student Mode":
        st.write("You have selected Student Mode.")
        # Import and run the student mode interface
        from pages.student_mode import create_student_interface
        create_student_interface()
        
    elif mode == "Placement Officer Mode":
        st.write("You have selected Placement Officer Mode.")
        # Import and run the placement officer mode interface
        from pages.placement_officer_mode import create_placement_officer_app
        create_placement_officer_app()

if __name__ == "__main__":
    main()