// composables/useLocationDropdown.js
import { ref, computed, watch, onMounted } from 'vue';

export function useLocationDropdown({
    parentValue = null,
    getOptions,
    initialValue = ''
}) {
    const showDropdown = ref(false);
    const searchQuery = ref('');
    const selectedValue = ref(initialValue);
    const options = ref([]);
    const focusedIndex = ref(-1);



    const filteredOptions = computed(() => {
        if (!searchQuery.value) return options.value || [];
        const query = searchQuery.value.toLowerCase();
        //console.log('filteredOptions query:', query);
        return options.value.filter(opt =>
            opt.name.toLowerCase().includes(query)
        );
    });

    

    const loadOptions = async () => {
        try {
            
            
            options.value = await getOptions(parentValue?.value);

            // Add debug logging here
            /*
            console.groupCollapsed(`[LocationDropdown] Loaded ${options.value.length} options (parent: ${parentValue?.value || 'none'})`);
            console.log('Parent value:', parentValue?.value);
            options.value?.forEach((opt, index) => {
                console.log(`Option ${index + 1}:`, {
                    name: opt.name,
                    isoCode: opt.isoCode,
                    countryCode: opt.countryCode,
                    stateCode: opt.stateCode
                });
            });
            console.groupEnd();
            */


            if (options.value.length === 0) {
                console.warn('No options found for parent value:', parentValue?.value);
            }

            //console.log('options value in loadoptions:', options.value);

        } catch (error) {
            console.error('Error loading options:', error);
            options.value = [];
        }
    };

    // Update search query to display the selected option's name
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

    watch(selectedValue, updateSearchQueryFromSelected);

    watch(parentValue, () => {
        selectedValue.value = '';
        loadOptions();
    }, { immediate: true });



    watch(selectedValue, () => {
        console.log('Selected value changed:', selectedValue.value);
    })



    watch(showDropdown, (newVal) => {
        console.log('Show dropdown value changed in watch useLocationDropdwon.js:', newVal);
        if (newVal) {
            searchQuery.value = '';
            focusedIndex.value = 0;
            loadOptions();
        }
    });

    watch(searchQuery, () => {
        console.log('Search query changed:', searchQuery.value);
    })

    const selectOption = (option) => {
        console.log('Select option in useLocation.js:', option);
        selectedValue.value = option.isoCode || option.name;
        searchQuery.value = option.name;
        console.log('show drop down false in selectOption useLocationDropdown.js:');
        showDropdown.value = false;
    };


    const keyboardNav = (direction) => {
        console.log('Keyboard navigation in useLocationDropdown.js:', direction);
        if (!showDropdown.value) return;
        if (direction === 'up') {
          focusedIndex.value = Math.max(focusedIndex.value - 1, 0);
          console.log('Focused index:', focusedIndex.value);
        } else {
          focusedIndex.value = Math.min(focusedIndex.value + 1, filteredOptions.value.length - 1);
          console.log('focused index:', focusedIndex.value);
        }
      };

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