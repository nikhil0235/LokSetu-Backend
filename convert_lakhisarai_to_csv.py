#!/usr/bin/env python3
import pandas as pd
from googletrans import Translator

def convert_to_csv():
    """Convert Lakhisarai.xlsx to CSV with proper column names and transformations"""
    
    # Read Excel file
    df = pd.read_excel('Suryagarha.xlsx', sheet_name='Sheet1')
    
    translator = Translator()
    
    def translate_name(hindi_name):
        """Translate Hindi name to English"""
        try:
            if pd.isna(hindi_name) or hindi_name.strip() == '':
                return ''
            result = translator.translate(hindi_name, src='hi', dest='en')
            return result.text.title()
        except:
            return hindi_name
    
    def split_name(name):
        """Split name by first space"""
        if pd.isna(name) or name.strip() == '':
            return '', ''
        parts = str(name).strip().split(' ', 1)
        fname = parts[0]
        lname = parts[1] if len(parts) > 1 else ''
        return fname, lname
    
    # Process voter names
    print("🔄 Processing voter names...")
    df['voter_fname_hin'], df['voter_lname_hin'] = zip(*df['Name'].apply(split_name))
    df['voter_fname'] = df['voter_fname_hin'].apply(translate_name)
    df['voter_lname'] = df['voter_lname_hin'].apply(translate_name)
    
    # Process guardian names
    print("🔄 Processing guardian names...")
    df['guardian_fname_hin'], df['guardian_lname_hin'] = zip(*df['Father Name'].apply(split_name))
    df['guardian_fname'] = df['guardian_fname_hin'].apply(translate_name)
    df['guardian_lname'] = df['guardian_lname_hin'].apply(translate_name)
    
    # Add 282 to booth_id
    df['booth_id'] = df['bhag_no'] + 750
    
    # Map gender
    gender_mapping = {
        'पुरुष': 'Male', 'M': 'Male', 'male': 'Male',
        'महिला': 'Female', 'F': 'Female', 'female': 'Female',
        'अन्य': 'Other', 'O': 'Other', 'other': 'Other'
    }
    df['gender'] = df['sex'].map(gender_mapping).fillna('Other')
    
    # Map relation
    relation_mapping = {
        'पिता': 'F', 'father': 'F', 'Father': 'F',
        'माता': 'M', 'mother': 'M', 'Mother': 'M', 
        'पति': 'H', 'husband': 'H', 'Husband': 'H',
        'अन्य': 'O', 'other': 'O', 'Other': 'O'
    }
    df['relation'] = df['Relation'].map(relation_mapping).fillna('O')
    
    # Final column selection and mapping
    final_df = pd.DataFrame({
        'serial_no_in_list': df['sr'],
        'voter_fname': df['voter_fname'],
        'voter_lname': df['voter_lname'],
        'voter_fname_hin': df['voter_fname_hin'],
        'voter_lname_hin': df['voter_lname_hin'],
        'relation': df['relation'],
        'guardian_fname': df['guardian_fname'],
        'guardian_lname': df['guardian_lname'],
        'guardian_fname_hin': df['guardian_fname_hin'],
        'guardian_lname_hin': df['guardian_lname_hin'],
        'epic_id': df['Number'],
        'gender': df['gender'],
        'house_no': df['makan'],
        'booth_id': df['booth_id'],
        'age': df['age'],
        'constituency_id': df['vidhansabha'],
    })
    
    # Save to CSV
    final_df.to_csv('suryagarha_voters.csv', index=False, encoding='utf-8')
    
    print(f"✅ Converted {len(final_df)} voter records to CSV")
    print(f"📊 Columns: {list(final_df.columns)}")
    print(f"💾 Saved as: lakhisarai_voters.csv")

if __name__ == "__main__":
    convert_to_csv()