<script setup>
import { ref, onMounted } from 'vue';
import { RouterLink } from 'vue-router';
import HelloWorld from '../components/HelloWorld.vue';
import axios from '../utils/apiRequester';

const ebooks = ref(null); // Use a ref to hold the ebooks data

// Fetch data asynchronously
onMounted(async () => {
  try {
    const res = await axios.get('ebooks');
    ebooks.value = res.data; // Set the response data
  } catch (error) {
    console.error('Error fetching ebooks:', error);
  }
});
</script>

<template>
    <EbookList />
    <ReadingList/>
    <PlanToRead/>
    <p id=ebooks>{{ebooks}}</p>
    <img alt="Vue logo" class="logo" src="@/assets/logo.svg" width="125" height="125" />

    <div class="wrapper">
        <HelloWorld msg="You did it!" />

        <nav>
        <RouterLink to="/">Home</RouterLink>
        <RouterLink to="/about">About</RouterLink>
        </nav>
    </div>
</template>
