# 🏆 Brasileirão Match Explorer ⚽

An interactive Streamlit app for exploring data from the top Brazilian football league (Brasileirão), visualizing team performance, and predicting match outcomes using simple statistical models.

---

## 📌 Project Summary

This project enables users to:

- 📊 Browse team performance season by season  
- ⚔️ Analyze head-to-head results between two teams  
- 🔮 Predict match outcomes (Win / Draw / Loss) based on past statistics  

Built entirely with open-source tools: `Streamlit`, `pandas`, `matplotlib`, `seaborn`, and `scikit-learn`.

---

## 🧠 Model Overview & Assumptions

The current predictive model is based on **Logistic Regression**, trained using past head-to-head data between two selected teams. It uses four basic features:

| Feature                      | Description                                          |
|-----------------------------|------------------------------------------------------|
| `home_as_home_avg_scored`   | Avg. goals scored by the home team at home           |
| `home_as_home_avg_conceded` | Avg. goals conceded by the home team at home         |
| `home_as_away_avg_scored`   | Avg. goals scored by the home team in away matches   |
| `home_as_away_avg_conceded` | Avg. goals conceded by the home team in away matches |

### 🔍 Assumptions

- Only historical **head-to-head** matches are used for training  
- No live form, injuries, or standings are included (yet)  
- Requires at least 3 home and 3 away matches to train  
- Logistic regression (multinomial: `H`, `D`, `A`) is used for classification  
- The model is designed to be **educational and interpretable**, not production-grade or betting-optimized

---

## 🖥️ App Interface

### **Tab 1: Team Overview**
- Filter by season and team
- Distribution of match outcomes (Win / Draw / Loss)
- Goals scored and conceded at home and away

### **Tab 2: Head-to-Head**
- View historical matchups between any two teams
- Visualize result distribution and goal patterns
- 🔮 Basic prediction of match outcome

---

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/brasileirao-football-predictor.git
cd brasileirao-football-predictor

# Install dependencies
pip install -r requirements.txt

# Launch the app
streamlit run app/streamlit_app.py
```


## 🛣️ Roadmap — Future Improvements

| Feature                                | Status     | Notes                                      |
|----------------------------------------|------------|--------------------------------------------|
| Team & season filtering                | ✅ Done     | Fully functional                           |
| Head-to-head analysis tab              | ✅ Done     | Interactive visualizations                 |
| Basic logistic regression model        | ✅ Done     | Based on avg. goals scored/conceded        |
| Predict match scores (Poisson)         | ⏳ Planned  | Use statistical models for goal prediction |
| Use full match history (not just H2H)  | ⏳ Planned  | Build generalizable models                 |
| Live data/API integration              | ⏳ Planned  | E.g. integrate football-data APIs          |
| SQLite or PostgreSQL database          | ⏳ Planned  | For persistent storage                     |
| Add advanced ML models (XGBoost, etc.) | ⏳ Planned  | For improved accuracy                      |
| UI enhancements                        | ⏳ Planned  | Logos, colors, layout                      |
| CI/CD + unit tests                     | ⏳ Planned  | Toward production-readiness                |

## 👨‍💻 Author

Vinicius Rodrigues De Almeida, PhD.

📍 Based in Lyon, France 🇫🇷

💡 Interests: optimization, machine learning, AI

🔗 https://www.linkedin.com/in/vinicius-rodrigues-de-almeida-2a575084/