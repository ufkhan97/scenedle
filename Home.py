import streamlit as st
import anthropic
import datetime

st.title('🎭 SCENEDLE  🤪')
st.subheader("Silly Scene Solver")
# Initialize the Anthropic client
client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])

def generate_daily_scenario():
    today = datetime.date.today().strftime("%Y-%m-%d")
    response = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=150,
        messages=[
            {
                "role": "user",
                "content": f"""Generate a ridiculous and absurd scenario where someone is in a comically inconvenient situation. Use the date {today} as a seed for consistency. Keep it brief and humorous. Here's an example:

                "It's {today}, and you find yourself stuck in an elevator with a mariachi band, a llama, and a malfunctioning karaoke machine that only plays 'Never Gonna Give You Up' on repeat. Your hearing aid is about to bust if they keep playing, but if you're rude, the llama will spit on you. What do you do to make it quieter without becoming a saliva statue?"

                "It's {today}, and you discover you've accidentally super-glued yourself to your office chair during a video conference with the CEO. Your cat is slowly pushing your laptop off the desk, and your roommate just started a very loud vacuum cleaning session. What do you do to maintain your professional composure and save your laptop without revealing your sticky situation?"

                "It's {today}, and you wake up to find you've been shrunk to the size of a mouse. Your smartphone is now the size of a billboard, and your cat thinks you're a new toy. You have an important job interview in an hour, but your car keys are now too heavy to lift. What do you do to get to your interview on time and explain your tiny predicament?"

                Now, generate a new scenario that's equally absurd and funny, but different from this example. Keep it under 70 words."""
            }
        ]
    )
    return response.content[0].text

def simulate_outcome(scenario, user_plan):
    simulation_prompt = f"""Given this scenario: {scenario}

    The person's plan to solve it is: {user_plan}

    Simulate what would happen if they did this. Be creative and humorous in your description. Keep the entire simulation under 110 words.

    Follow these steps:

    1. Start directly with the outcome, without any introductory phrases.
    2. Play out the scenario step by step, including:
       a. Initial actions based on the person's plan
       b. Immediate consequences of those actions
       c. Any unexpected twists that occur
       d. How the situation evolves or escalates
       e. The final resolution or outcome
    3. At the end, provide a success percentage (to 2 decimal points) based on how well the plan solved the original problem.
    4. At the end, use no more than 3 lines of 7 emojis each to summarize what happened. Never use the same emoji twice in a row. The first line should be the initial situation, the second line the outcome, and the third line the final resolution.

    Remember to maintain a lighthearted and entertaining tone throughout the simulation.
    
    """
    
    response = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=300,
        messages=[
            {"role": "user", "content": simulation_prompt}
        ]
    )
    
    return response.content[0].text



def create_shareable_text(scenario, user_plan, outcome):
    url = 'https://www.scenedle.streamlit.app'
    full_text = f"Scenario: {scenario}\n\nSolution Plan: {user_plan}\n\nOutcome: {outcome}\n\nPlay: {url}"
    st.code(full_text, language="text")
    st.info("Use the copy button in the top right to share your result!")

# Initialize session state variables
if 'daily_scenario' not in st.session_state:
    st.session_state.daily_scenario = generate_daily_scenario()

if 'user_input' not in st.session_state:
    st.session_state.user_input = ""

# Main app logic
st.write("Today's Silly Situation:")

st.markdown(f"**{st.session_state.daily_scenario}**")

user_input = st.text_input("What would you do to solve this situation?", value=st.session_state.user_input)

if user_input:
    st.session_state.user_input = user_input
    if 'simulation_outcome' not in st.session_state:
        st.session_state.simulation_outcome = simulate_outcome(st.session_state.daily_scenario, user_input)
    
    st.write(st.session_state.simulation_outcome)

    if st.button("Share Result"):
        create_shareable_text(st.session_state.daily_scenario, user_input, st.session_state.simulation_outcome)

if st.button("Generate New Scenario"):
    st.session_state.daily_scenario = generate_daily_scenario()
    st.session_state.user_input = ""
    if 'simulation_outcome' in st.session_state:
        del st.session_state.simulation_outcome
    st.rerun()