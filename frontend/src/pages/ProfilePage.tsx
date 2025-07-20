import React, { useState } from "react";
import TabNavigation from "../components/TabNavigation";
import { useAuth0 } from "@auth0/auth0-react";

const initialProfile = {
  name: "Jane Doe",
  location: "Toronto, Canada",
  gender: "Female",
  birthday: "1998-05-15",
  profilePic: "",
  travelStyle: ["Cultural", "Social"],
  activities: ["Outdoor Activities", "Arts & Culture", "Nightlife"],
  dietary: ["Vegetarian"],
  social: ["Open to Group Activities", "Looking to Meet New People"],
  accommodation: ["Hotels", "Hostels"],
  languages: ["English", "French"],
  accessibility: [],
};

const travelStyles = [
  "Adventurous",
  "Relaxed",
  "Cultural",
  "Social",
  "Nature-Lover",
  "Foodie",
  "Luxury",
  "Budget",
];
const activities = [
  "Outdoor Activities",
  "Arts & Culture",
  "Nightlife",
  "Shopping",
  "Wellness",
  "Sports",
  "Volunteering",
];
const dietaryOptions = [
  "Vegetarian",
  "Vegan",
  "Halal",
  "Kosher",
  "Gluten-Free",
  "Dairy-Free",
  "No Restrictions",
];
const socialOptions = [
  "Solo Traveler",
  "Open to Group Activities",
  "Looking to Meet New People",
  "Prefer Quiet/Private Experiences",
];
const accommodationOptions = [
  "Hotels",
  "Hostels",
  "Airbnbs",
  "Camping",
  "No Preference",
];
const languageOptions = [
  "English",
  "French",
  "Spanish",
  "Mandarin",
  "Hindi",
  "Arabic",
  "Other",
];
const accessibilityOptions = [
  "Wheelchair Accessible",
  "Service Animal Friendly",
  "Dietary Needs",
  "Other",
];

function MultiSelect({
  label,
  options,
  selected,
  onChange,
}: {
  label: string;
  options: string[];
  selected: string[];
  onChange: (v: string[]) => void;
}) {
  return (
    <div className="mb-4">
      <div className="font-semibold mb-1 text-blue-300">{label}</div>
      <div className="flex flex-wrap gap-2">
        {options.map((opt) => (
          <button
            key={opt}
            type="button"
            className={`px-3 py-1 rounded-full border text-sm transition
              ${
                selected.includes(opt)
                  ? "bg-blue-600 border-blue-400 text-white"
                  : "bg-gray-800 border-gray-700 text-gray-300 hover:bg-blue-900 hover:text-blue-300"
              }`}
            onClick={() =>
              selected.includes(opt)
                ? onChange(selected.filter((o) => o !== opt))
                : onChange([...selected, opt])
            }
          >
            {opt}
          </button>
        ))}
      </div>
    </div>
  );
}

const ProfilePage = () => {
  const [profile, setProfile] = useState(initialProfile);
  const { user, isLoading } = useAuth0();

  const handleChange = (
    field: keyof typeof initialProfile,
    value: string | string[] | File | null
  ) => {
    setProfile((prev) => ({ ...prev, [field]: value }));
  };

  if (isLoading) {
    return <div>Loading...</div>;
  }

  return (
    <div className="bg-gradient-to-b from-gray-900 to-gray-800 min-h-screen text-white flex flex-col">
      <TabNavigation activeTab="profile" />
      <main className="flex-1 flex flex-col items-center py-10 px-4">
        <div className="w-full max-w-3xl bg-gray-900 rounded-2xl shadow-xl p-8 mb-8">
          <div className="flex flex-col md:flex-row items-center gap-8 mb-8">
            <div className="flex flex-col items-center">
              <div className="w-32 h-32 rounded-full bg-gray-700 flex items-center justify-center text-5xl mb-2 overflow-hidden">
                {user != undefined ? (
                  <img
                    src={user.picture}
                    alt="Profile"
                    className="object-cover w-full h-full"
                  />
                ) : (
                  <span role="img" aria-label="profile">
                    👤
                  </span>
                )}
              </div>
              <input
                type="file"
                accept="image/*"
                className="text-xs text-gray-400"
                onChange={(e) => {
                  const file = e.target.files?.[0];
                  if (file) {
                    const reader = new FileReader();
                    reader.onload = (ev) => {
                      const result = ev.target?.result;
                      if (typeof result === "string") {
                        handleChange("profilePic", result);
                      }
                    };
                    reader.readAsDataURL(file);
                  }
                }}
              />
            </div>
            <div className="flex-1 grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-blue-300 font-semibold mb-1">
                  Name
                </label>
                <input
                  className="w-full bg-gray-800 border border-gray-700 rounded px-3 py-2 text-white"
                  value={profile.name}
                  onChange={(e) => handleChange("name", e.target.value)}
                />
              </div>
              <div>
                <label className="block text-blue-300 font-semibold mb-1">
                  Location
                </label>
                <input
                  className="w-full bg-gray-800 border border-gray-700 rounded px-3 py-2 text-white"
                  value={profile.location}
                  onChange={(e) => handleChange("location", e.target.value)}
                />
              </div>
              <div>
                <label className="block text-blue-300 font-semibold mb-1">
                  Gender
                </label>
                <input
                  className="w-full bg-gray-800 border border-gray-700 rounded px-3 py-2 text-white"
                  value={profile.gender}
                  onChange={(e) => handleChange("gender", e.target.value)}
                />
              </div>
              <div>
                <label className="block text-blue-300 font-semibold mb-1">
                  Birthday
                </label>
                <input
                  type="date"
                  className="w-full bg-gray-800 border border-gray-700 rounded px-3 py-2 text-white"
                  value={profile.birthday}
                  onChange={(e) => handleChange("birthday", e.target.value)}
                />
              </div>
            </div>
          </div>
          <div className="border-t border-gray-800 pt-6">
            <h2 className="text-2xl font-bold text-blue-400 mb-4">
              Interest Profile
            </h2>
            <MultiSelect
              label="Travel Style"
              options={travelStyles}
              selected={profile.travelStyle}
              onChange={(v) => handleChange("travelStyle", v)}
            />
            <MultiSelect
              label="Activity Preferences"
              options={activities}
              selected={profile.activities}
              onChange={(v) => handleChange("activities", v)}
            />
            <MultiSelect
              label="Dietary Restrictions"
              options={dietaryOptions}
              selected={profile.dietary}
              onChange={(v) => handleChange("dietary", v)}
            />
            <MultiSelect
              label="Social Preferences"
              options={socialOptions}
              selected={profile.social}
              onChange={(v) => handleChange("social", v)}
            />
            <MultiSelect
              label="Accommodation Preferences"
              options={accommodationOptions}
              selected={profile.accommodation}
              onChange={(v) => handleChange("accommodation", v)}
            />
            <MultiSelect
              label="Languages Spoken"
              options={languageOptions}
              selected={profile.languages}
              onChange={(v) => handleChange("languages", v)}
            />
            <MultiSelect
              label="Accessibility Needs"
              options={accessibilityOptions}
              selected={profile.accessibility}
              onChange={(v) => handleChange("accessibility", v)}
            />
          </div>
        </div>
      </main>
    </div>
  );
};

export default ProfilePage;
