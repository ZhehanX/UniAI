<template>
  <div class="map-container h-full w-full">
    <div id="map" class="h-full w-full rounded-lg"></div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, onUnmounted } from 'vue';
import { useInstitutions } from '@/composables/useInstitutions.js';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

// Props from parent component
const props = defineProps({
  cases: {
    type: Array,
    required: true
  }
});

// Map instance reference
const map = ref(null);
const markers = ref([]);

// Initialize map
const initMap = () => {
  //console.log('Initializing map');
  
  // Create map instance
  map.value = L.map('map').setView([41.3851, 2.1734], 5); // Default view centered on Barcelona
  //console.log('Map instance created');

  // Add OpenStreetMap tile layer
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    maxZoom: 19
  }).addTo(map.value);
  //console.log('Tile layer added');

  // Add markers for each case with institution data
  addMarkers();
  
  // Force a resize after initialization to ensure the map fills the container
  setTimeout(() => {
    if (map.value) {
      map.value.invalidateSize();
      //console.log('Map size invalidated');
    }
  }, 200);
};

// Add markers to the map
const addMarkers = async () => {
  // Clear existing markers
  clearMarkers();
  
  //console.log('Adding markers, cases data:', props.cases);
  
  // Import the useInstitutions composable
  const { fetchInstitutionDetailsById } = useInstitutions();
  
  // Group cases by institution to avoid duplicate markers
  const institutionMap = new Map();
  
  // Fetch institution details for each use case
  for (const useCase of props.cases) {
    //console.log('Processing use case:', useCase.id, useCase.title);
    
    try {
      // Fetch institution details if not already fetched
      if (!institutionMap.has(useCase.institution_id)) {
        //console.log('Fetching institution details for ID:', useCase.institution_id);
        const institutionDetails = await fetchInstitutionDetailsById(useCase.institution_id);
        
        institutionMap.set(useCase.institution_id, {
          institution: institutionDetails,
          cases: [useCase]
        });
      } else {
        institutionMap.get(useCase.institution_id).cases.push(useCase);
      }
    } catch (error) {
      console.error('Error fetching institution details:', error);
    }
  }
  

  
  // Create markers for each institution
  institutionMap.forEach(data => {
    const { institution, cases } = data;
    
    if (institution && institution.latitude && institution.longitude) {
      //console.log('Creating marker for institution:', institution.name, 'at', institution.latitude, institution.longitude);
      
      // Create marker
      const marker = L.marker([institution.latitude, institution.longitude])
        .addTo(map.value);
      
      // Create popup content
      let popupContent = `
        <div class="popup-content">
          <h3 class="font-bold">${institution.name}</h3>
          <p>${institution.city}, ${institution.state}, ${institution.country}</p>
          <p class="text-xs text-gray-500">Coordinates: ${institution.latitude.toFixed(4)}, ${institution.longitude.toFixed(4)}</p>
          <hr class="my-2">
          <h4 class="font-semibold">Use Cases:</h4>
          <ul class="list-disc pl-4">
      `;
      
      cases.forEach(useCase => {
        popupContent += `<li>${useCase.title}</li>`;
      });
      
      popupContent += `
          </ul>
        </div>
      `;
      
      // Bind popup to marker
      marker.bindPopup(popupContent);
      
      // Store marker reference for later cleanup
      markers.value.push(marker);
      //console.log('Marker added, total markers:', markers.value.length);
    } else {
      console.warn('Missing coordinates for institution:', institution?.name || 'Unknown');
    }
  });
  
  // Adjust map view to fit all markers if there are any
  if (markers.value.length > 0) {
    //console.log('Adjusting map view to fit', markers.value.length, 'markers');
    const group = L.featureGroup(markers.value);
    map.value.fitBounds(group.getBounds().pad(0.1));
  } else {
    console.warn('No markers to display on the map');
  }
};

// Clear all markers from the map
const clearMarkers = () => {
  markers.value.forEach(marker => {
    map.value.removeLayer(marker);
  });
  markers.value = [];
};

// Watch for changes in cases data
watch(() => props.cases, (newCases) => {
  //console.log('Cases data changed, new length:', newCases?.length);
  if (map.value) {
    addMarkers();
  }
}, { deep: true });

// Handle window resize
const handleResize = () => {
  if (map.value) {
    map.value.invalidateSize();
  }
};

// Initialize map when component is mounted
onMounted(() => {
  // Need to wait for the DOM to be ready
  setTimeout(() => {
    initMap();
  }, 100);
  
  // Add resize event listener
  window.addEventListener('resize', handleResize);
});

// Clean up when component is unmounted
onUnmounted(() => {
  if (map.value) {
    map.value.remove();
    map.value = null;
  }
  window.removeEventListener('resize', handleResize);
});
</script>

<style>
/* Fix for Leaflet marker icon issues */
.leaflet-default-icon-path {
  background-image: url('https://unpkg.com/leaflet@1.7.1/dist/images/marker-icon.png');
}

.leaflet-default-shadow-path {
  background-image: url('https://unpkg.com/leaflet@1.7.1/dist/images/marker-shadow.png');
}

/* Ensure the map container takes full height */
.map-container {
  min-height: 400px;
}

/* Style the popup content */
.popup-content h3 {
  font-size: 1.1rem;
  margin-bottom: 0.5rem;
}

.popup-content p {
  margin-bottom: 0.5rem;
}

.popup-content ul {
  margin-top: 0.5rem;
}

.popup-content li {
  margin-bottom: 0.25rem;
}
</style>