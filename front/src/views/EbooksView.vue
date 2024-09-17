<template>
    <main>

        <h1 class="text-5xl text-center my-10">Your books</h1>

        <SearchDetailCard :relation="route.params.key" :name="route.params.value" :related="related"/>
        <!-- DaisyUI Component -->
        <div class="overflow-x-auto">
            <table class="table table-zebra">
                <!-- head -->
                <thead>
                    <tr>
                        <!-- <th></th> -->
                        <th></th>
                        <th>Title</th>
                        <th>Author</th>
                        <th>Year of Publication</th>
                        <th>Publisher</th>
                        <th>Genre</th>
                        <th>Theme</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(e, i) in ebooks" :key="e.ebook_guid">
                        <EbookRow :ebook="e" :i="i" @get-ebooks-for="(key, value) => seeBooksFor(key, value)"/>
                    </tr>
                </tbody>
            </table>
        </div>
    </main>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue';
import axios from '../utils/apiRequester';
import { useRoute } from 'vue-router';
import EbookRow from '@/components/EbookRow.vue';
import SearchDetailCard from '@/components/SearchDetailCard.vue';

let ebooks = ref(null);
let related = computed(() => 
    ebooks.value 
    ? ebooks.value.flatMap(e => e.theme).filter(t => t !== route.params.value)
    : null
)
const route = useRoute()

onMounted(async() => {
    try {
        let res = await axios.get('ebooks',
        {
            params: { [ route.params.key ] : route.params.value}
        }
        );
        ebooks.value = res.data;
    }
    catch(error) {
        console.log("Error while fetching data : ", error);
    }
})

</script>