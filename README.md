📊 EduFlow Student Dashboard (Dash + Plotly)

A web-based interactive analytics dashboard built using Python, Dash, Plotly, and Pandas to analyze academic performance of BCA students. This dashboard allows faculty or administrators to upload student marks data and instantly visualize performance insights such as pass/fail status, gender-wise distribution, mark ranges, and KPIs.



🚀 Features

• 📂 Upload CSV or Excel files (Drag & Drop supported)

• 🎯 Subject-wise performance analysis

• 📈 Automatic calculation of Total Marks

• 🧮 Key Performance Indicators (KPIs):

   ○ Total Students

   ○ Boys Percentage (%)

   ○ Girls Percentage (%)

   ○ Average Marks


• 📊 Interactive visualizations:

  ○ Gender distribution (Pie chart)

  ○ Marks distribution by range (Histogram)

  ○ Pass vs Fail comparison (Bar chart)

  ○ Gender-wise Pass & Fail analysis (Donut charts)


• 🎨 Clean pastel UI suitable for academic dashboards



---

🛠️ Tech Stack

• Python 3.9+

• Dash – Web framework

• Plotly Express – Interactive charts

• Pandas – Data processing

• Base64 / IO – File upload handling




📁 Project Structure

student-dashboard/
│
├── app.py            # Main Dash application
├── README.md         # Project documentation
├── requirements.txt  # Python dependencies
└── sample_data.xlsx  # (Optional) Sample dataset



📊 Required Dataset Format

The uploaded file must contain the following columns:

Column Name	             Description

Course	                 Course name (e.g., BCA)
Gender	                 Boy / Girl
Subject	                 Subject name
Internal_1	             Internal exam 1 marks
Internal_2	             Internal exam 2 marks
External	               External exam marks




⚙️ Installation & Setup

1️⃣ Clone the Repository

git clone https://github.com/your-username/bca-student-dashboard.git
cd bca-student-dashboard

2️⃣ Create Virtual Environment (Optional but Recommended)

python -m venv venv
source venv/bin/activate   # For Windows: venv\Scripts\activate

3️⃣ Install Dependencies

pip install dash plotly pandas

4️⃣ Run the Application

python app.py

Open your browser and go to:

👉 http://127.0.0.1:8050/




🧠 How It Works

1. Upload student marks file (CSV / Excel)


2. Dashboard filters data for BCA course only


3. Select a subject from the dropdown


4. Dashboard updates all KPIs and charts dynamically


5. Pass/Fail is calculated using:



PASS_MARK = 50




🎯 Use Cases

• College internal assessment analysis

• Department level academic reviews

• Faculty performance tracking

• Student result visualization




📌 Customization Ideas

• Add semester-wise filters

• Export reports as PDF

• Role-based login (Admin / Faculty)

• Predict performance using ML

• Connect with database (MySQL / PostgreSQL)




📸 Screenshots
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/bb609b90-e1ef-4950-aa8a-282626d92165" />

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/d1363851-6540-48ac-9144-b224336cc2e4" />





🧑‍💻 Author

Sreelekshmi A A (https://github.com/sreelekshmiaa)

Theertha Sunil (https://github.com/theerthasunil066-boop)

Shivganga R T ()

Course: BCA (Data Science & AI)

Institution: Asian School of Business




📜 License

This project is for educational purposes. You are free to modify and use it for academic projects.
