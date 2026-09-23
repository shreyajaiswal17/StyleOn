import React, { useState } from "react";

const Contact = () => {
  const [email, setEmail] = useState("");
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = (event) => {
    event.preventDefault();
    setSubmitted(true);
  };

  return (
    <div className="contact-page-wrapper" id="contact">
      <h1 className="primary-heading">Have Question In Mind?</h1>
      <h1 className="primary-heading">Let Us Help You</h1>
      <form className="contact-form-container" onSubmit={handleSubmit}>
        <input type="email" value={email} onChange={(event) => setEmail(event.target.value)} placeholder="yourmail@gmail.com" aria-label="Email address" required />
        <button className="secondary-button" type="submit">Submit</button>
      </form>
      {submitted && <p role="status">Thanks. We will be in touch at {email}.</p>}
    </div>
  );
};

export default Contact;