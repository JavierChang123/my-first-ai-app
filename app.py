import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import { searchRestaurants } from '../services/geminiService';
import { RestaurantResult, GroundingChunk } from '../types';
import { LoadingSpinner } from './LoadingSpinner';

export const RestaurantFinder: React.FC = () => {
  const [location, setLocation] = useState('');
  const [budget, setBudget] = useState('Any');
  const [cuisine, setCuisine] = useState('Chinese');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<RestaurantResult | null>(null);

  const budgetOptions = ['Any', '$', '$$', '$$$', '$$$$'];
  const cuisineOptions = [
    'Chinese', 'Italian', 'Japanese', 'Korean', 'Mexican', 
    'Western', 'Thai', 'Indian', 'Malay', 'Spanish', 
    'French', 'Vietnamese', 'Taiwanese', 'Turkish'
  ];

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!location.trim()) return;

    setLoading(true);
    setResult(null);
    try {
      const data = await searchRestaurants(location, budget, cuisine);
      setResult(data);
    } catch (error) {
      console.error(error);
      setResult({ text: "Sorry, I couldn't find any restaurants at the moment. Please try again." });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-4 md:p-6">
      <div className="text-center mb-10">
        <h2 className="text-3xl font-serif font-bold text-imperial-red mb-4">Find the Best {cuisine} Cuisine</h2>
        <p className="text-gray-600 max-w-lg mx-auto">
          Enter a city or neighborhood to discover top-rated {cuisine} restaurants, filtered by your budget.
        </p>
      </div>

      <div className="max-w-xl mx-auto mb-12">
        {/* Cuisine Filter */}
        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-500 mb-2 text-center">Select Cuisine</label>
          <div className="flex flex-wrap justify-center gap-2">
            {cuisineOptions.map((opt) => (
              <button
                key={opt}
                type="button"
                onClick={() => setCuisine(opt)}
                className={`px-3 py-1.5 rounded-full text-xs font-medium transition-all border ${
                  cuisine === opt
                    ? 'bg-imperial-red text-white border-imperial-red shadow-md'
                    : 'bg-white text-gray-600 border-gray-200 hover:border-imperial-red hover:text-imperial-red'
                }`}
              >
                {opt}
              </button>
            ))}
          </div>
        </div>

        {/* Budget Filter */}
        <div className="mb-6">
           <label className="block text-sm font-medium text-gray-500 mb-2 text-center">Select Budget</label>
           <div className="flex justify-center flex-wrap gap-2">
            {budgetOptions.map((opt) => (
              <button
                key={opt}
                type="button"
                onClick={() => setBudget(opt)}
                className={`px-4 py-2 rounded-full text-sm font-medium transition-all border ${
                  budget === opt
                    ? 'bg-imperial-red text-white border-imperial-red shadow-md'
                    : 'bg-white text-gray-600 border-gray-200 hover:border-imperial-red hover:text-imperial-red'
                }`}
              >
                {opt === 'Any' ? 'Any Budget' : opt}
              </button>
            ))}
          </div>
        </div>

        <form onSubmit={handleSearch} className="relative w-full">
          <input
            type="text"
            value={location}
            onChange={(e) => setLocation(e.target.value)}
            placeholder={`e.g., San Francisco, for ${cuisine} food...`}
            className="w-full px-6 py-4 rounded-full border-2 border-gray-200 bg-charcoal text-white placeholder-gray-400 focus:border-imperial-red focus:ring-2 focus:ring-imperial-red/20 outline-none text-lg shadow-lg transition-all pr-24"
          />
          <button
            type="submit"
            disabled={loading || !location.trim()}
            className="absolute right-2 top-2 bottom-2 bg-imperial-red text-white px-6 rounded-full font-medium hover:bg-red-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {loading ? 'Searching...' : 'Find'}
          </button>
        </form>
      </div>

      {loading && <LoadingSpinner message={`Consulting the culinary maps for top 20 ${cuisine} spots...`} />}

      {result && (
        <div className="animate-fade-in bg-white rounded-2xl shadow-xl p-6 md:p-8 border border-gray-100">
          <div className="prose prose-red max-w-none">
            <ReactMarkdown
              components={{
                h2: ({node, ...props}) => <h2 className="text-2xl font-serif font-bold text-gray-800 mt-6 mb-4" {...props} />,
                ul: ({node, ...props}) => <ul className="list-none space-y-4 pl-0" {...props} />,
                li: ({node, ...props}) => <li className="bg-paper-white p-4 rounded-lg border border-gray-100" {...props} />,
                strong: ({node, ...props}) => <strong className="text-imperial-red font-semibold" {...props} />,
                a: ({node, ...props}) => <a className="text-imperial-red hover:text-red-700 hover:underline font-medium" target="_blank" rel="noopener noreferrer" {...props} />,
              }}
            >
              {result.text}
            </ReactMarkdown>
          </div>

          {result.groundingMetadata?.groundingChunks && result.groundingMetadata.groundingChunks.length > 0 && (
            <div className="mt-8 pt-6 border-t border-gray-100">
              <h3 className="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-4">Sources & Locations</h3>
              <div className="flex flex-wrap gap-2">
                {result.groundingMetadata.groundingChunks.map((chunk: GroundingChunk, idx: number) => {
                  if (chunk.maps) {
                    return (
                      <a
                        key={idx}
                        href={chunk.maps.uri}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="flex items-center gap-2 bg-white border border-gray-200 hover:border-imperial-red text-gray-700 hover:text-imperial-red px-3 py-1.5 rounded-full text-sm transition-all shadow-sm"
                      >
                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"></path><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"></path></svg>
                        {chunk.maps.title}
                      </a>
                    );
                  }
                  return null;
                })}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};