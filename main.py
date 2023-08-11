# % imports
import streamlit as st
import pandas as pd
from PIL import Image
from mplsoccer import VerticalPitch
import tools.logos_and_badges as lab
import warnings
import streamlit.components.v1 as components


st.set_page_config(
    page_title="Lineup Creator App",
    page_icon="👕",
    layout="centered",
    # initial_sidebar_state="expanded",
)


def get_XI(selected_players):
    players = pd.read_csv("resources/players.csv")
    XI = players.set_index('Name').loc[selected_players].reset_index(inplace=False)
    return XI


def create_lineup(title, formation, XI, competition, opponent, match_type="Home"):
    # create figure and pitch
    pitch = VerticalPitch(pitch_type='opta', pitch_color='#313332', line_color='white', line_alpha=0.2,
                          line_zorder=3)
    fig, axes = pitch.grid(endnote_height=0.05, endnote_space=0, title_height=0.12, axis=False, grid_height=0.79)
    fig.set_size_inches(7, 9)
    fig.set_facecolor('#313332')

    # Add competition logo
    add_competition_logo(fig, competition)

    # add header (titles, teams logo)
    add_header(fig, title, opponent, match_type)

    # add footer text
    add_footer(fig)

    # add twitter logo
    add_twitter_logo(fig)

    # add players
    add_players_to_the_pitch(formation, XI, pitch, axes['pitch'])

    return fig


def add_competition_logo(fig, competition):
    comp_logo = lab.get_competition_logo(competition, 2022, True)
    ax = fig.add_axes([0.03, 0.85, 0.14, 0.15])
    ax.axis("off")
    ax.imshow(comp_logo)


def add_header(fig, title, opponent, match_type="Home"):
    # title
    # title_text = f"Manchester City vs {opponent} - Predicted Lineup"
    fig.text(0.5, 0.965, title, fontweight="bold", ha="center", fontsize=11, color='w')

    # Add team 1 logo
    team1_logo, _ = lab.get_team_badge_and_colour("Man City")
    ax_team1 = fig.add_axes([0.26, 0.84, 0.115, 0.115])
    ax_team1.axis("off")

    # Add team 2 logo
    team2_logo, _ = lab.get_team_badge_and_colour(opponent)
    ax_team2 = fig.add_axes([0.62, 0.84, 0.115, 0.115])
    ax_team2.axis("off")

    if (match_type == "Home"):
        ax_team1.imshow(team1_logo)
        ax_team2.imshow(team2_logo)
    else:
        ax_team2.imshow(team1_logo)
        ax_team1.imshow(team2_logo)

    # Add vs badge
    vs_badge = Image.open('resources/pvp.png')
    ax_vs = fig.add_axes([0.465, 0.865, 0.075, 0.075])
    ax_vs.axis("off")
    ax_vs.imshow(vs_badge)


def add_footer(fig):
    # Add footer text
    fig.text(0.5, 0.025, "Created By: SaMiR (Twitter: @26RMCFC)",
             fontstyle="italic", ha="center", fontsize=9, color="white")


def add_twitter_logo(fig):
    # Add twitter logo
    logo_ax = fig.add_axes([0.91, -0.005, 0.07, 0.07])
    logo_ax.axis("off")
    badge = Image.open('resources/logo-rounded.png')
    logo_ax.imshow(badge)


def detect_positions_by_formation(formation):
    match formation:
        case '433':
            return [1, 2, 5, 6, 3, 4, 7, 8, 10, 11, 9]
        case '442':
            return [1, 2, 5, 6, 3, 7, 4, 8, 11, 10, 9]
        case '4411':
            return [1, 2, 5, 6, 3, 7, 4, 8, 11, 10, 9]
        case '4141':
            return [1, 2, 5, 6, 3, 4, 7, 8, 10, 11, 9]
        case '4231':
            return [1, 2, 5, 6, 3, 8, 4, 7, 10, 11, 9]
        case '3241':
            return [1, 6, 5, 4, 2, 3, 10, 7, 8, 11, 9]
        case default:
            return [1, 2, 5, 6, 3, 4, 7, 8, 10, 11, 9]

def add_players_to_the_pitch(formation, XI, pitch, ax_pitch):
    positions = detect_positions_by_formation(formation)
    players = XI['Name'].tolist()
    shirt_numbers = XI['Shirt Number'].tolist()
    player_images = [Image.open(image) for image in XI['Image'].tolist()]

    text_names = pitch.formation(formation, kind='text', positions=positions,
                                 text=players, ax=ax_pitch,
                                 xoffset=-2,  # offset the player names from the centers
                                 ha='center', va='center', color='white', fontsize=11)

    text_scores = pitch.formation(formation, kind='text', positions=positions,
                                  text=shirt_numbers, ax=ax_pitch,
                                  xoffset=-5,  # offset the scores from the centers
                                  ha='center', va='center', color='white', fontsize=11,
                                  bbox=dict(facecolor='#6CABDD', boxstyle='round,pad=0.2', linewidth=0))

    badge_axes = pitch.formation(formation, kind='image', positions=positions,
                                 image=player_images, height=10, ax=ax_pitch,
                                 xoffset=5,  # offset the images from the centers
                                 )


