from flask import Flask, request, jsonify
import pandas as pd
import random
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load your dataset
df = pd.read_csv("styles.csv", on_bad_lines="skip")
dfi = pd.read_csv('images.csv', on_bad_lines='skip')
dfi['id'] = dfi['filename'].str.replace('.jpg', '').astype(int)
dfi.drop('filename', axis=1, inplace=True)
df = pd.merge(df, dfi, on='id', how='inner')

# Ensure that columns are in lowercase
df.columns = df.columns.str.lower()

# Print unique values to understand the dataset
print("Unique genders:", df['gender'].unique())

# Your existing function definitions for color grouping and data preparation
def group_color(styles):
    styles["colorgroup"] = -1
    styles.loc[(styles.basecolour=='Red')|
           (styles.basecolour=='Brown')|
           (styles.basecolour=='Coffee Brown')|
           (styles.basecolour=='Maroon')|
           (styles.basecolour=='Rust')|
           (styles.basecolour=='Burgundy')|
           (styles.basecolour=='Mushroom Brown'),"colorgroup"] = 0
    styles.loc[(styles.basecolour=='Copper'),"colorgroup"] = 1
    styles.loc[(styles.basecolour=='Orange')|
               (styles.basecolour=='Bronze')|
               (styles.basecolour=='Skin')|
               (styles.basecolour=='Nude'),"colorgroup"] = 2
    styles.loc[(styles.basecolour=='Gold')|
               (styles.basecolour=='Khaki')|
               (styles.basecolour=='Beige')|
               (styles.basecolour=='Mustard')|
               (styles.basecolour=='Tan')|
               (styles.basecolour=='Metallic'),"colorgroup"]= 3
    styles.loc[(styles.basecolour=='Yellow'),"colorgroup"] = 4
    styles.loc[(styles.basecolour=='Lime Green'),"colorgroup"]= 5
    styles.loc[(styles.basecolour=='Green')|
           (styles.basecolour=='Sea Green')|
           (styles.basecolour=='Fluorescent Green')|
           (styles.basecolour=='Olive'),"colorgroup"] = 6
    styles.loc[(styles.basecolour=='Teal')|
           (styles.basecolour=='Turquoise Blue'),"colorgroup"] = 7
    styles.loc[(styles.basecolour=='Blue'),"colorgroup"]= 8
    styles.loc[(styles.basecolour=='Navy Blue'),"colorgroup"] = 9
    styles.loc[(styles.basecolour=='Purple')|
           (styles.basecolour=='Lavender'),"colorgroup"] = 10
    styles.loc[(styles.basecolour=='Pink')|
           (styles.basecolour=='Magenta')|
           (styles.basecolour=='Peach')|
           (styles.basecolour=='Rose')|
           (styles.basecolour=='Mauve'),"colorgroup"] = 11
    styles.loc[(styles.basecolour=='Black')|
           (styles.basecolour=='Charcoal'),"colorgroup"] = 12
    styles.loc[(styles.basecolour=='White')|
           (styles.basecolour=='Off White')|
           (styles.basecolour=='Cream'),"colorgroup"] = 13
    styles.loc[(styles.basecolour=='Grey')|
           (styles.basecolour=='Silver')|
           (styles.basecolour=='Taupe')|
           (styles.basecolour=='Grey Melange'),"colorgroup"] = 14
    styles.loc[(styles.basecolour=='Multi'),"colorgroup"] = 15

group_color(df)

color_group = {
    'Black': 0, 'Blue': 1, 'Red': 2, 'Green': 3, 'Yellow': 4,
    'White': 5, 'Orange': 6, 'Purple': 7, 'Brown': 8, 'Pink': 9,
    'Grey': 10, 'Beige': 11, 'Multi': 12
}

