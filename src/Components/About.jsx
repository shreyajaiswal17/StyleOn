import React from "react";
import AboutBackground from "../Assets/about-background.png";
import img4 from "../Assets/img4.jpg";
import { BsFillPlayCircleFill } from "react-icons/bs";

const About = () => {
  return (
    <div className="about-section-container" id="about">
      <div className="about-background-image-container">
        <img src={AboutBackground} alt="" />
      </div>
      <div className="about-section-image-container">
        <img src={img4} alt="" />
      </div>
      <div className="about-section-text-container">
        <p className="primary-subheading">About</p>
        <h1 className="primary-heading">
        "Fashion is what you buy, style is what you do with it."
        </h1>
        <p className="primary-text">
        Welcome to Style On—where your personal style meets smart technology! Our app is designed to help you navigate the world of fashion with ease and confidence. Whether you’re looking for the perfect outfit for a special occasion or just need some inspiration, Style On has got you covered.
        </p>
       
        <div className="about-buttons-container">
          <button className="secondary-button">Learn More</button>
          <button className="watch-video-button" type="button" onClick={() => document.getElementById("features")?.scrollIntoView({ behavior: "smooth" })}>
            <BsFillPlayCircleFill /> Watch Video
          </button>
        </div>
      </div>
    </div>
  );
};

export default About;
