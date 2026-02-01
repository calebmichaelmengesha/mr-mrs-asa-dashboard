# Mr & Mrs ASA Dashboard

A professional Streamlit-based competition scoring and management system for the Mr & Mrs ASA pageant. Features real-time scoring, dynamic leaderboards, financial tracking, and interactive data visualization.

## 🌟 Features

- **📊 Data View** - Browse and search all Excel sheets with an interactive data viewer
- **🎯 Scoring System** - Input and edit judge scores across multiple competition segments with automatic average calculation
- **🏆 Live Leaderboard** - Real-time rankings with medal displays for top 3 contestants in each category
- **💰 Financial Tracking** - Comprehensive revenue and expense management with visual analytics
- **📈 Interactive Charts** - Professional pie charts for revenue and expense distribution
- **🔍 Search & Filter** - Search functionality across all data sheets
- **📥 Export Options** - Download any data sheet as CSV

## 📸 Screenshots

### Finance Dashboard
Track revenue, expenses, and profitability at a glance with key metrics.

![Finance Metrics](screenshots/finance_metrics.png)

### Visual Analytics
Interactive pie charts for revenue and expense distribution.

![Finance Charts](screenshots/finance_charts.png)

### Scoring Interface
Intuitive side-by-side scoring interface for judges with automatic calculations.

![Scoring System](screenshots/scoring_system.png)

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/calebmichaelmengesha/mr-mrs-asa-dashboard.git
   cd mr-mrs-asa-dashboard
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Ensure the Excel file is present**
   - Make sure `mr_mrs_asa_dashboard.xlsx` is in the same directory as `app.py`

## 📖 Usage

Run the Streamlit app:
```bash
streamlit run app.py
```

The dashboard will open in your default web browser at `http://localhost:8501`

## 📁 Project Structure

```
mr-mrs-asa-dashboard/
│
├── app.py                          # Main Streamlit application
├── mr_mrs_asa_dashboard.xlsx       # Excel database (segments, scores, finances)
├── requirements.txt                # Python dependencies
├── README.md                       # Project documentation
└── screenshots/                    # Application screenshots
    ├── finance_metrics.png
    ├── finance_charts.png
    └── scoring_system.png
```

## 💾 Excel Data Structure

The Excel file contains the following sheets:

- **Participants** - Contestant information (Number, Name, Category)
- **Segments** - Competition rounds (Segment_Id, Segment_Name, Weight)
- **Scores** - Judge scores per segment per contestant
- **Tickets** - Detailed ticket sales tracking
- **Revenue** - Revenue sources and amounts
- **Expenses** - Expense categories and amounts

## 🎮 How to Use

### Scoring Tab
1. Select a competition segment from the dropdown (Introduction, Dance Performance, Talent Show)
2. Enter scores (0-10) for each of the 3 judges
3. Scores are automatically averaged in real-time
4. Click "💾 Update Scores" to save changes to the database
5. Celebrate with balloons! 🎈

### Leaderboard Tab
- View real-time rankings for Mr and Mrs ASA categories
- Top 3 contestants displayed with medal emojis 🥇🥈🥉
- Scores aggregated across all competition segments
- Expand "View Detailed Statistics" for full rankings table

### Finance & Insights Tab
- View key financial metrics: Total Revenue, Total Expenses, Net Profit/Loss
- Interactive pie charts show revenue and expense distribution
- Detailed breakdowns for each category
- Visual representation of financial health

### Data View Tab
- Browse all Excel sheets with dropdown selector
- Search functionality to filter data
- View column details including data types and null counts
- Export any sheet as CSV with one click

## 🛠️ Technologies Used

- **Streamlit** - Modern web framework for data applications
- **Pandas** - Data manipulation and analysis
- **Matplotlib** - Data visualization (pie charts)
- **OpenPyXL** - Excel file reading/writing engine

## ✨ Key Features Highlights

- **Real-time Updates** - All changes reflect immediately across tabs
- **Data Persistence** - All scores and data saved to Excel file
- **Responsive Design** - Clean, professional interface with wide layout
- **Error Handling** - Robust error messages and validation
- **Cached Data Loading** - Fast performance with `@st.cache_data`
- **User-Friendly** - Intuitive navigation with emoji icons and clear labels

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the issues page or submit a pull request.

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 👤 Author

**Caleb Mengesha**
- GitHub: [@calebmichaelmengesha](https://github.com/calebmichaelmengesha)

## ⭐ Show your support

Give a ⭐️ if this project helped you or if you found it interesting!

---

*Built with ❤️ using Streamlit*