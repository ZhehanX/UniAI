<template>
    <div class="map-container h-full w-full">
        <div id="map" class="h-full w-full rounded-lg"></div>
    </div>
</template>

<script setup>
import { ref, onMounted, watch, onUnmounted } from 'vue';
import { useInstitutions } from '@/composables/useInstitutions.js';
import Highcharts from 'highcharts';
import 'highcharts/modules/accessibility';
import 'highcharts/modules/map';
import 'highcharts/modules/tiledwebmap';
// Import the exporting module
import 'highcharts/modules/exporting';
// Import the offline-exporting module for client-side export
import 'highcharts/modules/offline-exporting';

// Props from parent component
const props = defineProps({
    projects: {
        type: Array,
        required: true
    }
});

// Map instance reference
const chart = ref(null);

// Initialize map
const initMap = async () => {
    // Group projects by institution to avoid duplicate markers
    const institutionMap = new Map();
    const { fetchInstitutionDetailsById } = useInstitutions();

    // Fetch institution details for each project
    for (const project of props.projects) {
        try {
            // Fetch institution details if not already fetched
            if (!institutionMap.has(project.institution_id)) {
                const institutionDetails = await fetchInstitutionDetailsById(project.institution_id);

                institutionMap.set(project.institution_id, {
                    institution: institutionDetails,
                    projects: [project]
                });
            } else {
                institutionMap.get(project.institution_id).projects.push(project);
            }
        } catch (error) {
            console.error('Error fetching institution details:', error);
        }
    }

    // Prepare data points for the map
    const mapData = [];

    institutionMap.forEach(data => {
        const { institution, projects } = data;

        if (institution && institution.latitude && institution.longitude) {

            // Convert latitude and longitude to numbers
            const lat = parseFloat(institution.latitude);
            const lon = parseFloat(institution.longitude);

            // Verify coordinates are valid numbers
            if (!isNaN(lat) && !isNaN(lon)) {
                // Add data point
                mapData.push({
                    name: institution.name,
                    lat: lat,
                    lon: lon,
                    institution: institution,
                    projects: projects
                });
            }
        }
    });

    // Calculate the center of the map based on the points
    let centerLon = 0;
    let centerLat = 0;
    let validPoints = 0;
    
    // Calculate average of all points
    mapData.forEach(point => {
        if (point.lat && point.lon) {
            centerLat += point.lat;
            centerLon += point.lon;
            validPoints++;
        }
    });
    
    // Set default center if no valid points
    if (validPoints === 0) {
        centerLon = 0;
        centerLat = 20;
    } else {
        centerLon = centerLon / validPoints;
        centerLat = centerLat / validPoints;
    }
    
    // Find appropriate zoom level based on point distribution
    let maxDistance = 0;
    mapData.forEach(point => {
        if (point.lat && point.lon) {
            const distance = Math.sqrt(
                Math.pow(point.lat - centerLat, 2) + 
                Math.pow(point.lon - centerLon, 2)
            );
            maxDistance = Math.max(maxDistance, distance);
        }
    });
    
    // Calculate zoom level - lower value for wider spread
    // Adjust these values based on testing
    let zoomLevel = 2; // Default world view
    if (maxDistance < 1) zoomLevel = 8;
    else if (maxDistance < 5) zoomLevel = 6;
    else if (maxDistance < 15) zoomLevel = 4;
    else if (maxDistance < 50) zoomLevel = 3;

    // Create the chart with OpenStreetMap and points
    chart.value = Highcharts.mapChart('map', {
        chart: {
            margin: 0,
            backgroundColor: '#f8fafc',
            style: {
                fontFamily: 'Inter, sans-serif'
            }
        },
        title: {
            text: ''
        },
        subtitle: {
            text: ''
        },
        // Configure client-side exporting
        exporting: {
            enabled: true,
            fallbackToExportServer: false, // Disable fallback to export server
            buttons: {
                contextButton: {
                    menuItems: ['downloadPNG', 'downloadJPEG', 'downloadPDF', 'downloadSVG']
                }
            }
        },
        navigation: {
            buttonOptions: {
                align: 'left',
                theme: {
                    stroke: '#e6e6e6'
                }
            }
        },
        mapNavigation: {
            enabled: true,
            buttonOptions: {
                alignTo: 'spacingBox'
            }
        },
        mapView: {
            center: [centerLon, centerLat], // Center on the calculated center point
            zoom: zoomLevel // Calculated zoom level
        },
        // Tooltip, information of the point (institution name, projects...)
        tooltip: {
            useHTML: true,
            headerFormat: '',
            pointFormat: '<b>{point.name}</b><br>{point.locationFormatted}<br><hr><b>Projects:</b><br>{point.projectsFormatted}',
            style: {
                fontSize: '0.9rem'
            },
            backgroundColor: 'rgba(255, 255, 255, 0.9)',
            borderWidth: 0,
            shadow: true
        },
        legend: {
            enabled: true,
            title: {
                text: 'Institutions'
            },
            align: 'left',
            symbolWidth: 20,
            symbolHeight: 20,
            itemStyle: {
                textOutline: '1 1 1px rgba(255,255,255)'
            },
            backgroundColor: 'rgba(255,255,255,0.8)',
            float: true,
            borderColor: '#e6e6e6',
            borderWidth: 1,
            borderRadius: 2,
            itemMarginBottom: 5
        },
        plotOptions: {
            mappoint: {
                dataLabels: {
                    enabled: false
                }
            }
        },
        series: [{
            type: 'tiledwebmap',
            name: 'Basemap',
            // type of map
            provider: {
                type: 'OpenStreetMap'
            },
            showInLegend: false
        }, {
            type: 'mappoint',
            name: 'Institutions',
            color: '#4f46e5',
            marker: {
                symbol: 'circle',
                radius: 8,
                fillColor: {
                    radialGradient: { cx: 0.5, cy: 0.5, r: 0.5 },
                    stops: [
                        [0, '#6366F1'],
                        [1, '#4338CA']
                    ]
                },
                lineWidth: 2,
                lineColor: '#ffffff'
            },
            data: mapData.map(point => {
                // Pre-format the projects list for the tooltip
                const projectsFormatted = point.projects.map(c => `• ${c.title}`).join('<br>');
                
                // Format location string to handle missing data
                // To avoid situations like: <, Hampshire, United Kingdom> (when the city is missing, because 
                // normally state and country won't be missing)
                const city = point.institution.city || '';
                const state = point.institution.state || '';
                const country = point.institution.country || '';
                
                let location = '';
                if (city) location += city;
                if (state) location += location ? `, ${state}` : state;
                if (country) location += location ? `, ${country}` : country;
                
                return {
                    name: point.name,
                    lon: point.lon,
                    lat: point.lat,
                    institution: point.institution,
                    projects: point.projects,
                    projectsFormatted: projectsFormatted,
                    locationFormatted: location
                };
            })
        }]
    });

};

// Watch for changes in projects data
watch(() => props.projects, () => {
    if (chart.value) {
        // Destroy existing chart and reinitialize
        chart.value.destroy();
        initMap();
    }
}, { deep: true });

// Handle window resize
const handleResize = () => {
    if (chart.value) {
        chart.value.reflow();
    }
};

// Initialize map when component is mounted
onMounted(() => {
    
    initMap();

    // Add resize event listener
    window.addEventListener('resize', handleResize);
});

// Clean up when component is unmounted
onUnmounted(() => {
    if (chart.value) {
        chart.value.destroy();
        chart.value = null;
    }
    window.removeEventListener('resize', handleResize);
});
</script>

<style>
/* Ensure the map container takes full height */
.map-container {
    min-height: 400px;
}
</style>