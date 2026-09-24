
# StyleOn 

StyleOn is a **rule-based outfit-completion application** that recommends compatible tops, bottoms, and footwear based on the user's selected clothing category, color, gender, season, and occasion.

🌐 **Live Demo:** https://styleeon.vercel.app/

## Features

* Outfit recommendations based on an existing clothing item
* Color compatibility-based matching
* Filters by gender, season, and occasion
* Supports Tops, Bottoms, and Footwear
* Responsive React interface
* Flask REST API for recommendation logic

## How It Works

```text
Top      → Bottoms + Footwear
Bottom   → Tops + Footwear
Footwear → Tops + Bottoms
```

StyleOn groups similar colors, applies predefined color compatibility rules, and filters the fashion dataset according to the user's preferences to recommend suitable outfit combinations.

## Tech Stack

**Frontend:** React.js, JavaScript, CSS, Axios, Material UI
**Backend:** Python, Flask, Pandas
**Deployment:** Vercel + Render

## Run Locally

```bash
npm install
npm start
```

In another terminal:

```bash
python -m pip install -r requirements.txt
python app.py
```

## Future Improvements

* Upload clothing images
* Automatic clothing and color detection
* ML-based outfit compatibility
* Digital wardrobe and saved outfits

## Author

**Shreya Jaiswal**
