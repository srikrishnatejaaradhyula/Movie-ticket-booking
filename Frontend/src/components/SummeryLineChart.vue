<template>
    <div>
        <Line
            :data="chartData"
            :options="{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                    title: { display: true, text: props.title },
                },
               
            }"
        />
    </div>
</template>

<script>
import { Line } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend,PointElement,LineElement, CategoryScale, LinearScale } from 'chart.js'
import { reactive } from 'vue'
ChartJS.register(Title, Tooltip, Legend, PointElement,LineElement, CategoryScale, LinearScale)
export default {
    name:"SummeryLineChart",
    components: { 
        Line
    },
    props: {
        title: {
            type: String,
            required: true
        },
        data: {
            type: Object,
            required: true
        },
        labels: {
            type: Object,
            required: true
        },
        chartData: {
            type: Object,
            required: true
        },
        chartOptions: {
            type: Object,
            default: () => {}
        }
    },
    setup(props){
            console.log(props.data)
            console.log(props.labels)
            console.log(props.title)
        const chartData = reactive({
            labels: props.labels,
            datasets: [{ 
                backgroundColor: ['#FFC107'],
                data: props.data, 
                borderWidth : 3,
                borderColor: '#cc99ff',
                pointBorderColor: '#ff0066',
            }],
            // title: {
            //     display: true,
            //     text: props.title // Use props.title in chartOptions
            // }
        })
        
        return {
            chartData,
            props
            
        }
    }
}
</script>