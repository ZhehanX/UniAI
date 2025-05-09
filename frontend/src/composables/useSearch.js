import { ref, computed } from 'vue';
import axios from 'axios';

export function useSearch() {
    const searchQuery = ref('');
    const searchResults = ref([]);
    const isSearching = ref(false);
    const errorMessage = ref('');
    
    /**
     * Performs a basic search with the given query
     * @param {string} query - The search query
     * @returns {Array} Array of search results
     */
    const performSearch = async (query) => {
        if (!query.trim()) {
            searchResults.value = [];
            return [];
        }

        isSearching.value = true;
        errorMessage.value = '';
        
        try {
            const response = await axios.get(
                `${import.meta.env.VITE_API_URL}/api/search?q=${encodeURIComponent(query)}`
            );
            
            searchResults.value = response.data;
            return searchResults.value;
        } catch (err) {
            console.error('Search error:', err);
            errorMessage.value = 'Search failed. Please try again later.';
            return [];
        } finally {
            isSearching.value = false;
        }
    };
    
    /**
     * Performs an advanced search with multiple criteria
     * @param {Object} filters - Object containing search filters
     * @returns {Array} Array of search results
     */
    const performAdvancedSearch = async (filters) => {
        if (!filters || Object.keys(filters).length === 0) {
            searchResults.value = [];
            return [];
        }
        
        isSearching.value = true;
        errorMessage.value = '';
        
        try {
            // Convert filters to query parameters
            const queryParams = new URLSearchParams();
            Object.entries(filters).forEach(([key, value]) => {
                queryParams.append(key, value);
            });
            
            const response = await axios.get(
                `${import.meta.env.VITE_API_URL}/api/advanced-search?${queryParams.toString()}`
            );
            
            searchResults.value = response.data;
            return searchResults.value;
        } catch (err) {
            console.error('Advanced search error:', err);
            errorMessage.value = 'Advanced search failed. Please try again later.';
            return [];
        } finally {
            isSearching.value = false;
        }
    };

    /**
     * Clears the current search
     */
    const clearSearch = () => {
        searchQuery.value = '';
        searchResults.value = [];
    };

    return {
        searchQuery,
        searchResults,
        isSearching,
        errorMessage,
        performSearch,
        performAdvancedSearch,
        clearSearch
    };
}