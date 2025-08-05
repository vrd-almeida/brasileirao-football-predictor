import streamlit as st
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

from prediction import predict_winner
from data_manager import get_data_from_database


st.set_page_config(layout="wide")
st.title("📊 Brasileirão Match Explorer")

df = get_data_from_database()

if True:

    # Create tabs
    tab1, tab2 = st.tabs(["📊 Team Overview", "⚔️ Head-to-Head"])

    with tab1:
        st.header("📊 Team Overview")

        team = st.selectbox("Select team", ["All"] + sorted(df["Home"].unique()))
        season = st.selectbox("Select season", sorted(df["Season"].unique()), index=0)

        filtered_df_home = df[df["Season"] == season].copy()
        filtered_df_away = df[df["Season"] == season].copy()

        if team != "All":
            filtered_df_home = filtered_df_home[filtered_df_home["Home"] == team]
            filtered_df_away = filtered_df_away[filtered_df_away["Away"] == team]
            home_result_map = {"H": "Win", "D": "Draw", "A": "Loss"}
            away_result_map = {"H": "Loss", "D": "Draw", "A": "Win"}
            filtered_df_home["ResultLabel"] = filtered_df_home["Res"].map(
                home_result_map
            )
            filtered_df_away["ResultLabel"] = filtered_df_away["Res"].map(
                away_result_map
            )

        st.subheader(f"Matches in {season}")
        st.dataframe(filtered_df_home)

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Match Result Distribution - Home")
            fig1, ax1 = plt.subplots(figsize=(4, 3))
            if team != "All" and "ResultLabel" in filtered_df_home.columns:
                sns.countplot(
                    x="ResultLabel",
                    data=filtered_df_home,
                    order=["Win", "Draw", "Loss"],
                    ax=ax1,
                )
                ax1.set_title(f"{team} at Home")
                st.pyplot(fig1, use_container_width=False)
            else:
                st.info("Please select a specific team to view home match results.")

        with col2:
            st.subheader("Match Result Distribution - Away")
            fig2, ax2 = plt.subplots(figsize=(4, 3))
            if team != "All" and "ResultLabel" in filtered_df_away.columns:
                sns.countplot(
                    x="ResultLabel",
                    data=filtered_df_away,
                    order=["Win", "Draw", "Loss"],
                    ax=ax2,
                )
                ax2.set_title(f"{team} Away")
                st.pyplot(fig2, use_container_width=False)
            else:
                st.info("Please select a specific team to view away match results.")

        st.subheader("Goal Statistics")
        col3, col4 = st.columns(2)

        hg = filtered_df_home["HG"].value_counts().sort_index()
        ag = filtered_df_home["AG"].value_counts().sort_index()
        with col3:
            if len(hg) > 0 or len(ag) > 0:
                fig3, ax3 = plt.subplots(figsize=(6, 3))
                x = np.arange(0, max(hg.index.max(), ag.index.max()) + 1)
                ax3.bar(
                    x - 0.2,
                    hg.reindex(x, fill_value=0),
                    width=0.4,
                    label="Team Goals (Home)",
                    color="blue",
                )
                ax3.bar(
                    x + 0.2,
                    ag.reindex(x, fill_value=0),
                    width=0.4,
                    label="Opponent Goals (Away)",
                    color="red",
                )
                ax3.set_title(f"{team} as Home")
                ax3.set_xlabel("Goals")
                ax3.set_ylabel("Matches")
                ax3.set_xticks(x)
                ax3.legend()
                st.pyplot(fig3, use_container_width=False)
            else:
                st.info(f"There are no matches of {team} in the selected year.")

        ag_team = filtered_df_away["AG"].value_counts().sort_index()
        hg_opp = filtered_df_away["HG"].value_counts().sort_index()
        with col4:
            if len(ag_team) > 0 or len(hg_opp) > 0:
                fig4, ax4 = plt.subplots(figsize=(6, 3))
                x2 = np.arange(0, max(ag_team.index.max(), hg_opp.index.max()) + 1)
                ax4.bar(
                    x2 - 0.2,
                    ag_team.reindex(x2, fill_value=0),
                    width=0.4,
                    label="Team Goals (Away)",
                    color="blue",
                )
                ax4.bar(
                    x2 + 0.2,
                    hg_opp.reindex(x2, fill_value=0),
                    width=0.4,
                    label="Opponent Goals (Home)",
                    color="red",
                )
                ax4.set_title(f"{team} as Away")
                ax4.set_xlabel("Goals")
                ax4.set_ylabel("Matches")
                ax4.set_xticks(x2)
                ax4.legend()
                st.pyplot(fig4, use_container_width=False)
            else:
                st.info(f"There are no matches of {team} in the selected year.")

    with tab2:
        st.header("⚔️ Head-to-Head Analysis")
        teams = sorted(set(df["Home"].unique()) | set(df["Away"].unique()))
        col1, col2 = st.columns(2)
        with col1:
            team_home = st.selectbox("Select Home Team", teams, key="team_home")
        with col2:
            team_away = st.selectbox("Select Away Team", teams, key="team_away")

        head_to_head = df[
            ((df["Home"] == team_home) & (df["Away"] == team_away))
            | ((df["Home"] == team_away) & (df["Away"] == team_home))
        ].copy()

        st.subheader(f"Matches between {team_home} and {team_away} (since 2012)")
        st.dataframe(head_to_head)

        home_result_map = {"H": "Win", "D": "Draw", "A": "Loss"}
        away_result_map = {"H": "Loss", "D": "Draw", "A": "Win"}

        h2h_home_vs_away = head_to_head[head_to_head["Home"] == team_home].copy()
        h2h_away_vs_home = head_to_head[head_to_head["Away"] == team_home].copy()

        h2h_home_vs_away["ResultLabel"] = h2h_home_vs_away["Res"].map(home_result_map)
        h2h_away_vs_home["ResultLabel"] = h2h_away_vs_home["Res"].map(away_result_map)

        col3, col4 = st.columns(2)

        with col3:
            st.subheader(f"{team_home} vs {team_away}")
            fig1, ax1 = plt.subplots(figsize=(4, 3))
            sns.countplot(
                x="ResultLabel",
                data=h2h_home_vs_away,
                order=["Win", "Draw", "Loss"],
                ax=ax1,
            )
            ax1.set_title(f"Results for {team_home}")
            st.pyplot(fig1, use_container_width=False)

        with col4:
            st.subheader(f"{team_away} vs {team_home}")
            fig2, ax2 = plt.subplots(figsize=(4, 3))
            sns.countplot(
                x="ResultLabel",
                data=h2h_away_vs_home,
                order=["Win", "Draw", "Loss"],
                ax=ax2,
            )
            ax2.set_title(f"Results for {team_away}")
            st.pyplot(fig2, use_container_width=False)

        st.subheader("Goals Scored in Head-to-Head Matches")
        col5, col6 = st.columns(2)

        hg = h2h_home_vs_away["HG"].value_counts().sort_index()
        ag = h2h_home_vs_away["AG"].value_counts().sort_index()
        with col5:
            if len(hg) > 0 or len(ag) > 0:
                fig3, ax3 = plt.subplots(figsize=(6, 3))

                x = np.arange(0, max(hg.index.max(), ag.index.max()) + 1)
                ax3.bar(
                    x - 0.2,
                    hg.reindex(x, fill_value=0),
                    width=0.4,
                    label=f"{team_home} Goals as Home",
                    color="blue",
                )
                ax3.bar(
                    x + 0.2,
                    ag.reindex(x, fill_value=0),
                    width=0.4,
                    label=f"{team_away} Goals as Away",
                    color="red",
                )
                ax3.set_title(f"{team_home} vs {team_away}")
                ax3.set_xticks(x)
                ax3.legend()
                st.pyplot(fig3, use_container_width=False)
            else:
                st.info(f"There are no matches of {team_home} vs. {team_away}.")

        ag_team = h2h_away_vs_home["AG"].value_counts().sort_index()
        hg_opp = h2h_away_vs_home["HG"].value_counts().sort_index()
        with col6:
            if len(ag_team) > 0 or len(hg_opp) > 0:
                fig4, ax4 = plt.subplots(figsize=(6, 3))
                x2 = np.arange(0, max(ag_team.index.max(), hg_opp.index.max()) + 1)
                ax4.bar(
                    x2 - 0.2,
                    ag_team.reindex(x2, fill_value=0),
                    width=0.4,
                    label=f"{team_home} Goals as Away",
                    color="blue",
                )
                ax4.bar(
                    x2 + 0.2,
                    hg_opp.reindex(x2, fill_value=0),
                    width=0.4,
                    label=f"{team_away} Goals as Home",
                    color="red",
                )
                ax4.set_title(f"{team_away} vs {team_home}")
                ax4.set_xticks(x2)
                ax4.legend()
                st.pyplot(fig4, use_container_width=False)
            else:
                st.info(f"There are no matches of {team_away} vs. {team_home}.")

        # Calculate simple features: win rate as home/away
        home_as_home_win_rate = (
            len(h2h_home_vs_away[h2h_home_vs_away["ResultLabel"] == "Win"])
            / len(h2h_home_vs_away)
            if len(h2h_home_vs_away) > 0
            else None
        )
        # home_as_away_win_rate = len(h2h_away_vs_home[h2h_away_vs_home["ResultLabel"] == "Win"]) / len(h2h_away_vs_home) if len(h2h_away_vs_home) > 0 else None
        away_as_away_win_rate = (
            len(h2h_home_vs_away[h2h_home_vs_away["ResultLabel"] == "Loss"])
            / len(h2h_home_vs_away)
            if len(h2h_home_vs_away) > 0
            else None
        )
        draws_home_vs_away = (
            len(h2h_home_vs_away[h2h_home_vs_away["ResultLabel"] == "Draw"])
            / len(h2h_home_vs_away)
            if len(h2h_home_vs_away) > 0
            else None
        )

        # Calculate average goals scored/conceded
        home_as_home_avg_scored = (
            h2h_home_vs_away["HG"].mean() if len(h2h_home_vs_away) > 0 else None
        )
        home_as_home_avg_conceded = (
            h2h_home_vs_away["AG"].mean() if len(h2h_home_vs_away) > 0 else None
        )
        home_as_away_avg_scored = (
            h2h_away_vs_home["AG"].mean() if len(h2h_away_vs_home) > 0 else None
        )
        home_as_away_avg_conceded = (
            h2h_away_vs_home["HG"].mean() if len(h2h_away_vs_home) > 0 else None
        )

        if team_home != team_away:

            result = predict_winner(
                df=df,
                home_as_home_avg_scored=home_as_home_avg_scored,
                home_as_home_avg_conceded=home_as_home_avg_conceded,
                home_as_away_avg_scored=home_as_away_avg_scored,
                home_as_away_avg_conceded=home_as_away_avg_conceded,
                team_home=team_home,
                team_away=team_away,
            )

            st.subheader("🔮 Match Outcome Prediction")
            st.markdown(
                f"**Prediction:** `{team_home}` vs `{team_away}` → **Predicted Result:** `{result}`"
            )

            # Optional: Show features
            st.markdown("**Feature Snapshot:**")
            st.json(
                {
                    f"Nb of matches since 2012 {team_home} as Home vs {team_away} as Away": len(
                        h2h_home_vs_away
                    ),
                    f"{team_home} as Home win rate": round(home_as_home_win_rate, 2),
                    f"{team_away} as Away win rate": round(away_as_away_win_rate, 2),
                    # f"{team_home} win rate as Away": round(home_as_away_win_rate, 2),
                    # f"{team_away} win rate as Home": None,
                    f"Draws {team_home} as Home vs {team_away} as Away": round(
                        draws_home_vs_away, 2
                    ),
                    # f"Draws {team_away} as Home": None,
                    f"{team_home} as Home avg goals scored": round(
                        home_as_home_avg_scored, 2
                    ),
                    # f"{team_home} as Home avg goals conceded": round(home_avg_conceded, 2),
                    f"{team_away} as Away avg goals scored": round(
                        home_as_home_avg_conceded, 2
                    ),
                    # f"{team_away} as Away avg goals conceded": round(away_avg_conceded, 2)
                }
            )
