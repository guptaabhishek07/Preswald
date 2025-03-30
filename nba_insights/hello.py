from preswald import text, plotly, connect, get_df, table, query, slider, selectbox, button
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Step 1: Load the Dataset
connect()
df = get_df("nba_data_processed")

# Step 2: Calculate Efficiency Metric
df["Efficiency"] = (df["PTS"] + df["TRB"] + df["AST"] + df["STL"] + df["BLK"]) - (df["FGA"] - df["FG"]) - df["TOV"]

# Step 3: UI Title
text("# NBA Player Stats Dashboard 🏀")
text("Analyzing player performance using NBA statistics.")

# Step 4: Filters
threshold = slider("Threshold for Points", min_val=0, max_val=50, default=20)
selected_team = selectbox("Select Team", options=list(df["Tm"].dropna().unique()))
player1 = selectbox("Select Player 1", options=list(df["Player"].dropna().unique()))
player2 = selectbox("Select Player 2", options=list(df["Player"].dropna().unique()))

# Step 5: Filtered Data Table
filtered_df = df[df["PTS"] > threshold]
table(filtered_df, title="Dynamic Player Stats View")

# Step 6: Team-Specific Data Table
team_df = df[df["Tm"] == selected_team]
table(team_df, title=f"Players from {selected_team}")

# Step 7: Visualization - Assists vs. Rebounds
fig1 = px.scatter(df, x="AST", y="TRB", color="Tm", title="NBA Players: Assists vs Rebounds")
plotly(fig1)

# Step 8: Visualization - Shooting Percentage by Player
fig2 = px.bar(df, x="Player", y="FG%", color="Tm", title="Shooting Percentage by Player")
plotly(fig2)

# Step 9: Visualization - Team Shooting Efficiency
fig3 = px.box(df, x="Tm", y="eFG%", title="Team Shooting Efficiency Distribution")
plotly(fig3)

# Step 10: Visualization - Player Efficiency Score
fig4 = px.bar(df, x="Player", y="Efficiency", color="Tm", title="Player Efficiency Score")
plotly(fig4)

# Step 11: Player Comparison
player1_stats = df[df["Player"] == player1]
player2_stats = df[df["Player"] == player2]

if not player1_stats.empty and not player2_stats.empty:
    player1_stats = player1_stats.iloc[0]
    player2_stats = player2_stats.iloc[0]

    fig5 = go.Figure()
    fig5.add_trace(go.Bar(name=player1, x=["Points", "Rebounds", "Assists"], 
                          y=[player1_stats["PTS"], player1_stats["TRB"], player1_stats["AST"]]))
    fig5.add_trace(go.Bar(name=player2, x=["Points", "Rebounds", "Assists"], 
                          y=[player2_stats["PTS"], player2_stats["TRB"], player2_stats["AST"]]))
    fig5.update_layout(barmode='group', title="Player Comparison: Points, Rebounds & Assists")
    plotly(fig5)
else:
    text("⚠️ Selected player data not found. Please choose valid players.")

# Step 12: Refresh Data Button
if button("Refresh Data"):
    df = get_df("nba_data_processed")
    table(df.head(100), title="Updated NBA Dataset")

# Step 13: Display Raw Data Table
table(df.head(100), title="NBA Player Data (First 100 Rows)")
