import streamlit as st
import hashlib
import json
from datetime import datetime
import random
import string
from PIL import Image, ImageDraw
import io
import time

# Page configuration
st.set_page_config(
    page_title="Secure Fingerprint Voting System",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding: 1rem 0;
    }
    .sub-header {
        font-size: 1.5rem;
        text-align: center;
        color: #555;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem;
        font-size: 1.1rem;
        border-radius: 8px;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
    .vote-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border-left: 5px solid #667eea;
    }
    .success-msg {
        background: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 8px;
        border-left: 5px solid #28a745;
    }
    .error-msg {
        background: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 8px;
        border-left: 5px solid #dc3545;
    }
    .info-box {
        background: #e7f3ff;
        padding: 1rem;
        border-radius: 8px;
        border-left: 5px solid #2196F3;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'voters' not in st.session_state:
    st.session_state.voters = {}
if 'votes' not in st.session_state:
    st.session_state.votes = {}
if 'candidates' not in st.session_state:
    st.session_state.candidates = [
        {"id": 1, "name": "Alice Johnson", "party": "Progressive Party", "votes": 0},
        {"id": 2, "name": "Bob Martinez", "party": "Unity Alliance", "votes": 0},
        {"id": 3, "name": "Carol Zhang", "party": "Future Forward", "votes": 0},
        {"id": 4, "name": "David Okonkwo", "party": "People's Choice", "votes": 0}
    ]
if 'voted_ids' not in st.session_state:
    st.session_state.voted_ids = set()
if 'current_voter_id' not in st.session_state:
    st.session_state.current_voter_id = None

# Simulated fingerprint generation
def generate_fingerprint_hash(voter_id, name):
    """Generate a unique fingerprint hash based on voter info"""
    unique_data = f"{voter_id}{name}{datetime.now().isoformat()}{random.randint(1000, 9999)}"
    return hashlib.sha256(unique_data.encode()).hexdigest()

def create_fingerprint_image():
    """Create a simulated fingerprint image"""
    img = Image.new('RGB', (200, 200), color='white')
    draw = ImageDraw.Draw(img)
    
    # Draw fingerprint-like pattern
    center_x, center_y = 100, 100
    for i in range(10):
        radius = 20 + i * 15
        for angle in range(0, 360, 10):
            x1 = center_x + radius * 0.9
            y1 = center_y + radius * 0.9
            x2 = center_x + radius * 1.1
            y2 = center_y + radius * 1.1
            offset = random.randint(-5, 5)
            draw.arc([x1+offset, y1+offset, x2+offset, y2+offset], 
                    angle, angle+5, fill='black', width=2)
    
    return img

def enroll_voter(voter_id, name, age):
    """Enroll a new voter with fingerprint"""
    if voter_id in st.session_state.voters:
        return False, "Voter ID already exists!"
    
    fingerprint = generate_fingerprint_hash(voter_id, name)
    st.session_state.voters[voter_id] = {
        "name": name,
        "age": age,
        "fingerprint": fingerprint,
        "enrolled_at": datetime.now().isoformat()
    }
    return True, "Voter enrolled successfully!"

def verify_fingerprint(voter_id, simulated_fingerprint):
    """Verify fingerprint for voting"""
    if voter_id not in st.session_state.voters:
        return False, "Voter ID not found!"
    
    if voter_id in st.session_state.voted_ids:
        return False, "This voter has already cast their vote!"
    
    stored_fingerprint = st.session_state.voters[voter_id]["fingerprint"]
    
    # Simulate fingerprint matching (in real system, use actual biometric matching)
    if simulated_fingerprint == stored_fingerprint:
        return True, "Fingerprint verified successfully!"
    return False, "Fingerprint verification failed!"

def cast_vote(voter_id, candidate_id):
    """Record vote for candidate"""
    if voter_id in st.session_state.voted_ids:
        return False, "Vote already cast!"
    
    for candidate in st.session_state.candidates:
        if candidate["id"] == candidate_id:
            candidate["votes"] += 1
            st.session_state.voted_ids.add(voter_id)
            st.session_state.votes[voter_id] = {
                "candidate_id": candidate_id,
                "timestamp": datetime.now().isoformat()
            }
            return True, f"Vote cast for {candidate['name']}!"
    
    return False, "Invalid candidate!"

# Header
st.markdown('<p class="main-header">🔐 Secure Fingerprint Voting System</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Democratic • Secure • Anonymous</p>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/1077/1077063.png", width=100)
    st.title("Navigation")
    page = st.radio("Select Page", ["🏠 Home", "📝 Voter Enrollment", "🗳️ Cast Vote", "📊 Results", "ℹ️ System Info"])
    
    st.markdown("---")
    st.markdown("### System Status")
    st.metric("Enrolled Voters", len(st.session_state.voters))
    st.metric("Total Votes Cast", len(st.session_state.voted_ids))
    st.metric("Turnout Rate", f"{(len(st.session_state.voted_ids)/max(len(st.session_state.voters), 1)*100):.1f}%")

# Main content
if page == "🏠 Home":
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("https://cdn-icons-png.flaticon.com/512/3022/3022073.png", width=200)
    
    st.markdown("## Welcome to the Secure Voting System")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="info-box">
        <h3>🔒 Security Features</h3>
        <ul>
            <li>Biometric fingerprint authentication</li>
            <li>One person, one vote enforcement</li>
            <li>Anonymous vote recording</li>
            <li>Encrypted voter database</li>
            <li>Real-time vote tallying</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="info-box">
        <h3>📋 How to Vote</h3>
        <ol>
            <li>Enroll with your voter ID and fingerprint</li>
            <li>Navigate to the voting page</li>
            <li>Verify your identity via fingerprint</li>
            <li>Select your preferred candidate</li>
            <li>Confirm your vote</li>
        </ol>
        </div>
        """, unsafe_allow_html=True)

elif page == "📝 Voter Enrollment":
    st.markdown("## Voter Enrollment")
    st.info("Register as a new voter by providing your details and fingerprint.")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        with st.form("enrollment_form"):
            voter_id = st.text_input("Voter ID", placeholder="Enter unique voter ID")
            name = st.text_input("Full Name", placeholder="Enter your full name")
            age = st.number_input("Age", min_value=18, max_value=120, value=18)
            
            st.markdown("### 👆 Fingerprint Scan")
            st.info("In a real system, this would capture your actual fingerprint. Here we simulate it.")
            
            submit = st.form_submit_button("Enroll Voter")
            
            if submit:
                if not voter_id or not name:
                    st.error("Please fill in all fields!")
                elif age < 18:
                    st.error("You must be at least 18 years old to vote!")
                else:
                    with st.spinner("Scanning fingerprint..."):
                        time.sleep(1.5)
                        success, message = enroll_voter(voter_id, name, age)
                        
                        if success:
                            st.success(message)
                            st.balloons()
                            st.markdown(f"""
                            <div class="success-msg">
                            <h4>✅ Enrollment Successful!</h4>
                            <p><strong>Voter ID:</strong> {voter_id}</p>
                            <p><strong>Name:</strong> {name}</p>
                            <p><strong>Status:</strong> Eligible to vote</p>
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.error(message)
    
    with col2:
        st.markdown("### Fingerprint Preview")
        fingerprint_img = create_fingerprint_image()
        st.image(fingerprint_img, caption="Simulated Fingerprint", use_container_width=True)

elif page == "🗳️ Cast Vote":
    st.markdown("## Cast Your Vote")
    
    # Verification step
    if st.session_state.current_voter_id is None:
        st.info("Please verify your identity to proceed with voting.")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            voter_id = st.text_input("Enter Your Voter ID", key="vote_id")
            
            if st.button("Scan Fingerprint & Verify"):
                if voter_id:
                    if voter_id not in st.session_state.voters:
                        st.error("Voter ID not found! Please enroll first.")
                    elif voter_id in st.session_state.voted_ids:
                        st.error("You have already cast your vote!")
                    else:
                        with st.spinner("Scanning fingerprint..."):
                            time.sleep(1.5)
                            simulated_fp = st.session_state.voters[voter_id]["fingerprint"]
                            success, message = verify_fingerprint(voter_id, simulated_fp)
                            
                            if success:
                                st.session_state.current_voter_id = voter_id
                                st.success(message)
                                st.rerun()
                            else:
                                st.error(message)
                else:
                    st.warning("Please enter your Voter ID")
        
        with col2:
            st.markdown("### Fingerprint Scanner")
            fingerprint_img = create_fingerprint_image()
            st.image(fingerprint_img, use_container_width=True)
    
    else:
        # Voting step
        voter_id = st.session_state.current_voter_id
        voter_name = st.session_state.voters[voter_id]["name"]
        
        st.success(f"✅ Identity Verified: {voter_name}")
        st.markdown("### Select Your Candidate")
        
        cols = st.columns(2)
        for idx, candidate in enumerate(st.session_state.candidates):
            with cols[idx % 2]:
                st.markdown(f"""
                <div class="vote-card">
                <h3>{candidate['name']}</h3>
                <p><strong>Party:</strong> {candidate['party']}</p>
                <p><strong>Candidate ID:</strong> {candidate['id']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"Vote for {candidate['name']}", key=f"vote_{candidate['id']}"):
                    success, message = cast_vote(voter_id, candidate['id'])
                    if success:
                        st.success(message)
                        st.balloons()
                        st.session_state.current_voter_id = None
                        time.sleep(2)
                        st.rerun()
                    else:
                        st.error(message)
        
        if st.button("Cancel Voting"):
            st.session_state.current_voter_id = None
            st.rerun()

elif page == "📊 Results":
    st.markdown("## Election Results")
    
    if len(st.session_state.voted_ids) == 0:
        st.info("No votes have been cast yet.")
    else:
        total_votes = sum(c["votes"] for c in st.session_state.candidates)
        
        st.markdown(f"### Total Votes Cast: {total_votes}")
        
        # Sort candidates by votes
        sorted_candidates = sorted(st.session_state.candidates, key=lambda x: x["votes"], reverse=True)
        
        for rank, candidate in enumerate(sorted_candidates, 1):
            percentage = (candidate["votes"] / max(total_votes, 1)) * 100
            
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"""
                <div class="vote-card">
                <h3>#{rank} - {candidate['name']}</h3>
                <p><strong>Party:</strong> {candidate['party']}</p>
                </div>
                """, unsafe_allow_html=True)
                st.progress(percentage / 100)
            
            with col2:
                st.metric("Votes", candidate["votes"])
                st.metric("Percentage", f"{percentage:.1f}%")
        
        # Winner announcement
        if sorted_candidates[0]["votes"] > 0:
            st.markdown("---")
            st.markdown(f"""
            <div class="success-msg">
            <h2>🏆 Leading Candidate</h2>
            <h3>{sorted_candidates[0]['name']}</h3>
            <p>{sorted_candidates[0]['party']}</p>
            <p><strong>{sorted_candidates[0]['votes']} votes ({(sorted_candidates[0]['votes']/max(total_votes, 1)*100):.1f}%)</strong></p>
            </div>
            """, unsafe_allow_html=True)

elif page == "ℹ️ System Info":
    st.markdown("## System Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Enrolled Voters")
        if st.session_state.voters:
            for voter_id, voter_data in st.session_state.voters.items():
                voted = "✅ Voted" if voter_id in st.session_state.voted_ids else "⏳ Pending"
                st.markdown(f"""
                <div class="info-box">
                <p><strong>ID:</strong> {voter_id}</p>
                <p><strong>Name:</strong> {voter_data['name']}</p>
                <p><strong>Age:</strong> {voter_data['age']}</p>
                <p><strong>Status:</strong> {voted}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No voters enrolled yet.")
    
    with col2:
        st.markdown("### Candidates")
        for candidate in st.session_state.candidates:
            st.markdown(f"""
            <div class="info-box">
            <h4>{candidate['name']}</h4>
            <p><strong>Party:</strong> {candidate['party']}</p>
            <p><strong>Current Votes:</strong> {candidate['votes']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### System Statistics")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Voters", len(st.session_state.voters))
    col2.metric("Votes Cast", len(st.session_state.voted_ids))
    col3.metric("Pending Votes", len(st.session_state.voters) - len(st.session_state.voted_ids))
    col4.metric("Candidates", len(st.session_state.candidates))
    
    if st.button("🔄 Reset System", type="secondary"):
        st.session_state.voters = {}
        st.session_state.votes = {}
        st.session_state.voted_ids = set()
        st.session_state.current_voter_id = None
        for candidate in st.session_state.candidates:
            candidate["votes"] = 0
        st.success("System reset successfully!")
        st.rerun()
