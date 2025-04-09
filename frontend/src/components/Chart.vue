<template>
  <div class="chart-container h-full w-full">
    <div v-if="!hasData" class="flex items-center justify-center h-full text-gray-500">
      No data available
    </div>
    <div v-else id="chart-container" class="h-full w-full"></div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, onUnmounted, computed } from 'vue';
import Highcharts from 'highcharts';
import AccessibilityModule from 'highcharts/modules/accessibility';

// Initialize Highcharts accessibility module correctly
if (typeof AccessibilityModule === 'function') {
  AccessibilityModule(Highcharts);
}

const props = defineProps({
  data: {
    type: [Array, Object], // Allow both array (for pie) and object (for line)
    required: true
  },
  title: {
    type: String,
    default: 'AI Technologies Distribution'
  },
  xAxisTitle: {
    type: String,
    default: 'Year'
  },
  yAxisTitle: {
    type: String,
    default: 'Quantity'
  },
  chartType: {
    type: String,
    default: 'pie',
    validator: (value) => ['pie', 'line', 'bar'].includes(value)
  }
});

const chart = ref(null);
const hasData = computed(() => {
  if (props.chartType === 'pie') {
    return props.data && props.data.length > 0;
  } else if (props.chartType === 'line') {
    return props.data && props.data.categories && props.data.series && props.data.series.length > 0;
  }
  return false;
});

const createChart = () => {
  if (!hasData.value) return;

  try {
    // Make sure the container exists before creating the chart
    const container = document.getElementById('chart-container');
    if (!container) {
      console.warn('Chart container not found');
      return;
    }

    let chartOptions = {};

    if (props.chartType === 'pie') {
      // Prepare data for pie chart
      const chartData = props.data.map(item => ({
        name: item.name,
        y: item.value
      }));

      chartOptions = {
        chart: {
          type: 'pie',
          backgroundColor: 'transparent',
          style: {
            fontFamily: 'Inter, sans-serif'
          }
        },
        title: {
          text: props.title,
          style: {
            fontSize: '16px',
            fontWeight: 'bold'
          }
        },
        tooltip: {
          pointFormat: '{series.name}: <b>{point.y}</b> ({point.percentage:.1f}%)'
        },
        accessibility: {
          enabled: true,
          description: 'Chart showing distribution of AI technologies across use cases',
          keyboardNavigation: {
            enabled: true
          }
        },
        plotOptions: {
          pie: {
            allowPointSelect: true,
            cursor: 'pointer',
            dataLabels: {
              enabled: true,
              format: '<b>{point.name}</b>: {point.y} ({point.percentage:.1f}%)'
            },
            showInLegend: true
          }
        },
        series: [{
          name: 'Use Cases',
          colorByPoint: true,
          data: chartData
        }]
      };
    } else if (props.chartType === 'line') {
      // Line chart configuration
      chartOptions = {
        chart: {
          type: 'line',
          backgroundColor: 'transparent',
          style: {
            fontFamily: 'Inter, sans-serif'
          }
        },
        title: {
          text: props.title,
          style: {
            fontSize: '16px',
            fontWeight: 'bold'
          }
        },
        xAxis: {
          categories: props.data.categories,
          title: {
            text: props.xAxisTitle
          }
        },
        yAxis: {
          title: {
            text: props.yAxisTitle
          }
        },
        tooltip: {
          pointFormat: '{series.name}: <b>{point.y}</b>'
        },
        accessibility: {
          enabled: true,
          description: 'Chart showing AI use cases over time',
          keyboardNavigation: {
            enabled: true
          }
        },
        series: props.data.series
      };
    }

    // Add common options
    chartOptions.credits = { enabled: false };

    // Create the chart
    chart.value = Highcharts.chart('chart-container', chartOptions);
  } catch (error) {
    console.error('Error creating chart:', error);
    chart.value = null;
  }
};

// Watch for changes in data and chart type
watch([() => props.data, () => props.chartType], () => {
  try {
    if (chart.value) {
      // Check if chart is valid before destroying
      if (chart.value.destroy && typeof chart.value.destroy === 'function') {
        chart.value.destroy();
      }
      chart.value = null;
    }
  } catch (error) {
    console.error('Error destroying chart:', error);
    chart.value = null;
  }

  // Need to wait for the DOM to update
  setTimeout(() => {
    createChart();
  }, 0);
}, { deep: true });

// Initialize chart when component is mounted
onMounted(() => {
  // Need to wait for the DOM to be ready
  setTimeout(() => {
    createChart();
  }, 0);

  // Add resize event listener
  window.addEventListener('resize', handleResize);
});

// Handle window resize
const handleResize = () => {
  if (chart.value) {
    chart.value.reflow();
  }
};

// Clean up when component is unmounted
onUnmounted(() => {
  try {
    if (chart.value) {
      if (chart.value.destroy && typeof chart.value.destroy === 'function') {
        chart.value.destroy();
      }
      chart.value = null;
    }
  } catch (error) {
    console.error('Error destroying chart on unmount:', error);
    chart.value = null;
  }
  window.removeEventListener('resize', handleResize);
});
</script>

<style scoped>
.chart-container {
  min-height: 300px;
}
</style>
