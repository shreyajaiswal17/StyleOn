import React from "react";

import { AiFillStar } from "react-icons/ai";

const Testimonial = () => {
  return (
    <div className="work-section-wrapper">
      <div className="work-section-top">
        <p className="primary-subheading">Testimonial</p>
        <h1 className="primary-heading">What They Are Saying</h1>
      </div>
      <div className="testimonial-section-bottom">
        
        <p>
        I’ve always struggled with putting together outfits that match the season and occasion. Style On has been a game changer for me! The app’s intuitive system takes all the guesswork out of styling, and I’ve received so many compliments on my outfits since I started using it. It’s a must-have tool for anyone who wants to elevate their fashion game effortlessly!
        </p>
        <div className="testimonials-stars-container">
          <AiFillStar />
          <AiFillStar />
          <AiFillStar />
          <AiFillStar />
          <AiFillStar />
        </div>
        <h2>Alice Doe</h2>
      </div>
    </div>
  );
};

export default Testimonial;