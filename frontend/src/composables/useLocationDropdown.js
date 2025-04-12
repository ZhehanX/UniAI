import { ref, computed, watch, onMounted } from 'vue';

/**
 * Composable for managing location dropdown functionality
 * @param {Object} options - Configuration options
 * @param {Ref} parentValue - Reference to parent location value (e.g., country for state dropdown)
 * @param {Function} getOptions - Function to fetch location options
 * @param {String} initialValue - Initial selected value
 * @returns {Object} - Dropdown state and methods
 */
export function useLocationDropdown({
    parentValue = null,
    getOptions,
    initialValue = ''
}) {
    // State management
    const showDropdown = ref(false);        // Controls dropdown visibility
    const searchQuery = ref('');            // Stores user's search input
    const selectedValue = ref(initialValue); // Currently selected location value
    const options = ref([]);                // Available location options
    const focusedIndex = ref(-1);           // Index of currently focused option for keyboard navigation

    /**
     * Computed property that filters options based on search query
     * Returns all options if no search query is present
     */
    const filteredOptions = computed(() => {
        if (!searchQuery.value) return options.value || [];
        const query = searchQuery.value.toLowerCase();
        return options.value.filter(opt =>
            opt.name.toLowerCase().includes(query)
        );
    });

    /**
     * Loads location options from the provided getOptions function
     * Options depend on the parent value (e.g., country for states)
     */
    const loadOptions = async () => {
        try {
            options.value = await getOptions(parentValue?.value);

            if (options.value.length === 0) {
                console.warn('No options found for parent value:', parentValue?.value);
            }

        } catch (error) {
            console.error('Error loading options:', error);
            options.value = [];
        }
    };

    /**
     * Updates the search query to display the selected option's name
     * This ensures the dropdown shows the correct name after selection
     */
    const updateSearchQueryFromSelected = () => {
        if (selectedValue.value) {
            const selectedOption = options.value.find(opt => 
                opt.isoCode === selectedValue.value || opt.name === selectedValue.value
            );
            
            searchQuery.value = selectedOption ? selectedOption.name : '';
        } else {
           
            searchQuery.value = '';
        }
    };

    // Watch for changes to selectedValue to update the displayed text
    watch(selectedValue, updateSearchQueryFromSelected);

    // Watch for changes to parent value (e.g., country) to reset selection and load new options
    watch(parentValue, () => {
        selectedValue.value = '';
        loadOptions();
    }, { immediate: true });

    // When dropdown opens, reset search and focus first item
    watch(showDropdown, (newVal) => {
        if (newVal) {
            searchQuery.value = '';
            focusedIndex.value = 0;
            loadOptions();
        }
    });

    /**
     * Handles option selection
     * @param {Object} option - The selected location option
     */
    const selectOption = (option) => {
        selectedValue.value = option.isoCode || option.name;
        searchQuery.value = option.name;
        showDropdown.value = false;
    };

    /**
     * Handles keyboard navigation through dropdown options
     * @param {String} direction - Direction of navigation ('up' or 'down')
     */
    const keyboardNav = (direction) => {
        if (!showDropdown.value) return;
        if (direction === 'up') {
          focusedIndex.value = Math.max(focusedIndex.value - 1, 0);
        } else {
          focusedIndex.value = Math.min(focusedIndex.value + 1, filteredOptions.value.length - 1);
        }
      };

    // Return state and methods for use in components
    return {
        showDropdown,
        searchQuery,
        selectedValue,
        filteredOptions,
        selectOption,
        keyboardNav,
        loadOptions,
        focusedIndex
    };
}