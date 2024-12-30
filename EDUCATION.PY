import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns



# Data
data = {
    'Country': ['India (Private)', 'India (Govt)', 'Russia', 'Philippines', 'USA'],
    'Cost (in Lakhs)': [90, 10, 35, 38, 100]
}



# Create DataFrame
df = pd.DataFrame(data)



# Bar Graph for Cost Comparison
plt.figure(figsize=(8, 5))
sns.barplot(x='Country', y='Cost (in Lakhs)', data=df, palette='viridis')
plt.title('Cost of Medical Education')
plt.xlabel('Country')
plt.ylabel('Cost (in Lakhs)')
plt.show()



# Percentage of Students Admission
total_neet_students = 1500000  # Approximate
seats_in_india = 109000
percent_admission = (seats_in_india / total_neet_students) * 100
percent_abroad = 100 - percent_admission



# Pie Chart
labels = ['India Admission', 'Abroad Admission']
sizes = [percent_admission, percent_abroad]
colors = ['gold', 'lightblue']
explode = (0.1, 0)  # Highlight the first slice




plt.figure(figsize=(6, 6))
plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
plt.title('Medical Admissions: India vs Abroad')
plt.show()