def find_combo_by_top(item_color_group, combotype, gender):
    co = int(combotype / 30)
    if item_color_group == 15:
        bottom_color_group = random.choice([12, 13, 14])
        if bottom_color_group == 12:
            shoes_color_group = 13
        elif bottom_color_group == 13:
            shoes_color_group = random.choice([12, 13, 14])
        else:
            shoes_color_group = random.choice([12, 13])
    elif item_color_group in [12, 13, 14]:
        if item_color_group == 12:
            bottom_color_group = random.choice([12, 13])
            shoes_color_group = 13 if bottom_color_group == 12 else random.choice([12, 13])
        elif item_color_group == 13:
            bottom_color_group = random.choice([12, 13])
            shoes_color_group = 13 if bottom_color_group == 12 else 12
        else:
            bottom_color_group = random.choice([12, 13])
            shoes_color_group = random.choice([12, 13])
    else:
        bottom_color_group = random.choice([item_color_group - co, item_color_group + co])
        shoes_color_group = item_color_group + co if bottom_color_group == item_color_group - co else item_color_group - co
        if bottom_color_group == 12: bottom_color_group = 0
        if bottom_color_group == 13: bottom_color_group = 1
        if bottom_color_group == 14: bottom_color_group = 2
        if bottom_color_group == 15: bottom_color_group = 3
        if bottom_color_group == 16: bottom_color_group = 4
        if bottom_color_group == 17: bottom_color_group = 5
        if shoes_color_group == 12: shoes_color_group = 0
        if shoes_color_group == 13: shoes_color_group = 1
        if shoes_color_group == 14: shoes_color_group = 2
        if shoes_color_group == 15: shoes_color_group = 3
        if shoes_color_group == 16: shoes_color_group = 4
        if shoes_color_group == 17: shoes_color_group = 5
        if bottom_color_group < 0: bottom_color_group = 11 + bottom_color_group
        if shoes_color_group < 0: shoes_color_group = 11 + shoes_color_group

    print(f"Filters: gender={gender}")
    
    matching_bottoms = df[(df['subcategory'] == 'bottomwear') & (df['colorgroup'] == bottom_color_group) & (df['gender'] == gender)]
    matching_shoes = df[(df['subcategory'] == 'footwear') & (df['colorgroup'] == shoes_color_group) & (df['gender'] == gender)]
    
    print(f"Matching bottoms: {len(matching_bottoms)}")
    print(f"Matching shoes: {len(matching_shoes)}")
    
    return matching_bottoms, matching_shoes

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.json
    print("Received data:", data)
    color = data.get('color', 'Multi')
    subcategory = data.get('subcategory', 'top').lower()
    gender = data.get('gender', 'unisex').lower()
    print("color:", color, "subcategory:", subcategory, "gender:", gender)
    item_color_group = color_group.get(color, 15)
    combotype = 90
    recommendations = {}
    if subcategory == 'top':
        bottoms, shoes = find_combo_by_top(item_color_group, combotype, gender)
        recommendations['bottoms'] = bottoms.to_dict('records')
        recommendations['shoes'] = shoes.to_dict('records')
    elif subcategory == 'bottom':
        tops = df[(df['subcategory'] == 'topwear') & (df['colorgroup'] == item_color_group) & (df['gender'] == gender)]
        shoes = df[(df['subcategory'] == 'footwear') & (df['colorgroup'] == item_color_group) & (df['gender'] == gender)]
        recommendations['tops'] = tops.to_dict('records')
        recommendations['shoes'] = shoes.to_dict('records')
    elif subcategory == 'footwear':
        tops = df[(df['subcategory'] == 'topwear') & (df['colorgroup'] == item_color_group) & (df['gender'] == gender)]
        bottoms = df[(df['subcategory'] == 'bottomwear') & (df['colorgroup'] == item_color_group) & (df['gender'] == gender)]
        recommendations['tops'] = tops.to_dict('records')
        recommendations['bottoms'] = bottoms.to_dict('records')
    print("Recommendations:", recommendations)
    return jsonify(recommendations)

if __name__ == '__main__':
    app.run(debug=True)
