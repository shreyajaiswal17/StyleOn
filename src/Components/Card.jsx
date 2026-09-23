// Card.jsx
import React from 'react';
import './Card.css'; // Assuming you have some CSS for the card

const Card = ({ data }) => {
  return (
    <div className="card">
      <div>
        <img src={data.link} alt={`${data.company} ${data.articleType}`} />
      </div>
      <div className="card-info">
        <div className="com">{data.company}</div>
        <div className="des">{data.baseColour + ' ' + data.articleType}</div>
      </div>
    </div>
  );
};
export default Card;
