import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import os

cwd = os.getcwd()

# Load the data from the Excel file
path = os.path.join(cwd, 'mains/results/TYPE_IID/processed_outputs')
file_path = os.path.join(path, 'stacked_bar_chart.xlsx')
df = pd.read_excel(file_path, sheet_name='Tabelle1')


# Set the 'Formations' column as index (optional, based on how your data is structured)
df.set_index('Formacion', inplace=True)
# Compute the mean values for each row (i.e., for each formation)
print(df.mean(axis=1))


cmap = cm.get_cmap('viridis', len(df.columns))
# Plot the stacked bar chart
df.plot(kind='bar', stacked=True, figsize=(10, 7), color = cmap(range(len(df.columns))))

# Customize chart labels and title
plt.ylabel('Índice TTI')
plt.xlabel('Formaciones geológicas')
plt.xticks(rotation = 0)
plt.title('Gráfico de barras apiladas del índice TTI para las formaciones de la Cuenca Atrato\nQuerógeno tipo IID')

# Display the legend and the plot
plt.legend(title='Rangos de temperatura')
plt.tight_layout()
figurepath = os.path.join(path, 'stacked_bar_chart.png')
plt.savefig(figurepath, dpi = 300)
#plt.show()
