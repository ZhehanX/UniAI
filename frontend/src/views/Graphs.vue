<template>
    <div class="min-h-screen bg-gray-50">
        <!-- Header -->
        <header class="bg-white shadow mb-6 -mx-6 px-6 py-4">
            <div class="container mx-auto flex items-center justify-between">
                <h1 class="text-2xl font-bold text-gray-900">AI Use Projects Analytics</h1>
                <button @click="$router.push('/')" class="text-blue-600 hover:text-blue-800 flex items-center">
                    ← Back to Overview
                </button>
            </div>
        </header>

        <!-- Toggle Buttons -->
        <div class="flex justify-center mb-6">
            <div class="inline-flex rounded-md shadow-sm" role="group">
                <!-- Map Tab -->
                <button @click="activeTab = 'map'" :class="[
                    'px-4 py-2 text-sm font-medium rounded-l-lg border',
                    activeTab === 'map'
                        ? 'bg-blue-200 text-blue-800 border-blue-300'
                        : 'bg-white text-gray-700 border-gray-300 hover:bg-gray-100'
                ]">
                    Map
                </button>
                <!-- Stats Tab -->
                <button @click="activeTab = 'stats'" :class="[
                    'px-4 py-2 text-sm font-medium rounded-r-lg border',
                    activeTab === 'stats'
                        ? 'bg-blue-200 text-blue-800 border-blue-300'
                        : 'bg-white text-gray-700 border-gray-300 hover:bg-gray-100'
                ]">
                    Stats
                </button>
            </div>
        </div>

        <!-- Content Area -->
        <div class="bg-white rounded-lg shadow p-6">
            <!-- Map Section -->
            <div v-if="activeTab === 'map'" class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div class="h-[650px] bg-white rounded-lg shadow p-4 overflow-auto map-container" 
                     tabindex="0" 
                     @keydown.down.prevent="scrollDown" 
                     @keydown.up.prevent="scrollUp"
                     @keydown.page-down.prevent="pageDown"
                     @keydown.page-up.prevent="pageUp"
                     @keydown.home.prevent="scrollToTop"
                     @keydown.end.prevent="scrollToBottom">
                    <!-- Map Component -->
                    <MapComponent :projects="filteredProjects" />
                </div>
                <div class="bg-white border border-gray-200 rounded-lg p-4">
                    <!-- Filters for Map -->
                    <h3 class="text-lg font-medium mb-4">Filters</h3>
                    <!-- Intitution filter section -->
                    <div class="mb-4">
                        <h4 class="font-medium mb-2">Institution</h4>
                        <div class="space-y-2">
                            <div v-for="institution in institutions" :key="institution.id" class="flex items-center">
                                <input type="checkbox" :id="`inst-${institution.id}`" v-model="selectedInstitutions"
                                    :value="institution.id" class="mr-2" 
                                    @keydown.enter.prevent="toggleCheckbox($event.target)">
                                <label :for="`inst-${institution.id}`">{{ institution.name }}</label>
                            </div>
                        </div>
                    </div>
                    <!-- AI Tech filter section -->
                    <div>
                        <h4 class="font-medium mb-2">AI Tech</h4>
                        <div class="space-y-2">
                            <div v-for="tech in aiTechnologies" :key="tech.id" class="flex items-center">
                                <input type="checkbox" :id="`tech-${tech.id}`" v-model="selectedTechnologies"
                                    :value="tech.id" class="mr-2"
                                    @keydown.enter.prevent="toggleCheckbox($event.target)">
                                <label :for="`tech-${tech.id}`">{{ tech.name }}</label>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Stats Section -->
            <div v-else-if="activeTab === 'stats'" class="flex flex-col gap-4">
                
                <!-- Chart Navigation -->
                <div class="flex justify-center items-center mb-2">
                    <button @click="prevChart" class="px-3 py-1 text-gray-600 hover:text-gray-800">
                        &lt;
                    </button>
                    <span class="mx-4 text-sm text-gray-700 font-medium">
                        {{ availableCharts[currentChartIndex] === 'technology' ? 'Technology Distribution' : 'Yearly Trends' }}
                    </span>
                    <button @click="nextChart" class="px-3 py-1 text-gray-600 hover:text-gray-800">
                        &gt;
                    </button>
                </div>

                <!-- Charts and Filters Grid -->
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <!-- Added tabindex and keyboard event handlers for scroll navigation -->
                    <div class="h-[650px] bg-white rounded-lg shadow p-4 overflow-auto chart-container" 
                         tabindex="0" 
                         @keydown.down.prevent="scrollDown" 
                         @keydown.up.prevent="scrollUp"
                         @keydown.page-down.prevent="pageDown"
                         @keydown.page-up.prevent="pageUp"
                         @keydown.home.prevent="scrollToTop"
                         @keydown.end.prevent="scrollToBottom">
                        <!-- Pie Chart -->
                        <ChartComponent v-if="currentChartType === 'pie'" :data="chartData"
                            title="AI Technologies Distribution" chartType="pie" :showDataTable="true" />
                        <!-- Line Chart -->
                        <ChartComponent v-else-if="currentChartType === 'line'" :data="yearlyTrendData"
                            title="AI Technologies Adoption Over Time" xAxisTitle="Year" 
                            yAxisTitle="Quantity" chartType="line" :showDataTable="true" />
                    </div>
                    <div class="bg-white border border-gray-200 rounded-lg p-4">
                        <!-- Filters for Stats -->
                        <h3 class="text-lg font-medium mb-2">Filters</h3>
                        <p class="text-sm text-gray-600 mb-4">
                            {{ currentChartType === 'pie'
                    ? 'Filter technology distribution by location.'
                    : 'Filter yearly trends by AI technology.' }}
                            Select only what you need.
                        </p>

                        <!-- Location filters (for pie chart: AI Technologies Distribution) -->
                        <div v-if="currentChartType === 'pie'">
                            <!--country dropdown-->
                            <div class="mb-4">
                                <h4 class="font-medium mb-2">Country</h4>
                                <LocationDropdown id="country-dropdown" v-model="countryDropdown.selectedValue"
                                    v-model:show="countryDropdown.showDropdown.value"
                                    :options="countryDropdown.filteredOptions"
                                    :focused-index="countryDropdown.focusedIndex" @select="countryDropdown.selectOption"
                                    @navigate="countryDropdown.keyboardNav" />
                            </div>
                            <!--state dropdown-->
                            <div class="mb-4">
                                <h4 class="font-medium mb-2">State <span class="text-xs text-gray-500">(optional)</span>
                                </h4>
                                <LocationDropdown id="state-dropdown" v-model="stateDropdown.selectedValue"
                                    v-model:show="stateDropdown.showDropdown.value"
                                    :options="stateDropdown.filteredOptions" :focused-index="stateDropdown.focusedIndex"
                                    @select="stateDropdown.selectOption" @navigate="stateDropdown.keyboardNav"
                                    :disabled="!countryDropdown.selectedValue" />
                            </div>
                            <!--city dropdown-->
                            <div class="mb-4">
                                <h4 class="font-medium mb-2">City <span class="text-xs text-gray-500">(optional)</span>
                                </h4>
                                <LocationDropdown id="city-dropdown" v-model="cityDropdown.selectedValue"
                                    v-model:show="cityDropdown.showDropdown.value"
                                    :options="cityDropdown.filteredOptions" :focused-index="cityDropdown.focusedIndex"
                                    @select="cityDropdown.selectOption" @navigate="cityDropdown.keyboardNav"
                                    :disabled="!stateDropdown.selectedValue" />
                            </div>
                        </div>

                        <!-- AI Technology filters (for line chart: AI Technologies Adoption Over Time) -->
                        <div v-else>
                            <h4 class="font-medium mb-2">AI Technology</h4>
                            <div class="space-y-2">
                                <div v-for="tech in aiTechnologies" :key="tech.id" class="flex items-center">
                                    <input type="checkbox" :id="`stat-tech-${tech.id}`" v-model="selectedTechnologies"
                                        :value="tech.id" class="mr-2"
                                        @keydown.enter.prevent="toggleCheckbox($event.target)">
                                    <label :for="`stat-tech-${tech.id}`">{{ tech.name }}</label>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

            </div>
        </div>
    </div>
    <AppFooter />
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { useProjects } from '@/composables/useProjects.js';
import { useInstitutions } from '@/composables/useInstitutions.js';
import { useAiTechnologies } from '@/composables/useAiTechnologies.js';
import { useLocationDropdown } from '@/composables/useLocationDropdown.js';
import { Country, State, City } from 'country-state-city';
import MapComponent from '@/components/Map.vue';
import ChartComponent from '@/components/Chart.vue';
import LocationDropdown from '@/components/LocationDropdown.vue';
import AppFooter from '@/components/AppFooter.vue';

