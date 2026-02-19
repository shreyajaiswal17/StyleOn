
import React, { useState } from "react";
import axios from "axios";
import BannerBackground from "../Assets/home-banner-background.png";
import img3 from "../Assets/img3.png";
import Navbar from "./Navbar";
import { FiArrowRight } from "react-icons/fi";
import Card from "./Card"; // Correct import
import "./Home.css";

const Home = () => {
  const [usage, setUsage] = useState("");
  const [gender, setGender] = useState("");
  const [season, setSeason] = useState("");
  const [color, setColor] = useState("");
  const [subcategory, setSubcategory] = useState("");
  const [recommendations, setRecommendations] = useState({});

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post("http://localhost:5000/recommend", {
        usage,
        gender,
        season,
        color,
        subcategory,
      });
      setRecommendations(response.data);
    } catch (error) {
      console.error("Error fetching recommendations:", error);
    }
  };

  const renderCards = (items) => {
    if (!items || items.length === 0) {
      return <div>No recommendations found.</div>;
    }

    return (
      <div className="container">
        {items.map((item) => (
          <Card key={item.id} data={item} />
        ))}
      </div>
    );
  };

  return (
    <div className="home-container">
      <Navbar />
      <div className="home-banner-container">
        <div className="home-bannerImage-container">
          <img src={BannerBackground} alt="Banner Background" />
        </div>
        <div className="home-text-section">
          <h1 className="primary-heading">Your Personal Stylist!</h1>
          <p className="primary-text">
            Stay stylish and fashionable using StyleOn that gives you
            AI-generated style recommendations based on the latest trends.
          </p>
          <form onSubmit={handleSubmit} className="form-container">
            <select
              value={usage}
              onChange={(e) => setUsage(e.target.value)}
              className="dropdown"
            >
              <option value="">Select Usage</option>
              <option value="Casual">Casual</option>
              <option value="Formal">Formal</option>
              <option value="Party">Party</option>
              <option value="Ethnic">Ethnic</option>
              <option value="Sports">Sports</option>
              <option value="Smart Casual">Smart Casual</option>
            </select>
            <select
              value={gender}
              onChange={(e) => setGender(e.target.value)}
              className="dropdown"
            >
              <option value="">Select Gender</option>
              <option value="Men">Men</option>
              <option value="Women">Women</option>
              <option value="Unisex">Unisex</option>
            </select>
            <select
              value={season}
              onChange={(e) => setSeason(e.target.value)}
              className="dropdown"
            >
              <option value="">Select Season</option>
              <option value="Summer">Summer</option>
              <option value="Winter">Winter</option>
              <option value="Spring">Spring</option>
              <option value="Fall">Fall</option>
            </select>
            <select
              value={color}
              onChange={(e) => setColor(e.target.value)}
              className="dropdown"
            >
              <option value="">Select Color</option>
              <option value="Red">Red</option>
              <option value="Blue">Blue</option>
              <option value="Green">Green</option>
              <option value="Black">Black</option>
              <option value="White">White</option>
              <option value="Grey">Grey</option>
              <option value="Pink">Pink</option>
              <option value="Yellow">Yellow</option>
              <option value="Orange">Orange</option>
              <option value="Purple">Purple</option>
              <option value="Brown">Brown</option>
              <option value="Beige">Beige</option>
              <option value="Multi">Multi</option>
            </select>
            <select
              value={subcategory}
              onChange={(e) => setSubcategory(e.target.value)}
              className="dropdown"
            >
              <option value="">Select Subcategory</option>
              <option value="Top">Top</option>
              <option value="Bottom">Bottom</option>
              <option value="Footwear">Footwear</option>
            </select>
            <button type="submit" className="secondary-button">
              Get Recommendations <FiArrowRight />
            </button>
          </form>
        </div>
        <div className="home-image-section">
          <img src={img3} alt="Fashion" />
        </div>
      </div>
      <div>
        <div className="selectioncontainer">
          {recommendations.bottoms && (
            <>
              <h2>Recommended Bottoms:</h2>
                {renderCards(recommendations.bottoms)}
            </>
          )}
          {/* {recommendations.shoes && (
              // <>
              // <h2>Recommended Shoes:</h2>

              //   {renderCards(recommendations.shoes)}
              // </>

          )} */}
          {recommendations.tops && (
            <>
              <h2>Recommended Tops:</h2>
                {renderCards(recommendations.tops)}
              
            </>
          )}
        </div>
      </div>
    </div>
  );
};

export default Home;
