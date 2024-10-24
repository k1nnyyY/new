import React, { useState } from 'react';
import ReCAPTCHA from 'react-google-recaptcha';

function RegistrationForm() {
  const [formData, setFormData] = useState({
    mos: '',
    inpol: '',
    first_name: '',
    last_name: '',
    passport_code: '',
    country: '',
    email: '',
    radio_choice: '',
    date_of_birth: '',
    guardian_name: '',
    captcha_verified: false,
  });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleCaptcha = (value) => {
    setFormData({ ...formData, captcha_verified: value !== null });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!formData.captcha_verified) {
      alert("Please complete the captcha!");
      return;
    }
    console.log(formData);
    alert('Form submitted successfully!');
  };

  return (
    <div className="App">
      <h1>Registration Form</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="number"
          name="mos"
          value={formData.mos}
          onChange={handleChange}
          placeholder="MOS"
          required
        />
        <input
          type="number"
          name="inpol"
          value={formData.inpol}
          onChange={handleChange}
          placeholder="INPOL"
          required
        />
        <input
          type="text"
          name="first_name"
          value={formData.first_name}
          onChange={handleChange}
          placeholder="First Name"
          required
        />
        <input
          type="text"
          name="last_name"
          value={formData.last_name}
          onChange={handleChange}
          placeholder="Last Name"
          required
        />
        <input
          type="text"
          name="passport_code"
          value={formData.passport_code}
          onChange={handleChange}
          placeholder="Passport Code"
          required
        />
        <input
          type="text"
          name="country"
          value={formData.country}
          onChange={handleChange}
          placeholder="Country"
          required
        />
        <input
          type="email"
          name="email"
          value={formData.email}
          onChange={handleChange}
          placeholder="Email"
          required
        />
        
        <label>
          <input
            type="radio"
            name="radio_choice"
            value="1"
            onChange={handleChange}
            required
          />
          Option 1
        </label>
        <label>
          <input
            type="radio"
            name="radio_choice"
            value="2"
            onChange={handleChange}
          />
          Option 2
        </label>

        <input
          type="date"
          name="date_of_birth"
          value={formData.date_of_birth}
          onChange={handleChange}
          required
        />
        <input
          type="text"
          name="guardian_name"
          value={formData.guardian_name}
          onChange={handleChange}
          placeholder="Guardian Name"
          required
        />

        <ReCAPTCHA
          sitekey="6Lez0moqAAAAAIZZ7Di6OLeXF0g86ydDWPO27Ndu"  // Укажи свой сайт ключ reCAPTCHA
          onChange={handleCaptcha}
        />

        <button type="submit">Submit</button>
      </form>
    </div>
  );
}

export default RegistrationForm;