// Tab state
const activeTab = ref('map');

// Chart type and navigation
const currentChartType = ref('pie');
const currentChartIndex = ref(0);
const availableCharts = computed(() => {
    if (currentChartType.value === 'pie') {
        return ['technology']; // Could add more pie chart types in the future
    } else {
        return ['yearly']; // Could add more line chart types in the future
    }
});

// Chart navigation functions
const nextChart = () => {
    // Check if we have more charts of the current type
    if (currentChartIndex.value < availableCharts.value.length - 1) {
        // Move to next chart of same type
        currentChartIndex.value++;
    } else {
        // Switch to next chart type and reset index
        currentChartType.value = currentChartType.value === 'pie' ? 'line' : 'pie';
        currentChartIndex.value = 0;
    }
};

const prevChart = () => {
    // Check if we have previous charts of the current type
    if (currentChartIndex.value > 0) {
        // Move to previous chart of same type
        currentChartIndex.value--;
    } else {
        // Switch to previous chart type and set index to last chart of that type
        currentChartType.value = currentChartType.value === 'pie' ? 'line' : 'pie';
        // Get the new available charts after changing the type
        const newCharts = currentChartType.value === 'pie'
            ? ['technology']
            : ['yearly'];
        currentChartIndex.value = newCharts.length - 1;
    }
};

