// Card.jsx
import React from 'react';
import './Card.css'; // Assuming you have some CSS for the card

const Card=((data)=> {
    {console.log(data.data.articleType)}
  return (
    <div className="card">
      <div>
        <img src={data.data.link} alt="a" />
      </div>
      <div className="card-info">
        <div className="com">{data.data.company}</div>
        <div className="des">{data.data.baseColour + ' ' + data.data.articleType}</div>
      </div>
    </div>
  );

}
)
export default Card;
