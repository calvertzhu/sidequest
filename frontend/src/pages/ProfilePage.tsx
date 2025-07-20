import React, { useState, useEffect } from 'react';
import TabNavigation from '../components/TabNavigation';
import { useAuth0 } from '@auth0/auth0-react';
import api from '../api';

interface ProfileData {
  name: string;
  location: string;
  gender: string;
  birthday: string;
  profilePic: string;
  travelStyle: string[];
  activities: string[];
  dietary: string[];
  social: string[];
}

const travelStyles = [
  'Adventurous',
  'Relaxed',
  'Cultural',
  'Social',
  'Nature-Lover',
  'Foodie',
  'Luxury',
  'Budget',
];

const activities = [
  'Outdoor Activities',
  'Arts & Culture',
  'Nightlife',
  'Shopping',
  'Wellness',
  'Sports',
  'Volunteering',
];

const dietaryOptions = [
  'Vegetarian',
  'Vegan',
  'Halal',
  'Kosher',
  'Gluten-Free',
  'Dairy-Free',
  'No Restrictions',
];

const socialOptions = [
  'Solo Traveler',
  'Open to Group Activities',
  'Looking to Meet New People',
  'Prefer Quiet/Private Experiences',
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
                  ? 'bg-blue-600 border-blue-400 text-white'
                  : 'bg-gray-800 border-gray-700 text-gray-300 hover:bg-blue-900 hover:text-blue-300'
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
  const { user } = useAuth0();
  const [profile, setProfile] = useState<ProfileData>({
    name: '',
    location: '',
    gender: '',
    birthday: '',
    profilePic: '',
    travelStyle: [],
    activities: [],
    dietary: [],
    social: [],
  });
  const [loading, setLoading] = useState(false);
  const [isLoadingProfile, setIsLoadingProfile] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  // Load user profile from database
  useEffect(() => {
    const loadUserProfile = async () => {
      if (!user?.email) {
        setIsLoadingProfile(false);
        return;
      }

      try {
        const response = await api.get(`/users/search?email=${user.email}`);
        if (response.data.exists && response.data.user) {
          const userData = response.data.user;

          // Parse interests into different categories
          const interests = userData.interests || [];
          const travelStyle = interests.filter((interest: string) =>
            travelStyles.includes(interest)
          );
          const userActivities = interests.filter((interest: string) =>
            activities.includes(interest)
          );
          const social = interests.filter((interest: string) =>
            socialOptions.includes(interest)
          );

          setProfile({
            name: userData.name || '',
            location: userData.location || '',
            gender: userData.gender || '',
            birthday: userData.birthday || '',
            profilePic: userData.profile_pic || '',
            travelStyle,
            activities: userActivities,
            dietary: userData.dietary_restrictions
              ? [userData.dietary_restrictions]
              : [],
            social,
          });
        }
      } catch (err) {
        console.error('Failed to load user profile:', err);
        setError('Failed to load profile data');
      } finally {
        setIsLoadingProfile(false);
      }
    };

    loadUserProfile();
  }, [user]);

  const handleChange = (
    field: keyof ProfileData,
    value: string | string[] | File | null
  ) => {
    setProfile((prev) => ({ ...prev, [field]: value }));
  };

  const handleSave = async () => {
    setLoading(true);
    setError(null);
    setSuccess(null);

    // Validate required fields
    if (
      !profile.name ||
      !profile.location ||
      !profile.gender ||
      !profile.birthday
    ) {
      setError(
        'Please fill in all required fields (Name, Location, Gender, Birthday)'
      );
      setLoading(false);
      return;
    }

    try {
      // Combine all interests
      const allInterests = [
        ...profile.travelStyle,
        ...profile.activities,
        ...profile.social,
      ];

      const userData = {
        name: profile.name,
        email: user?.email,
        birthday: profile.birthday,
        gender: profile.gender,
        interests: allInterests,
        profile_pic: profile.profilePic,
        dietary_restrictions: profile.dietary[0] || '',
        location: profile.location,
        travel_dates: {
          from: '',
          to: '',
        },
      };

      // Update user in database
      await api.put(`/users/${user?.email}`, userData);
      setSuccess('Profile updated successfully!');
    } catch (err) {
      console.error('Failed to save profile:', err);
      setError('Failed to save profile. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  if (isLoadingProfile) {
    return (
      <div className="bg-gradient-to-b from-gray-900 to-gray-800 min-h-screen text-white flex items-center justify-center">
        <div className="text-xl">Loading profile...</div>
      </div>
    );
  }

  return (
    <div className="bg-gradient-to-b from-gray-900 to-gray-800 min-h-screen text-white flex flex-col">
      <TabNavigation activeTab="profile" />
      <main className="flex-1 flex flex-col items-center py-10 px-4">
        <div className="w-full max-w-3xl bg-gray-900 rounded-2xl shadow-xl p-8 mb-8">
          {/* Status Messages */}
          {error && (
            <div className="mb-4 p-4 bg-red-900 border border-red-700 rounded-lg text-red-200">
              {error}
            </div>
          )}
          {success && (
            <div className="mb-4 p-4 bg-green-900 border border-green-700 rounded-lg text-green-200">
              {success}
            </div>
          )}

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
                      if (typeof result === 'string') {
                        handleChange('profilePic', result);
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
                  Name <span className="text-red-400">*</span>
                </label>
                <input
                  className="w-full bg-gray-800 border border-gray-700 rounded px-3 py-2 text-white"
                  value={profile.name}
                  onChange={(e) => handleChange('name', e.target.value)}
                  required
                />
                {!profile.name && (
                  <p className="text-red-400 text-sm mt-1">Name is required</p>
                )}
              </div>
              <div>
                <label className="block text-blue-300 font-semibold mb-1">
                  Location <span className="text-red-400">*</span>
                </label>
                <input
                  className="w-full bg-gray-800 border border-gray-700 rounded px-3 py-2 text-white"
                  value={profile.location}
                  onChange={(e) => handleChange('location', e.target.value)}
                  required
                />
                {!profile.location && (
                  <p className="text-red-400 text-sm mt-1">
                    Location is required
                  </p>
                )}
              </div>
              <div>
                <label className="block text-blue-300 font-semibold mb-1">
                  Gender <span className="text-red-400">*</span>
                </label>
                <select
                  className="w-full bg-gray-800 border border-gray-700 rounded px-3 py-2 text-white"
                  value={profile.gender}
                  onChange={(e) => handleChange('gender', e.target.value)}
                  required
                >
                  <option value="">Select gender</option>
                  <option value="Male">Male</option>
                  <option value="Female">Female</option>
                  <option value="Other">Other</option>
                  <option value="Prefer not to say">Prefer not to say</option>
                </select>
                {!profile.gender && (
                  <p className="text-red-400 text-sm mt-1">
                    Gender is required
                  </p>
                )}
              </div>
              <div>
                <label className="block text-blue-300 font-semibold mb-1">
                  Birthday <span className="text-red-400">*</span>
                </label>
                <input
                  type="date"
                  className="w-full bg-gray-800 border border-gray-700 rounded px-3 py-2 text-white"
                  value={profile.birthday}
                  onChange={(e) => handleChange('birthday', e.target.value)}
                  required
                />
                {!profile.birthday && (
                  <p className="text-red-400 text-sm mt-1">
                    Birthday is required
                  </p>
                )}
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
              onChange={(v) => handleChange('travelStyle', v)}
            />
            <MultiSelect
              label="Activity Preferences"
              options={activities}
              selected={profile.activities}
              onChange={(v) => handleChange('activities', v)}
            />
            <MultiSelect
              label="Dietary Restrictions"
              options={dietaryOptions}
              selected={profile.dietary}
              onChange={(v) => handleChange('dietary', v)}
            />
            <MultiSelect
              label="Social Preferences"
              options={socialOptions}
              selected={profile.social}
              onChange={(v) => handleChange('social', v)}
            />
          </div>

          {/* Save Button */}
          <div className="mt-8 flex justify-center">
            <button
              onClick={handleSave}
              disabled={loading}
              className={`px-8 py-3 rounded-full font-bold text-lg transition-all ${
                loading
                  ? 'bg-gray-600 text-gray-400 cursor-not-allowed'
                  : 'bg-blue-600 hover:bg-blue-700 text-white shadow-lg'
              }`}
            >
              {loading ? 'Saving...' : 'Update Profile'}
            </button>
          </div>
        </div>
      </main>
    </div>
  );
};

export default ProfilePage;