// Data sources
const { projects, fetchAllProjects } = useProjects();
const { institutions, fetchAllInstitutions } = useInstitutions();
const { technologies: aiTechnologies, fetchAllTechnologies } = useAiTechnologies();

// Filter states for Map
const selectedInstitutions = ref([]);
const selectedTechnologies = ref([]);

// Location tracking variables
const currentCountrycode = ref('');
const currentStatecode = ref('');

// Keep the existing filter states for Stats but connect them to the dropdowns
const selectedCountry = ref('');
const selectedState = ref('');
const selectedCity = ref('');

// Country dropdown setup
const countryDropdown = useLocationDropdown({
    getOptions: () => Country.getAllCountries(),
    initialValue: ''
});

// State dropdown setup
const stateDropdown = useLocationDropdown({
    parentValue: countryDropdown.selectedValue,
    getOptions: (countryCode) => countryCode ? State.getStatesOfCountry(countryCode) : [],
    initialValue: ''
});

// City dropdown setup
const cityDropdown = useLocationDropdown({
    parentValue: stateDropdown.selectedValue,
    getOptions: (stateCode) => stateCode ? City.getCitiesOfState(currentCountrycode.value, stateCode) : [],
    initialValue: ''
});

// Watch for country changes
watch(countryDropdown.selectedValue, (newValue) => {
    const country = Country.getCountryByCode(newValue);
    selectedCountry.value = country?.name || '';
    currentCountrycode.value = newValue;
    stateDropdown.selectedValue = '';
    cityDropdown.selectedValue = '';
    selectedState.value = '';
    selectedCity.value = '';
});

// Watch for state changes
watch(stateDropdown.selectedValue, (newValue) => {
    const state = State.getStateByCodeAndCountry(newValue, currentCountrycode.value);
    selectedState.value = state?.name || '';
    currentStatecode.value = newValue;
    cityDropdown.selectedValue = '';
    selectedCity.value = '';
});

// Watch for city changes
watch(cityDropdown.selectedValue, (newValue) => {
    selectedCity.value = newValue;
});

// Function to toggle checkbox with Enter key
const toggleCheckbox = (checkbox) => {
    checkbox.checked = !checkbox.checked;
    // Trigger the change event to update the v-model
    checkbox.dispatchEvent(new Event('change', { bubbles: true }));
};

// Computed properties for filtered data
const filteredProjects = computed(() => {
    let result = projects.value || [];
    
    // First filter by status - only show approved projects
    result = result.filter(c => c.status === 'approved');

    if (activeTab.value === 'map') {
        if (selectedInstitutions.value.length > 0) {
            result = result.filter(c => selectedInstitutions.value.includes(c.institution_id));
        }

        if (selectedTechnologies.value.length > 0) {
            result = result.filter(c => {
                return c.ai_technologies && c.ai_technologies.some(tech => selectedTechnologies.value.includes(tech));
            });
        }
    } else if (activeTab.value === 'stats') {
        // For stats tab, filter by location
        if (selectedCountry.value) {
            // Filter by country - need to match institution_id with institutions data
            result = result.filter(c => {
                // Find the institution for this project
                const institution = institutions.value.find(inst => inst.id === c.institution_id);
                if (!institution) return false;

                // Match by country name
                return institution.country === selectedCountry.value;
            });
        }

        // Only apply state filter if state is selected
        if (selectedState.value) {
            result = result.filter(c => {
                const institution = institutions.value.find(inst => inst.id === c.institution_id);
                if (!institution) return false;
                return institution.state === selectedState.value;
            });
        }

        // Only apply city filter if city is selected
        if (selectedCity.value) {
            result = result.filter(c => {
                const institution = institutions.value.find(inst => inst.id === c.institution_id);
                if (!institution) return false;
                return institution.city === selectedCity.value;
            });
        }
        
    }


    return result;
});



// Prepare chart data based on filtered projects
const chartData = computed(() => {
    // Group projects by AI technology
    const techCounts = {};

    // Use the filtered projects which already have location filters applied
    filteredProjects.value.forEach(c => {
        if (c.ai_technologies && c.ai_technologies.length > 0) {
            c.ai_technologies.forEach(techId => {
                techCounts[techId] = (techCounts[techId] || 0) + 1;
            });
        }
    });

    // Format data for chart component
    return Object.entries(techCounts).map(([techId, count]) => {
        const tech = aiTechnologies.value.find(t => t.id === parseInt(techId));
        return {
            name: tech ? tech.name : `Tech ${techId}`,
            value: count
        };
    });
});

