<template>
  <div class="chart-test-container">
    <h1>Chart Test View</h1>
    
    <div class="chart-controls">
      <label>
        <input type="checkbox" id="patterns-enabled" checked> Enable Patterns
      </label>
    </div>
    
    <div id="container" class="chart-container"></div>
  </div>
</template>

<script setup>
import { onMounted, onUnmounted } from 'vue';
import Highcharts from 'highcharts';
import 'highcharts/modules/pattern-fill';
import 'highcharts/modules/accessibility';
import 'highcharts/modules/exporting';
import 'highcharts/modules/export-data';
// Add the data module
import 'highcharts/modules/data';

let chart = null;

onMounted(() => {
  // Initialize the chart after the component is mounted
  setTimeout(() => {
    initChart();
  }, 100);
});

onUnmounted(() => {
  // Clean up the chart when component is unmounted
  if (chart) {
    chart.destroy();
    chart = null;
  }
});

const initChart = () => {
  const clrs = Highcharts.getOptions().colors;
  const pieColors = [clrs[2], clrs[0], clrs[3], clrs[1], clrs[4]];

  // Get a default pattern, but using the pieColors above.
  // The i-argument refers to which default pattern to use
  function getPattern(i) {
    return {
      pattern: Highcharts.merge(Highcharts.patterns[i], {
        color: pieColors[i]
      })
    };
  }

  // Get 5 patterns
  const patterns = [0, 1, 2, 3, 4].map(getPattern);

  chart = Highcharts.chart('container', {
    chart: {
      type: 'pie'
    },
    exporting: {
      enabled: false,
      showTable: true,
      tableCaption: 'Data table for screen reader usage statistics'
    },
    // Add custom table styling
    dataTableOptions: {
      tableClass: 'custom-data-table',
      rowClass: 'data-table-row',
      cellClass: 'data-table-cell'
    },
    title: {
      text: 'Primary desktop/laptop screen readers',
      align: 'left'
    },

    subtitle: {
      text: 'Source: WebAIM. Click on point to visit official website',
      align: 'left'
    },

    colors: patterns,

    tooltip: {
      valueSuffix: '%',
      borderColor: '#8ae',
      shape: 'rect',
      backgroundColor: 'rgba(255, 255, 255, 0.94)',
      followPointer: false,
      stickOnContact: true
    },

    plotOptions: {
      series: {
        dataLabels: {
          enabled: true,
          connectorColor: '#777',
          format: '<b>{point.name}</b>: {point.percentage:.1f} %'
        },
        point: {
          events: {
            click: function () {
              window.location.href = this.website;
            }
          }
        },
        cursor: 'pointer',
        borderWidth: 3
      }
    },

    series: [{
      name: 'Screen reader usage',
      data: [{
        name: 'NVDA',
        y: 40.6,
        website: 'https://www.nvaccess.org',
        accessibility: {
          description: 'This is the most used desktop screen reader'
        }
      }, {
        name: 'JAWS',
        y: 40.1,
        website: 'https://www.freedomscientific.com/Products/Blindness/JAWS'
      }, {
        name: 'VoiceOver',
        y: 12.9,
        website: 'http://www.apple.com/accessibility/osx/voiceover'
      }, {
        name: 'ZoomText',
        y: 2,
        website: 'http://www.zoomtext.com/products/zoomtext-magnifierreader'
      }, {
        name: 'Other',
        y: 4.4,
        website: 'http://www.disabled-world.com/assistivedevices/computer/screen-readers.php'
      }]
    }],

    responsive: {
      rules: [{
        condition: {
          maxWidth: 500
        },
        chartOptions: {
          plotOptions: {
            series: {
              dataLabels: {
                format: '<b>{point.name}</b>'
              }
            }
          }
        }
      }]
    }
  });

  // Toggle patterns enabled
  document.getElementById('patterns-enabled').onclick = function () {
    chart.update({
      colors: this.checked ? patterns : pieColors
    });
  };
};
</script>

<style scoped>
.chart-test-container {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.chart-controls {
  margin: 20px 0;
}

.chart-container {
  min-height: 400px;
  border: 1px solid #eaeaea;
  border-radius: 8px;
  padding: 10px;
}

h1 {
  color: #333;
  margin-bottom: 20px;
}

label {
  display: flex;
  align-items: center;
  cursor: pointer;
}

input[type="checkbox"] {
  margin-right: 8px;
}

/* Add custom styling for the data table */
:deep(.custom-data-table) {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
  font-family: Inter, sans-serif;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  overflow: hidden;
}

:deep(.custom-data-table caption) {
  font-weight: bold;
  padding: 12px;
  text-align: left;
  background-color: #f9fafb;
  border-bottom: 1px solid #e5e7eb;
  font-size: 1.1em;
}

:deep(.custom-data-table th) {
  background-color: #f3f4f6;
  padding: 12px;
  text-align: left;
  font-weight: 600;
  border-bottom: 2px solid #e5e7eb;
}

:deep(.custom-data-table td) {
  padding: 10px 12px;
  border-bottom: 1px solid #e5e7eb;
}

:deep(.custom-data-table tr:last-child td) {
  border-bottom: none;
}

:deep(.custom-data-table tr:nth-child(even)) {
  background-color: #f9fafb;
}

:deep(.custom-data-table tr:hover) {
  background-color: #f3f4f6;
}
</style>