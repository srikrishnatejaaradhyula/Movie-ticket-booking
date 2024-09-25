<template>
    <div>
        <Bar
            :data="chartData"
            :options="{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                    title: { display: true, text: props.title },
                },
            }"
            style="width:100%;max-width:600px"
        />
    </div>
</template>

<script>
import { Bar } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js'
import { reactive } from 'vue'
ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

export default {
    name:"SummeryBarChart",
    components: { 
        Bar 
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
        },
        color: {
            type: Object
        }
    },
    setup(props){

            console.log(props.data)
            console.log(props.labels)
            console.log(props.title)
        const chartData = reactive({
            labels: props.labels,
            datasets: [{ 
                backgroundColor: props.color,
                data: props.data, 
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