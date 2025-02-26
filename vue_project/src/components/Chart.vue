<template>
  <div class="p-4 border rounded-lg shadow">
    <highcharts 
      :options="chartOptions" 
      class="min-h-[400px]"
      v-if="hasData"
    />
    <div v-else class="text-gray-500 p-4">
      No chart data available
    </div>
  </div>
</template>

<script setup>
import { ref, computed, defineProps } from 'vue';

const props = defineProps({
  chartData: {
    type: Object,
    required: true
  },
  chartTitle: {
    type: String,
    default: 'Performance Metrics'
  },
  chartType: {
    type: String,
    default: 'line',
    validator: (value) => ['line', 'bar', 'pie', 'spline'].includes(value)
  }
});

const hasData = computed(() => 
  props.chartData?.series?.length > 0 && 
  props.chartData?.categories?.length > 0
);

const chartOptions = computed(() => ({
  chart: {
    type: props.chartType
  },
  plotOptions: {
    bar: {
      // Optional: Customize bar appearance
      borderRadius: 4,
      dataLabels: {
        enabled: true
      }
    }
  },
  title: {
    text: props.chartTitle
  },
  xAxis: {
    categories: props.chartData.categories || [],
    title: {
      text: props.chartData.xAxisTitle || 'Categories'
    }
  },
  yAxis: {
    title: {
      text: props.chartData.yAxisTitle || 'Values'
    }
  },
  series: props.chartData.series.map(s => ({
    name: s.name,
    data: s.data,
    color: s.color || '#3B82F6' // default blue color
  }))
}));
</script>