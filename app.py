
from flask import Flask, request, jsonify
import pandas as pd
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load your dataset
df = pd.read_csv("styles.csv", on_bad_lines="skip")
dfi = pd.read_csv('images.csv', on_bad_lines='skip')
dfi['id'] = dfi['filename'].str.replace('.jpg', '').astype(int)
dfi.drop('filename', axis=1, inplace=True)
df = pd.merge(df, dfi, on='id', how='inner')

# Your existing function definitions for color grouping and data preparation
def group_color(styles):
    # Create a color mapping dictionary for efficiency
    color_mapping = {
        # Reds and Browns
        'Red': 0, 'Brown': 0, 'Coffee Brown': 0, 'Maroon': 0, 
        'Rust': 0, 'Burgundy': 0, 'Mushroom Brown': 0,
        # Copper
        'Copper': 1,
        # Oranges
        'Orange': 2, 'Bronze': 2, 'Skin': 2, 'Nude': 2,
        # Golds and Beiges
        'Gold': 3, 'Khaki': 3, 'Beige': 3, 'Mustard': 3, 'Tan': 3, 'Metallic': 3,
        # Yellow
        'Yellow': 4,
        # Lime Green
        'Lime Green': 5,
        # Greens
        'Green': 6, 'Sea Green': 6, 'Fluorescent Green': 6, 'Olive': 6,
        # Teals
        'Teal': 7, 'Turquoise Blue': 7,
        # Blue
        'Blue': 8,
        # Navy
        'Navy Blue': 9,
        # Purples
        'Purple': 10, 'Lavender': 10,
        # Pinks
        'Pink': 11, 'Magenta': 11, 'Peach': 11, 'Rose': 11, 'Mauve': 11,
        # Blacks
        'Black': 12, 'Charcoal': 12,
        # Whites
        'White': 13, 'Off White': 13, 'Cream': 13,
        # Greys
        'Grey': 14, 'Silver': 14, 'Taupe': 14, 'Grey Melange': 14,
        # Multi
        'Multi': 15
    }
    
    styles['colorgroup'] = styles['baseColour'].map(color_mapping).fillna(-1)
    styles.loc[(styles.baseColour=='Black')|
           (styles.baseColour=='Charcoal'),"colorgroup"] = 12
    styles.loc[(styles.baseColour=='White')|
           (styles.baseColour=='Off White')|
           (styles.baseColour=='Cream'),"colorgroup"] = 13
    styles.loc[(styles.baseColour=='Grey')|
           (styles.baseColour=='Silver')|
           (styles.baseColour=='Taupe')|
           (styles.baseColour=='Grey Melange'),"colorgroup"] = 14
    styles.loc[(styles.baseColour=='Multi'),"colorgroup"] = 15

def df_drop(styles, col, item):
    for i in item:
        styles = styles.drop(styles[styles[col] == i].index)
    return styles

group_color(df)

color_group = {
    'Red': 0, 'Orange': 2, 'Yellow': 4, 'Green': 6, 
    'Blue': 8, 'Purple': 10, 'Pink': 11, 
    'Black': 12, 'White': 13, 'Grey': 14, 'Beige': 3, 'Brown': 0,
    'Multi': 15
}

# Smart color complementarity rules based on fashion principles
COLOR_COMPLEMENTS = {
    0: [12, 13, 14, 3],      # Red/Brown -> Black, White, Grey, Beige
    2: [12, 13, 14, 0],      # Orange -> Black, White, Grey, Brown
    3: [12, 13, 14, 8],      # Beige -> Black, White, Grey, Blue
    4: [12, 13, 14],         # Yellow -> Black, White, Grey
    6: [12, 13, 14, 0, 3],   # Green -> Black, White, Grey, Brown, Beige
    8: [13, 14, 0, 3],       # Blue -> White, Grey, Brown, Beige
    10: [12, 13, 14],        # Purple -> Black, White, Grey
    11: [12, 13, 14],        # Pink -> Black, White, Grey
    12: [13, 14, 8, 0],      # Black -> White, Grey, Blue, Red
    13: [12, 14, 8, 0, 6],   # White -> Black, Grey, Blue, Red, Green
    14: [12, 13, 8, 0],      # Grey -> Black, White, Blue, Red
    15: [12, 13, 14]         # Multi -> Black, White, Grey
}

def get_complementary_colors(color_group):
    """Get complementary colors for matching"""
    if color_group in COLOR_COMPLEMENTS:
        return COLOR_COMPLEMENTS[color_group]
    return [12, 13, 14]  # Default to neutrals