// Prepare yearly trend data based on project_initiation_date
const yearlyTrendData = computed(() => {
    // Get filtered Projects 
    let filteredResult = filteredProjects.value || [];
    
    // Create a map to store data by year and technology
    // output of techsByYear = techId:{year:quantity, year:quantity, (...)} 
    // Example: 3: {2023: 1, 2024: 1}
    const techsByYear = {};
    // Include all if no filter
    const techsToInclude = selectedTechnologies.value.length > 0 
        ? selectedTechnologies.value 
        : aiTechnologies.value.map(tech => tech.id);
    
    // Initialize the years set to track all years
    const yearsSet = new Set();    
    // Process each project
    filteredResult.forEach(c => {
        if (c.project_initiation_date) {
            try {
                // Extract year from the date string (assuming format like "dd-mm-yyyy")
                const dateParts = c.project_initiation_date.split('-');
                const year = parseInt(dateParts[2], 10);
                
                if (!isNaN(year)) {
                    // add year to yearsSet
                    yearsSet.add(year);
                    
                    // For each technology in this project
                    if (c.ai_technologies && c.ai_technologies.length > 0) {
                        c.ai_technologies.forEach(techId => {
                            // Only include technologies that are in our filter (or all if no filter (see when declare techsToInclude))
                            if (techsToInclude.includes(techId)) {
                                if (!techsByYear[techId]) {
                                    // initialize techsByYear[techId] if it doesn't exist
                                    techsByYear[techId] = {};
                                }
                                // counter for ai technologies by year
                                techsByYear[techId][year] = (techsByYear[techId][year] || 0) + 1;
                            }
                        });
                    }
                }
            } catch (e) {
                console.error("Error parsing date:", c.project_initiation_date, e);
            }
        }
    });
    
    // Sort years for consistent x-axis
    const years = Array.from(yearsSet).sort();
    
    // Prepare series data for each technology
    const series = [];
    
    Object.entries(techsByYear).forEach(([techId, yearData]) => {
        const tech = aiTechnologies.value.find(t => t.id === parseInt(techId));
        if (tech) {
            // Create a data point for each year (0 if no data)
            const data = years.map(year => yearData[year] || 0);
            
            series.push({
                name: tech.name,
                data: data
            });
        }
    });
    
    return {
        categories: years,
        series: series
    };
});

// Load data on component mount
onMounted(async () => {
    await fetchAllProjects();
    await fetchAllInstitutions();
    await fetchAllTechnologies();
});

// Scroll navigation methods for chart container
const scrollDown = (event) => {
    const container = event.target;
    container.scrollTop += 40; // Scroll down by 40px
};

const scrollUp = (event) => {
    const container = event.target;
    container.scrollTop -= 40; // Scroll up by 40px
};

const pageDown = (event) => {
    const container = event.target;
    container.scrollTop += container.clientHeight * 0.8; // Scroll down by 80% of visible height
};

const pageUp = (event) => {
    const container = event.target;
    container.scrollTop -= container.clientHeight * 0.8; // Scroll up by 80% of visible height
};

const scrollToTop = (event) => {
    const container = event.target;
    container.scrollTop = 0; // Scroll to the top
};

const scrollToBottom = (event) => {
    const container = event.target;
    container.scrollTop = container.scrollHeight; // Scroll to the bottom
};
</script>



<style>
/* Added styles for data table */

.highcharts-data-table {
    display: flex;
    flex-direction: column;
    justify-content: space-around;
}

#highcharts-data-table-0,
#highcharts-data-table-1 {
    margin: 0;
}

/* Added styles for chart container focus state */
.chart-container:focus,
.map-container:focus {
    outline: 2px solid #3b82f6;
    outline-offset: -2px;
}

.chart-container:focus:not(:focus-visible),
.map-container:focus:not(:focus-visible) {
    outline: none;
}

.highcharts-data-table table {
    border-collapse: collapse;
    border-spacing: 0;
    background: white;
    min-width: 100%;
    margin-top: 10px;
    font-family: sans-serif;
    font-size: 0.9em;
}

.highcharts-data-table td,
.highcharts-data-table th,
.highcharts-data-table caption {
    border: 1px solid silver;
    padding: 0.5em;
}

.highcharts-data-table thead tr,
.highcharts-data-table tbody tr:nth-child(even) {
    background: #f8f8f8;
}

.highcharts-data-table tr:hover {
    background: #eff;
}

.highcharts-data-table caption {
    border-bottom: none;
    font-size: 1.1em;
    font-weight: bold;
}

</style>