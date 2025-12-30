import time
import streamlit as st
from utils import get_chain, get_portfolio, process_institution_url, scrape_page_content
from ddgs import DDGS

def create_placement_officer_app():
    st.title("📧 Placement Officer Email Generator")
    
    # Initialize session state variables
    if 'page' not in st.session_state:
        st.session_state.page = 'setup'
    if 'user_details' not in st.session_state:
        st.session_state.user_details = {}
    if 'institution_summary' not in st.session_state:
        st.session_state.institution_summary = ""
    if 'search_results' not in st.session_state:
        st.session_state.search_results = []
    if 'current_report' not in st.session_state:
        st.session_state.current_report = None
    if 'current_url' not in st.session_state:
        st.session_state.current_url = None
    if 'display_name' not in st.session_state:
        st.session_state.display_name = ""
    if 'selected_job' not in st.session_state:
        st.session_state.selected_job = None
    if 'outreach_mode' not in st.session_state:
        st.session_state.outreach_mode = False
    if 'generated_mail' not in st.session_state:
        st.session_state.generated_mail = None
    
    # SETUP PAGE
    if st.session_state.page == 'setup':
        st.markdown('<div class="css-card"><h2>Institutional Profile Setup</h2></div>', unsafe_allow_html=True)
        
        with st.form("user_setup_form"):
            name = st.text_input("Your Full Name (e.g. Prof. Mohan Kumar)")
            designation = st.text_input("Your Designation (e.g. Head of Corporate Relations)")
            inst_name = st.text_input("Institution Name")
            inst_url = st.text_input("Institution Website URL")
            
            submitted = st.form_submit_button("Continue to Engine")
            
            if submitted:
                if name and designation and inst_name and inst_url:
                    st.session_state.user_details = {
                        "name": name,
                        "designation": designation,
                        "institution_name": inst_name,
                        "institution_url": inst_url
                    }
                    
                    chain = get_chain()
                    if chain:
                        with st.status("Analyzing Institution Workforce Pipeline...") as status:
                            summary = process_institution_url(chain, inst_url)
                            if summary:
                                st.session_state.institution_summary = summary
                                status.update(label="✅ Institution Analysis Complete", state="complete")
                                time.sleep(1)
                                st.session_state.page = 'main'
                                st.rerun()
                            else:
                                status.update(label="⚠️ Scraper Limited. Proceeding with manual context.", state="complete")
                                time.sleep(1)
                                st.session_state.page = 'main'
                                st.rerun()
                else:
                    st.warning("All professional credentials are required for persona initialization.")

    # MAIN PAGE
    elif st.session_state.page == 'main':
        chain = get_chain()
        portfolio = get_portfolio()
        
        if not chain or not portfolio:
            st.error("Engine Initialization Error. Check API Configuration.")
            return

        with st.sidebar:
            st.markdown(f"### 👤 Senior Persona")
            st.info(f"**{st.session_state.user_details.get('name')}**\n\n{st.session_state.user_details.get('designation')}\n\n{st.session_state.user_details.get('institution_name')}")
            if st.button("🔄 Edit Profile", use_container_width=True):
                st.session_state.page = 'setup'
                st.rerun()

        st.title("Strategic Opportunities")
        portfolio.load_portfolio()
        
        col1, col2 = st.columns([3, 1])
        with col1:
            company_query = st.text_input("Target Company (e.g. 'Google', 'Nike', 'Wipro')")
        with col2:
            search_trigger = st.button("Search Intelligence", use_container_width=True)

        if search_trigger and company_query:
            company_query = company_query.strip()
            display_name = company_query.title()
            st.session_state.display_name = display_name
            
            with st.status(f"Scanning Global Opportunities for {display_name}...") as status:
                try:
                    inst_name = st.session_state.user_details.get('institution_name', '')
                    
                    with DDGS() as ddgs:
                        # Multi-Stage Search
                        results_raw = list(ddgs.text(f"{display_name} careers jobs openings", max_results=8))
                        if not results_raw:
                            results_raw = list(ddgs.text(f"{display_name} careers", max_results=5))
                    
                    if results_raw:
                        snippets = "\n".join([f"- {res['title']}: {res['body']}" for res in results_raw[:5]])
                        report = chain.generate_company_report(display_name, snippets, st.session_state.institution_summary)
                        st.session_state.current_report = report
                        
                        career_url = next((res['href'] for res in results_raw if 'career' in res['href'].lower() or 'job' in res['href'].lower()), results_raw[0]['href'])
                        st.session_state.current_url = career_url
                        
                        data = scrape_page_content(career_url)
                        inst_context = f"Institution: {inst_name}. Summary: {st.session_state.institution_summary}. Company: {display_name}."
                        
                        if data and len(data) > 300:
                            jobs = chain.extract_jobs(data, institution_context=inst_context)
                        else:
                            fallback_data = "\n".join([f"Title: {res['title']}\nSnippet: {res['body']}" for res in results_raw])
                            jobs = chain.extract_jobs(fallback_data, institution_context=inst_context)
                        
                        st.session_state.search_results = jobs
                        status.update(label=f"✅ {display_name} Intelligence Ready", state="complete")
                    else:
                        st.error(f"Unable to locate career data for {display_name}.")
                except Exception as e:
                    st.error(f"Intelligence failure: {e}")

        # PERSISTENT DISPLAY
        if st.session_state.get('current_report'):
            st.subheader(f"📊 Market Analysis: {st.session_state.display_name}")
            st.markdown(f'<div class="job-card">{st.session_state.current_report}</div>', unsafe_allow_html=True)
            
            if st.button("Draft Executive Outreach Email", use_container_width=True):
                st.session_state.selected_job = None
                st.session_state.outreach_mode = True
                st.session_state.generated_mail = None
                st.rerun()

        if st.session_state.get('outreach_mode'):
            st.divider()
            title = f"📧 Pitching to {st.session_state.display_name}"
            if st.session_state.get('selected_job'):
                title += f" ({st.session_state.selected_job.get('role')})"
            st.header(title)
            
            with st.form("outreach_form_premium"):
                col_n, col_d = st.columns(2)
                with col_n:
                    rec_name = st.text_input("Recipient Name", placeholder="e.g. Jane Smith")
                with col_d:
                    rec_desg = st.text_input("Recipient Designation", placeholder="e.g. HR Head")
                    
                intent = st.selectbox("Strategic Intent", ["Campus Hiring Drive 2024-25", "Student Internships", "MOU & Partnerships"])
                
                gen_btn = st.form_submit_button("Generate Masterful Draft")
                
                if gen_btn:
                    if not rec_name:
                        st.error("Recipient name is required for executive persona.")
                    else:
                        with st.spinner("Drafting as Senior TPO..."):
                            skills = st.session_state.selected_job.get('skills', []) if st.session_state.get('selected_job') else st.session_state.institution_summary.split()[:5]
                            links = portfolio.query_links(skills)
                            email = chain.write_mail(
                                job=st.session_state.selected_job,
                                links=links,
                                user_details=st.session_state.user_details,
                                recipient_details={"name": rec_name, "designation": rec_desg},
                                intent=intent,
                                company_name=st.session_state.display_name,
                                institution_summary=st.session_state.institution_summary
                            )
                            if email:
                                st.session_state.generated_mail = email
                                st.rerun()

            if st.session_state.get('generated_mail'):
                st.text_area("Final Executive Draft", value=st.session_state.generated_mail, height=450, key="final_outreach_text")
                st.download_button("📩 Download Proposal", st.session_state.generated_mail, 
                file_name="proposal.txt", use_container_width=True)
                if st.button("New Action / Clear", use_container_width=True):
                    st.session_state.outreach_mode = False
                    st.session_state.generated_mail = None
                    st.rerun()

        if st.session_state.search_results and not st.session_state.get('outreach_mode'):
            st.divider()
            st.write(f"### Specific Vacancies at {st.session_state.display_name}")
            for idx, job in enumerate(st.session_state.search_results):
                with st.expander(f"📋 {job.get('role', 'Opportunity')}", expanded=(idx==0)):
                    st.write(f"**Brief:** {job.get('description', 'N/A')}")
                    st.write(f"**Skills:** {job.get('skills', 'N/A')}")
                    if st.button(f"Draft Pitch for this Role", key=f"job_btn_{idx}"):
                        st.session_state.selected_job = job
                        st.session_state.outreach_mode = True
                        st.session_state.generated_mail = None
                        st.rerun()

if __name__ == "__main__":
    create_placement_officer_app()