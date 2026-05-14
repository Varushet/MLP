import numpy as np 
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from IPython.display import Markdown, display

def eda(df, target=None):
    """
        Realiza un EDA automático visual.
    """
    
    # 1. MUESTRA
    print('='*100)
    display(Markdown("### 📋 Muestra"))
    display(df.head()) # Head es suficiente y más rápido
    
    # 2. INFO
    print('='*100)
    display(Markdown(f"### 📊 Info → `{df.shape[0]:,}` filas × `{df.shape[1]}` columnas"))
    # df.info() puede ser muy lento en consola, mejor mostrar dtypes resumidos si es gigante
    # Pero lo dejo como pediste:
    print(df.info())
    display(Markdown('#### Uniques'))
    print(df.nunique())
    
    # 3. NULOS
    print('='*100)
    display(Markdown("### ⚠️ Null & NaN"))
    print(df.isna().sum())
    # Mostrar solo las filas con nulos si no son demasiadas, para no colgar el notebook
    null_rows = df[df.isnull().any(axis=1)]
    if len(null_rows) > 0:
        display(null_rows.head())
    
    # 4. BOXPLOTS (Solo numéricas)
    print('='*100)
    display(Markdown("### 📦 Describe"))
    display(df.describe().round(3))
    
    cols = df.describe().columns
    n = len(cols)

    if n > 0:
        # Crear rejilla
        fig, axes = plt.subplots(nrows=(n//3)+1, ncols=3, figsize=(15, 5*((n//3)+1)))
        axes = axes.flatten()

        for i, col in enumerate(cols):
            sns.boxplot(y=df[col], ax=axes[i], showmeans=True)
            axes[i].set_title(col)

        # Limpiar gráficos vacíos sobrantes
        for j in range(i+1, len(axes)):
            axes[j].set_visible(False)
            
        plt.tight_layout()
        plt.show()
    
    # 5. PAIRPLOT
    print('='*100)
    display(Markdown(f"### 📈 Comparación"))
    
    df_for_plot = df.sample(min(2000, len(df))) if len(df) > 2000 else df

    if target is not None:
        t_name = target.name if hasattr(target, 'name') else target
        display(Markdown(f"### (target: {t_name})"))
        
        if t_name not in df_for_plot.columns:
            # CAMBIO CLAVE: .copy() para evitar SettingWithCopyWarning y alineación lenta
            df_plot = df_for_plot[cols].copy()
            df_plot[t_name] = target.loc[df_plot.index] if hasattr(target, 'loc') else target
        else:
            df_plot = df_for_plot[cols]

        # Si el target no está en cols, lo añadimos al plot manualmente si es necesario
        if t_name not in df_plot.columns:
             df_plot[t_name] = df_for_plot[t_name]

        sns.pairplot(df_plot, hue=t_name)
        plt.show()
        
    else:
        sns.pairplot(df_for_plot)
        plt.show()
        
    # HEATMAP
    if n > 1:
        plt.figure(figsize=(10, 10)) 
        # CAMBIO CLAVE: fmt='.2f' es correcto para correlaciones (-1 a 1). '.1%' da error.
        sns.heatmap(df[cols].corr(), annot=True, fmt='.2f', vmin=-1, vmax=1, cmap="coolwarm")
        plt.show()

