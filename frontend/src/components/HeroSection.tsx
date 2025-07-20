import { Divide } from "lucide-react";
import React, { useEffect, useState } from "react";
import BG from "../images/landscape.png";
import api from "../api";

var currentDate = new Date();
currentDate.setDate(currentDate.getDate() - 1);

const HeroSection = () => {
  const [form, setForm] = useState<any>({
    tripName: "",
    budget: "",
    startDate: currentDate.toISOString().split("T")[0],
    endDate: currentDate.toISOString().split("T")[0],
    locations: "",
    activities: "",
  });

  const handleFormChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    setForm((prev: any) => ({ ...prev, [e.target.name]: e.target.value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    // await api.post("/api/trips", {});
  };

  return (
    <>
      <section className="relative flex flex-col items-center justify-center text-center">
        {/* Background image */}
        <div
          className="fixed absolute inset-0 bg-no-repeat bg-cover bg-center opacity-50 z-[-5]"
          style={{ backgroundImage: `url(${BG})` }}
        ></div>
        <div className="relative z-0 bg-black flex flex-col opacity-70 items-center justify-center text-center py-24 px-4">
          <h1 className="text-4xl md:text-6xl font-extrabold mb-4 tracking-tight text-white drop-shadow-lg">
            Travel Smarter. Connect Deeper.
          </h1>
          <p className="text-lg md:text-2xl mb-8 text-gray-300 max-w-2xl">
            Personalized itineraries, new friends, and unforgettable
            adventures—tailored just for you.
          </p>
          <div className="flex gap-4">
            <div className="w-screen flex items-center justify-center">
              <div className="bg-gray-900 rounded-2xl shadow-2xl p-8 w-full max-w-lg relative border border-blue-800">
                <h3 className="text-xl font-bold text-blue-400 mb-4">
                  Create a New Trip
                </h3>
                <form
                  onSubmit={handleSubmit}
                  className="grid grid-cols-1 gap-4"
                >
                  <div>
                    <label className="block text-blue-300 font-semibold mb-1">
                      Trip Name
                    </label>
                    <input
                      className="w-full bg-gray-800 border border-gray-700 rounded px-3 py-2 text-white"
                      name="tripName"
                      placeholder="e.g. Summer in Spain"
                      onChange={(e) => handleFormChange(e)}
                      required
                    />
                  </div>
                  <div className="flex justify-between">
                    <div>
                      <label className=" block text-blue-300 font-semibold mb-1">
                        Budget (USD)
                      </label>
                      <input
                        className=" bg-gray-800 border border-gray-700 rounded px-3 py-2 text-white"
                        name="budget"
                        type="number"
                        placeholder="e.g. 1500"
                        onChange={(e) => handleFormChange(e)}
                        required
                      />
                    </div>
                    <div>
                      <label className="block text-blue-300 font-semibold mb-1">
                        Location(s)
                      </label>
                      <input
                        className="w-full bg-gray-800 border border-gray-700 rounded px-3 py-2 text-white"
                        name="locations"
                        placeholder="e.g. Barcelona, Madrid"
                        onChange={(e) => handleFormChange(e)}
                        required
                      />
                    </div>
                  </div>
                  <div className="flex gap-4">
                    <div className="flex-1">
                      <label className="block text-blue-300 font-semibold mb-1">
                        Start Date
                      </label>
                      <input
                        type="date"
                        className="w-full bg-gray-800 border border-gray-700 rounded px-3 py-2 text-white"
                        name="startDate"
                        value={form.startDate}
                        onChange={(e) => handleFormChange(e)}
                        min={currentDate.toISOString().split("T")[0]}
                        required
                      />
                    </div>
                    <div className="flex-1">
                      <label className="block text-blue-300 font-semibold mb-1">
                        End Date
                      </label>
                      <input
                        type="date"
                        className="w-full bg-gray-800 border border-gray-700 rounded px-3 py-2 text-white"
                        name="endDate"
                        value={form.EndDate}
                        onChange={(e) => handleFormChange(e)}
                        min={form.startDate}
                        required
                      />
                    </div>
                  </div>
                  <div>
                    <label className="block text-blue-300 font-semibold mb-1">
                      Activities/Preferences (optional)
                    </label>
                    <textarea
                      className="w-full bg-gray-800 border border-gray-700 rounded px-3 py-2 text-white"
                      name="activities"
                      placeholder="e.g. beach, art museums, local food"
                      onChange={(e) => handleFormChange(e)}
                      rows={2}
                    />
                  </div>
                  <button
                    type="submit"
                    className="mt-2 bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-6 rounded-full shadow-lg transition-all"
                  >
                    Add Trip
                  </button>
                </form>
              </div>
            </div>
          </div>
        </div>
      </section>
    </>
  );
};

export default HeroSection;
