
import io
import os
import pandas as pd  

def process_single_csv(csv_path):
    try:
        with open(csv_path, 'r', encoding='utf-8', errors='ignore') as f:
            all_lines = f.readlines()
            site_name = ""
            processed_csv = io.StringIO("")
            
            if len(all_lines) >= 4:  
                line4 = all_lines[3].strip('\n').strip()
                line4_columns = line4.split(',')
                if len(line4_columns) >= 3:  
                    site_name = line4_columns[2].replace(',', '').strip()
                print(f"Result of site name extraction: {site_name}")
            else:
                print(f"Warning: {os.path.basename(csv_path)} Skip site name extraction.")
            
            if len(all_lines) > 4:
                lines_after_4 = all_lines[4:]
                lines_after_4 = [line for line in lines_after_4 if line.strip()] 
                processed_csv = io.StringIO(''.join(lines_after_4))
                print(f"successfully read the main part. Valid row count:{len(lines_after_4)}")
            else:
                print(f"Warning:{os.path.basename(csv_path)} Missing valid data.")
        
        df = pd.read_csv(
            processed_csv,
            header=None,
            engine='python',
            on_bad_lines='skip',
            sep=None
        )
        print(f"\nShape of the parsed data: {df.shape}")
        if not df.empty:
            print("Preview of the first 3 rows: ")
            print(df.head().fillna("NaN"))
        
        df_cleaned = df.reset_index(drop=True)
        
        if len(df_cleaned) < 1:
            print(f"Warning: Missing valid data in {os.path.basename(csv_path)}")
            return None
        
        df_cleaned.columns = df_cleaned.iloc[0].tolist()
        df_cleaned = df_cleaned.iloc[1:].reset_index(drop=True)
        df_cleaned = df_cleaned.dropna(axis=1, how='all') 
        
        columns = df_cleaned.columns.tolist()
        new_columns = columns.copy()
        for i in range(2, len(columns), 3):
            if i + 2 < len(columns):  
                base_col = columns[i]
                if pd.notna(base_col) and str(base_col).strip() != '':
                    new_columns[i+1] = f"{columns[i+1]}_{base_col}"
                    new_columns[i+2] = f"{columns[i+2]}_{base_col}"
        df_cleaned.columns = new_columns
        
        df_cleaned['site_name'] = site_name
        df_cleaned = df_cleaned[['site_name'] + [col for col in df_cleaned.columns if col != 'site_name']]
        
        print(f"successfully processed:{os.path.basename(csv_path)}")
        return df_cleaned

    except Exception as e:
        print(f"Error: An error occurred when processing {os.path.basename(csv_path)} - {str(e)}")
        return None

def obsaq_data_clean(CSV_DIR,OUTPUT_FILE):
    
    if not os.path.exists(CSV_DIR):
        print(f"Error: The directory {CSV_DIR} does not exist.")
        return

    csv_files = [f for f in os.listdir(CSV_DIR) if f.endswith('.csv')]
    if not csv_files:
        print(f"Warning: The directory {CSV_DIR} has no valid file.")
        return

    print(f"found {len(csv_files)} .csv files，starting batch processing…\n")
    df_list = []

    for csv_file in csv_files:
        csv_path = os.path.join(CSV_DIR, csv_file)
        processed_df = process_single_csv(csv_path) 
        if processed_df is not None and not processed_df.empty:
            df_list.append(processed_df)

    if df_list:
        final_df = pd.concat(df_list, ignore_index=True)
        
        final_df.to_csv(OUTPUT_FILE, index=False, encoding='utf-8')
        print(f"\nProcessing completed! The merged data has been saved to: {OUTPUT_FILE}")
        print(f"Merged data: {len(final_df)} rows，{len(final_df.columns)} columns")
    else:
        print("\nWarning: No CSV files were successfully processed")

