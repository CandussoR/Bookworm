<template>
    <p>JOEMAMA</p>
    <li v-if="currentlyReading">
        <i v-for="(e, i) in currentlyReading" :key="i">
            <span class="font-semibold">{{e.title}}</span>, {{e.author}} ;
        </i>
    </li>
    <div v-else>
        <p>You are not currently reading anything.</p>
        <button>Add a book...</button>
    </div>

    <!-- Open the modal using ID.showModal() method -->

</template>

<script setup>
import axios from '../utils/apiRequester';
import { onMounted, ref } from 'vue';

let currentlyReading = ref([])
onMounted(async () => {
    // try {
    //     let res = await axios.get('readings')
    //     if (res.data) {
    //         currentlyReading.value = res.data
    //     }
    // } catch(error) {
    //     console.error(error)
    // }
})
</script>

<style scoped>

</style>