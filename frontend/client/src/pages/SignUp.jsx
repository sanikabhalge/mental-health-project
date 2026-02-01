import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";

function SignUp() {
  const navigate = useNavigate();
  const [form, setForm] = useState({
    username: "",
    password: "",
    age: "",
    gender: "",
    emergencyContact: "",
    phoneNumber: "",
    address: "",
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const { username, password, age, phoneNumber, address, emergencyContact } = form;
    if (!username || !password) {
      alert("Please enter username and password");
      return;
    }
    if (!age || !phoneNumber || !address || !emergencyContact) {
      alert("Please fill all required fields");
      return;
    }
    navigate("/chat");
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-purple-200 via-pink-100 to-blue-100 py-8 px-4">
      <div className="bg-white rounded-3xl shadow-2xl p-8 w-full max-w-md">
        <h1 className="text-4xl font-extrabold text-purple-700 mb-2 text-center">MindCare Bot</h1>
        <p className="text-gray-600 text-center mb-6">Create your account</p>

        <form onSubmit={handleSubmit} className="flex flex-col gap-4">
          <input
            type="text"
            name="username"
            placeholder="Username *"
            className="p-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-400 transition"
            value={form.username}
            onChange={handleChange}
            required
          />
          <input
            type="password"
            name="password"
            placeholder="Password *"
            className="p-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-400 transition"
            value={form.password}
            onChange={handleChange}
            required
          />
          <div className="grid grid-cols-2 gap-4">
            <input
              type="number"
              name="age"
              placeholder="Age *"
              min="1"
              max="120"
              className="p-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-400 transition"
              value={form.age}
              onChange={handleChange}
              required
            />
            <select
              name="gender"
              className="p-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-400 transition bg-white"
              value={form.gender}
              onChange={handleChange}
            >
              <option value="">Gender</option>
              <option value="male">Male</option>
              <option value="female">Female</option>
              <option value="other">Other</option>
              <option value="prefer-not-to-say">Prefer not to say</option>
            </select>
          </div>
          <input
            type="tel"
            name="phoneNumber"
            placeholder="Phone number *"
            className="p-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-400 transition"
            value={form.phoneNumber}
            onChange={handleChange}
            required
          />
          <input
            type="text"
            name="emergencyContact"
            placeholder="Emergency contact name & number *"
            className="p-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-400 transition"
            value={form.emergencyContact}
            onChange={handleChange}
            required
          />
          <textarea
            name="address"
            placeholder="Address *"
            rows="2"
            className="p-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-400 transition resize-none"
            value={form.address}
            onChange={handleChange}
            required
          />
          <button
            type="submit"
            className="bg-purple-600 text-white py-3 rounded-xl font-semibold hover:bg-purple-700 shadow-md hover:shadow-lg transition-all mt-2"
          >
            Sign Up
          </button>
        </form>

        <p className="mt-6 text-center text-gray-600">
          Already have an account?{" "}
          <Link to="/" className="text-purple-600 font-semibold hover:underline">
            Log In
          </Link>
        </p>
      </div>
    </div>
  );
}

export default SignUp;
