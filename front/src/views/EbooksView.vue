<template>
    <main>

        <h1 class="text-5xl text-center my-10">Your books</h1>

        <div class="flex justify-center my-5">
            <SearchDetailCard :relation="route.params.key" :name="route.params.value" :related="related"/>
        </div>

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
                <TableBody :ebooks="ebooks" @get-ebooks-for="(key, value) => seeBooksFor(key, value)"/>
            </table>
        </div>
    </main>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue';
import axios from '../utils/apiRequester';
import { useRoute } from 'vue-router';
import TableBody from '@/components/TableBody.vue';
import SearchDetailCard from '@/components/SearchDetailCard.vue';

let ebooks = ref([]);
const route = useRoute()
let related = computed(() => {
    if (ebooks.value.length === 0) return []

    let related = []
    let present_relations = new Map();
    present_relations.set(route.params.value, 1)

    for (let i = 0; i < ebooks.value.length; i++) {
        const themes = ebooks.value[i].theme
        if (themes.length === 0) continue;

        for (let j = 0; j < themes.length ; j++) {
            if (present_relations.has(themes[j])) continue;
            else {
                present_relations.set([themes[j]],1)
                related.push(themes[j])
            }
        }
    }
    return related
});

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