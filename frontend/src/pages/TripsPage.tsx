import React, { useState } from 'react';
import TabNavigation from '../components/TabNavigation';

interface ItineraryActivity {
  name: string;
  time: string;
  description: string;
  price: string;
  mapsUrl: string;
}

interface ItineraryFood {
  name: string;
  price: string;
  mapsUrl: string;
}

interface ItineraryDay {
  day: number;
  activities: ItineraryActivity[];
  food: ItineraryFood[];
}

interface Trip {
  id: number;
  name: string;
  budget: string;
  startDate: string;
  endDate: string;
  locations: string;
  preferences: string;
  itinerary?: ItineraryDay[];
}

const emptyForm = {
  name: '',
  budget: '',
  startDate: '',
  endDate: '',
  locations: '',
  preferences: '',
};

// Mock function to generate a detailed itinerary
const generateDetailedItinerary = (): ItineraryDay[] => {
  // For demo, generate 3 days with mock data
  return [
    {
      day: 1,
      activities: [
        {
          name: 'City Walking Tour',
          time: '09:00 - 12:00',
          description: 'Guided tour of the city center and main attractions.',
          price: '$30',
          mapsUrl: 'https://maps.google.com/?q=city+center',
        },
        {
          name: 'Art Museum',
          time: '13:00 - 15:00',
          description: 'Explore local and international art exhibits.',
          price: '$15',
          mapsUrl: 'https://maps.google.com/?q=art+museum',
        },
      ],
      food: [
        {
          name: 'Cafe Aroma',
          price: '$12',
          mapsUrl: 'https://maps.google.com/?q=cafe+aroma',
        },
        {
          name: 'Bistro Central',
          price: '$25',
          mapsUrl: 'https://maps.google.com/?q=bistro+central',
        },
      ],
    },
    {
      day: 2,
      activities: [
        {
          name: 'Kayaking Adventure',
          time: '10:00 - 13:00',
          description: 'Kayak on the river with a local guide.',
          price: '$40',
          mapsUrl: 'https://maps.google.com/?q=river+kayak',
        },
        {
          name: 'Botanical Gardens',
          time: '15:00 - 17:00',
          description: 'Relax and enjoy the beautiful gardens.',
          price: '$10',
          mapsUrl: 'https://maps.google.com/?q=botanical+gardens',
        },
      ],
      food: [
        {
          name: 'Green Leaf Vegan',
          price: '$18',
          mapsUrl: 'https://maps.google.com/?q=green+leaf+vegan',
        },
        {
          name: 'Pizza Palace',
          price: '$20',
          mapsUrl: 'https://maps.google.com/?q=pizza+palace',
        },
      ],
    },
    {
      day: 3,
      activities: [
        {
          name: 'Local Market',
          time: '09:30 - 11:00',
          description: 'Shop for souvenirs and local products.',
          price: 'Free',
          mapsUrl: 'https://maps.google.com/?q=local+market',
        },
        {
          name: 'Beach Afternoon',
          time: '13:00 - 17:00',
          description: 'Relax at the beach and swim.',
          price: 'Free',
          mapsUrl: 'https://maps.google.com/?q=beach',
        },
      ],
      food: [
        {
          name: 'Seaside Grill',
          price: '$28',
          mapsUrl: 'https://maps.google.com/?q=seaside+grill',
        },
        {
          name: 'Ice Cream Bar',
          price: '$7',
          mapsUrl: 'https://maps.google.com/?q=ice+cream+bar',
        },
      ],
    },
  ];
};