def get_all_players():
    df = pd.read_csv("resources/players.csv")
    return df['Name'].tolist()


def get_positions(formation):
    df = pd.read_csv("resources/formations_and_positions.csv")
    return df[formation].tolist()


def get_default_selected_players_idx(formation):
    match formation:
        case '433':
            return [2, 3, 11, 6, 8, 20, 13, 14, 21, 15, 23]
        case '442':
            return [1, 12, 11, 6, 4, 21, 20, 19, 15, 22, 23]
        case '4411':
            return [1, 12, 11, 6, 8, 21, 20, 16, 14, 13, 23]
        case '4141':
            return [1, 3, 11, 6, 4, 20, 21, 13, 16, 15, 23]
        case '4231':
            return [2, 3, 11, 6, 8, 20, 16, 21, 13, 14, 23]
        case '3241':
            return [1, 12, 6, 3, 11, 20, 21, 13, 14, 15, 23]
        case default:
            return [2, 3, 11, 6, 8, 20, 13, 14, 21, 15, 23]

# Remove Warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)
pd.options.mode.chained_assignment = None

st.markdown('<p style="font-size: 48px; font-weight: bold;">👕 Man City Lineup Creator:</p>', unsafe_allow_html=True)
st.markdown("""---""")

# % user inputs
# formation = "433"
# competition = "EPL"
# opponent = "Burnley"
# match_type = "Away"
# selected = ['Ortega', 'Akanji', 'Stones', 'Dias', 'Gvardiol', 'Rodri', 'De Bruyne', 'Foden', 'Bernardo', 'Grealish', 'Haaland']

#######################################################################
############################# Sidebar #################################
with st.sidebar:
    st.markdown('<h4 style="font-family: Consolas; font-size: 24px;">Config Lineup Here ...</h4>',
                unsafe_allow_html=True)

    clubs = ['Arsenal', 'Aston Villa', 'Bournemouth', 'Brentford', 'Brighton', 'Burnley',
             'Chelsea', 'Crystal Palace', 'Everton', 'Fulham', 'Liverpool', 'Luton Town', 'Manchester Utd',
             'Newcastle United', 'Nottingham Forest', 'Sheffield Utd', 'Tottenham Hotspur',
             'West Ham United', 'Wolves', 'Sevilla']

    selected_players = [None] * 11

    players = get_all_players()

    title = st.text_input('Title', max_chars=55,
                          placeholder="Ex: Manchester City vs Liverpool")

    st.markdown(
        '<p style="color: #FFC659; font-size: 10px; margin-top: -0.8rem; padding-left: 4px;">Note: You can leave it blank and we will take care</p>',
        unsafe_allow_html=True)

    formation = st.selectbox('Shape:', ['433', '442', '4411', '4141', '4231', '3241'], index=5,
                             format_func=lambda shape: '-'.join(list(shape)))
    competition = st.selectbox('Competition:', ['Premier League', 'UEFA Super Cup', 'UEFA Champions League'], index=0)
    match_type = st.selectbox('Match Type:', ['Home', 'Away'], index=0)
    opponent = st.selectbox('Opponent:', clubs, index=0)

    if not title:
        title = f"Manchester City vs {opponent} - Predicted Lineup"

    st.markdown('<h4 style="font-family: Consolas; font-size: 18px;">Now Select Players ...</h4>',
                unsafe_allow_html=True)

    default_players_idx = get_default_selected_players_idx(formation)
    positions = get_positions(formation)

    for i, position in enumerate(positions):
        selected_players[i] = st.selectbox(f'{position}:', players, index=default_players_idx[i])

    st.markdown('<h4 style="font-family: Consolas; font-size: 20px;">And Let The Magic Happen ➡️</h1>', unsafe_allow_html=True)

    components.html(
        """
            <div style="margin-top: 20px; display: flex; align-items: end; justify-content: center;">
                <script type="text/javascript" 
                    src="https://cdnjs.buymeacoffee.com/1.0.0/button.prod.min.js" 
                    data-name="bmc-button" 
                    data-slug="samiir" 
                    data-color="#6CABDD" 
                    data-emoji=""  
                    data-font="Cookie" 
                    data-text="Buy me a coffee" 
                    data-outline-color="#000000" 
                    data-font-color="#000000" 
                    data-coffee-color="#ffffff">
                </script>
            <div>
        """, height=100
    )


XI = get_XI(selected_players)
fig = create_lineup(title, formation, XI, competition, opponent, match_type)

st.pyplot(fig)

f_title = f"ManchesterCity_VS_{opponent}_PredictedLineup"
fig.savefig(f"output/{f_title}", dpi=850)
col1, col2, col3 = st.columns(3)

with open(f"output/{f_title}.png", "rb") as file:
    btn = col2.download_button(
            label="Download High Quality Image",
            data=file,
            file_name=f"{f_title}.png",
            mime="image/png"
          )

#st.markdown("""---""")

info_expander = st.expander("See Explanation")
info_expander.write("Simple app to create line-up for manchester city, allows you to choose the formation, players ...")
info_expander.write(">*Created By SaMiR (Twitter: :blue[@26rmcfc])*")
