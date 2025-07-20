import React, { useState } from 'react';
import { useAuth0 } from '@auth0/auth0-react';
import api from '../api';

interface ProfileData {
  name: string;
  location: string;
  gender: string;
  birthday: string;
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

const ProfileSetup = () => {
  const { user } = useAuth0();
  const [currentStep, setCurrentStep] = useState(0);
  const [loading, setLoading] = useState(false);
  const [profile, setProfile] = useState<ProfileData>({
    name: '',
    location: '',
    gender: '',
    birthday: '',
    travelStyle: [],
    activities: [],
    dietary: [],
    social: [],
  });

  const steps = [
    {
      title: 'Basic Information',
      fields: ['name', 'location', 'gender', 'birthday'],
    },
    { title: 'Travel Style', fields: ['travelStyle'] },
    { title: 'Activities', fields: ['activities'] },
    { title: 'Dietary Preferences', fields: ['dietary'] },
    { title: 'Social Preferences', fields: ['social'] },
  ];

  const handleInputChange = (
    field: keyof ProfileData,
    value: string | string[]
  ) => {
    setProfile((prev) => ({ ...prev, [field]: value }));
  };

  const handleMultiSelect = (field: keyof ProfileData, value: string) => {
    setProfile((prev) => {
      const current = prev[field] as string[];
      const updated = current.includes(value)
        ? current.filter((item) => item !== value)
        : [...current, value];
      return { ...prev, [field]: updated };
    });
  };

  const isCurrentStepValid = () => {
    const currentStepFields = steps[currentStep].fields;

    // Check if all required fields in current step are filled
    if (currentStepFields.includes('name') && !profile.name) {
      return false;
    }
    if (currentStepFields.includes('location') && !profile.location) {
      return false;
    }
    if (currentStepFields.includes('gender') && !profile.gender) {
      return false;
    }
    if (currentStepFields.includes('birthday') && !profile.birthday) {
      return false;
    }

    return true;
  };

  const nextStep = () => {
    // Validate current step before allowing to proceed
    if (!isCurrentStepValid()) {
      alert('Please fill in all required fields before proceeding');
      return;
    }

    if (currentStep < steps.length - 1) {
      setCurrentStep(currentStep + 1);
    }
  };

  const prevStep = () => {
    if (currentStep > 0) {
      setCurrentStep(currentStep - 1);
    }
  };

  const handleSubmit = async () => {
    setLoading(true);
    try {
      // Validate required fields
      if (
        !profile.name ||
        !profile.location ||
        !profile.gender ||
        !profile.birthday
      ) {
        alert('Please fill in all required fields');
        setLoading(false);
        return;
      }

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
        profile_pic: user?.picture || '',
        dietary_restrictions: profile.dietary[0] || '',
        location: profile.location,
        travel_dates: {
          from: '',
          to: '',
        },
      };

      await api.post('/users', userData);

      // Redirect directly to trips page
      window.location.href = '/trips';
    } catch (error) {
      console.error('Failed to save profile:', error);
      alert('Failed to save profile. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const renderStep = () => {
    const step = steps[currentStep];

    return (
      <div className="max-w-md mx-auto">
        <div className="mb-8">
          <h2 className="text-2xl font-bold text-blue-400 mb-2">
            {step.title}
          </h2>
          <div className="flex justify-between items-center mb-4">
            <span className="text-gray-400 text-sm">
              Step {currentStep + 1} of {steps.length}
            </span>
            <div className="flex space-x-1">
              {steps.map((_, index) => (
                <div
                  key={index}
                  className={`w-2 h-2 rounded-full ${
                    index <= currentStep ? 'bg-blue-500' : 'bg-gray-600'
                  }`}
                />
              ))}
            </div>
          </div>
        </div>

        {step.fields.includes('name') && (
          <div className="mb-4">
            <label className="block text-blue-300 font-semibold mb-2">
              Name <span className="text-red-400">*</span>
            </label>
            <input
              type="text"
              value={profile.name}
              onChange={(e) => handleInputChange('name', e.target.value)}
              className="w-full bg-gray-800 border border-gray-700 rounded px-3 py-2 text-white"
              placeholder="Enter your name"
              required
            />
            {!profile.name && (
              <p className="text-red-400 text-sm mt-1">Name is required</p>
            )}
          </div>
        )}

        {step.fields.includes('location') && (
          <div className="mb-4">
            <label className="block text-blue-300 font-semibold mb-2">
              Location <span className="text-red-400">*</span>
            </label>
            <input
              type="text"
              value={profile.location}
              onChange={(e) => handleInputChange('location', e.target.value)}
              className="w-full bg-gray-800 border border-gray-700 rounded px-3 py-2 text-white"
              placeholder="e.g., Toronto, Canada"
              required
            />
            {!profile.location && (
              <p className="text-red-400 text-sm mt-1">Location is required</p>
            )}
          </div>
        )}

        {step.fields.includes('gender') && (
          <div className="mb-4">
            <label className="block text-blue-300 font-semibold mb-2">
              Gender <span className="text-red-400">*</span>
            </label>
            <select
              value={profile.gender}
              onChange={(e) => handleInputChange('gender', e.target.value)}
              className="w-full bg-gray-800 border border-gray-700 rounded px-3 py-2 text-white"
              required
            >
              <option value="">Select gender</option>
              <option value="Male">Male</option>
              <option value="Female">Female</option>
              <option value="Other">Other</option>
              <option value="Prefer not to say">Prefer not to say</option>
            </select>
            {!profile.gender && (
              <p className="text-red-400 text-sm mt-1">Gender is required</p>
            )}
          </div>
        )}

        {step.fields.includes('birthday') && (
          <div className="mb-4">
            <label className="block text-blue-300 font-semibold mb-2">
              Birthday <span className="text-red-400">*</span>
            </label>
            <input
              type="date"
              value={profile.birthday}
              onChange={(e) => handleInputChange('birthday', e.target.value)}
              className="w-full bg-gray-800 border border-gray-700 rounded px-3 py-2 text-white"
              required
            />
            {!profile.birthday && (
              <p className="text-red-400 text-sm mt-1">Birthday is required</p>
            )}
          </div>
        )}

        {step.fields.includes('travelStyle') && (
          <div className="mb-4">
            <label className="block text-blue-300 font-semibold mb-2">
              Travel Style
            </label>
            <div className="grid grid-cols-2 gap-2">
              {travelStyles.map((style) => (
                <button
                  key={style}
                  type="button"
                  onClick={() => handleMultiSelect('travelStyle', style)}
                  className={`p-2 rounded border text-sm transition ${
                    profile.travelStyle.includes(style)
                      ? 'bg-blue-600 border-blue-400 text-white'
                      : 'bg-gray-800 border-gray-700 text-gray-300 hover:bg-blue-900'
                  }`}
                >
                  {style}
                </button>
              ))}
            </div>
          </div>
        )}

        {step.fields.includes('activities') && (
          <div className="mb-4">
            <label className="block text-blue-300 font-semibold mb-2">
              Activity Preferences
            </label>
            <div className="grid grid-cols-2 gap-2">
              {activities.map((activity) => (
                <button
                  key={activity}
                  type="button"
                  onClick={() => handleMultiSelect('activities', activity)}
                  className={`p-2 rounded border text-sm transition ${
                    profile.activities.includes(activity)
                      ? 'bg-blue-600 border-blue-400 text-white'
                      : 'bg-gray-800 border-gray-700 text-gray-300 hover:bg-blue-900'
                  }`}
                >
                  {activity}
                </button>
              ))}
            </div>
          </div>
        )}

        {step.fields.includes('dietary') && (
          <div className="mb-4">
            <label className="block text-blue-300 font-semibold mb-2">
              Dietary Restrictions
            </label>
            <div className="grid grid-cols-2 gap-2">
              {dietaryOptions.map((option) => (
                <button
                  key={option}
                  type="button"
                  onClick={() => handleMultiSelect('dietary', option)}
                  className={`p-2 rounded border text-sm transition ${
                    profile.dietary.includes(option)
                      ? 'bg-blue-600 border-blue-400 text-white'
                      : 'bg-gray-800 border-gray-700 text-gray-300 hover:bg-blue-900'
                  }`}
                >
                  {option}
                </button>
              ))}
            </div>
          </div>
        )}

        {step.fields.includes('social') && (
          <div className="mb-4">
            <label className="block text-blue-300 font-semibold mb-2">
              Social Preferences
            </label>
            <div className="grid grid-cols-2 gap-2">
              {socialOptions.map((option) => (
                <button
                  key={option}
                  type="button"
                  onClick={() => handleMultiSelect('social', option)}
                  className={`p-2 rounded border text-sm transition ${
                    profile.social.includes(option)
                      ? 'bg-blue-600 border-blue-400 text-white'
                      : 'bg-gray-800 border-gray-700 text-gray-300 hover:bg-blue-900'
                  }`}
                >
                  {option}
                </button>
              ))}
            </div>
          </div>
        )}

        <div className="flex justify-between mt-8">
          {currentStep > 0 && (
            <button
              onClick={prevStep}
              className="px-6 py-2 bg-gray-600 hover:bg-gray-700 text-white rounded-lg"
            >
              Previous
            </button>
          )}

          {currentStep < steps.length - 1 ? (
            <button
              onClick={nextStep}
              disabled={!isCurrentStepValid()}
              className={`px-6 py-2 rounded-lg ml-auto ${
                isCurrentStepValid()
                  ? 'bg-blue-600 hover:bg-blue-700 text-white'
                  : 'bg-gray-600 text-gray-400 cursor-not-allowed'
              }`}
            >
              Next
            </button>
          ) : (
            <button
              onClick={handleSubmit}
              disabled={loading}
              className={`px-6 py-2 rounded-lg ml-auto ${
                loading
                  ? 'bg-gray-600 text-gray-400 cursor-not-allowed'
                  : 'bg-green-600 hover:bg-green-700 text-white'
              }`}
            >
              {loading ? 'Saving...' : 'Complete Setup'}
            </button>
          )}
        </div>
      </div>
    );
  };

  return (
    <div className="bg-gradient-to-b from-gray-900 to-gray-800 min-h-screen text-white flex items-center justify-center">
      <div className="w-full max-w-lg">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-blue-400 mb-2">
            Complete Your Profile
          </h1>
          <p className="text-gray-400">
            Let's get to know you better to personalize your experience
          </p>
        </div>
        {renderStep()}
      </div>
    </div>
  );
};

export default ProfileSetup;
