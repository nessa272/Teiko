import pandas as pd
import matplotlib.pyplot as plt
import os

df = pd.read_csv("cell-count.csv")
immune_cells = ['b_cell','cd8_t_cell','cd4_t_cell','nk_cell','monocyte']
os.makedirs('output', exist_ok=True)

def get_relative_frequencies():
    # total cell count for each sample
    df['total_count'] = df[immune_cells].sum(axis=1) 
    # calculate relative frequency of each immune cell
    df[[cell + '_freq' for cell in immune_cells]] = df[immune_cells].div(df['total_count'], axis=0) 
    # write CSV file with sample ID, immune cell counts, total cell count, and immune cell rel freqs for each sample
    output_cols = ['sample'] + immune_cells + ['total_count'] + [cell + '_freq' for cell in immune_cells]
    df[output_cols].to_csv('output/cell-frequencies.csv', index=False)
    print('Saved immune cell frequency output to "output/cell-frequencies.csv"')

def melanoma_tr1_responders():
    os.makedirs('output/boxplots', exist_ok=True)
    # filter PBMC samples of melanoma patients who received tr1
    melanoma_df_y = df[(df['condition']=='melanoma') & (df['sample_type']=='PBMC') & (df['treatment']=='tr1') & (df['response']=='y')]
    melanoma_df_n = df[(df['condition']=='melanoma') & (df['sample_type']=='PBMC') & (df['treatment']=='tr1') & (df['response']=='n')]
    for cell in immune_cells:
        plt.boxplot([melanoma_df_y[cell + '_freq'],melanoma_df_n[cell + '_freq']], tick_labels=['Yes', 'No'])
        plt.title(cell + ' relative frequencies for responders vs. non-responders')
        plt.xlabel('Response')
        plt.ylabel('Relative Frequency')
        plt.savefig('output/boxplots/' + cell + '_plot.jpg', dpi=300, bbox_inches='tight')
        plt.close()
        print('Saved relative frequency of ' + cell + ' of responders vs. non-responders to "output/boxplots/' + cell + '_plot.jpg"')

get_relative_frequencies()
melanoma_tr1_responders()