const TripsPage = () => {
  const [trips, setTrips] = useState<Trip[]>([]);
  const [form, setForm] = useState<Omit<Trip, 'id'>>({ ...emptyForm });
  const [modalOpen, setModalOpen] = useState(false);
  const [editingId, setEditingId] = useState<number | null>(null);
  const [viewingItineraryId, setViewingItineraryId] = useState<number | null>(
    null
  );

  const openModal = (trip?: Trip) => {
    if (trip) {
      const { id, ...rest } = trip;
      setForm(rest);
      setEditingId(id);
    } else {
      setForm({ ...emptyForm });
      setEditingId(null);
    }
    setModalOpen(true);
  };

  const closeModal = () => {
    setModalOpen(false);
    setForm({ ...emptyForm });
    setEditingId(null);
  };

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (
      !form.name ||
      !form.budget ||
      !form.startDate ||
      !form.endDate ||
      !form.locations
    )
      return;
    const itinerary = generateDetailedItinerary();
    if (editingId !== null) {
      setTrips((prev) =>
        prev.map((trip) =>
          trip.id === editingId
            ? { ...trip, ...form, id: editingId, itinerary }
            : trip
        )
      );
    } else {
      setTrips((prev) => [
        ...prev,
        {
          id: Date.now(),
          ...form,
          itinerary,
        },
      ]);
    }
    closeModal();
  };

  const handleDelete = (id: number) => {
    setTrips((prev) => prev.filter((trip) => trip.id !== id));
    if (viewingItineraryId === id) setViewingItineraryId(null);
  };

  const handleViewItinerary = (id: number) => {
    setViewingItineraryId(id);
  };

  const handleCloseItinerary = () => {
    setViewingItineraryId(null);
  };

  const viewingTrip = trips.find((trip) => trip.id === viewingItineraryId);

  return (
    <div className="bg-gradient-to-b from-gray-900 to-gray-800 min-h-screen text-white flex flex-col">
      <TabNavigation activeTab="trips" />
      <main className="flex-1 flex flex-col items-center py-10 px-4 relative">
        <div className="w-full max-w-2xl mb-8">
          <h2 className="text-2xl font-bold text-blue-400 mb-6 flex items-center justify-between">
            Your Trips
            <button
              className="bg-blue-600 hover:bg-blue-700 text-white rounded-full w-10 h-10 flex items-center justify-center shadow-lg text-2xl focus:outline-none"
              onClick={() => openModal()}
              aria-label="Add Trip"
            >
              +
            </button>
          </h2>
          {trips.length === 0 ? (
            <div className="text-gray-400">
              No trips yet. Click + to create one!
            </div>
          ) : (
            <ul className="space-y-4">
              {trips.map((trip) => (
                <li
                  key={trip.id}
                  className="bg-gray-800 rounded-xl p-4 shadow flex flex-col md:flex-row md:items-center md:justify-between gap-2"
                >
                  <div className="flex-1">
                    <div className="font-bold text-lg text-blue-200">
                      {trip.name}
                    </div>
                    <div className="text-gray-300 text-sm mb-1">
                      {trip.locations}
                    </div>
                    <div className="text-gray-400 text-xs">
                      {trip.startDate} to {trip.endDate} &bull; Budget: $
                      {trip.budget}
                    </div>
                    {trip.preferences && (
                      <div className="text-gray-400 text-xs mt-1">
                        Preferences: {trip.preferences}
                      </div>
                    )}
                    <button
                      className="mt-4 bg-blue-700 hover:bg-blue-800 text-white px-4 py-1 rounded-full text-sm font-semibold"
                      onClick={() => handleViewItinerary(trip.id)}
                    >
                      View Itinerary
                    </button>
                  </div>
                  <div className="flex flex-col gap-2 mt-2 md:mt-0 md:ml-4">
                    <button
                      className="bg-blue-700 hover:bg-blue-800 text-white px-4 py-1 rounded-full text-sm font-semibold"
                      onClick={() => openModal(trip)}
                    >
                      Edit
                    </button>
                    <button
                      className="bg-red-600 hover:bg-red-700 text-white px-4 py-1 rounded-full text-sm font-semibold"
                      onClick={() => handleDelete(trip.id)}
                    >
                      Delete
                    </button>
                  </div>
                </li>
              ))}
            </ul>
          )}
        </div>
        {/* Modal for create/edit trip */}
        {modalOpen && (
          <div className="fixed inset-0 z-30 flex items-center justify-center">
            <div className="bg-gray-900 rounded-2xl shadow-2xl p-8 w-full max-w-lg relative border border-blue-800">
              <button
                className="absolute top-4 right-4 text-gray-400 hover:text-white text-2xl"
                onClick={closeModal}
                aria-label="Close"
              >
                &times;
              </button>
              <h3 className="text-xl font-bold text-blue-400 mb-4">
                {editingId !== null ? 'Edit Trip' : 'Create a New Trip'}
              </h3>
              <form onSubmit={handleSubmit} className="grid grid-cols-1 gap-4">
                <div>
                  <label className="block text-blue-300 font-semibold mb-1">
                    Trip Name
                  </label>
                  <input
                    className="w-full bg-gray-800 border border-gray-700 rounded px-3 py-2 text-white"
                    name="name"
                    value={form.name}
                    onChange={handleChange}
                    placeholder="e.g. Summer in Spain"
                    required
                  />
                </div>
                <div>
                  <label className="block text-blue-300 font-semibold mb-1">
                    Budget (USD)
                  </label>
                  <input
                    className="w-full bg-gray-800 border border-gray-700 rounded px-3 py-2 text-white"
                    name="budget"
                    value={form.budget}
                    onChange={handleChange}
                    placeholder="e.g. 1500"
                    required
                  />
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
                      onChange={handleChange}
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
                      value={form.endDate}
                      onChange={handleChange}
                      required
                    />
                  </div>
                </div>
                <div>
                  <label className="block text-blue-300 font-semibold mb-1">
                    Location(s)
                  </label>
                  <input
                    className="w-full bg-gray-800 border border-gray-700 rounded px-3 py-2 text-white"
                    name="locations"
                    value={form.locations}
                    onChange={handleChange}
                    placeholder="e.g. Barcelona, Madrid"
                    required
                  />
                </div>
                <div>
                  <label className="block text-blue-300 font-semibold mb-1">
                    Activities/Preferences (optional)
                  </label>
                  <textarea
                    className="w-full bg-gray-800 border border-gray-700 rounded px-3 py-2 text-white"
                    name="preferences"
                    value={form.preferences}
                    onChange={handleChange}
                    placeholder="e.g. beach, art museums, local food"
                    rows={2}
                  />
                </div>
                <button
                  type="submit"
                  className="mt-2 bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-6 rounded-full shadow-lg transition-all"
                >
                  {editingId !== null ? 'Save Changes' : 'Add Trip'}
                </button>
              </form>
            </div>
          </div>
        )}
        {/* Modal for viewing itinerary */}
        {viewingItineraryId !== null && viewingTrip && (
          <div className="fixed left-0 right-0 top-24 z-40 flex items-start justify-center">
            <div className="bg-gray-900 border border-blue-800 rounded-2xl shadow-2xl p-8 w-full max-w-2xl relative overflow-y-auto max-h-[80vh]">
              <button
                className="absolute top-4 right-4 text-gray-400 hover:text-white text-2xl"
                onClick={handleCloseItinerary}
                aria-label="Close"
              >
                &times;
              </button>
              <div className="font-bold text-blue-300 text-xl mb-4">
                Itinerary for {viewingTrip.name}
              </div>
              <div className="space-y-8">
                {viewingTrip.itinerary?.map((day) => (
                  <div key={day.day}>
                    <div className="font-semibold text-blue-200 mb-2">
                      Day {day.day}
                    </div>
                    <div className="mb-2">
                      <div className="font-semibold text-gray-200 mb-1">
                        Activities:
                      </div>
                      <ul className="list-disc list-inside space-y-1">
                        {day.activities.map((act, idx) => (
                          <li key={idx}>
                            <span className="font-bold text-white">
                              {act.name}
                            </span>{' '}
                            <span className="text-gray-400">({act.time})</span>
                            <div className="text-gray-300 text-sm">
                              {act.description}
                            </div>
                            <div className="text-gray-400 text-xs">
                              Price: {act.price} &bull;{' '}
                              <a
                                href={act.mapsUrl}
                                target="_blank"
                                rel="noopener noreferrer"
                                className="text-blue-400 underline"
                              >
                                Google Maps
                              </a>
                            </div>
                          </li>
                        ))}
                      </ul>
                    </div>
                    <div>
                      <div className="font-semibold text-gray-200 mb-1">
                        Food:
                      </div>
                      <ul className="list-disc list-inside space-y-1">
                        {day.food.map((food, idx) => (
                          <li key={idx}>
                            <span className="font-bold text-white">
                              {food.name}
                            </span>
                            <span className="text-gray-400 text-xs ml-2">
                              Price: {food.price} &bull;{' '}
                              <a
                                href={food.mapsUrl}
                                target="_blank"
                                rel="noopener noreferrer"
                                className="text-blue-400 underline"
                              >
                                Google Maps
                              </a>
                            </span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
};

export default TripsPage;
