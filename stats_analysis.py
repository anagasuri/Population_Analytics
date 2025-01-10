import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from datetime import datetime
import matplotlib.pyplot as plt
import scipy.stats as stats
import seaborn as sns
from scipy.stats import f_oneway

df = pd.read_csv("ms_data_edited.csv")

df['visit_date'] = pd.to_datetime(df['visit_date'])

# 1. Analyze walking speed:
#    - Multiple regression with education and age
#    - Account for repeated measures
#    - Test for significant trends

walkingSpeedRegress = smf.mixedlm("walking_speed ~ age + education_level", df, groups=df["patient_id"])
result = walkingSpeedRegress.fit()
print(result.summary())

# 2. Analyze costs:
#    - Simple analysis of insurance type effect
#    - Box plots and basic statistics
#    - Calculate effect sizes

plt.figure(figsize=(8, 6))
sns.boxplot(x='insurance_type', y='visit_cost', data=df)
plt.title('Cost Distributions by Insurance Type')
plt.xlabel('Insurance')
plt.ylabel('Cost')
plt.savefig('inscostbox.png')
plt.show()

anovaAnalysis = smf.ols('visit_cost ~ insurance_type', data=df).fit()
statTable = sm.stats.anova_lm(anovaAnalysis, typ=2)  
print("ANOVA Table:")
print(statTable)

insurance_groups = [group['visit_cost'].values for name, group in df.groupby('insurance_type')]
f_stat, p_value = f_oneway(*insurance_groups)
print(f"ANOVA F-stat: {f_stat}, p-value: {p_value}")

plt.figure(figsize=(8, 6))
sns.barplot(x='insurance_type', y='visit_cost', data=df, errorbar='sd')
plt.title('Mean Visit Costs by Insurance Type')
plt.xlabel('Insurance')
plt.ylabel('Cost')
plt.savefig('inscostmeanbox.png')
plt.show()

# 3. Advanced analysis:
#    - Education age interaction effects on walking speed
#    - Control for relevant confounders
#    - Report key statistics and p-values

column = 'walking_speed'

Q1 = df[column].quantile(0.25)
Q3 = df[column].quantile(0.75)
IQR = Q3 - Q1

lower = Q1 - 1.5 * IQR
upper = Q3 + 1.5 * IQR

outliers = df[(df[column] < lower) | (df[column] > upper)]
df_cleaned = df[(df[column] >= lower) & (df[column] <= upper)]

df_cleaned['education_level_encoded'] = df_cleaned['education_level'].astype('category').cat.codes
df_cleaned['education_age_interaction'] = df_cleaned['education_level_encoded'] * df_cleaned['age']


model_interaction = smf.ols('walking_speed ~ education_level * age', data=df_cleaned).fit()
print(model_interaction.summary())

model_confounded = smf.ols('walking_speed ~ education_level * age + insurance_type', data=df_cleaned).fit()
print(model_confounded.summary())

formula = "walking_speed ~ age + education_level + education_age_interaction + insurance_type + season"
model = smf.mixedlm(formula, data=df_cleaned, groups=df_cleaned['patient_id'])
result = model.fit()
print(result.summary())