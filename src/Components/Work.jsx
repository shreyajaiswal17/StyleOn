import React from "react";


const Work = () => {
  const workInfoData = [
    {
      
      title: "Personalized Input",
      text: "Start by providing details about your needs, including gender, season, color preferences, and the type of clothing you're interested in (top, bottom, or footwear).",
    },
    {
     
      title: "Occasion-Based Suggestions",
      text: "Our intelligent model analyzes your input and offers tailored outfit recommendations that suit your specific occasion.",
    },
    {
      
      title: "Fashionable Outcomes",
      text: "With just a few clicks, you’ll receive stylish suggestions that not only fit the season and color but also match the occasion perfectly",
    },
  ];
  return (
    <div className="work-section-wrapper">
      <div className="work-section-top">
        <p className="primary-subheading">Embrace effortless styling and make every occasion a fashion statement with Style On!</p>
        <h1 className="primary-heading">How It Works</h1>
        
      </div>
      <div className="work-section-bottom">
        {workInfoData.map((data) => (
          <div className="work-section-info" key={data.title}>
            
            <h2>{data.title}</h2>
            <p>{data.text}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Work;