def smart_filter(df_subset, gender, season, usage, limit=8):
    """
    Smart filtering that provides good results even with strict criteria
    Priority: Gender > Color > Usage >= Season
    """
    if len(df_subset) == 0:
        return df_subset
    
    # Filter by gender (mandatory)
    filtered = df_subset[df_subset['gender'] == gender].copy()
    
    if len(filtered) == 0:
        return filtered
    
    # Score each item based on matching criteria
    filtered['match_score'] = 0
    
    # Season match (but not mandatory)
    if season and season != 'None' and season in filtered['season'].values:
        filtered.loc[filtered['season'] == season, 'match_score'] += 3
    
    # Usage match (important but not mandatory)
    if usage and usage != 'None' and usage in filtered['usage'].values:
        filtered.loc[filtered['usage'] == usage, 'match_score'] += 2
    
    # Prefer recent years
    if 'year' in filtered.columns:
        filtered['match_score'] += (filtered['year'] - 2010) * 0.1
    
    # Sort by match score and return top items
    filtered = filtered.sort_values('match_score', ascending=False)
    filtered = filtered.drop('match_score', axis=1)
    
    return filtered.head(limit)

def find_combo_by_item(item_color_group, subcategory, gender, season, usage):
    """
    Smart recommendation based on item type and color
    Returns matching items for outfit completion
    """
    
    if subcategory == 'top':
        # For tops, find bottoms and shoes
        # Bottoms should be complementary or neutral
        complementary = get_complementary_colors(item_color_group)
        
        bottoms = df[
            (df['subCategory'] == 'Bottomwear') & 
            (df['colorgroup'].isin(complementary))
        ]
        bottoms = smart_filter(bottoms, gender, season, usage, limit=4)
        
        # Shoes - prefer neutrals
        shoes = df[
            (df['subCategory'].isin(['Shoes', 'Sandal', 'Flip Flops'])) & 
            (df['colorgroup'].isin([12, 13, 14]))  # Black, White, Grey
        ]
        shoes = smart_filter(shoes, gender, season, None, limit=4)  # Don't filter shoes by usage
        
        return bottoms, shoes
    
    elif subcategory == 'bottom':
        # For bottoms, find matching/complementary tops
        complementary = get_complementary_colors(item_color_group)
        # Add the same color for monochrome looks
        if item_color_group not in [12, 13, 14]:
            complementary.append(item_color_group)
        
        tops = df[
            (df['subCategory'] == 'Topwear') & 
            (df['colorgroup'].isin(complementary))
        ]
        tops = smart_filter(tops, gender, season, usage, limit=4)
        
        # Shoes - match with bottom or neutral
        shoes = df[
            (df['subCategory'].isin(['Shoes', 'Sandal', 'Flip Flops'])) & 
            (df['colorgroup'].isin([item_color_group, 12, 13, 14]))
        ]
        shoes = smart_filter(shoes, gender, season, None, limit=4)
        
        return tops, shoes
    
    elif subcategory == 'footwear':
        # For footwear, suggest complete outfit
        complementary = get_complementary_colors(item_color_group)
        
        tops = df[
            (df['subCategory'] == 'Topwear') & 
            (df['colorgroup'].isin(complementary))
        ]
        tops = smart_filter(tops, gender, season, usage, limit=4)
        
        bottoms = df[
            (df['subCategory'] == 'Bottomwear') & 
            (df['colorgroup'].isin(complementary))
        ]
        bottoms = smart_filter(bottoms, gender, season, usage, limit=4)
        
        return tops, bottoms
    
    return pd.DataFrame(), pd.DataFrame()

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.json
    color = data.get('color', 'Multi')
    subcategory = data.get('subcategory', 'Top').lower()
    gender = data.get('gender', 'Women')
    season = data.get('season', None)
    usage = data.get('usage', 'Casual')
    
    item_color_group = color_group.get(color, 15)
    recommendations = {}
    
    print(f"\n{'='*60}")
    print(f"NEW REQUEST:")
    print(f"  Type: {subcategory} | Color: {color} (group {item_color_group})")
    print(f"  Gender: {gender} | Season: {season} | Usage: {usage}")
    print(f"{'='*60}")
    
    # Get smart recommendations using new algorithm
    first_items, second_items = find_combo_by_item(
        item_color_group, subcategory, gender, season, usage
    )
    
    # Map results based on subcategory
    if subcategory == 'top':
        recommendations['bottoms'] = first_items.to_dict('records')
        recommendations['shoes'] = second_items.to_dict('records')
        print(f"✓ Found {len(first_items)} bottoms, {len(second_items)} shoes")
        
    elif subcategory == 'bottom':
        recommendations['tops'] = first_items.to_dict('records')
        recommendations['shoes'] = second_items.to_dict('records')
        print(f"✓ Found {len(first_items)} tops, {len(second_items)} shoes")
        
    elif subcategory == 'footwear':
        recommendations['tops'] = first_items.to_dict('records')
        recommendations['bottoms'] = second_items.to_dict('records')
        print(f"✓ Found {len(first_items)} tops, {len(second_items)} bottoms")
    
    # Log complementary colors used
    complements = get_complementary_colors(item_color_group)
    print(f"  Complementary color groups used: {complements}")
    print(f"{'='*60}\n")
    
    return jsonify(recommendations)

if __name__ == '__main__':
    app.run(debug=True)
